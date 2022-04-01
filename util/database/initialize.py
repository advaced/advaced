# Path management
from os.path import exists, join
from os import getcwd

# SQLite connector
from sqlite3 import connect

# Database path
# from ...__init__ import DATABASE_FILE
DATABASE_FILE = join('/usr', 'lib', 'advaced', 'database', 'db.db')


def create_tables(cursor):
    """Create tables from sql file

    :param cursor: Cursor of sqlite-connection
    :type cursor: :py:class:`sqlite3.Cursor`

    :return: Status code wether cursor-execution was successful
    :rtype: bool
    """

    # Read the sql-script
    with open(join(getcwd(), 'util/database/sql/db.sql')) as sql_file:
        sql_script = sql_file.read()

    # Execute the script
    cursor.executescript(sql_script)



def create_database(overwrite=False):
    """Create the database-file and add the required tables

    :param overwrite: Says if file should be overwritten or not.
    :param overwrite: bool

    :return: Status code wether creation was successful
    :rtype: bool
    """

    # Check if the database already exists
    if exists(DATABASE_FILE) and not overwrite:
        # Dev log
        print(f'already exists: {DATABASE_FILE}')

        return False

    # try:
    # Create the file
    connection = connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Create the tables
    create_tables(cursor)

    # Commit and close connection
    connection.commit()
    cursor.close()
    connection.close()

    # except:
    #     return False

    return True
