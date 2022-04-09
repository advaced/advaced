# gRPC
from grpc import insecure_channel

# Protobuf
from blockchain_pb2_grpc import BlockchainStub
from wallet_pb2 import WalletRequest, WalletResponse
from wallet_pb2_grpc import WalletStub

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project version
from __init__ import RPC_PORT

from time import sleep


class Client:
    def __init__(self, ip_address, port=None):
        self.ip_address = ip_address
        self.port = port if port else RPC_PORT

    def getBlock(self, block_request):
        """Fetch block from blockchain.

        :param block_request: Given block parameters to fetch.
        :type block_request: :py:class:`rpc.blockchain_pb2.BlockRequest`

        :return: Result of requested block.
        :rtype: :py:class:`rpc.blockchain_pb2.Block`
        """

        # TODO -> Fetch from multiple servers and compare the values

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the block and return it to the user
                return stub.getBlock(block_request)

        except:
            return False

    def getBlocks(self, block_request):
        """Fetch blocks from blockchain.

        :param block_request: Given parameters of the blocks to fetch.
        :type block_request: :py:class:`rpc.blockchain_pb2.BlockRequest`

        :return: Result of requested blocks.
        :rtype: :py:class:`rpc.blockchain_pb2.Blocks`
        """

        # TODO -> Fetch from multiple servers and compare the values

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the blocks and return it to the user
                return stub.getBlocks(block_request)

        except:
            return False

    def getTransaction(self, tx_request):
        """Fetch transaction from blockchain.

        :param tx_request: Given parameters of the transaction to fetch.
        :type tx_request: :py:class:`rpc.blockchain_pb2.TransactionRequest`

        :return: Result of requested transaction.
        :rtype: :py:class:`rpc.blockchain_pb2.Transaction`
        """

        # TODO -> Fetch from multiple servers and compare the values

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the transaction and return it to the user
                return stub.getTransaction(tx_request)

        except:
            return False

    def getTransactions(self, tx_request):
        """Fetch transactions from blockchain.

        :param tx_request: Given parameters of the transactions to fetch.
        :type tx_request: :py:class:`rpc.blockchain_pb2.TransactionRequest`

        :return: Result of requested transactions.
        :rtype: :py:class:`rpc.blockchain_pb2.Transactions`
        """

        # TODO -> Fetch from multiple servers and compare the values

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the transactions and return it to the user
                return stub.getTransactions(tx_request)

        except:
            return False

    def addTransaction(self, tx):
        """Add transaction to blockchain.

        :param tx: Given parameters of the transaction to add.
        :type tx: :py:class:`rpc.blockchain_pb2.Transaction`

        :return: Status wether the transaction was added successful or not.
        :rtype: :py:class:`rpc.blockchain_pb2.Success`
        """

        # TODO -> Send data to multiple servers

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the status of success and return it to the user
                return stub.addTransaction(tx)

        except:
            return False

    def addTransactions(self, tx):
        """Add transactions to blockchain.

        :param tx: Given parameters of the transactions to add.
        :type tx: :py:class:`rpc.blockchain_pb2.Transactions`

        :return: Status wether the transactions were added successful or not.
        :rtype: :py:class:`rpc.blockchain_pb2.Success`
        """

        # TODO -> Send data to multiple servers

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the status of success and return it to the user
                return stub.addTransactions(tx)

        except:
            return False

    # def run(self):
    #     """Connect to rpc server.

    #     """
    #     # Create connection to rpc server
    #     with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
    #         #stub = BlockchainStub(channel)
    #         wallet_stub = WalletStub(channel)

    #         # Test connection
    #         while True:
    #             try:
    #                 response = wallet_stub.getCoins(WalletRequest(public_key="187"))
    #                 print(response)
    #                 # response = stub.getBlock(BlockRequest(index=123))

    #             except KeyboardInterrupt:
    #                 channel.unsubscribe(self.close)

    # def close(channel):
    #     channel.close()


if __name__ == '__main__':
    cl = Client('localhost')
    # cl.run()
    from rpc.blockchain_pb2 import Transaction

    print(cl.addTransaction(Transaction(
        sender='690ec29bae1791c134acfa0a5f49ebcc43491493e41f751ed319a67db8f75d6dc2acc288b7e7d160ed3362c9490b40ff399047e639a9a0862f6dcd227fbd9f99',
        recipient='187',
        amount=420,
        fee=2,
        type='tx',
        timestamp='2022-04-01 01:10:51.364127+00:00',
        hash='0a874cab556a53fc0b9ce256e4239c8c0ffb1d4f11e9854dd1244f37124c607e',
        signature='aa8a17a754a3007f9ee0d7ff9429f716f6f82327ad6dc1fd66fae546d20914bde43771e25ff75c33598f0e8680cbfd3ef557ce7532d2bc939ea1e5667e4ad860'
        )))
