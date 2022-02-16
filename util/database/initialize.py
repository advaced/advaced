from os.path import exists, join
from os import remove
from sys import path

# SQLite connector
from sqlite3 import connect

DATABASE_FILE = join(path[0], 'db.db')


def create_tables(cursor):
    """Create tables from sql file

    :param cursor: Cursor of sqlite-connection
    :type cursor: :py:class:`sqlite3.Cursor`

    :return: Status code wether cursor-execution was successful
    :rtype: bool
    """


    pass


def create_database():
    """Create the database-file and add the required tables

    :return: Status code wether creation was successful
    :rtype: bool
    """

    # Check if the database already exists
    if exists(DATABASE_FILE):
        # Dev log
        print(f'already exists: {DATABASE_FILE}')

        return False

    try:
        # Create the file
        connection = connect(DATABASE_FILE)
        cursor = connection.cursor()

        # Create the tables
        create_tables(cursor)

        # Commit and close connection
        connection.commit()
        cursor.close()
        connection.close()

    except:
        return False

    return True
