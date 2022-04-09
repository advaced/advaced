# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Required for giving help
from __init__ import __version__, NAME, USAGE, OPTIONS, COMMANDS

def print_help(options: list, option_values: list):
    # Print the name information
    print(f'\nName:\n\t{NAME}')

    # Print the usage of the protocol
    print(f'\nUsage:\n\t{USAGE}')

    # Print the version
    print(f'\nVersion:\n\t{__version__}')

    # Print out the options
    print('\nOptions:')

    for _, opt in OPTIONS.items():
        # Check if a value is required
        if opt['value']:
            if 'value-required' in opt:
                if opt['value-required']:
                    value = ' value'

                else:
                    value = ' [value]'

            else:
                value = ' value'

        else:
            value = ''

        if 'min' in opt and 'standard' in opt and 'max' in opt:
            option = f'\t{opt["min"]}, {opt["standard"]}, {opt["max"]}{value}'

        elif 'min' in opt and 'standard' in opt:
            option = f'\t{opt["min"]}, {opt["standard"]}{value}'

        elif 'min' in opt and 'max' in opt:
            option = f'\t{opt["min"]}, {opt["max"]}{value}'

        elif 'standard' in opt and 'max' in opt:
            option = f'\t{opt["standard"]}, {opt["max"]}{value}'

        elif 'min' in opt:
            option = f'\t{opt["min"]}{value}'

        elif 'standard' in opt:
            option = f'\t{opt["standard"]}{value}'

        elif 'max' in opt:
            option = f'\t{opt["max"]}{value}'

        else:
            # Development log
            print('Error: No option value')
            
            return False

        # Add some space
        if 33 - len(option) > 0:
            for x in range(0, round((36 - len(option)) / 8)):
                option += '\t'

        # Add the description
        option += f'\t{opt["description"]}'

        print(option)

    # Print out the commands
    print('\nCommands:')

    for _, cmd in COMMANDS.items():

        if 'min' in cmd and 'standard' in cmd and 'max' in cmd:
            command = f'\t{cmd["min"]}, {cmd["standard"]}, {cmd["max"]}'

        elif 'min' in cmd and 'standard' in cmd:
            command = f'\t{cmd["min"]}, {cmd["standard"]}'

        elif 'min' in cmd and 'max' in cmd:
            command = f'\t{cmd["min"]}, {cmd["max"]}'

        elif 'standard' in cmd and 'max' in cmd:
            command = f'\t{cmd["standard"]}, {cmd["max"]}'

        elif 'min' in cmd:
            command = f'\t{cmd["min"]}'

        elif 'standard' in cmd:
            command = f'\t{cmd["standard"]}'

        elif 'max' in cmd:
            command = f'\t{cmd["max"]}'

        else:
            command = 'Could not find the command!'

        # Add some space
        if 33 - len(command) > 0:
            for x in range(0, round((36 - len(command)) / 8)):
                command += '\t'

        # Add the description
        command += f'\t{cmd["description"]}'

        print(command)
