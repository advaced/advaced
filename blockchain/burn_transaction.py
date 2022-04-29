import json
from datetime import datetime, timezone

# Project modules
from blockchain.block import Block
from blockchain.transaction import Transaction


class BurnTransaction(Transaction):
    def __init__(self, sender, recipient, amount, proof_data, fee=0):
        super().__init__(sender, recipient, amount, fee, tx_type='burn')

        self.proof_data = proof_data

    @staticmethod
    def valid_proof(proof_data, blockchain) -> bool:
        """Check if the proof is valid.

        :param proof_data: Proof-data to validate
        :type proof_data: str
        :param blockchain: Blockchain to validate the proof.
        :type blockchain: :py:class:`blockchain.blockchain.Blockchain`

        :return: Status whether the proof-data is valid or not.
        :rtype: bool
        """

        # Load the proof-data from json
        proof_data = json.loads(proof_data)

        # Check which type of proof-data is used
        if proof_data['type'] == 'tx':
            # Fetch the transaction from the proof-data
            tx = Transaction('', '', 0)
            success = tx.from_dict(proof_data['data'])

            # Check if the transaction was created successfully
            if not success:
                return False

            # Check if the transaction is invalid
            if tx.is_valid(blockchain, in_chain=False):
                return False

            return True

        elif proof_data['type'] == 'block':
            # Fetch the block from the proof-data
            block = Block()
            success = block.from_dict(proof_data['data'])

            # Check if the block was created successfully
            if not success:
                return False

            # Check if the block is invalid
            if block.is_valid(blockchain, in_chain=False):
                return False

            return True

        return False

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
            'signature': self.signature,

            # Proof data (normally in json format)
            'proof_data': self.proof_data
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

            self.proof_data = dict_data['proof_data']

        # Return the status
        except:
            return False

        return True
