import abc


class ServerPinger(object):
    address = None

    def __init__(self, address):
        """
        Creates a new ServerPinger
        :param address: a 2-tuple, (string host, int port)
        :type address tuple
        """
        if len(address) != 2:
            raise ValueError("Invalid address!")

        self.address = address


    @abc.abstractmethod
    def ping(self):
        """
        Pings the server, and returns a ServerPingResponse
        :return a ServerPingResponse object
        :rtype ServerPingResponse
        """
        pass