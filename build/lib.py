from os import path, getcwd
from shutil import rmtree, copytree, Error as SHUtilError
from logging import basicConfig, info as log_info, error as log_error, warning as log_warning

# Add to path
from sys import path as sys_path
from os.path import dirname, abspath, join

sys_path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from __init__ import __version__, LOG_LEVEL
from util.log.logger import init_logger


def build() -> int:
    """Sets the project files up and copies them into the program/library directory of
       the operating system (linux: `/usr/lib/`, windows: `C:\Program Files\`).

    :returns: The state of success from the process
    :rtype: bool

    :raises: shutil.Error: Failed to copy project to program/library directory

    """
    handler = init_logger()
    basicConfig(level=LOG_LEVEL, handlers=[handler])

    # Check if build already exists
    if path.isdir(f'/lib/advaced/{__version__}'):
        # Logging for development
        log_info('Found another build')
        log_info('Removing old build...')

        # Try to remove current build
        try:
            rmtree(f'/lib/advaced/{__version__}')

            log_info('Removed old build')

        except OSError:
            # Logging for development
            log_error('Could not remove old build, it is may due to lack of permission')

            return False

    # Set the paths for copying
    source = getcwd()
    destination = f'/lib/advaced/{__version__}'

    # Logging for development
    log_info(f'Building into {destination}...')

    # Try to copy the source into destination
    try:
        copytree(source, destination)

    except SHUtilError:
        log_error('Could not build project')

        return False

    log_info('Finished building project')

    return True
