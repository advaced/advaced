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

        :return: Status whether the transaction was added successful or not.
        :rtype: :py:class:`rpc.blockchain_pb2.Success`
        """

        # TODO -> Send data to multiple servers

        try:
            print(f'Sending transaction to {self.ip_address}:{self.port}')
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the status of success and return it to the user
                return stub.addTransaction(tx)

        except Exception as e:
            raise e
            # return False

    def addTransactions(self, tx):
        """Add transactions to blockchain.

        :param tx: Given parameters of the transactions to add.
        :type tx: :py:class:`rpc.blockchain_pb2.Transactions`

        :return: Status whether the transactions were added successful or not.
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

    def getBaseFee(self):
        """Get base fee of the blockchain.

        :return: Base fee of the blockchain.
        :rtype: :py:class:`rpc.blockchain_pb2.BaseFee`
        """

        # TODO -> Fetch from multiple servers and compare the values

        try:
            with insecure_channel(f'{self.ip_address}:{self.port}') as channel:
                stub = BlockchainStub(channel)

                # Fetch the base fee and return it to the user
                return stub.getBaseFee()

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
        sender='6ae5c2a44e5ae92193de10297879955061db681b3099d9aa06ef31791ce2153ec9cebf2e4f8644e84a2d028201c1a8de438ef43f2a18e83b9ff0b850e5f01638',
        recipient='sdfasdfadsfdasfawergraeg',
        amount=1,
        fee=1,
        type='tx',
        timestamp='2022-05-02 15:23:55.578422+00:00',
        hash='5c93e060d3fcf716d97ea0f7ca324770054803b3ae11f5ef17701926699d547f',
        signature='2397c39325d09acb3d5ae0d9ec6353c539636f74457c8f8e7719aaaf58a105adf353a373848db0d28201b58c1da30e607d4a588a895d313d2704ff836931795e'
    )))
