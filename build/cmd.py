# File remover
from os import path, remove, getcwd

# Project version
from __init__ import __version__


def build() -> int:
    """Creates the command in the `/usr/bin` directory (only for linux)

    :returns: The state of success from the process
    :rtype: bool

    :raises: OSError
    :raises: BaseException
    """

    # Check if file already exists
    if path.isfile('/bin/advaced'):
        # Logging for development
        print('found another file')

        # Try to remove current start-file
        try:
            # Logging for development
            print('removing old file')

            remove('/bin/advaced')

        except OSError as error:
            # Logging for development
            print('finished with error')

            # Raise the error
            raise OSError

    # Logging for development
    print('creating bash file...')

    try:
        # Create bash file to run
        with open('/bin/advaced', 'a') as shell_file:
            shell_file.writelines(['#!/bin/sh\n', f'python3 "/lib/advaced/{__version__}/" $@'])

    except OSError or BaseException as error:
        # Logging for development
        print('finished with error')

        # Raise the error
        raise error

    # Logging for development
    print('build finished')

    return True
