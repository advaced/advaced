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

        # TODO -> Calc coin age and select winner through merkle tree with first psoitioning from the bigness of the hash

        # Selection scheme (with a merkle tree)
        # block validator:              0x132F45
        # winner:                        ^^^^
        # next round:                   14_589                               |  11_653,7        (first round enemies + own coin age*.9^rank)
        # winner:                       ^^^^           |                     |   ^^^^                |
        # sum of coin_age*.9^rank:  8_200*.9^1 = 7_380 | 8_900*.9^2 = 7_209  | 12_300*.9^3 = 8_966.7 |  4_096*.9^4 = 2_687  <<< coin_age * pow(0.9, rank) >>>
        # (1 against 2, 3 against 4 ... if the one with the biggest hash in decimal has no partner he gets sorted out)

        # hash in decimal:          12_232             | 271_348             | 372_489_348_324       | 524_234_234_342
        # validators:               0x132F45            |  0x3B45              |  0x43543B456           | 73457458AB234C
