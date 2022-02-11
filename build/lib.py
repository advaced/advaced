# Modules for directory-copying
from os import path, getcwd, rmdir, chmod
from shutil import rmtree, copytree, Error as shutil_error

# Permissions
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH

# Version util
from __init__ import __version__


def build() -> int:
    """Sets the project files up and copies them into the program/library directory of the operating system (linux: `/usr/lib/`, windows: `C:\Program Files\`).

    :returns: The state of success from the process
    :rtype: bool

    :raises: shutil.Error: Failed to copy project to program/library directory

    """

    # Check if build already exists
    if path.isdir(f'/usr/lib/advaced/{__version__}'):
        # Logging for development
        print('found another build')

        # Try to remove current build
        try:
            # Logging for development
            print('removing old build')

            rmtree(f'/usr/lib/advaced/{__version__}')

        except OSError as error:
            # Raise the error
            raise

            # Logging for development
            print('finished with error')

            return False


    # Set the paths for copying
    source = getcwd()
    destination = f'/usr/lib/advaced/{__version__}'

    # Logging for development
    print(f'copying to {destination}...')

    # Try to copy the source into destination
    try:
        copytree(source, destination)

        # Set needed permissions
        chmod(f'/usr/lib/advaced/', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP | S_IROTH | S_IWOTH | S_IXOTH)
        chmod(f'/usr/lib/advaced/{__version__}', S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IWGRP | S_IXGRP | S_IROTH | S_IWOTH | S_IXOTH)

    except shutil_error:
        # Raise the error
        raise

        # Logging for development
        print('finished with error')

        return False

    # Logging for development
    print('finished without error')

    return True
