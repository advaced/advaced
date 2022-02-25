# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '../'))

# Blockchain
from blockchain import Block

# Signatures
from accounts import Wallet

class Validator():
    def __init__(self, private_key):
        """Initialize required values for the validation process.

        :param private_key: Private-key of the validator.
        :type private_key: str
        """

        # Fetch public from private key
        public_key = Wallet.get_public_key(private_key)

        # Initialize wallet
        self.wallet = Wallet('Validator', public_key, private_key)

        # The temporary blocks for the next validation
        self.temp_blocks = [ ]


    def validate_block(self, block: Block):
        """Validate and sign the block (only for new blocks).

        :param block: Block to validate and sign.
        :type block: :py:class:`blockchain.Block`

        :return: Validated and signed block and the success of the validation.
        :rtype: :py:class:`blockchain.Block`, bool
        """
        # Set the validator with the public key
        block.validator = self.wallet.public_key

        # Sign the block
        block.sign_block(self.wallet.private_key)

        # Check if the validation was successful
        if not block.validator or not block.signature:
            return block, False

        # Return block with success
        return block, True


    def select_winner(self):
        """Decides who wins the next validation-lottery (everyone in the network has the same result).

        :return: Block who won the lottery.
        :rtype: :py:class:`blockchain.Block`
        """
        pass
