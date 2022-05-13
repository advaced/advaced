from os import path, remove
from logging import basicConfig, info as log_info, error as log_error, warning as log_warning

# Add to path
from sys import path as sys_path
from os.path import dirname, abspath, join

sys_path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from __init__ import COMMAND_FILE, LOG_LEVEL
from util.log.logger import init_logger


def build() -> bool:
    """Creates the command in the `/usr/bin` directory (only for linux)

    :returns: The state of success from the process
    :rtype: bool

    :raises: OSError
    :raises: BaseException
    """
    handler = init_logger()
    basicConfig(level=LOG_LEVEL, handlers=[handler])

    # Check if file already exists
    if path.isfile(COMMAND_FILE):
        log_warning('Compiled command already exists!')

        # Ask for confirmation
        if not input('Do you want to overwrite the existing Advaced command? [y/N] ').lower() == 'y':
            return True

        # Try to remove current file
        try:
            log_info('Removing old command...')

            remove(COMMAND_FILE)

        except OSError:
            log_error('Failed to remove old command!')

    log_info('[✔️] Ready to compile command')

    return True
