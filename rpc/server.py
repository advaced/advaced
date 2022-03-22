# gRPC
from concurrent.futures import ThreadPoolExecutor
from grpc import server as grpc_server

# Threading
from threading import Thread, Event

# Blockchain protobuf
from blockchain_pb2 import Transaction, Block, Transactions, Blocks, Success
from blockchain_pb2_grpc import BlockchainServicer, add_BlockchainServicer_to_server as add_blockchain

# Wallet protobuf
from wallet_pb2 import WalletResponse
from wallet_pb2_grpc import WalletServicer, add_WalletServicer_to_server as add_wallet

# Dev log
from time import sleep

# Add to path
from sys import path, argv
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project version
from __init__ import RPC_PORT


class BlockchainListener(BlockchainServicer):
    def __init__(self, port=None):
        """Initialize the server-values.

        :param port: Port to listen on.
        :type port: int
        """
        self.port = port if port else RPC_PORT


    def getBlock(self, request, context):
        """Fetch block from the given values.

        :param request: Information about the request.
        :param context: Context of the request.

        :return: Block protocol-message.
        :rtype: :py:object:`blockchain_pb2.Block`
        """

        # TODO -> Fetch block that was requested

        return Block(index=1, previousHash='23234342', version='1.0.0', timestamp='123', baseFee=2,
        tx=[ Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx', timestamp='1234',
        hash='123231wef', signature='asdf'), Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23,
        type='tx', timestamp='1234', hash='123231wef', signature='asdf')], hash='fasd', signature='asfd')


    def getBlocks(self, request, context):
        """Fetch blocks from the given values.

        :param request: Information about the request.
        :param context: Context of the request.

        :return: Blocks protocol-message.
        :rtype: :py:object:`blockchain_pb2.Blocks`
        """

        # TODO -> Fetch the blocks that were requested

        return Blocks(blocks=[ Block(index=1, previousHash='23234342', version='1.0.0', timestamp='123', baseFee=2,
        tx=[ Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx', timestamp='1234',
        hash='123231wef', signature='asdf'), Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23,
        type='tx', timestamp='1234', hash='123231wef', signature='asdf')], hash='fasd', signature='asfd'),
        Block(index=1, previousHash='23234342', version='1.0.0', timestamp='123', baseFee=2,
        tx=[ Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx', timestamp='1234',
        hash='123231wef', signature='asdf'), Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23,
        type='tx', timestamp='1234', hash='123231wef', signature='asdf')], hash='fasd', signature='asfd') ])


    def getTransaction(self, request, context):
        """Fetch transaction from the given values.

        :param request: Information about the request.
        :param context: Context of the request.

        :return: Transaction protocol-message.
        :rtype: :py:object:`blockchain_pb2.Transaction`
        """

        # TODO -> Fetch transaction that was requested

        return Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx', timestamp='1234',
        hash='123231wef', signature='asdf')


    def getTransactions(self, request, context):
        """Fetch transactions from the given values.

        :param request: Information about the request.
        :param context: Context of the request.

        :return: Transactions protocol-message.
        :rtype: :py:object:`blockchain_pb2.Transactions`
        """

        # TODO -> Fetch transactions that were requested

        return Transactions(tx=[ Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx',
        timestamp='1234', hash='123231wef', signature='asdf'), Transaction(sender='sdf', recipient='sdwf',
        amount=12, fee=23, type='tx', timestamp='1234', hash='123231wef', signature='asdf') ])


    def addTransaction(self, request, context):
        Success(True)


    def addTransactions(self, request, context):
        Success(True)


class WalletListener(WalletServicer):
    def getCoins(self, request, context):
        return WalletResponse(0)


    def getStake(self, request, context):
        return WalletResponse(0)


    def getScore(self, request, context):
        return WalletResponse(0)


    def getClaims(self, request, context):
        return WalletResponse(0)


    def getBurns(self, request, context):
        return WalletResponse(0)


class RPCServer():
    def __init__(self, port=None, start=False):
        """Initialize the server-values.

        :param port: Port to listen on.
        :type port: int
        :param start: Start automatically or not
        :type start: bool
        """
        self.port = port if port else RPC_PORT

        self.stop_event = Event()
        self.thread = Thread(target=self.run)

        if start:
            self.start()


    def run(self):
        server = grpc_server(ThreadPoolExecutor(max_workers=1))

        add_blockchain(BlockchainListener(), server)
        add_wallet(WalletListener(), server)

        server.add_insecure_port(f'[::]:{RPC_PORT}')
        server.start()

        while not self.stop_event.is_set():
            sleep(.1)

        server.stop(0)


    def start(self):
        """Starts the rpc server.

        :return: Status if server start was successful.
        :rtype: bool
        """

        # Check if database is already running
        if self.thread.is_alive():
            return False

        # Check if stop-event is set
        if self.stop_event.is_set():
            self.stop_event = Event()
            self.db_thread = Thread(target=self.run)

        # Start the database-handler
        self.thread.start()

        return True


    def stop(self):
        """Stops the rpc server.

        :return: Status if stop was successful.
        :rtype: bool
        """
        # Check if database is not running
        if not self.thread.is_alive():
            return False

        # Check if stop-event is set
        # if self.stop_event.is_set():
        #     return False

        # Stop the server
        self.stop_event.set()

        return True


    def restart(self):
        """Restarts the rpc server.

        :return: Status if restart was successful.
        :rtype: bool
        """

        # Check wether the thread is running or not
        if not self.thread.is_alive():
            return False

        # Stop the server
        self.stop()

        # Wait until stop is injected
        while self.thread.is_alive():
            time_sleep(.01)

        # Start the server
        self.start()

        # Check if restart was not successful
        if not self.thread.is_alive():
            return False

        return True
