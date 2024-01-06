# Copyright Formic Technologies 2023
import asyncio
import logging
import threading
import warnings
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type

from asyncua import Client, Node
from asyncua.common.subscription import Subscription
from asyncua.ua import NodeClass, uaerrors
from asyncua.ua.uatypes import DataValue, DateTime, Variant

from formic_opcua.client.subscription_handler import SubHandler
from formic_opcua.core import InvalidClientArgsError, convert_type, parse_settings
from formic_opcua.core.connection_delays import CONNECTION_DELAYS

logger = logging.getLogger(__name__)
warnings.simplefilter('error')


class ConnectionStatus(Enum):
    INITIAL = 0
    CONNECTING = 10
    CONNECTED = 20
    DISCONNECTED = 30
    MAX_RETRIES_EXCEEDED = 40
    TERMINATE = 50


class AsyncOpcuaClient:
    def __init__(
        self,
        server_config_file: str | None = None,
        connect_timeout: float = 0.5,
        url: Optional[str] = None,
        uri: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        prefixes: Optional[list[str]] | None = None,
    ) -> None:
        if not (server_config_file or (url and uri)):
            error_message = 'No configuration arguments passed to client.'
            logger.critical(error_message)
            raise InvalidClientArgsError(error_message)

        if server_config_file and (url or uri):
            error_message = (
                'Conflicting arguments passed to client. Either pass a value for server_config_file or for url and uri.'
                'Do not pass arguments for server_config_file and url+uri at the same time.'
            )
            logger.critical(error_message)
            raise InvalidClientArgsError(error_message)

        if server_config_file:
            self.config = parse_settings(server_config_file)
            self._url = self.config['server_settings']['url']
            self._uri = self.config['server_settings']['uri']
            self._prefixes = self.config['server_settings'].get('prefixes', [''])
        else:
            self._url = url
            self._uri = uri
            self._prefixes = prefixes or ['']

        self._idx = -1
        self._node_path_list: List[str] = []
        self._node_map: Dict[str, Tuple] = {}
        self._client = Client(url=self._url)

        self._username = None
        self._password = None

        if username and password:
            self._username = username
            self._password = password
        elif username or password:
            logger.warning('Both username AND password should be provided. Skipping credentials.')
        self.connect_timeout = connect_timeout
        self.connection_status = ConnectionStatus.DISCONNECTED
        self._connection_thread: Optional[threading.Thread] = None

        self.sub_handler: Optional[SubHandler] = None
        self._sub: Optional[Subscription] = None
        self._requested_subscription_period = 10
        self._requested_subscription_prefixes: List[str] = ['']
        self._requested_subscription_handler: Optional[Type[SubHandler]] = None
        self._subscription_requested: bool = False

        logger.info(f'Client created with url: {self._url}, and uri: {self._uri}')

    async def __aenter__(self):
        self.persistent_connect()
        while self.connection_status != ConnectionStatus.CONNECTED:
            await asyncio.sleep(1)
        return self

    async def __aexit__(self, *args) -> None:
        await self._disconnect()
        self.connection_status = ConnectionStatus.TERMINATE

    async def _connect(self) -> bool:
        try:
            if self._client:
                await self._client.disconnect()
            self._client = Client(url=self._url, timeout=self.connect_timeout)
            if self._username is not None and self._password is not None:
                self._client.set_user(self._username)
                self._client.set_password(self._password)
            await self._client.connect()
            return True
        except Exception:
            logger.exception(
                f'Unable to connect to server. Client expects server to have url: {self._url} and uri: {self._uri}. '
                f'Server is not running or the configs are not matched with client.'
            )
            return False

    async def _disconnect(self) -> bool:
        logger.info('Cleaning up client - disconnecting.')
        try:
            await self._client.disconnect()
            return True
        except (RuntimeError, ConnectionError):
            logger.exception('Tried to disconnect but there was no connection.')
            return False
        except Exception:
            logger.exception('Unhandled exception while disconnecting from server.')
            return False

    def persistent_connect(self) -> None:
        self._connection_thread = threading.Thread(target=asyncio.run, args=(self._persistent_connect_thread(),))
        self._connection_thread.daemon = True
        self._connection_thread.start()

    @staticmethod
    async def _async_sleep(seconds: float) -> None:
        logger.debug(f'Waiting {seconds} seconds')
        await asyncio.sleep(seconds)

    def _log_connection_status(self, level=logging.INFO) -> None:
        logger.log(level, f'Connection status: {self.connection_status.name}')

    async def _persistent_connect_thread(self) -> None:
        self.connection_status = ConnectionStatus.DISCONNECTED
        connection_index = 0
        while True:
            # with self._connection_status_lock:
            if self.connection_status == ConnectionStatus.DISCONNECTED:
                self._log_connection_status(logging.WARNING)
                self.connection_status = ConnectionStatus.CONNECTING
            elif self.connection_status == ConnectionStatus.CONNECTING:
                await self._async_sleep(CONNECTION_DELAYS[connection_index])
                self._log_connection_status()
                try:
                    if not await self._connect():
                        self.connection_status = ConnectionStatus.DISCONNECTED
                        continue
                    await self._establish_server_structure()
                    if self._requested_subscription_handler:
                        self._subscription_requested = True
                    self.connection_status = ConnectionStatus.CONNECTED
                    self._log_connection_status()
                    connection_index = 0
                except Exception:
                    logger.exception('Exception was raised when client was reconnecting to the server')
                    self.connection_status = ConnectionStatus.DISCONNECTED
                finally:
                    if connection_index < len(CONNECTION_DELAYS) - 1:
                        connection_index += 1

            elif self.connection_status == ConnectionStatus.CONNECTED:
                if await self._test_server_connection():
                    await self._async_sleep(1)
                else:
                    self.connection_status = ConnectionStatus.DISCONNECTED
                    continue
                if self._subscription_requested:
                    logger.info('Subscription was requested when client was disconnected and it will be restored now')
                    await self._create_subscription()

            elif self.connection_status == ConnectionStatus.TERMINATE:
                break

    async def _dfs_mapper(self, node: Node, path: str) -> None:
        try:
            browse_path = await node.read_browse_name()
            node_class = await node.read_node_class()
            path_to_node = path + '/' + browse_path.Name
        except asyncio.TimeoutError:
            logger.exception(f'Timeout occurred, node and child dropped: {node}:{path}')
            return
        # Remove root path "/Objects" since this client is intended for reading only custom nodes
        path_to_node = '' if path_to_node == '/Objects' else path_to_node
        # One of prefix should start with mapped path, or mapped path should start with prefix
        if not (
            any(prefix.startswith(path_to_node) for prefix in self._prefixes)
            or any(path_to_node.startswith(prefix) for prefix in self._prefixes)
        ):
            return
        if node_class == NodeClass.Variable:
            var_type = await node.read_data_type_as_variant_type()
            logger.info(f'Found OPCUA variable {path_to_node}, of variant type {var_type}')
            if not path_to_node.startswith('/'):
                self._node_map[path_to_node] = (node, var_type)
            else:
                self._node_map[path_to_node] = (node, var_type)

        #  Operations on children
        try:
            array_length = await node.read_array_dimensions()
            if array_length not in ([0], None):
                logger.info(f'Node {node}:{path} is an array of length {array_length}, skipping its children')
                return
        except uaerrors.BadAttributeIdInvalid:
            pass
        node_children = await node.get_properties() + await node.get_children()
        child_node_list = []
        for idx, child_node in enumerate(node_children):
            child_node_list.append(self._dfs_mapper(child_node, path_to_node))
            # Gather all threads every 32 child
            if (idx + 1) % 32 == 0:
                await asyncio.gather(*child_node_list)
                child_node_list = []
        if child_node_list:
            await asyncio.gather(*child_node_list)
        return

    async def _establish_server_structure(self) -> None:
        try:
            logger.info(f'Mapping namespace using {self._url} and {self._uri}')
            self._idx = await self._client.get_namespace_index(self._uri)
            logger.info(f'Namespace index = {self._idx}')
            root_object_node = await self._client.nodes.root.get_child(['0:Objects'])
            await self._dfs_mapper(node=root_object_node, path='')
            self._node_path_list = list(self._node_map.keys())
            logger.info(f'All nodes successfully mapped: {self._node_path_list}')
        except (AttributeError, ConnectionError, RuntimeWarning, ValueError):
            logger.exception(f'Unable to map opcua nodes from {self._url} and {self._uri}')
        except Exception:
            logger.exception('Unhandled exception while to mapping server structure')

    async def _test_server_connection(self) -> bool:
        try:
            await self._client.check_connection()
            return True
        except Exception:
            logger.exception('Failed server connectivity test.')
            return False

    async def _write_helper(self, path: str, value: Any) -> bool:
        try:
            var, var_type = self._node_map[path]
        except KeyError:
            logger.warning(f'Unable to find {path} in client map {self._node_map}')
            return False
        try:
            value = convert_type(value=value, var_type=var_type)
        except (KeyError, TypeError, Exception):
            logger.warning(f'Unable to convert value {value} to variant type {var_type}')
            return False
        try:
            current_time: DateTime = datetime.utcnow()
            await var.write_value(
                DataValue(
                    Value=Variant(value, var_type),
                    SourceTimestamp=current_time,
                    ServerTimestamp=current_time,
                )
            )
            logger.debug(f'Wrote value {value} of type {var_type} to {path}')
            return True
        except ConnectionError:
            logger.exception(f'Unable to write value {value} of type {var_type} to {path}')
        return False

    async def write(self, path: str, value: Any) -> bool:
        if self.connection_status == ConnectionStatus.CONNECTED:
            if await self._write_helper(path=path, value=value):
                logger.debug(f'Write attempt succeeded {path}:{value}')
                return True
            else:
                logger.warning(f'Write attempt failed {path}:{value}')
        return False

    async def _read_helper(self, path: str) -> Any:
        try:
            node = self._node_map[path][0]
        except (KeyError, IndexError):
            logger.warning(f'Unable to get node {path} from client map {self._node_map}')
            return None
        try:
            value = await node.read_value()
            logger.info(f'Read value {value} from path {path}')
            return value
        except Exception:
            logger.exception(f'Unable to read node at {path}')
        return None

    async def read(self, path: str) -> Any:
        logger.info(f'Attempting to read path {path}.')
        value = await self._read_helper(path=path)
        if value is not None:
            logger.info('Read attempt succeeded')
            logger.info(f'Value: {value}')
            return value
        else:
            logger.warning('Read attempt failed')
        return None

    async def read_all(self, prefixes: Optional[List[str]] = None) -> Dict[str, Any]:
        if not prefixes:
            prefixes = self._prefixes
        logger.info(f'Attempting to read all variables on server at uri: {self._uri} and url: {self._url}.')
        results = {}
        future_results = {}

        if self.connection_status == ConnectionStatus.CONNECTED:
            for path in self._node_path_list:
                if any([path.startswith(prefix) for prefix in prefixes]):
                    task_value = asyncio.create_task(self._read_helper(path))
                    future_results[path] = task_value
        await asyncio.gather(*future_results.values())

        for path, task in future_results.items():
            task_value = task.result()
            if task_value is not None:
                logger.info(f'Successfully read value: {task_value} for path: {path}')
                results[path] = task_value
            else:
                logger.warning(f'Unsuccessful read attempt for path {path}')

        logger.info(f'{results}')
        return results

    async def subscribe_all(
        self, prefixes: Optional[List[str]] = None, period: int = 10, subscription_handler=SubHandler
    ) -> None:
        # Save all requested subscription parameters to reuse them after client recreation/reconnection
        self._requested_subscription_period = period
        self._requested_subscription_handler = subscription_handler
        self._requested_subscription_prefixes = self._prefixes if not prefixes else prefixes
        if not self.connection_status == ConnectionStatus.CONNECTED:
            logger.warning(
                'Subscription was requested, but client is disconnected from server. '
                'Subsciption will be restored after successful reconnection.'
            )
        self._subscription_requested = True
        await asyncio.sleep(0.1)

    async def _create_subscription(self):
        nodes_with_prefix = {
            k: v
            for k, v in self._node_map.items()
            if any([k.startswith(prefix) for prefix in self._requested_subscription_prefixes])
        }
        self.sub_handler = self._requested_subscription_handler(nodes_with_prefix)
        self._sub = await self._client.create_subscription(self._requested_subscription_period, self.sub_handler)
        await self._sub.subscribe_data_change(self.sub_handler.reversed_node_mapping)
        self._subscription_requested = False
        await asyncio.sleep(0.1)

    async def read_all_from_subscription(self) -> Dict[str, Any]:
        if not self.sub_handler or not self.sub_handler.current_values:
            logger.warning('Reading from subscription was requested, but none of nodes was subscribed.')
            return {}
        logger.debug(f'Read subscribed nodes: {self.sub_handler.current_values}')
        return self.sub_handler.current_values

    def identifier_from_string(self, path: str) -> List[str]:
        identifier = [f'{self._idx}:{path_part}' for path_part in path.split('/')]
        return ['0:Objects'] + identifier
