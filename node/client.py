# Network handling
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from requests import get

# Add to path
from sys import path as sys_path
from os import path, getcwd
sys_path.insert(0, path.join(getcwd(), '..'))

# Ports
from __init__ import CLIENT_PORT, SERVER_PORT


class Client(Thread):
    def __init__(self):
        pass
