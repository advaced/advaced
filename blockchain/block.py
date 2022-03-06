# SHA256 hash-algorithm
from hashlib import sha3_256

from datetime import datetime
import json

# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '../'))

# Project version
from __init__ import __version__

# Blockchain-classes
from blockchain import Transaction

# Wallet
from accounts import Wallet

class Block:
    def __init__(self, transactions=[], previous_block=None, validator=None, signature=None):
        """Set the block-values up.

        :param transactions: All transactions included into the block.
        :type transactions: [ :py:class: Transaction ]
        :param validator: The public-key of the validator.
        :type validator: str (hex-digest)
        :param signature: Signed hash with the private-key of the validator.
        :type signature: str (hex-digest)
        :param previous_block: The last-block in the blockchain.
        :type previous_block: :py:class: blockchain.block.Block
        """

        # Check if there was a previous-block
        if previous_block:
            self.index = previous_block.index + 1
            self.previous_hash = previous_block.hash

        # Set values for the genesis-block
        else:
            self.index = 1
            self.previous_hash = \
            '0000000000000000000000000000000000000000000000000000000000000000'

        self.version = __version__

        # Create the timestamp of the block
        self.timestamp = datetime.now()

        self.base_fee = 1
        # TODO -> Calculate the base-fee of a transaction (maybe with current
        #         average block creation-time and node-count)

        self.tx = transactions

        self.validator = validator
        self.signature = signature

    @property
    def tx_dict(self) -> list:
        """Creates dictionary-list version of the included transactions.

        :return: List of all transactions in dictionary-format.
        :rtype: list (contains dictionaries)
        """

        # Add all transactions in json-format to a list
        tx_list = []
        for tx in self.tx:
            tx_list.append(tx.to_dict())

        return tx_list

    @property
    def hash(self) -> str:
        """Calculates the hash of the block with the SHA3_256 hash-algorithm.

        :return: Hex-digest of transaction-hash
        :rtype: str (hex-digest)
        """

        # Check if the block contains an important value
        if not self.validator:
            # Development logs
            print("WARNING!: Block incomplete, hash is not completely right!")

        return sha3_256((str(self.index) + self.version + str(self.timestamp) + str(self.base_fee) + str(self.tx_dict) \
                       + self.validator if self.validator else "").encode()).hexdigest()


    @property
    def score(self) -> float:
        """Returns the staking and hash worth of the block.

        :return: Block score (the higher the score the higher is the probability of
                 getting chosen to verify a block).
        :rtype: float
        """
        pass


    def sign_block(self, private_key):
        """Signs the block with the private-key of the validators keypair (The validator must be set).

        :param key: The private-key of the validator
        :type key: str

        :return: Status whether the signature-process worked or not.
        :rtype: bool
        """
        # Fetch the paired public-key
        public_key = Wallet.get_public_key(private_key)

        # Check if private-key is valid
        if not public_key:
            return False

        # Check if the public-key belongs to the validator
        if not self.validator == public_key:
            return False

        # Set signature
        self.signature = Wallet.sign_data(private_key, self.hash)

        # Check if the signature worked
        if not self.signature:
            # Reset the signature
            self.signature = None

            return False

        return True


    def is_valid(self, blockchain, in_chain=False) -> bool:
        """Check if the block is valid.

        :param blockchain: The blockchain where the block is in or should go in.
        :type blockchain: :py:class:`blockchain.Blockchain`
        :param in_chain: Wether the block is already included or not.
        :type in_chain: bool

        :return: Validity of block.
        :rtype: bool
        """

        # Check if the block is the genesis block
        if self.index == 1:
            # TODO -> Compare to the real genesis block
            return True

        # Fetch the previous block
        if in_chain:
            previous_block = blockchain.fetch_block(self.index -1)

        else:
            previous_block = blockchain.last_blocks[0]

        # Check if they could fetch the previous-block
        if previous_block:
            # Check if the previous hash matches with the previous blocks hash
            if not self.previous_hash == previous_block.hash:
                return False

            # Compare the timestamps
            if self.timestamp < previous_block.timestamp:
                # Previous block was generated after current block
                return False

        # Check version
        if not self.version == blockchain.version: # TODO -> Add versionstamp checks, not only for current version
            return False

        # Check timestamp
        if self.timestamp > datetime.now():
            # Block is from the future
            return False

        # TODO -> Add base-fee checker

        # Check if transactions are valid
        for transaction in self.tx:
            if not transaction.is_valid(blockchain, in_chain):
                return False

        # Check if validators signature is valid
        if not Wallet.valid_signature(self.validator, self.signature, self.hash):
            return False

        # TODO -> Add stake check (if the validator has staked enough to validate a block)

        return True


    def to_dict(self) -> dict:
        """Creates dictionary from block-information.

        :return: Block in dict-format
        :rtype: dict
        """
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,

            'version': self.version,
            'timestamp': str(self.timestamp),

            'base_fee': self.base_fee,
            'tx': self.tx_dict,

            'hash': self.hash,
            'validator': self.validator,
            'signature': self.signature
        }


    def to_json(self):
        """For data transportation/storing purposes, a json-format is created

        :return: Block in json-format
        :rtype: str (stringified json)
        """
        return json.dumps(self.to_dict())


    def from_dict(self, block_dict):
        """Set block-data from dictionary.

        :param block_dict: Information of block.
        :type block_dict: dict

        :return: A status wether the data-load was successful or not
        :rtype: bool
        """
        try:
            # Reinitialize block from data
            self.index = block_dict['index']
            self.version = block_dict['version']
            self.base_fee = block_dict['base_fee']

            success = self.from_tx_dict(block_dict['tx'])

            # Check if transaction initialization was successful
            if not success:
                return False

            # Create datetime-object from string
            self.timestamp = datetime.strptime(block_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')

            self.previous_hash = block_dict['previous_hash']

            # Check if the validator is included in the json-data
            if block_dict['validator']:
                self.validator = block_dict['validator']

            # Check if the signature is included in the json-data
            if block_dict['signature']:
                self.signature = block_dict['signature']

            # Check if the hashes are the same
            if block_dict['hash'] and not self.hash == block_dict['hash']:
                return False

        # An error occurred while assigning data
        except:
            return False

        return True


    def from_tx_dict(self, tx_dict):
        """Create transactions from dict-data

        :param tx_dict: List that includes transaction-values as dict-object.
        :type tx_dict: list

        :return: A status wether the data-load was successful or not
        :rtype: bool
        """

        # Set transactions class-list up
        tx_list = []
        for tx in tx_dict:
            # Set transaction class up
            new_tx = Transaction("", "", 0)
            success = new_tx.from_dict(tx)

            # Check if something did not seem to work
            if not success:
                return False

            # Add to list
            tx_list.append(new_tx)

        # Parse the list
        self.tx = tx_list

        return True


    def from_json(self, json_data):
        """Create block from json-data.

        :param json_data: String in json-format that includes the block-values
        :type json_data: str

        :return: A status wether the data-load was successful or not
        :rtype: bool
        """
        try:
            # Convert json to dictionary
            dict_data = json.loads(json_data)

            # Assign dictionary-data to the class
            success = self.from_dict(dict_data)

            # Check if data initialization was successful
            if not success:
                return False

        # Return the status
        except KeyError or json.JSONDecodeError:
            return False

        return True
