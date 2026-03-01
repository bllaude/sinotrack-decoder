import asyncio
from decoder.server.async_stream_server import AsyncStreamServer
from decoder.registry import PacketRegistry
from decoder.core.dispatcher import PacketDispatcher

def run_server():
    registry = PacketRegistry()
    dispatcher = PacketDispatcher(registry)

    server = AsyncStreamServer(dispatcher, port=5300)

    asyncio.run(server.start_tcp())

if __name__ == "__main__":
    run_server()
