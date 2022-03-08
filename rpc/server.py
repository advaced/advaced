# gRPC
from concurrent.futures import ThreadPoolExecutor
from grpc import server as grpc_server

# Protobuf
from blockchain_pb2 import Transaction, Block, Transactions, Blocks
from blockchain_pb2_grpc import BlockchainServicer, add_BlockchainServicer_to_server as add_blockchain

# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '..'))

from time import time

# Project version
from __init__ import RPC_PORT

class Listener(BlockchainServicer):
    def __init__(self, port=None):
        """Initialize the server-values.

        :param port: Port to listen on.
        :type port: int
        """
        self.port = port if port else RPC_PORT

    def getBlock(self, request, context):
        return Block(index=1, previousHash='23234342', version='1.0.0', timestamp='123', baseFee=2,
        tx=[ Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx', timestamp='1234',
        hash='123231wef', signature='asdf'), Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23,
        type='tx', timestamp='1234', hash='123231wef', signature='asdf')], hash='fasd', signature='asfd')

from time import sleep
def run():
    server = grpc_server(ThreadPoolExecutor(max_workers=1))
    add_blockchain(Listener(), server)

    server.add_insecure_port(f'[::]:{RPC_PORT}')
    server.start()

    try:
        while True:
            # Dev log
            print(f'runnin')

            sleep(16)

    except KeyboardInterrupt:
        # Dev log
        print('shuttin down')

        server.stop(0)

if __name__ == '__main__':
    run()
