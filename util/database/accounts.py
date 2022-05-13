# Database handler
from util.database.database import Database


def fetch_account(account_name, database=None):
    """Fetches the account from the database.

    :param account_name: The name of the account to fetch.
    :type account_name: str
    :param database: The database to use.
    :type database: :py:class:`database.Database`

    :returns: The account data in a dictionary or False if no account is found.
    :rtype: dict | bool
    """
    # Check if a database is given
    if database:
        account_data = database.fetchone('SELECT password_hash, private_key_hash FROM accounts WHERE name = :name',
                                         {'name': account_name})

    else:
        account_data = Database.fetchone_from_db('SELECT password_hash, private_key_hash FROM accounts WHERE \
                                                  name = :name', {'name': account_name})

    # Check if the account exists
    if not account_data:
        return False

    return {'password_hash': account_data[0], 'private_key_hash': account_data[1]}


def push_account(account_name, password_hash, private_key_hash, database=None):
    """Pushes the account to the database.

    :param account_name: The name of the account to push.
    :type account_name: str
    :param password_hash: The password hash of the account.
    :type password_hash: str
    :param private_key_hash: The private key hash of the account.
    :type private_key_hash: str
    :param database: The database to use.
    :type database: :py:class:`database.Database`

    :returns: True if the account was pushed successfully.
    :rtype: bool
    """
    # Check if a database is given
    if database:
        database.push('INSERT INTO accounts (name, password_hash, private_key_hash) VALUES (:name, :password_hash, \
                       :private_key_hash)', {'name': account_name, 'password_hash': password_hash,
                                             'private_key_hash': private_key_hash})

    else:
        Database.push_to_db('INSERT INTO accounts (name, password_hash, private_key_hash) VALUES (:name, \
                            :password_hash, :private_key_hash)', {'name': account_name, 'password_hash': password_hash,
                                                                  'private_key_hash': private_key_hash})

    return True


def delete_account(account_name, database=None):
    """Deletes the account from the database.

    :param account_name: The name of the account to delete.
    :type account_name: str
    :param database: The database to use.
    :type database: :py:class:`database.Database`

    :returns: True if the account was deleted successfully.
    :rtype: bool
    """
    # Check if a database is given
    if database:
        database.push('DELETE FROM accounts WHERE name = :name', {'name': account_name})

    else:
        Database.push_to_db('DELETE FROM accounts WHERE name = :name', {'name': account_name})

    return True
