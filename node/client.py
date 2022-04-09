# Network handling
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from requests import get

# Ports
from __init__ import CLIENT_PORT, SERVER_PORT


class Client(Thread):
    def __init__(self):
        super().__init__()
