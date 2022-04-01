# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Block class to recreate cache
from blockchain.block import Block

# Database-connector
from util.database.blockchain import fetch_block
from util.database.database import Database


def load_cache():
    """Loads the last 100 blocks from the chain.

    :return: Status when no blocks are available or fetchable
    :rtype: bool
    :return: List of blocks.
    :rtype: :py:class:`blockchain.Block`
    """
    biggest_index = Database.fetchone_from_db('SELECT MAX(block_index) AS block_index FROM blockchain', { })

    if not type(biggest_index) == int:
        biggest_index = biggest_index[0]

    # Check if there are any blocks
    if not biggest_index:
        return False

    # Set the cache up
    last_blocks = [ ]

    if biggest_index == 1:
        block_dict = fetch_block(1)

        block = Block()
        block.from_dict(block_dict)
        last_blocks.append(block)

        return last_blocks

    # Go through all blocks that come into the cache
    for x in reversed(range(biggest_index - 100, biggest_index + 1)):
        # Check if no more blocks can be fetched
        if x < 0:
            return last_blocks

        block_dict = fetch_block(x)

        block = Block()
        block.from_dict(block_dict)
        last_blocks.append(block)

    return last_blocks
