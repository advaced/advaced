# Modules for project-building
from cmd import build as build_cmd
from lib import build as build_lib
from db import build as build_db


def build_project() -> bool:
    # Build the command(s)
    success_cmd = build_cmd()

    # Build the library
    success_lib = build_lib()

    # Check if the builds were successful
    if not success_cmd or not success_lib:
        # Logging for development
        print('build failed')

        return False

    success_db = build_db()

    # Check wether the database-build was successful or not
    if not success_db:
        # Logging for development
        print('database-build failed')

        return False

    return True


if __name__ == '__main__':
    build_project()
