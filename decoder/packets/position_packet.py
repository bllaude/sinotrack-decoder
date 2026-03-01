import struct
from decoder.core.base_packet import BasePacket

class PositionPacket(BasePacket):
    def parse(self, payload: bytes) -> dict:
        try:
            imei = payload[0:8].hex()

            timestamp_raw = struct.unpack(">I", payload[8:12])[0]

            latitude = struct.unpack(">f", payload[12:16])[0]
            longitude = struct.unpack(">f", payload[16:20])[0]

            speed = payload[20]

            return {
                "type": "position",
                "imei": imei,
                "timestamp": timestamp_raw,
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed
            }

        except Exception as e:
            return {"error": str(e)}
