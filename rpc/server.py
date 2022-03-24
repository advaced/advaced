# gRPC
from concurrent.futures import ThreadPoolExecutor
from grpc import server as grpc_server

# Threading
from threading import Thread, Event

# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__))))

# Blockchain protobuf
from blockchain_pb2 import Transaction, Block, Transactions, Blocks, Success
from blockchain_pb2_grpc import BlockchainServicer, add_BlockchainServicer_to_server as add_blockchain

# Wallet protobuf
from wallet_pb2 import WalletResponse
from wallet_pb2_grpc import WalletServicer, add_WalletServicer_to_server as add_wallet

# Dev log
from time import sleep

# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project version
from __init__ import RPC_PORT

# Project modules
from accounts import Wallet
from blockchain.transaction import Transaction
from blockchain.block import Block
from blockchain.blockchain import Blockchain


class BlockchainListener(BlockchainServicer):
    def __init__(self, blockchain, db_q=None):
        """Initialize the required values.

        :param blockchain: Chain to fetch from
        :type blockchain: :py:class:`blockchain.Blockchain`
        """
        self.blockchain = blockchain

        self.db_q = db_q


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
        Success(success=True)


    def addTransactions(self, request, context):
        Success(success=True)


class WalletListener(WalletServicer):
    def __init__(self, blockchain, db_q=None):
        """Initialize the required values.

        :param blockchain: Chain to fetch from
        :type blockchain: :py:class:`blockchain.Blockchain`
        """
        self.blockchain = blockchain

        self.db_q = db_q

    def getCoins(self, request, context):
        coins = Wallet.coins(request.public_key, self.blockchain)

        # Check if coins were fetched correctly
        if not coins:
            return WalletResponse(amount=-1)

        return WalletResponse(amount=coins)


    def getStake(self, request, context):
        stake = Wallet.stake(request.public_key, self.blockchain)

        # Check if coins were fetched correctly
        if not stake:
            return WalletResponse(amount=-1)

        return WalletResponse(amount=stake)


    def getScore(self, request, context):
        score = Wallet.score(request.public_key, self.blockchain)

        # Check if coins were fetched correctly
        if not score:
            return WalletResponse(amount=-1)

        return WalletResponse(amount=score)


    def getClaims(self, request, context):
        claims = Wallet.claims(request.public_key, self.blockchain)

        # Check if coins were fetched correctly
        if not claims:
            return WalletResponse(amount=-1)

        return WalletResponse(amount=claims)


class RPCServer():
    def __init__(self, blockchain, port=None, start=False, db_q=None):
        """Initialize the server-values.

        :param blockchain: Chain to fetch from
        :type blockchain: :py:class:`blockchain.Blockchain`
        :param port: Port to listen on.
        :type port: int
        :param start: Start automatically or not
        :type start: bool
        """
        self.port = port if port else RPC_PORT
        self.blockchain = blockchain

        self.server = None

        self.db_q = db_q

        if start:
            self.start()


    def start(self):
        """Starts the rpc server.

        :return: Status if server start was successful.
        :rtype: bool
        """
        if self.server:
            return False

        self.server = grpc_server(ThreadPoolExecutor(max_workers=10))

        add_blockchain(BlockchainListener(self.blockchain, db_q=self.db_q), self.server)
        add_wallet(WalletListener(self.blockchain, db_q=self.db_q), self.server)

        self.server.add_insecure_port(f'[::]:{RPC_PORT}')
        self.server.start()

        return True


    def stop(self):
        """Stops the rpc server.

        :return: Status if stop was successful.
        :rtype: bool
        """
        if not self.server:
            return False

        self.server.stop(0)
        self.server = None

        return True


    def restart(self):
        """Restarts the rpc server.

        :return: Status if restart was successful.
        :rtype: bool
        """
        success = self.stop()

        if not success:
            return False

        self.start()

        if not success:
            return False

        return True
