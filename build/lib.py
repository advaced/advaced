# Modules for directory-copying
from os import path, getcwd, rmdir
from shutil import rmtree, copytree, Error

# Project version
from __init__ import __version__


def build() -> int:
    """Sets the project files up and copies them into the program/library directory of
       the operating system (linux: `/usr/lib/`, windows: `C:\Program Files\`).

    :returns: The state of success from the process
    :rtype: bool

    :raises: shutil.Error: Failed to copy project to program/library directory

    """

    # Check if build already exists
    if path.isdir(f'/lib/advaced/{__version__}'):
        # Logging for development
        print('found another build')

        # Try to remove current build
        try:
            # Logging for development
            print('removing old build')

            rmtree(f'/lib/advaced/{__version__}')

        except OSError as error:
            # Logging for development
            print('finished with error')

            # Raise the error
            raise OSError

    # Set the paths for copying
    source = getcwd()
    destination = f'/lib/advaced/{__version__}'

    # Logging for development
    print(f'copying to {destination}...')

    # Try to copy the source into destination
    try:
        copytree(source, destination)

    except Error as error:
        # Logging for development
        print('finished with error')

        # Raise the error
        raise error

    # Logging for development
    print('finished without error')

    return True
