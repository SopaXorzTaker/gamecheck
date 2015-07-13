from server_ping.mcpe_pinger import MinecraftPEPinger
from server_ping.minecraft_pinger import MinecraftPinger


class ServerPingHelper(object):
    @staticmethod
    def ping(address, server_type):
        if not (len(address) == 2 and type(address[0]) == str and type(address[1]) == int):
            raise ValueError("Invalid address given")
        if server_type == "minecraft":
            return MinecraftPinger(address).ping()
        elif server_type == "mcpe":
            return MinecraftPEPinger(address).ping()
        else:
            raise ValueError("Invalid server type")
