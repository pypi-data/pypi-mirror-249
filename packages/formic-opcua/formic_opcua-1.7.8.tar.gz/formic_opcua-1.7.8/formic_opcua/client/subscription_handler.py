class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def __init__(self, node_mapping: dict, initial_values: dict | None = None):
        self.current_values = initial_values or {}
        self.reversed_node_mapping = self.reverse_node_mapping(node_mapping)

    @staticmethod
    def reverse_node_mapping(node_mapping):
        reversed_mapping = {}
        for path, node in node_mapping.items():
            if node[0] not in reversed_mapping:
                reversed_mapping[node[0]] = path
        return reversed_mapping

    def datachange_notification(self, node, val, data):
        var = self.reversed_node_mapping[node]
        self.current_values[var] = val
