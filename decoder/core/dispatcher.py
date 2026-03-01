from decoder.registry import PacketRegistry

class PacketDispatcher:
    def __init__(self, registry: PacketRegistry):
        self.registry = registry

    def dispatch(self, packet_type: int, payload: bytes):
        handler = self.registry.get(packet_type)

        if not handler:
            return {
                "error": "unsupported_packet_type",
                "packet_type": packet_type
            }

        parser = handler()
        return parser.parse(payload)
