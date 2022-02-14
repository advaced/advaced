# SHA256 hash-algorithm
from hashlib import sha256

from datetime import datetime
import json


class Transaction:
    def __init__(self, sender, recipient, amount, fee=None, tx_type='tx', signature=None):
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
        :param signature: Signed hash with the private-key of the sender (or in some cases with the private-key
                          of the recipient).
        :type signature: str (hex-digest)
        """

        self.sender = sender
        self.recipient = recipient
        self.amount = amount

        # Set the base-fee when no fee is set
        self.fee = fee if fee else 1 # TODO -> Create a base-fee fetching-function

        self.type = tx_type
        self.signature = signature

        # Add a timestamp
        self.timestamp = datetime.now()


    @property
    def hash(self) -> str:
        """Calculates the hash of the transaction with the SHA256 hash-algorithm.

        :return: Hex-digest of transaction-hash
        """
        return sha256((self.sender + self.recipient + str(self.amount) + str(self.fee) + self.type + str(self.timestamp)).encode()).hexdigest()


    def sign_tx(self, key) -> str:
        """Signs the transaction with the private-key of the keypair (in most cases the private-key of the sender)

        :param key: The private-key of the sender (in some cases the key of the recipient)
        :type key: str

        :return: Signature of the transaction-hash and private-key
        """
        return ''


    def to_json(self):
        """For data transportation/storing purposes, a json-format is created

        """
        tx_dict = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'type': self.type,
            'timestamp': str(self.timestamp),
            'hash': self.hash,
            'signature': self.signature
        }

        return json.dumps(tx_dict)


    def from_json(self, json_data) -> bool:
        """Create transaction from json-data

        :param json_data: String in json-format that includes the transaction-values
        :type json_data: str

        :return: A status wether the data-load was successful or not
        :rtype: bool
        """

        # Convert json to dictionary
        dict_data = json.loads(json_data)

        try:
            # Set the data to the transaction
            self.sender = dict_data['sender']
            self.recipient = dict_data['recipient']
            self.amount = dict_data['amount']
            self.fee = dict_data['fee']
            self.type = dict_data['type']

            # Check if the signature is included in the json-data
            if dict_data['signature']:
                self.signature = dict_data['signature']

            self.timestamp = dict_data['timestamp']

        # Return the status
        except KeyError:

            return False

        return True
