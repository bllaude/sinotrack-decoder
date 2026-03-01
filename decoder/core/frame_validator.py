import struct

class FrameValidator:
    @staticmethod
    def validate_length(packet: bytes, min_length: int = 12) -> bool:
        if not packet:
            return False

        return len(packet) >= min_length

    @staticmethod
    def verify_checksum(packet: bytes) -> bool:
        if len(packet) < 2:
            return False

        data = packet[:-2]
        checksum = struct.unpack(">H", packet[-2:])[0]

        computed = FrameValidator.simple_checksum(data)

        return checksum == computed

    @staticmethod
    def simple_checksum(data: bytes) -> int:
        return sum(data) & 0xFFFF
