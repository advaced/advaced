# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Blockchains
from blockchain.block import Block

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
        self.wallet = Wallet(public_key, private_key)

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
        success = block.sign_block(self.wallet.private_key)

        # Check if signature was successful
        if not success:
            return block, False

        # Check if the validation was successful
        if not block.validator or not block.signature:
            return block, False

        # Return block with success
        return block, True


    def select_winner(self, blockchain, clear_temp=False):
        """Decides who wins the next validation-lottery (everyone in the network has the same result).

        :return: Block who won the lottery.
        :rtype: :py:class:`blockchain.Block`
        """
        attendees = [ ]

        # Go through all temporary blocks
        for tmp in self.temp_blocks:
            # Add the validators staking score (stake and its age), his address and the decimal-version of the blocks hash
            attendees.append([Wallet.score(tmp.validator, blockchain), tmp.validator, int(tmp.hash, 16)])

        # Sort the attendees after the smallest to the biggest decimal hash value
        attendees.sort(key=lambda x: x[2])

        # Drop the hash value
        attendees = list(map(lambda x: x[0:2], attendees))

        for i in range(0, len(attendees)):
            # Calculate the validators staking score with his current rank
            attendees[i][0] * .9 ** (i + 1)

        # Filter attendees out until a winner gets found
        while len(attendees) > 1:
            for i in range(0, len(attendees), 2):
                # Check if there is another competitor
                if len(attendees) <= pos + 1:
                    # Drop this attendee from the competitors list
                    attendees.pop(i)
                    break

                # Check if the second score is bigger than the first one
                if attendees[i][0] < attendees[i + 1][0]:
                    attendees[i + 1][0] += attendees[i][0]
                    attendees[i] = None

                else:
                    # Drop the second, beacause the first score is bigger or,
                    # even if they are equal, the first one has a better rank
                    attendees[i][0] += attendees[i + 1][0]
                    attendees[i + 1] = None

            # Filter the atendees out, that lost in this round
            attendees = list(filter(None, attendees))

        # Fetch the block that won this round
        winner_block = list(filter(lambda x: x.validator == attendees[0][1], self.temp_blocks))[0]

        # Check if the temporary blocks should be cleaned
        if clear_temp:
            self.temp_blocks = [ ]

        return winner_block

        # Selection scheme (with a merkle tree)
        # block validator:              0x132F45
        # winner:                        ^^^^
        # next round:                   14_589                               |  11_653,7        (first round enemies + own coin age*.9^rank)
        # winner:                       ^^^^           |                     |   ^^^^                |
        # sum of coin_age*.9^rank:  8_200*.9^1 = 7_380 | 8_900*.9^2 = 7_209  | 12_300*.9^3 = 8_966.7 |  4_096*.9^4 = 2_687  <<< coin_age * 0.9 ** rank >>>
        # (1 against 2, 3 against 4 ... if the one with the biggest hash in decimal has no partner he gets sorted out)

        # hash in decimal:          12_232             | 271_348             | 372_489_348_324       | 524_234_234_342
        # validators:               0x132F45            |  0x3B45              |  0x43543B456           | 73457458AB234C
