# Add to path
from sys import path
import os

path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Project version
from __init__ import __version__

# Blockchain-classes
from blockchain.transaction import Transaction
from blockchain.block import Block

# Database-handler
from util.database.blockchain import (add_block, fetch_block, fetch_transaction_block_index, fetch_transactions,
                                      fetch_version_stamps, add_version_stamp)
from util.database.cache import load_cache


class Blockchain:
    def __init__(self, network='mainnet', genesis_block=None, genesis_tx: [Transaction] = None):
        # Set chain-versioning
        self.version = __version__
        self.version_stamps = fetch_version_stamps(network)

        # Check if a genesis-block was provided
        if genesis_block:
            # Last block cache contains the last 100 blocks | Include genesis block into chain
            self.last_blocks = [genesis_block]

        # Check if genesis-transactions were given
        elif genesis_tx:
            genesis_block = self.create_genesis(genesis_tx if genesis_tx else [])

            # Last block cache contains the last 100 blocks | Include genesis block into chain
            self.last_blocks = [genesis_block]
            add_block(genesis_block.to_dict())

        # Fetch last-blocks from database
        else:
            self.load_last_blocks()

    @property
    def is_valid(self) -> bool:
        """Check whether the blockchain is valid or not (Pretty important to make sure, that the block a node shares is valid).

        :return: Status of the chain-validity
        :rtype: bool
        """

        # Check if the cache is valid
        if not self.valid_cache:
            return False

        # Check if there are any blocks that are not cached
        if self.last_blocks[-1].index - 1 > 1:

            # Go through all the blocks in the database
            for x in range(1, self.last_blocks[-1].index - 1):
                # Fetch dict-data of the block
                block_data = fetch_block(x)

                # Check if the block could be fetched
                if not block_data:
                    # TODO -> Ask other nodes for block
                    return False

                # Skip, if it is the genesis block
                if block_data['index'] == 1:
                    continue

                # Initialize block from the data
                block = Block()
                success = block.from_dict(block_data)

                # Check if the block recreation was successful
                if not success:
                    return False

                # Check if the block and its transactions are valid
                if not block.is_valid(self, in_chain=True):
                    print('no valid')
                    block.to_dict()
                    return False

        return True

    @property
    def valid_cache(self) -> bool:
        """Check whether the last 100 blocks are valid or not (Pretty important to make sure,
           that the block a node shares is valid).

        :return: Status of the last 100 blocks-validity
        :rtype: bool
        """

        # Go through blocks and check their validity
        for block in reversed(self.last_blocks):
            if not block.is_valid(self, in_chain=True):
                return False

        return True

    @staticmethod
    def create_genesis(tx_data: [Transaction] = None):
        """Create the first block in the chain.

        :param tx_data: All transactions, that the first block should include.
        :type tx_data: [ Transaction ]

        :return: First block in chain
        :rtype: :py:class:`blockchain.Block`
        """

        return Block(tx_data if tx_data else [],
                     # Not a real public-key and no real signature
                     validator='00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                     signature='00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def load_last_blocks(self):
        """Loads the cache (last 100 blocks) from the database.

        :return: Load was successful.
        :rtype: bool
        """

        # Fetch last 100 blocks (or as much as there is) from the database
        new_cache = load_cache()

        # Something went wrong
        if not new_cache:
            return False

        # Currently there is nothing to cache
        if new_cache == True:
            self.last_blocks = []

            return True

        # Set the new cache
        self.last_blocks = new_cache

        return True

    def add_block(self, block: Block, genesis=False):
        """Adds block to the blockchain.

        :param block: The block to add.
        :type block: :py:class:`blockchain.Block`
        :param genesis: Is this the genesis block?
        :type genesis: bool

        :return: State of success.
        :rtype: bool
        """

        # Check if block contains all necessary values
        if (not self.last_blocks[0].hash == block.previous_hash or self.last_blocks[0].timestamp > block.timestamp or
            not self.last_blocks[0].index == block.index - 1 or not block.version == self.version or
            not block.validator or not block.signature):
            # Return with no success
            return False

        # Check if block is valid
        if not block.is_valid(self):
            return False

        # Add block to chain if it is not the genesis block
        if not genesis:
            self.last_blocks.insert(0, block)

        # Push block to database
        success = add_block(block.to_dict())

        # Reduce all blocks in last-blocks cache, that are over the last 100
        while len(self.last_blocks) > 100:
            # Remove the last block from the caching-list
            self.last_blocks.pop(len(self.last_blocks) - 1)

        # Check if the data is wrong or the block already is included into the chain
        if not success:
            # TODO -> Check why the operation failed
            #         (becuase the data was wrong or the block is already included into the chain)
            return False

        return True

    def fetch_block(self, index=None, tx: Transaction = None, address=None):
        """Fetch block from its index, from an included transaction or from a mentioned address.

        :param index: Index of the block.
        :type index: :py:class:`blockchain.Block.index`
        :param tx: Transaction contained in the block.
        :type tx: :py:class:`blockchain.Transaction`
        :param address: Public key mentioned in the block to fetch.
        :type address: str

        :return: Block to fetch or false whether the block could or could not be found.
        :rtype: :py:class:`blockchain.Block` | bool
        """

        # Check which value for the fetching is used
        if index:
            # Check if index is in ratio
            if index < 0:
                return False

            # Check whether the index is higher than the chains highest
            if index > self.last_blocks[0].index:
                return False

            # Check if block is within the block cache
            if index > self.last_blocks[-1].index:
                # Go through the cache and find the block
                for block in self.last_blocks:
                    if index == block.index:
                        return block

            # If not in cache fetch it from the database
            block_dict = fetch_block(index)

            # Check if block was fetched successful
            if not block_dict:
                return False

            # Set block up
            block_dict = fetch_block(index)

            block = Block()
            block.from_dict(block_dict)

            # Check if the block was fetched successful
            if not block:
                return False

            return block

        elif tx:
            pass

        elif address:
            pass

        return False

    @staticmethod
    def fetch_transactions(public_key: str, tx_type: str = None, is_sender: bool = None):
        """Fetch all transactions the account made in the past.

        :param public_key: Verifying key of the account.
        :type public_key: str
        :param tx_type: Type of the transaction.
        :type tx_type: str
        :param is_sender: If the account is the sender, the recipient or both.
        :type is_sender: bool | NoneType

        :return: List of transactions the account made or received.
        :rtype: [ Transaction ]
        """
        return fetch_transactions(public_key, tx_type, is_sender)

    def block_included(self, block: Block) -> bool:
        """Check whether the block is in the chain or not.

        :param block: Block to search for.
        :type block: :py:class:`blockchain.Block`

        :return: Block is included in the blockchain (True | False).
        :rtype: bool
        """
        # Check if block is in cache
        if block in self.last_blocks:
            return True

        # Fetch block from the database
        block_dict = fetch_block(block.index)

        # Check if block-dict was fetched successful
        if not block_dict:
            return False

        # Check if fetched block is equal to the other block
        if not block_dict["timestamp"] == str(block.timestamp):
            return False

        if not block_dict["validator"] == block.validator:
            return False

        if not block_dict["signature"] == block.signature:
            return False

        return True

    def tx_included(self, tx: Transaction) -> bool:
        """Check whether the transaction is in the chain or not.

        :param tx: Transaction to search for.
        :type tx: :py:class:`blockchain.Transaction`

        :return: Transaction is included in the blockchain (True | False).
        :rtype: bool
        """

        # Check if transaction is in block-cache
        for block in reversed(self.last_blocks):
            # Check if timestamp of the transaction is in the ratio
            if tx.timestamp <= block.timestamp:
                # TODO -> Improve cache searching (no for loop, the position can be calculated!)

                # Go through blocks transactions
                for transaction in block.tx:
                    # Check if the transaction is the same
                    if tx == transaction:
                        return True

        # Check if transaction is in the database
        if fetch_transaction_block_index(tx):
            return True

        return False

    def add_version_stamp(self, version, timestamp, network, public_key, signature, db_q=None):
        """Add a version stamp to the cache and the database.

        :param version: Version that should be added
        :type version: str
        :param timestamp: Timestamp that should be added
        :type timestamp: int
        :param network: Network that the stamp should be added to
        :type network: str
        :param public_key: Public key of the account to verify the version stamps signature.
        :type public_key: str
        :param signature: Signature of the version stamp.
        :type signature: str
        :param db_q: Database query to use.
        :type db_q: :py:class:`queue.Queue`

        :return: Status of the success of the operation.
        :rtype: bool
        """
        # Add version stamp to cache
        self.version_stamps[timestamp] = version

        # Add version stamp to database
        return add_version_stamp(version, timestamp, network, public_key, signature, db_q)
