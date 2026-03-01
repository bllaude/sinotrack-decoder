from decoder.core.dispatcher import PacketDispatcher
from decoder.registry import PacketRegistry
from decoder.packets.position_packet import PositionPacket

def main():
    registry = PacketRegistry()

    registry.register(0x01, PositionPacket)

    dispatcher = PacketDispatcher(registry)

    packet_type = 0x01
    payload = b"\x00" * 20

    result = dispatcher.dispatch(packet_type, payload)

    print(result)

if __name__ == "__main__":
    main()
