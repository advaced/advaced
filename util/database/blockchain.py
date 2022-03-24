# Add to path
from sys import path
from os import getcwd
path.insert(0, getcwd())

# Transaction-class
from blockchain.transaction import Transaction

# Database-connector
from util.database.database import Database


def recreate_block(block_data):
    """Recreates block from database-data.

    :param block_data: Data fetched from the database.
    :type block_data: tuple | list

    :return: Information of a block as dict-format.
    :rtype: dict
    """
    return {
        'index': block_data[0],
        'previous_hash': block_data[1],

        'version': block_data[2],
        'timestamp': block_data[3],

        'base_fee': block_data[4],

        'hash': block_data[5],
        'validator': block_data[6],
        'signature': block_data[7]
    }


def recreate_tx(tx_data):
    """Recreates transaction from database-data.

    :param tx_data: Data fetched from the database.
    :type tx_data: tuple | list

    :return: Information of a transaction as dict-format.
    :rtype: dict
    """
    return {
        'sender': tx_data[0],
        'recipient': tx_data[1],
        'amount': float(tx_data[2]),
        'fee': float(tx_data[3]),
        'type': tx_data[4],
        'timestamp': tx_data[5],
        'hash': tx_data[6],
        'signature': tx_data[7]
    }


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

    # Check if the block includes transactions
    if type(block_dict['tx']) == list and len(block_dict['tx']) > 0:
        # Add transactions to database
        for transaction in block_dict['tx']:
            transaction['block_index'] = block_dict['index']

            success = Database.push_to_db('INSERT INTO transactions VALUES (:block_index, :sender, :recipient, :amount, :fee, \
                                        :type, :timestamp, :hash, :signature)', transaction)

    # Add block to the database
    success = Database.push_to_db('INSERT INTO blockchain VALUES (:index, :previous_hash, :version, :timestamp, \
                                   :base_fee, :hash, :validator, :signature)', block_dict)

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
    success = Database.push_to_db('DELETE FROM blockchain WHERE block_index = :id', { 'id': index })

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

    # Fetch the block
    block_data = Database.fetchone_from_db('SELECT * FROM blockchain WHERE block_index = :id', { 'id': index })

    # Check if the response of the database is correct
    if not block_data:
        return False

    # Fetch the blocks transactions
    tx = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, signature FROM \
                                    transactions WHERE block_index = :index', { 'index': index })
    tx_dicts = [ ]

    # Check if there are any transactions in the block
    if tx:
        # Check if multiple transactions are inclueded into the block
        if type(tx) == list:

            # Go through all transactions and add them to a dict-list
            for transaction in tx:
                tx_dicts.append(recreate_tx(transaction))

        # Only one transaction was fetched
        else:
            tx_dicts.append(recreate_tx(transaction))

    # Convert block to dictionary format
    block_dict = recreate_block(block_data)

    # Add the transactions to the block
    block_dict['tx'] = tx_dicts

    return block_dict


def fetch_transaction_block_index(tx: Transaction):
    """Check if a transaction is included into the database.

    :param tx: Transaction to search for.
    :type tx: :py:class:`blockchain.Transaction`

    :return: Index of its block.
    :rtype: int
    """
    index = Database.fetchone_from_db('SELECT block_index FROM transactions WHERE timestamp = :timestamp AND \
                                       hash = :hash AND signature = :signature',
                                       {
                                           'timestamp': str(tx.timestamp),
                                           'hash': tx.hash,
                                           'signature': tx.signature
                                       })

    # Check if fetch was successful
    if not index:
        return False

    return index


def fetch_transactions(public_key: str, tx_type: str=None, is_sender: bool=None):
    """Fetch all transactions the account made in the past.

    :param public_key: Verifying key of the account.
    :type public_key: str
    :param tx_type: Type of the transaction.
    :type tx_type: str
    :param is_sender: If the account is the sender, the recipient or both.
    :type is_sender: bool | NoneType

    :return: List of transactions the account made or received.
    :rtype: [ Transaction ]
    """
    # Check if the type of the transaction is provided and no other specifications
    if tx_type and is_sender == None:
        # Fetch the transactions
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE type = :type AND \
                                                       (sender = :public_key OR recipient = :public_key)',
                                                      { 'type': tx_type, 'public_key': public_key })

    # Check if the type of the transaction is provided and the account should be the sender
    elif tx_type and is_sender == True:
        # Fetch the transactions
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE type = :type AND \
                                                       sender = :public_key',
                                                      { 'type': tx_type, 'public_key': public_key })

    # Check if the type of the transaction is provided and the account should be the sender
    elif tx_type and is_sender == False:
        # Fetch the transactions
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE type = :type AND \
                                                       recipient = :public_key',
                                                      { 'type': tx_type, 'public_key': public_key })

    # Check if only the transactions should be fetched were the account is the sender
    elif is_sender == True:
        # Fetch the transactions
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE sender = :public_key',
                                                      { 'public_key': public_key })

    # Check if only the transactions should be fetched were the account is the recipient
    elif is_sender == True:
        # Fetch the transactions
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE recipient = :public_key',
                                                      { 'public_key': public_key })

    # Fetch all transactions where this account is involved
    else:
        transactions_data = Database.fetchall_from_db('SELECT sender, recipient, amount, fee, type, timestamp, hash, \
                                                       signature FROM transactions WHERE sender = :public_key OR \
                                                       recipient = :public_key',
                                                      { 'type': tx_type, 'public_key': public_key })

    # Check if no transactions were found
    if not transactions_data:
        return [ ]

    transactions = [ ]

    # Check if multiple transactions were fetched
    if type(transactions_data) == list:
        # Go through all transaction datasets and recreate them to classes
        for tx_data in transactions_data:
            tx_dict = recreate_tx(tx_data)

            tx = Transaction('', '', 0)
            tx.from_dict(tx_dict)

            transactions.append(tx)

    # Only one tx was fetched
    else:
        tx_dict = recreate_tx(transactions_data)

        tx = Transaction('', '', 0)
        tx.from_dict(tx_dict)

        transactions.append(tx)

    return transactions


def fetch_versionstamps(network='mainnet', db=None):
    """Fetch the timestamps for the versions.

    :return: Dictionary that consists of versions as keys and timestamps as values
    :rtype: dict
    """

    # Check if a database-class was parsed
    if db:
        response = db.fetchall('SELECT version, timestamp FROM versionstamps WHERE network = :net', { 'net': network })

    else:
        response = Database.fetchall_from_db('SELECT version, timestamp FROM versionstamps WHERE network = :net', { 'net': network })

    # Check if response exists
    if not response:
        return { }

    versionstamps = { }

    # Check if multiple stamps were fetched
    if type(response) == list:
        for stamp in response:
            versionstamps[stamp[0]] = stamp[1]

    else:
        # Only one value was returned
        versionstamps[response[0]] = response[1]

    return versionstamps
