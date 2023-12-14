# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Required for giving help
from __init__ import __version__, NAME, USAGE, OPTIONS, COMMANDS


def print_help():
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
        if 36 - len(option) > 0:
            option += '\t' * (round((37 - len(option)) / 8))

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
        if 36 - len(command) > 0:
            command += '\t' * (round((37 - len(command)) / 8))

        # Add the description
        command += f'\t{cmd["description"]}'

        print(command)


def print_cmd_help(cmd):
    # Print the name information
    print(f'\nName:\n\t{NAME}')

    # Print the usage of the protocol
    print(f'\nUsage:\n\t{USAGE}')

    # Print the version
    print(f'\nVersion:\n\t{__version__}')

    # Check if the command contains options
    if 'cmd-opts' not in COMMANDS[cmd]:
        # Print the command name and its description
        print(f'\nCommand:\n\t{cmd}')
        print(f'\nDescription:\n\t{COMMANDS[cmd]["description"]}')

        return True

    # Print the command usage and its description
    print(f'\nCommand:\n\t{cmd} [COMMAND-OPTION]')
    print(f'\nDescription:\n\t{COMMANDS[cmd]["description"]}')

    # Print out the commands
    print('\nCommand options:')

    for _, cmd_opt in COMMANDS[cmd]['cmd-opts'].items():
        if 'min' in cmd_opt and 'standard' in cmd_opt and 'max' in cmd_opt:
            cmd_option = f'\t{cmd_opt["min"]}, {cmd_opt["standard"]}, {cmd_opt["max"]}'

        elif 'min' in cmd_opt and 'standard' in cmd_opt:
            cmd_option = f'\t{cmd_opt["min"]}, {cmd_opt["standard"]}'

        elif 'min' in cmd_opt and 'max' in cmd_opt:
            cmd_option = f'\t{cmd_opt["min"]}, {cmd_opt["max"]}'

        elif 'standard' in cmd_opt and 'max' in cmd_opt:
            cmd_option = f'\t{cmd_opt["standard"]}, {cmd_opt["max"]}'

        elif 'min' in cmd_opt:
            cmd_option = f'\t{cmd_opt["min"]}'

        elif 'standard' in cmd_opt:
            cmd_option = f'\t{cmd_opt["standard"]}'

        elif 'max' in cmd_opt:
            cmd_option = f'\t{cmd_opt["max"]}'

        else:
            cmd_option = 'Could not find the command option!'

        # Check if the command includes a value
        if cmd_opt['value'] is True:

            # Check if the value is required
            if cmd_opt['value-required'] is True:
                cmd_option += f' <{cmd_opt["value-name"]}>'

            else:
                cmd_option += f' [{cmd_opt["value-name"]}]'

        # Add some space
        if 33 - len(cmd_option) > 0:
            cmd_option += '\t' * (round(37 - len(cmd_option) / 8))

        # Add the description
        cmd_option += f'\t{cmd_opt["description"]}'

        print(cmd_option)
