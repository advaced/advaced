from getpass import getpass

# Add to path
from sys import path, argv
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project version
from __init__ import __version__

# Valid arguments
from __init__ import OPTIONS, COMMANDS

# Help
from .help import print_help

# Validation
from validator.processor import Processor

def handle_input():
    '''Handle the input and all its arguments

    :param arguments: The given arguments when the command was executed
    :type arguments: string

    :raises: :py:class:`cmd.error.InvalidArgument`: If an argument doesn't exist
    :raises: :py:class:`cmd.error.TooManyArguments`: If too many arguments are used
    :raises: :py:class:`cmd.error.TooFewArguments`:
    '''

    # Check if their are any arguments provided
    if len(argv) < 2:
        return False

    opt = [ ]
    opt_values = [ ]

    cmd = None
    cmd_opt = None
    cmd_opt_value = None

    skip = False

    # Go through all arguments
    for pos, argument in enumerate(argv):
        # Check if the value was the execution path
        if pos == 0:
            continue

        if skip:
            skip = False

            continue

        found = False

        # Check if the command was already found
        if not cmd:
            for name, option in OPTIONS.items():

                # Check if argument is this option
                if (argument == (option['min'] if 'min' in option else None) or
                    argument == (option['standard'] if 'standard' in option else None) or
                    argument == (option['max'] if 'max' in option else None)):
                    opt.append(name)

                    # Check if a value should be provided
                    if option['value'] == True and option['value-required'] == True:
                        if len(argv) == pos + 1:
                            return False

                        # Check if it is not a value
                        if (not is_option(argv[pos + 1]) and
                            not is_command(argv[pos + 1]) and
                            not is_command_option(argv[pos + 1])):
                            # Add the argument behind this argument as the value
                            opt_values.append(argv[pos + 1])

                            skip = True
                            found = True

                            break

                    # Check if a value could be provided
                    elif option['value'] == True and not option['value-required']:

                        # Check if it is not a value
                        if (not is_option(argv[pos + 1]) and
                            not is_command(argv[pos + 1]) and
                            not is_command_option(argv[pos + 1])):
                            if len(argv) == pos + 1:
                                return False

                            opt_values.append(argv[pos + 1])

                            skip = True
                            found = True

                            break

                    # Value is not required and also not provided
                    opt_values.append(None)
                    found = True

                    break

            if found:
                continue

            # Go through all the commands and check if this argument is one
            for name, command in COMMANDS.items():

                # Check if argument is this command
                if (argument == (command['min'] if 'min' in command else None) or
                    argument == (command['standard'] if 'standard' in command else None) or
                    argument == (command['max'] if 'max' in command else None)):
                    cmd = name
                    found = True

                    break

            if found:
                continue

        # Check if command has options and option was not already fetched
        elif 'cmd-opts' in COMMANDS[cmd] and not cmd_opt:
            for name, cmd_option in COMMANDS[cmd]['cmd-opts'].items():

                # Check if argument is this command-option
                if (argument == (cmd_option['min'] if 'min' in cmd_option else None) or
                    argument == (cmd_option['standard'] if 'standard' in cmd_option else None) or
                    argument == (cmd_option['max'] if 'max' in cmd_option else None)):
                    cmd_opt = name
                    found = True

                    # Check if a value could be provided
                    if (cmd_option['value'] == True and
                        (cmd_option['value-required'] if 'value-required' in cmd_option else false) == False):
                        if len(argv) <= pos + 1:
                            return False

                        # Check if it is not a value
                        if (not is_option(argv[pos + 1]) and
                            not is_command(argv[pos + 1]) and
                            not is_command_option(argv[pos + 1])):
                            if len(argv) <= pos + 1:
                                break

                            cmd_opt_value = argv[pos + 1]
                            skip = True

                            break

                    # Check if a value should be provided
                    elif cmd_option['value'] == True and cmd_option['value-required'] == True:
                        if len(argv) <= pos + 1:
                            return False

                        # Add the argument behind this argument as the value
                        cmd_opt_value = argv[pos + 1]
                        skip = True

                        break

        if found:
            continue

        else:
            # Dev log
            print('Provided value was not found! Value:', argument, '| Position:', pos - 1)

            # Value was not found in options, commands, command options and their values
            return False

    # Check wich action the protocol should handle
    if cmd == 'account':
        if cmd_opt == 'create':
            # TODO -> Create account (with input fields for the password etc.) and save it to the db
            pass

        elif cmd_opt == 'export':
            # TODO -> Export account-data into file (ask for pwd)
            pass

        elif cmd_opt == 'import':
            # TODO -> Import account-data from path (set new password)
            pass

        elif cmd_opt == 'list':
            # TODO -> List accounts
            pass

    elif cmd == 'run':
        if cmd_opt == 'validate':
            password = getpass(prompt=f'Password for {cmd_opt_value}: ')

            # TODO -> Find user account and get private-key from password and the stored "hash"
            private_key = '5f83c097f06fa806dfd4023b429b704335df5c5377695bd5d85cd03950ce5b70'

            # Iniitialize the processor and start it
            processor = Processor(private_key=private_key)

            try:
                processor.start()

            except:
                processor.stop()

        elif cmd_opt == 'synchronize':
            # TODO -> Sync the chain with the others
            pass

        elif cmd_opt == 'serve':
            # TODO -> Run the rpc server and frequently sync with the chain
            pass

    elif cmd == 'export':
        if cmd_opt == 'json':
            # TODO -> Export blockchain-data into json-file
            pass

        elif cmd_opt == 'sqlite':
            # TODO -> Export blockchain-data into sqlite-file
            pass

    elif cmd == 'import':
        if cmd_opt == 'json':
            # TODO -> Import blockchain-data from json-file
            pass

        elif cmd_opt == 'sqlite':
            # TODO -> Import blockchain-data from sqlite-file
            pass

    elif cmd == 'transaction':
        # TODO -> Create a transaction (ask for tx values)
        pass

    elif cmd == 'stake':
        # TODO -> Create a stake transaction (ask for tx values)
        pass

    elif cmd == 'unstake':
        # TODO -> Create an unstake transaction (ask for tx values)
        pass

    elif cmd == 'claim':
        # TODO -> Create a claim transaction (ask for tx values)
        pass

    elif cmd == 'burn':
        # TODO -> Create a burn transaction (ask for tx values)
        pass

    elif cmd == 'version':
        # TODO -> Print out the version of the protocol
        pass

    elif cmd == 'version-audit':
        # TODO -> Checks for newer versions and if this version has vulnerabilities or bugs
        pass

    elif cmd == 'help':
        print_help(opt, opt_values)


