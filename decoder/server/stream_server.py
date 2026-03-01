import socket
from decoder.core.dispatcher import PacketDispatcher

class StreamServer:
    def __init__(self, dispatcher: PacketDispatcher, host="0.0.0.0", port=9000, protocol="tcp"):
        self.dispatcher = dispatcher
        self.host = host
        self.port = port
        self.protocol = protocol.lower()
        self.buffer = b""

    def start(self):
        if self.protocol == "tcp":
            self._start_tcp()
        else:
            self._start_udp()

    def _start_tcp(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()

            print(f"[stream] TCP listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print(f"[stream] connection from {addr}")

                self._handle_connection(conn)

    def _handle_connection(self, conn):
        with conn:
            while True:
                data = conn.recv(4096)

                if not data:
                    break

                self.buffer += data
                self._process_buffer()

    def _start_udp(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))

            print(f"[stream] UDP listening on {self.host}:{self.port}")

            while True:
                data, addr = s.recvfrom(4096)

                self.buffer += data
                self._process_buffer()

    def _process_buffer(self):
        """
        Packet boundary detection depends on your protocol format.

        Here we assume:
        [packet_type][payload_length][payload][checksum(2 bytes)]
        """

        while True:
            if len(self.buffer) < 4:
                return

            packet_type = self.buffer[0]
            length = int.from_bytes(self.buffer[1:3], "big")

            total_len = 3 + length + 2

            if len(self.buffer) < total_len:
                return

            packet = self.buffer[:total_len]
            self.buffer = self.buffer[total_len:]

            payload = packet[3:-2]

            result = self.dispatcher.dispatch(packet_type, payload)

            self.on_decode(result)

    def on_decode(self, result: dict):
        """
        Override this method to send decoded output to database, MQTT, or HTTP.
        """

        print(result)
