from getpass import getpass
from random import choice
from queue import Queue
from time import sleep as time_sleep
from os import getcwd
import json

# Error handling
from .error import InvalidCommand, InvalidArgument, MissingArguments

# Add to path
from sys import path, argv
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from __init__ import __version__, OPTIONS, COMMANDS

from .help import print_help, print_cmd_help

from validator.processor import Processor
from rpc.server import RPCServer
from rpc.client import Client
from rpc.blockchain_pb2 import Transaction as RPCTransaction

from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction

from accounts.account import Account
from util.database.database import Database


def handle_input():
    """Handle the input and all its arguments

    :raises: :py:class:`cmd.error.InvalidCommand` If the command is invalid.
    :raises: :py:class:`cmd.error.InvalidArgument` If an argument doesn't exist
    :raises: :py:class:`cmd.error.TooManyArguments` If too many arguments are used
    :raises: :py:class:`cmd.error.MissingArgument` If an argument is missing
    """

    # Check if there are any arguments provided
    if len(argv) < 2:
        raise MissingArguments('No arguments provided.')

    opt = []
    opt_values = []

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
                    if option['value'] is True and option['value-required'] is True:
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
                    elif option['value'] is True and not option['value-required']:

                        # Check if it is not a value
                        if (not is_option(argv[pos + 1]) and not is_command(argv[pos + 1]) and
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
            cmd = next(iter(name for name, command in COMMANDS.items()
                                   if (argument == (command['min'] if 'min' in command else None) or
                                       argument == (command['standard'] if 'standard' in command else None) or
                                       argument == (command['max'] if 'max' in command else None))),
                              (None, False))
            
            
            if not cmd:
                continue

            else:
                found = True

        elif argument == 'help' or argument == 'h' and not cmd_opt and cmd:
            cmd_opt = 'help'

            if len(argv) <= pos + 1:
                break

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
                    if (cmd_option['value'] is True and 'value-required' in cmd_option and
                       cmd_option['value-required'] is False):
                        if len(argv) <= pos + 1:
                            return False

                        # Check if it is not a value
                        if (not is_option(argv[pos + 1]) and not is_command(argv[pos + 1]) and
                           not is_command_option(argv[pos + 1])):
                            if len(argv) <= pos + 1:
                                break

                            cmd_opt_value = argv[pos + 1]
                            skip = True

                            break

                    # Check if a value should be provided
                    elif cmd_option['value'] is True and cmd_option['value-required'] is True:
                        if len(argv) <= pos + 1:
                            return False

                        # Add the argument behind this argument as the value
                        cmd_opt_value = argv[pos + 1]
                        skip = True

                        break

        if found:
            continue

        else:
            # Check if this argument is not a command
            if cmd:
                raise InvalidArgument(argument)

            else:
                raise InvalidCommand(argument)

    # Check which action the protocol should handle
    if cmd_opt == 'help':
        print_cmd_help(cmd)

        return True

    if cmd == 'account':
        if cmd_opt == 'create':
            print('Please provide the following information')

            # Fetch the account name
            account_name = input('Account name: ')

            # Fetch the account password
            account_password = getpass('Account password: ')

            # Check if the user wants to use existing keys
            if input('Use existing keys? (y/n): ').lower() == 'y':
                # Fetch the public key
                account_public_key = input('Public key: ')

                # Fetch the private key
                account_private_key = getpass('Private key: ')

            else:
                account_public_key = account_private_key = None

            print('Creating account...')

            # Create the account
            account = Account(account_name, account_password, account_public_key, account_private_key)
            account.save()

            print('Account created successfully\n')

            print('Account information')
            print('Account name: ' + account.name)
            print('Account public key: ' + account.public_key)
            print('Account private key: ' + account.private_key[:15] + '...')

            return True

        elif cmd_opt == 'export':
            print('Please provide the following information')

            # Fetch the account name
            account_name = input('Account name: ')

            # Fetch the account password
            account_password = getpass('Account password: ')

            # Ask user for the file name
            file_name = input('File name (default= account name): ')

            print('Exporting account...')

            # Load the account
            account = Account(account_name, account_password)
            account.load()

            # Check if file name is provided
            if file_name == '':
                file_name = account.name

            # Set the file directory
            directory = join(cmd_opt_value, f'{file_name}.json') \
                if cmd_opt_value.startswith('/') \
                else join(getcwd(), cmd_opt_value, f'{file_name}.json')

            try:
                with open(directory, 'w') as f:
                    json.dump({'public_key': account.public_key, 'private_key': account.private_key}, f, indent=4)

            except:
                print('Failed to export account')

                return False

            print('Account exported successfully\n')

            return True

        elif cmd_opt == 'import':
            print('Please provide the following information')

            # Fetch the account name
            account_name = input('Account name: ')

            # Fetch the account password
            account_password = getpass('Account password: ')

            # Ask user for the file name
            file_name = input('File name: ')

            print('Importing account...')

            # Set the file directory
            directory = join(cmd_opt_value, f'{file_name}') \
                if cmd_opt_value.startswith('/') \
                else join(getcwd(), cmd_opt_value, f'{file_name}')

            try:
                with open(directory, 'r') as f:
                    account_data = json.load(f)

            except:
                print('Failed to import account')

                return False

            print('Saving account...')

            # Save the account to the database
            account = Account(account_name, account_password, account_data['public_key'], account_data['private_key'])
            success = account.save()

            if not success:
                print('Failed to save account')

                return False

            print('Account imported successfully\n')

            print('Account information')
            print('Account name: ' + account_name)
            print('Account public key: ' + account_data['public_key'])
            print('Account private key: ' + account_data['private_key'][:15] + '...')

            return True

        elif cmd_opt == 'list':
            # Fetch all accounts
            account_names = Database.fetchall_from_db('SELECT name FROM accounts', {})

            if not account_names:
                print('No accounts found')

                return True

            print('--- Accounts ---')

            if type(account_names) is list:
                iter(print(str(index + 1) + ': ' + account_name[0] if type(account_name) is tuple else account_name)
                     for index, account_name in enumerate(account_names))

            else:
                print(f'1: {account_names}')

            return True

    elif cmd == 'run':
        if cmd_opt == 'validate':
            password = getpass(prompt=f'Password for {cmd_opt_value}: ')

            print('Validating password...')

            # Set account up
            account = Account(cmd_opt_value, password)
            success = account.load()

            if not success:
                print('Failed to validate password')

                return False

            print('Password validated successfully\n')

            # Check if the user wants to create a new blockchain
            if 'genesis' in opt:
                # Check if the user wants to reset the database
                if not input('Are you sure that you want to create a new blockchain and with that reset the database? '
                             '(y/n): ').lower() == 'y':
                    print('Aborting...')

                    return True

            print('Initializing processor...')

            # Initialize the processor and start it
            processor = Processor(private_key=account.private_key, genesis_validation=('genesis' in opt))

            processor.start()

            # Dev log
            print('Processor is running...')

            while processor.thread.is_alive():
                time_sleep(10)

            print('Processor stopped')

            return True

        elif cmd_opt == 'synchronize':
            # TODO -> Sync the chain with the others
            pass

        elif cmd_opt == 'serve':
            # TODO -> Run the rpc server and frequently sync with the chain

            # Setup rpc server
            blockchain = Blockchain()
            rpc_server = RPCServer(blockchain, Queue())

            # Serve and frequently sync the chain
            try:
                rpc_server.start()

                # TODO -> Sync the chain

            except:
                rpc_server.stop()

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
        while True:
            account = fetch_account()

            # Check if the load was successful
            if not account:
                return False

            # Ask who to send the transaction to and how much
            recipient = input('Recipient (public key): ')
            amount = input('Amount: ')

            try:
                float(amount)

            except:
                print('Invalid amount')

                return False

            tip = None

            # Ask if user wants to add a tip to the transaction
            if input('Add tip? (y/n): ').lower() == 'y':
                try:
                    tip = float(input('Please enter the tip: '))

                except:
                    print('Invalid tip')

                    return False

            print('Fetching required data...')

            # Fetch a node from user input
            node = fetch_node()

            # Fetch current transaction fee
            client = Client(node[0], node[1])
            transaction_fee = client.getBaseFee() * 1.03125

            # Check if the user wants to use a custom fee
            print('The current transaction fee is VAC ' + str(transaction_fee))
            if input('Use custom fee (Fee too low = transaction will not be included)? (y/n): ').lower() == 'y':
                transaction_fee = input('Please enter the transaction fee: ')

                try:
                    float(transaction_fee)

                except:
                    print('Invalid transaction fee')

                    return False

            print('Creating transaction...')

            # Create transaction
            transaction = Transaction(account.public_key, recipient, amount, fee=transaction_fee,
                                      tx_type='tx', tip=(tip if tip else 0))

            # Sign transaction
            success = transaction.sign_tx(account.private_key)

            if not success:
                print('Failed to sign transaction')

                return False

            print('Transaction created successfully\n')

            print('Transaction information')
            print('Sender: ' + transaction.sender)
            print('Recipient: ' + transaction.recipient)
            print('Amount: ' + str(transaction.amount))
            print('Fee: ' + str(transaction.fee))
            print('Timestamp: ' + str(transaction.timestamp))
            print('Hash: ' + transaction.hash)
            print('Signature: ' + transaction.signature)

            # Ask if the user wants to send the transaction
            if not input('\nSend transaction? (y/n): ').lower() == 'y':
                print('Transaction aborted')

                return False

            # Send transaction
            print('Sending transaction...')

            try:
                success = client.addTransaction(RPCTransaction(sender=transaction.sender,
                                                               recipient=transaction.recipient,
                                                               amount=transaction.amount, fee=transaction.fee,
                                                               type='tx', timestamp=str(transaction.timestamp),
                                                               hash=transaction.hash, signature=transaction.signature))

            except:
                # TODO -> Send to another node

                print('Failed to send transaction')

                return False

            if not success:
                print('Failed to send transaction :(')

                return False

            print('Transaction sent successfully\n')

            # Ask if the user wants to send another transaction
            if input('Send another transaction? (y/n): ').lower() == 'y':
                continue

            break

    elif cmd == 'stake':
        while True:
            account = fetch_account()

            # Check if the load was successful
            if not account:
                return False

            # Ask who to delegate the stake to and how much
            recipient = input('Delegate to (public key of the recipient; default: own address): ')
            amount = input('Amount to stake: ')

            try:
                float(amount)

            except:
                print('Invalid amount')

                return False

            tip = None

            # Ask if user wants to add a tip to the transaction
            if input('Add tip for the validators? (y/n): ').lower() == 'y':
                try:
                    tip = float(input('Please enter the tip: '))

                except:
                    print('Invalid tip')

                    return False

            print('\nFetching required data...')

            # Fetch the node to use
            node = fetch_node()

            # TODO -> Send it to multiple nodes

            # Fetch current transaction fee
            client = Client(node[0], node[1])
            transaction_fee = (client.getBaseFee() * 1.03125) / 2

            # Check if the user wants to use a custom fee
            print('The current transaction fee is VAC ' + str(transaction_fee))
            if input('Use custom fee (Fee too low = transaction will not be included)? (y/n): ').lower() == 'y':
                transaction_fee = input('Please enter the transaction fee: ')

                try:
                    transaction_fee = float(transaction_fee)

                except:
                    print('Invalid transaction fee')

                    return False

            print('Creating stake transaction...')

            # Create transaction
            transaction = Transaction(account.public_key, recipient, amount, fee=transaction_fee,
                                      tx_type='stake', tip=(tip if tip else 0))

            # Sign transaction
            success = transaction.sign_tx(account.private_key)

            if not success:
                print('Failed to sign transaction')

                return False

            print('Stake transaction created successfully\n')

            print('Stake transaction information')
            print('Sender: ' + transaction.sender)
            print('Recipient: ' + transaction.recipient)
            print('Amount: ' + str(transaction.amount))
            print('Fee: ' + str(transaction.fee))
            print('Timestamp: ' + str(transaction.timestamp))
            print('Hash: ' + transaction.hash)
            print('Signature: ' + transaction.signature)

            # Ask if the user wants to send the transaction
            if not input('\nSend stake transaction? (y/n): ').lower() == 'y':
                print('Stake transaction aborted')

                return False

            # Send transaction
            print('Sending stake transaction...')

            try:
                success = client.addTransaction(RPCTransaction(sender=transaction.sender,
                                                               recipient=transaction.recipient,
                                                               amount=transaction.amount, fee=transaction.fee,
                                                               type='tx', timestamp=str(transaction.timestamp),
                                                               hash=transaction.hash, signature=transaction.signature))

            except:
                # TODO -> Send to another node

                print('Failed to send transaction')

                return False

            if not success:
                print('Failed to send transaction :(')

                return False

            print('Transaction sent successfully\n')

            # Ask if the user wants to send another transaction
            if input('Send another transaction? (y/n): ').lower() == 'y':
                continue

            break

    elif cmd == 'unstake':
        # TODO -> Create an unstake transaction (ask for tx values)
        pass

    elif cmd == 'claim':
        # TODO -> Create a claim transaction (ask for tx values)
        pass

    elif cmd == 'version':
        print(f'Advaced {__version__}')

    elif cmd == 'version-audit':
        # TODO -> Checks for newer versions and if this version has vulnerabilities or bugs
        pass

    elif cmd == 'help':
        print_help()


def is_option(value):
    """Check if value is an option.

    :param value: The value to check.
    :type value: str

    :return: Is an option or not.
    :rtype: bool
    """
    if any(value == (option['min'] if 'min' in option else None) or
           value == (option['standard'] if 'standard' in option else None) or
           value == (option['max'] if 'max' in option else None)
           for _, option in OPTIONS.items()):
        return True

    return False


def is_command(value):
    """Check if value is a command.

    :param value: The value to check.
    :type value: str

    :return: Is an option or not.
    :rtype: bool
    """
    if any(value == (command['min'] if 'min' in command else None) or
           value == (command['standard'] if 'standard' in command else None) or
           value == (command['max'] if 'max' in command else None)
           for _, command in COMMANDS.items()):
        return True

    return False


def is_command_option(value, command_name=None):
    """Check if value is a command option.

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
            if any(value == (cmd_option['min'] if 'min' in cmd_option else None) or
                   value == (cmd_option['standard'] if 'standard' in cmd_option else None) or
                   value == (cmd_option['max'] if 'max' in cmd_option else None)
                   for _, cmd_option in COMMANDS[command_name]['cmd-opts'].items()):
                return True

    # Go through all commands
    elif any(is_command_option(value, command) for _, command in COMMANDS.items()):
        return True

    return False


def fetch_account() -> Account | bool:
    """Fetch account from user input.

    :return: An account if it was successful and False if it was unsuccessful
    :rtype: :py:class:`accounts.account.Account` | bool
    """
    # Check if the account or the private key should be used
    if input('Use account that exists on this device? (y/n): ').lower() == 'y':
        account_name = input('Account name: ')
        account_password = getpass(prompt=f'Password for {account_name}: ')

        print('Loading account...')

        # Set account up
        account = Account(account_name, account_password)
        success = account.load()

        if not success:
            print('Failed to load account')

            return False

        print('Account loaded successfully\n')

    else:
        print('Use private key instead')

        private_key = input('Private key: ')

        print('Loading account...')

        account = Account('', '', private_key=private_key)
        account.public_key = account.get_public_key(private_key)

        if not account.public_key:
            print('Failed to load account')

            return False

        print('Account loaded successfully\n')

    return account


def fetch_node() -> list:
    """Fetches a node the user wants to use.

    :return: Node to use
    :rtype: list
    """

    # Fetch a known node
    nodes = Database.fetchall_from_db('SELECT ip_address, port FROM nodes_archive', {})

    while True:
        if not nodes:
            # TODO -> Search for nodes

            print('No nodes found')

            # Check if the user wants to use the advaced-org node
            if input('Use the advaced foundation node instead? (y/n): ').lower() == 'y':
                nodes = [('localhost', 87878)]

                # TODO -> Change ip address to advaced-org ip address

                # Save the node to the database
                Database.push_to_db('INSERT INTO nodes_archive (ip_address, port) VALUES (:ip, :port)',
                                    {'ip': nodes[0][0], 'port': nodes[0][1]})

        if type(nodes) == list:
            # Select a random node
            node = choice(nodes)

        else:
            node = nodes

        # Ask if the user wants to use the node
        if input(f'Use node {node[0]}:{node[1]}? (y/n): ').lower() == 'y':
            return node