def is_option(value):
    """Check if value is an option.

    :param value: The value to check.
    :type value: str

    :return: Is an option or not.
    :rtype: bool
    """
    for _, option in OPTIONS.items():
        if (value == (option['min'] if 'min' in option else None) or
            value == (option['standard'] if 'standard' in option else None) or
            value == (option['max'] if 'max' in option else None)):
            return True

    return False


def is_command(value):
    """Check if value is an option.

    :param value: The value to check.
    :type value: str

    :return: Is an option or not.
    :rtype: bool
    """
    for _, command in COMMANDS.items():
        if (value == (command['min'] if 'min' in command else None) or
            value == (command['standard'] if 'standard' in command else None) or
            value == (command['max'] if 'max' in command else None)):
            return True

    return False


def is_command_option(value, command_name=None):
    """Check if value is an option.

    :param value: The value to check.
    :type value: str
    :param command_name: The command to check the options for
    :type command_name: str

    :return: Is an option or not.
    :rtype: bool
    """

    # Check if a specific command is used
    if command_name:
        if 'cmd-opts' in COMMANDS[command_name]:
            # Go through all command options
            for _, cmd_option in COMMANDS[command_name]['cmd-opts'].items():

                # Check if the option is equal to the given value
                if (value == (cmd_option['min'] if 'min' in cmd_option else None) or
                    value == (cmd_option['standard'] if 'standard' in cmd_option else None) or
                    value == (cmd_option['max'] if 'max' in cmd_option else None)):
                    return True

        else:
            # No command options were found
            return False

    else:
        # Go through all commands
        for name, command in COMMANDS.items():

            # Check if any command options are provided
            if 'cmd-opts' in COMMANDS[name]:
                # Go through all options of the commands
                for _, cmd_option in command['cmd-opts'].items():

                    # Check if the option is equal to the given value
                    if (value == (cmd_option['min'] if 'min' in cmd_option else None) or
                        value == (cmd_option['standard'] if 'standard' in cmd_option else None) or
                        value == (cmd_option['max'] if 'max' in cmd_option else None)):
                        return True

    return False
