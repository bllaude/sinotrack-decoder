from decoder.core.frame_validator import FrameValidator

class PacketDispatcher:
    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, packet_type: int, payload: bytes):
        if not FrameValidator.validate_length(payload):
            return {"error": "invalid_length"}

        if not FrameValidator.verify_checksum(payload):
            return {"error": "checksum_failed"}

        handler = self.registry.get(packet_type)

        if not handler:
            return {
                "error": "unsupported_packet_type",
                "packet_type": packet_type
            }

        parser = handler()

        return parser.parse(payload)
