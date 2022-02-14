# SHA256 hash-algorithm
from hashlib import sha256

# Datetime-module
from datetime import datetime

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
        :param type: tx (transaction), stake (staking event), unstake (unstaking event)
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
        :type: str

        :return: Signature of the transaction-hash and private-key
        """
        return ''
