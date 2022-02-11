# File remover
from os import path, remove, chmod

# Permissions
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH

# Version
from __init__ import __version__


def build() -> int:
    """Creates the command in the `/usr/bin` directory (only for linux)

    :returns: The state of success from the process
    :rtype: bool

    :raises: OSError
    :raises: BaseException

    """

    # Check if file already exists
    if path.isfile('/usr/bin/advaced'):
        # Logging for development
        print('found another file')

        # Try to remove current start-file
        try:
            # Logging for development
            print('removing old file')

            remove('/usr/bin/advaced')

        except OSError as error:
            # Raise the error
            raise

            # Logging for development
            print('finished with error')

            return False

    # Logging for development
    print('creating bash file...')

    try:
        # Create bash file to run
        with open('/usr/bin/advaced', 'a') as shell_file:
            shell_file.writelines(['#!/usr/bin/sh\n', f'python "/usr/lib/advaced/{__version__}/"'])

        # Set the needed permission
        chmod('/usr/bin/advaced', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP | S_IROTH | S_IWOTH | S_IXOTH)

    except OSError as error:
        # Logging for development
        print(f'error: {error}')
        raise

        return False

    except BaseException as error:
        # Logging for development
        print(f'error: {error}')
        raise

        return False

    # Logging for development
    print('build finished')

    return True
