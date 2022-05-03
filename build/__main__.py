from logging import basicConfig, info as log_info, error as log_error, warning as log_warning

# Modules for project-building
from cmd import build as build_cmd
from lib import build as build_lib
from db import build as build_db

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

from __init__ import LOG_LEVEL
from util.log.logger import init_logger


def build_project() -> bool:
    handler = init_logger()
    basicConfig(level=LOG_LEVEL, handlers=[handler])

    log_info('Checking environment...')

    # Build the command(s)
    success_cmd = build_cmd()

    # Check if the builds were successful
    if not success_cmd:
        log_error('Build failed: It is likely that the program does not have enough permissions or the command is '
                  'currently in use')

        return False

    log_info('Building project...')

    # Build the library
    success_lib = build_lib()

    # Check if the build was successful
    if not success_lib:
        log_error('Build failed: It is likely that the program does not have enough permissions or the command is '
                  'currently in use')

        return False

    log_info('Building project database...')

    # Build the database
    success_db = build_db()

    # Check whether the database-build was successful or not
    if not success_db:
        log_error('Database build failed: It is likely that the program does not have enough permissions')

        return False

    log_info('Build successful')

    return True


if __name__ == '__main__':
    build_project()
