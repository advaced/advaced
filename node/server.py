# Network handling
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from requests import get


class Server(Thread):
    def __init__(self, host=None, port=None):
        """Initializes socket for the node.

        :param host: IP-address of host (normally the public ip-address).
        :type host: str (ip-address format)
        :param port: Port of the server connection.
        :type port: int
        """

        # Set host and port
        self.host = host if host else get('https://api.ipify.org').content.decode('utf8')
        self.port = port if port else 57575 # standard advaced tcp port: 57575

        # Set socket up
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # Set the nodes-list
        self.nodes = []
