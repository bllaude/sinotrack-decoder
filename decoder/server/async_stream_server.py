import asyncio
from decoder.core.dispatcher import PacketDispatcher

class AsyncStreamServer:
    def __init__(self, dispatcher: PacketDispatcher, host="0.0.0.0", port=9000):
        self.dispatcher = dispatcher
        self.host = host
        self.port = port
        self.buffer_map = {}

    async def start_tcp(self):
        server = await asyncio.start_server(
            self._handle_tcp_client,
            self.host,
            self.port
        )

        addr = server.sockets[0].getsockname()
        print(f"[async_stream] TCP listening on {addr}")

        async with server:
            await server.serve_forever()

    async def _handle_tcp_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info("peername")
        print(f"[async_stream] connection from {peer}")

        buffer = b""

        try:
            while True:
                data = await reader.read(4096)

                if not data:
                    break

                buffer += data
                buffer = await self._process_buffer(buffer)

        except asyncio.CancelledError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    async def start_udp(self):
        loop = asyncio.get_running_loop()

        transport, _ = await loop.create_datagram_endpoint(
            lambda: self._UDPProtocol(self),
            local_addr=(self.host, self.port)
        )

        print(f"[async_stream] UDP listening on {self.host}:{self.port}")

        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            transport.close()

    async def _process_buffer(self, buffer: bytes) -> bytes:
        while True:
            if len(buffer) < 4:
                return buffer

            packet_type = buffer[0]
            length = int.from_bytes(buffer[1:3], "big")

            total_len = 3 + length + 2

            if len(buffer) < total_len:
                return buffer

            packet = buffer[:total_len]
            buffer = buffer[total_len:]

            payload = packet[3:-2]

            result = self.dispatcher.dispatch(packet_type, payload)

            await self.on_decode(result)

        return buffer

    async def on_decode(self, result: dict):
        print(result)

    class _UDPProtocol(asyncio.DatagramProtocol):
        def __init__(self, server):
            self.server = server
            self.buffer = b""

        def datagram_received(self, data, addr):
            self.buffer += data
            asyncio.create_task(self.server._process_buffer(self.buffer))


async def main():
registry = PacketRegistry()
    dispatcher = PacketDispatcher(registry)

    server = AsyncStreamServer(dispatcher, port=5300)
    await server.start_tcp()

if __name__ == "__main__":
    asyncio.run(main())
