from hashlib import sha3_256
from datetime import datetime, timezone
import json

# Add to path
from sys import path
import os

path.insert(0, os.path.join(os.getcwd(), '..'))

# Wallet
from accounts import Wallet


class Transaction:
    def __init__(self, sender, recipient, amount, fee=0, tx_type='tx', tip=0):
        """Set the transaction-values up.

        :param sender: The public-key of the sender.
        :type sender: str (hex-digest)
        :param recipient: The public-key of the recipient.
        :type recipient: str (hex-digest)
        :param amount: The amount of coins that the sender transacts.
        :type amount: int
        :param fee: The transaction-fee, that is added to the incentive for the validators.
        :type fee: int
        :param type: tx (transaction), stake (staking event), claim (claiming event), burn (expropriation event)
        :type type: str
        :param tip: Tip for the validators (if the transactor wants to donate some money to get prioritized).
        :type tip: int
        """

        self.sender = sender
        self.recipient = recipient
        self.amount = amount

        # Set the fee
        if tx_type == 'tx':
            self.fee = fee + tip

        elif tx_type == 'stake' or tx_type == 'unstake' or tx_type == 'claim':
            # Cut the fee in half
            self.fee = fee / 2 + tip

        else:
            # Is a burn transaction
            self.fee = fee / 8

        self.type = tx_type
        self.signature = None

        # Add a timestamp
        self.timestamp = datetime.now(timezone.utc)

    @property
    def hash(self) -> str:
        """Calculates the hash of the transaction with the SHA3-256 hash-algorithm.

        :return: Hex-digest of transaction-hash
        :rtype: str (hex-digest)
        """
        return sha3_256((str(self.sender) + str(self.recipient) + str(float(self.amount)) + str(float(self.fee)) +
                         str(self.type) + str(self.timestamp)).encode()).hexdigest()

    def sign_tx(self, private_key):
        """Signs the transaction with the private-key of the keypair (in most cases the private-key of the sender)

        :param private_key: The private-key of the sender (in some cases the key of the recipient)
        :type private_key: str

        :return: Status whether the signature-process worked or not.
        :rtype: bool
        """

        # Fetch the paired public-key
        public_key = Wallet.get_public_key(private_key)

        # Check if private-key is valid
        if not public_key:
            return False

        # Check if public-key is either the senders or the recipients key
        # if ((not self.sender == public_key and not self.type == 'tx' and not self.type == 'stake'
        #     and not self.type == 'unstake' and not self.type == 'claim') or (not self.recipient == public_key
        #     and not self.type == 'burn')):
        #     return False

        # Set signature
        self.signature = Wallet.sign_data(private_key, self.hash)

        # Check if the signature worked
        if not self.signature:
            # Reset the signature
            self.signature = None

            return False

        return True

    def is_valid(self, blockchain, in_chain=False) -> bool:
        """Check if transactions-signature is valid.

        :param blockchain: The blockchain where the transaction should go in.
        :type blockchain: :py:class:`blockchain.Blockchain`
        :param in_chain: If the transaction is already in the chain.
        :type in_chain: bool

        :return: Validity of transaction and its signature.
        :rtype: bool
        """

        # Check if numbers are negative or zero
        if self.amount < 0 or self.fee <= 0:
            return False

        # Check if transaction is parsed
        if not self.signature:
            return False

        # Set the verifying-key for signature-validity check
        verifying_key = self.sender

        if self.type == 'burn':
            verifying_key = self.recipient

        # Check if the transaction type is wrong
        if (not self.type == 'tx' and not self.type == 'stake' and not self.type == 'unstake'
            and not self.type == 'claim'):
            return False

        # Check if the signature is valid
        if not Wallet.valid_signature(verifying_key, self.signature, self.hash):
            return False

        # Check if transaction is signed for the future
        if self.timestamp > datetime.now(timezone.utc):
            return False

        # Only for not in-chain transactions
        if not in_chain:
            # Check if transaction is already in the chain if it should not be
            if blockchain.tx_included(self):
                return False

            # TODO -> Check whether the sender (if its a tx or stake) can afford it
            #         (or at unstake, if the sender has enough stake)

        return True

    def to_dict(self) -> dict:
        """Create dictionary format of the transaction

        :return: Transaction in dict-format
        :rtype: dict
        """
        return {
            'sender': self.sender,
            'recipient': self.recipient,

            'amount': self.amount,
            'fee': self.fee,

            'type': self.type,
            'timestamp': str(self.timestamp),

            'hash': self.hash,
            'signature': self.signature
        }

    def from_dict(self, dict_data) -> bool:
        """Create transaction from dict-data.

        :param dict_data: Dictionary that includes the transaction-values
        :type dict_data: dict

        :return: Status whether the transaction was created or not.
        :rtype: bool
        """
        try:
            # Set the data to the transaction
            self.sender = dict_data['sender']
            self.recipient = dict_data['recipient']
            self.amount = dict_data['amount']
            self.fee = dict_data['fee']
            self.type = dict_data['type']

            # Check if the signature is included in the dict-data
            if dict_data['signature']:
                self.signature = dict_data['signature']

            self.timestamp = datetime.strptime(dict_data['timestamp'], '%Y-%m-%d %H:%M:%S.%f%z').replace(
                                               tzinfo=timezone.utc)

        # Return the status
        except:
            return False

        return True

    def to_json(self) -> str:
        """For data transportation/storing purposes, a json-format is created

        :return: Transaction in json-format
        :rtype: str (json)
        """
        return json.dumps(self.to_dict())

    def from_json(self, json_data) -> bool:
        """Create transaction from json-data

        :param json_data: String in json-format that includes the transaction-values
        :type json_data: str

        :return: A status whether the data-load was successful or not
        :rtype: bool
        """

        # Convert json to dictionary
        dict_data = json.loads(json_data)

        self.from_dict(dict_data)

        return True
