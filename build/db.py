# Add to path
from sys import path

from os.path import join, exists
from os import getcwd, mkdir, chmod

path.insert(0, getcwd())

# Database-handler
from util.database.initialize import create_database, create_tables, DATABASE_FILE


def build():
    """Creates the database and its tables.

    :return: Successfulness of the build.
    :rtype: bool
    """

    # Check if the database does not exist
    if exists(DATABASE_FILE):
        create_database(False)

        return True

    # Create the directory
    try:
        mkdir('/lib/advaced/database')
    except:
        return False

    # Create the database
    create_database(True)

    return True
