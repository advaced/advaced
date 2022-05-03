from logging import basicConfig, info as log_info, error as log_error, warning as log_warning
from sqlite3 import connect
from os.path import exists, join
from os import getcwd

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..', '..'))

from __init__ import DATABASE_FILE, LOG_LEVEL
from util.log.logger import init_logger


def create_tables(cursor):
    """Create tables from sql file

    :param cursor: Cursor of sqlite-connection
    :type cursor: :py:class:`sqlite3.Cursor`

    :return: Status code whether cursor-execution was successful
    :rtype: bool
    """

    # Read the sql-script
    with open(join(dirname(abspath(__file__)), 'sql', 'db.sql')) as sql_file:
        sql_script = sql_file.read()

    # Execute the script
    cursor.executescript(sql_script)


def create_database(overwrite=False):
    """Create the database-file and add the required tables

    :param overwrite: Says if file should be overwritten or not.
    :param overwrite: bool

    :return: Status code whether creation was successful
    :rtype: bool
    """
    handler = init_logger()
    basicConfig(level=LOG_LEVEL, handlers=[handler])

    # Check if the database already exists
    if exists(DATABASE_FILE) and not overwrite:
        log_warning('Database already exists, not overwriting')

        return False

    # Create the file
    connection = connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Create the tables
    create_tables(cursor)

    # Commit and close connection
    connection.commit()
    cursor.close()
    connection.close()

    return True
