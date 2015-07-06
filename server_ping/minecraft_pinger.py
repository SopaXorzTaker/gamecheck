import json
import socket
import time
from server_ping.minecraft.data_types import DataTypes
from server_ping.minecraft.packets import encode_handshake, encode_request, decode_response, encode_ping, decode_pong
from server_ping.server_ping_response import ServerPingResponse
from server_ping.server_pinger import ServerPinger

PROTOCOL_VERSION = 47


class MinecraftPinger(ServerPinger):
    _sock = None

    def _receive_packet(self):
        # TODO: clean up, the issue here is because we don't receive the full frame first
        length = 0
        offset = 0
        data = self._sock.recv(1024)
        while length == 0:
            data  += self._sock.recv(1024)
            offset, length = DataTypes.read_varint(data, 0)

        while len(data) < length - offset - 1:
            data += self._sock.recv(1024)

        return data

    def _do_ping(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(5)
        self._sock.connect(self.address)
        self._sock.send(encode_handshake(PROTOCOL_VERSION, self.address[0], self.address[1], 1))
        self._sock.send(encode_request())
        data = self._receive_packet()
        offset, response = decode_response(data)
        start = int(time.time() * 1000.0)
        self._sock.send(encode_ping(start))
        data = self._receive_packet()
        offset, timestamp = decode_pong(data)
        elapsed = int(time.time() * 1000.0) - start
        self._sock.close()
        if timestamp != start:
            raise ValueError("Invalid ping reply from the server")
        return response, elapsed

    def ping(self):
        try:
            resp, ping_time = self._do_ping()
            response = json.loads(resp)
            return ServerPingResponse("minecraft",
                    (response['players']['online'], response['players']['max']),
                     response['description'], response['version']['name'], ping_time,
                     response['favicon'], None
                    )

        except BaseException as exception:
            raise exception
            #return ServerPingResponse(ServerType.MINECRAFT, None, None, None, None, None, str(exception))
