# gRPC
from grpc import insecure_channel

# Protobuf
from blockchain_pb2 import BlockRequest, TransactionRequest
from blockchain_pb2_grpc import BlockchainStub

# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '..'))

# Project version
from __init__ import RPC_PORT

from time import sleep

class Client:
    def __init__(self, ip_address, port=None):
        self.ip_address = ip_address
        self.port = port if port else RPC_PORT


    def run(self):
        """Connect to rpc server.

        """
        # Create connection to rpc server
        with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
            stub = BlockchainStub(channel)

            while True:
                try:
                    response = stub.getBlock(BlockRequest(index=123))

                except KeyboardInterrupt:
                    channel.unsubscribe(self.close)

                    exit()


    def close(channel):
        channel.close()

cl = Client('localhost')
cl.run()
