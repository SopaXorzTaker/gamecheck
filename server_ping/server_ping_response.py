from collections import namedtuple

ServerPingResponse = namedtuple("ServerPingResponse", ["server_type", "players",
                                "description", "version", "ping_time", "icon_url", "error"])
