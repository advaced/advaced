# Add to path
from sys import path, argv
import os
path.insert(0, os.path.join(os.getcwd(), '../'))

# Project version
from __init__ import __version__

# Valid arguments
from __init__ import OPTIONS, COMMANDS

def handle_input():
    '''Handle the input and all its arguments

    :param arguments: The given arguments when the command was executed
    :type arguments: string

    :raises: :py:class:`cmd.error.InvalidArgument`: If an argument doesn't exist
    :raises: :py:class:`cmd.error.TooManyArguments`: If too many arguments are used
    :raises: :py:class:`cmd.error.TooFewArguments`:
    '''
    return
