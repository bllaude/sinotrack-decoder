class PacketRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, packet_type: int, handler):
        self._registry[packet_type] = handler

    def get(self, packet_type: int):
        return self._registry.get(packet_type)
