import socket
import time
from server_ping.mcpe.packets import encode_serverlist_ping, decode_serverlist_pong
from server_ping.server_ping_response import ServerPingResponse
from server_ping.server_pinger import ServerPinger


class MinecraftPEPinger(ServerPinger):
    _sock = None

    def _do_ping(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(5)
        start = int(time.time() * 1000)
        self._sock.sendto(encode_serverlist_ping(start), self.address)
        data, addr = self._sock.recvfrom(1024)
        info, timestamp = decode_serverlist_pong(data)
        elapsed = int(time.time() * 1000) - start
        if timestamp != start:
            raise ValueError("Invalid ping response")

        self._sock.close()
        return info, elapsed

    def ping(self):
        # MCPE RESPONSE FORMAT (new)
        # MCPE;<name>;<PROTOCOL>;<VERSION>;<players>;<maxplayers>
        try:
            resp, ping_time = self._do_ping()
            response = resp.split(";")
            if response[0] != "MCPE":
                raise ValueError("Old or unsupported protocol")
            return ServerPingResponse(
                     "mcpe",
                     (int(response[4]), int(response[5])),
                     response[1], response[3], ping_time,
                     None, None
            )

        except BaseException as exception:
            raise exception
            #return ServerPingResponse(ServerType.MINECRAFT, None, None, None, None, None, str(exception))
