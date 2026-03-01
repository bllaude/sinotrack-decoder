class BasePacket:
    def parse(self, payload: bytes) -> dict:
        raise NotImplementedError
