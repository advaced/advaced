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
from blockchain_pb2 import Transaction as RPCTransaction, Block as RPCBlock, Transactions, Blocks, Success
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

from util.database.blockchain import fetch_block, fetch_block_from_timestamp, fetch_block_from_signature


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

        if request.index:
            block_dict = fetch_block(request.index)

        elif request.timestamp:
            block_dict = fetch_block_from_timestamp(request.timestamp)

        elif request.hash and request.signature:
            block_dict = fetch_block_from_signature(request.signature, request.hash)

        # Check if fetch was successful
        if not block_dict:
            return RPCBlock(index=0, previousHash='', version='', timestamp='',
                            baseFee=0, tx=[], hash='', signature='')

        tx = []

        for transaction in block_dict['tx']:
            tx.append(RPCTransaction(sender=transaction['sender'], recipient=transaction['recipient'],
                                     amount=transaction['amount'], fee=transaction['fee'], type=transaction['tx_type'],
                                     timestamp=transaction['timestamp'], hash=transaction['hash'],
                                     signature=transaction['signature']))

        return RPCBlock(index=block_dict['index'], previousHash=block_dict['previous_hash'],
                        version=block_dict['version'], timestamp=str(block_dict['timestamp']),
                        baseFee=block_dict['base_fee'], tx=tx, hash=block_dict['hash'],
                        signature=block_dict['signature'])

    def getBlocks(self, request, context):
        """Fetch blocks from the given values.

        :param request: Information about the request.
        :param context: Context of the request.

        :return: Blocks protocol-message.
        :rtype: :py:object:`blockchain_pb2.Blocks`
        """

        # TODO -> Fetch the blocks that were requested

        blocks = []

        for req_block in request:
            if req_block.index:
                block_dict = fetch_block(req_block.index)

            elif req_block.timestamp:
                block_dict = fetch_block_from_timestamp(req_block.timestamp)

            elif req_block.hash and req_block.signature:
                block_dict = fetch_block_from_signature(req_block.signature, req_block.hash)

            # Check if fetch was successful
            if not block_dict:
                blocks.append(RPCBlock(index=0, previousHash='', version='', timestamp='',
                                       baseFee=0, tx=[], hash='', signature=''))

            tx = []

            for transaction in block_dict['tx']:
                tx.append(RPCTransaction(sender=transaction['sender'], recipient=transaction['recipient'],
                                         amount=transaction['amount'], fee=transaction['fee'],
                                         type=transaction['tx_type'],
                                         timestamp=transaction['timestamp'], hash=transaction['hash'],
                                         signature=transaction['signature']))

            blocks.append(RPCBlock(index=block_dict['index'], previousHash=block_dict['previous_hash'],
                                   version=block_dict['version'], timestamp=str(block_dict['timestamp']),
                                   baseFee=block_dict['base_fee'], tx=tx, hash=block_dict['hash'],
                                   signature=block_dict['signature']))

        return Blocks(blocks=blocks)

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

        return Transactions(tx=[Transaction(sender='sdf', recipient='sdwf', amount=12, fee=23, type='tx',
                                            timestamp='1234', hash='123231wef', signature='asdf'),
                                Transaction(sender='sdf', recipient='sdwf',
                                            amount=12, fee=23, type='tx', timestamp='1234', hash='123231wef',
                                            signature='asdf')])

    def addTransaction(self, request, context):
        # Recreate the transaction
        tx = Transaction('', '', 0)
        tx.from_dict({
            'sender': request.sender,
            'recipient': request.recipient,

            'amount': request.amount,
            'fee': request.fee,

            'type': request.type,
            'timestamp': request.timestamp,

            'hash': request.hash,
            'signature': request.signature
        })

        # Put it to the processor-queue
        input_queue.put({'type': 'tx', 'data': tx})

        return Success(success=True)

    def addTransactions(self, request, context):
        # Go through all provided transactions
        for transaction in request.transactions:
            # Recreate the transaction
            tx = Transaction('', '', 0)
            tx.from_dict({
                'sender': transaction.sender,
                'recipient': transaction.recipient,

                'amount': transaction.amount,
                'fee': transaction.fee,

                'type': transaction.type,
                'timestamp': transaction.timestamp,

                'hash': transaction.hash,
                'signature': transaction.signature
            })

            # Put it to the processor-queue
            input_queue.put({'type': 'tx', 'data': tx})

        return Success(success=True)


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
    def __init__(self, blockchain, processor_queue, port=None, start=False, db_q=None):
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

        global input_queue
        input_queue = processor_queue

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

        self.server = grpc_server(ThreadPoolExecutor(max_workers=1))

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
