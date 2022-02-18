# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '../'))

# Project version
from __init__ import __version__

# Blockchain-classes
from blockchain import Block, Transaction

# Wallet
from accounts import Wallet

class Blockchain:
    def __init__(self, genesis_block=None, genesis_keys: [ str ]=None, versionstamps=None):
        # Set chain-versioning
        self.version = __version__
        self.versionstamps = versionstamps if versionstamps else {
            # TODO -> Add auto-fetching from new versions and its migration-timestamps
        }

        # Contains the last 100 blocks / Create the genesis blocks
        self.last_blocks = [ genesis_block if genesis_block else self.create_genesis(igenesis_keys if genesis_keys else [ ]) ]


    @property
    def is_valid(self) -> bool:
        """Check whether the blockchain is valid or not (Pretty important to make sure, that the block a node shares is valid).

        :return: Status of the chain-validity
        :rtype: bool
        """

        # Check if the cache is valid
        if not self.valid_cache:
            return False

        # TODO -> Add verification for whole chain (also the table in the database)

        return True


    @property
    def valid_cache(self) -> bool:
        """Check whether the last 100 blocks are valid or not (Pretty important to make sure, that the block a node shares is valid).

        :return: Status of the last 100 blocks-validity
        :rtype: bool
        """

        # Go through blocks and check their validity
        for block in reversed(self.last_blocks):
            if not block.is_valid(self, True):
                return False

        return True


    @staticmethod
    def create_genesis(tx_data: [ Transaction ]=None):
        """Create the first block in the chain.

        :param tx_data: All transactions, that the first block should include.
        :type tx_data: [ Transaction ]

        :return: First block in chain
        :rtype: :py:class:`blockchain.Block`
        """

        return Block(tx_data if tx_data else [ ], None,
                    # Not a real public-key and no real signature
                    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')


    def add_block(self, block: Block):
        """Adds block to the blockchain.

        :param block: The block to add.
        :type block: :py:class:`blockchain.Block`

        :return: State of success.
        :rtype: bool
        """

        # Check if block contains all necessary values
        if not self.last_blocks[0].hash == block.previous_hash or self.last_blocks[0].timestamp > block.timestamp or \
           not self.last_blocks[0].index == block.index - 1 or not block.version == self.version or \
           not block.validator or not block.signature:
           # Return with no success
           return False

        # Check if block is valid
        if not block.is_valid(self):
            return False

        # Add block to chain
        self.last_blocks.insert(0, block)

        # Push block to database
        # TODO -> Push block 101 to database

        # Reduce all blocks in last-blocks cache, that are over the last 100
        while len(self.last_blocks) > 100:
            # Remove the last block from the caching-list
            self.last_blocks.pop(len(self.last_blocks) -1)

        return True


    def fetch_block(self, index=None, tx: Transaction=None, address=None):
        """Fetch block from its index, from an included transaction or from a mentionend adress.

        :param index: Index of the block.
        :type index: :py:class:`blockchain.Block.index`
        :param tx: Transaction contained in the block.
        :type tx: :py:class:`blockchain.Transaction`
        :param address: Public-key mentionend in the block to fetch.
        :type address: str (hex-digest)

        :return: Block to fetch or false whether the block could or could not be found.
        :rtype: :py:class:`blockchain.Block` | bool
        """

        # Check wich value for the fetching is used
        if index:
            # Check if index is in ratio
            if index < 0:
                return False

            # Check wether the index is higher than the chains highest
            if index > self.last_blocks[0].index:
                return False

            # Check if block is within the block cache
            if index > self.last_blocks[-1].index:
                # Go through the cache and find the block
                for block in self.last_blocks:
                    if index == block.index:
                        return block

        elif tx:
            pass

        elif address:
            pass

        return False


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

        # TODO -> Create inclusion-checks for blocks within the database

        return False


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
                # TODO -> Improve cache searching (no for loop, the position is calculatable!)

                # Go through blocks transactions
                for transaction in block.tx:
                    # Check if the transaction is the same
                    if tx == transaction:
                        return True

        # TODO -> Create inclusion-checks for blocks within the database

        return False
