# Add to path
from sys import path
from os import getcwd
path.insert(0, getcwd())

# Transaction-class
from blockchain import Transaction

# Database-connector
from util.database.database import Database


def add_block(block_dict: dict, overwrite: bool=False):
    """Add block to the database.

    :param block_dict: Dictionary of block-information.
    :type block_dict: dict
    :param overwrite: If block already exists do or do not overwrite.
    :type overwrite: bool

    :return: Status if the block was added successful.
    :rtype: bool
    """

    # Check if block already exists in the database
    if fetch_block(block_dict['index']):
        # Check if overwriting blocks is set to off
        if not overwrite:
            return False

        remove_block(block_dict['index'])

    # Transform transaction-dict to json-format
    tx = Transaction('', '', 0)
    tx.from_dict(block_dict['tx'])

    tx = tx.to_json()
    block_dict['tx'] = tx

    # Add block to the database
    success = Database.push_to_db('INSERT INTO blockchain_v1_0_0 VALUES (:index, :previous_hash, :version, :timestamp, \
                                   :base_fee, :tx, :hash, :validator, :signature)', block_dict)

    # Check if block was successfully added to the database
    if not success:
        return False

    return True


def remove_block(index: int):
    """Remove block from its index.

    :param index: Index of the block to delete.
    :type idnex: int

    :return: Status if the block was removed successful.
    :rtype: bool
    """

    # Delete block from database
    success = Database.push_to_db('DELETE FROM blockchain_v1_0_0 WHERE block_index = :id', { 'id': index })

    # Check if execution was not succesful
    if not success:
        return False

    return True


def fetch_block(index: int):
    """Fetch block from its index.

    :param index: Index of the block to fetch.
    :type idnex: int

    :return: Fetch was not succesful.
    :rtype: bool
    :return: Dict-data of the block.
    :rtype: dict
    """
    block_data = Database.fetchone_from_db("SELECT * FROM blockchain_v1_0_0 WHERE block_index = :id", { 'id': index })

    # Check if the response of the database is correct
    if not block_data:
        return False

    return block_data
