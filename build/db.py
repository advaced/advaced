# Add to path
from sys import path
from os.path import dirname, abspath, join, exists
from os import makedirs

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Database-handler
from util.database.initialize import create_database
from __init__ import DATABASE_FILE


def build():
    """Creates the database and its tables.

    :return: Successfulness of the build.
    :rtype: bool
    """

    # Create the directory
    if not exists(DATABASE_FILE):
        try:
            makedirs(dirname(abspath(DATABASE_FILE)))

        except OSError:
            return False

    # Create the database
    create_database(overwrite=False)

    return True
