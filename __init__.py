from platform import system
from os.path import join
from os import getcwd
from logging import INFO, DEBUG, ERROR, WARNING, CRITICAL

# Project version
__version__ = '1.0.0'

# System to use
OS = system()

# Set the database path from used operating system
if OS == 'Linux':
    DATABASE_FILE = join('/lib', 'advaced', 'database', 'db.db')
    LOG_FILE = join('/lib', 'advaced', 'logs', 'advaced.log')

elif OS == 'Windows':
    DATABASE_FILE = join(getcwd(), 'db.db')  # Path firstly used only for development
    LOG_FILE = join(getcwd(), 'advaced.log')  # Path firstly used only for development

elif OS == 'Darwin':
    DATABASE_FILE = join('/Library', 'advaced', 'database', 'db.db')
    LOG_FILE = join('/Library', 'advaced', 'logs', 'advaced.log')

# Standard logging format
FORMAT = '[{levelname:^9}] Advaced: {asctime} → {message}'
FORMATS = {
    INFO: FORMAT,
    DEBUG: f'\33[36m{FORMAT}\33[0m',
    ERROR: f'\33[31m{FORMAT}\33[0m',
    WARNING: f'\33[33m{FORMAT}\33[0m',
    CRITICAL: f'\33[1m\33[31m{FORMAT}\33[0m'
}

# Set the log level
level = 'INFO'

match level:
    case 'INFO':
        LOG_LEVEL = INFO
    case 'DEBUG':
        LOG_LEVEL = DEBUG
    case 'ERROR':
        LOG_LEVEL = ERROR
    case 'WARNING':
        LOG_LEVEL = WARNING
    case 'CRITICAL':
        LOG_LEVEL = CRITICAL
    case _:
        LOG_LEVEL = INFO

# Socket server and client ports
SERVER_PORT = 57575
CLIENT_PORT = 67676

# RPC connection endpoint
RPC_PORT = 87878

# Name of the interface
NAME = 'advaced - the Advaced protocol command line interface'

# Command line interface usage
USAGE = 'advaced [OPTIONS] COMMAND [COMMAND-OPTION]'

# Set options dict up
OPTIONS = {
    # Which network to use
    'mainnet': {
        'min': '-mn',
        'standard': '--mainnet',
        'max': '--main-network',

        'value': False,

        'description': 'Use the Advaced main-network (set as default)'
    },

    'testnet': {
        'min': '-tn',
        'standard': '--testnet',
        'max': '--test-network',

        'value': False,

        'description': 'Use the Advaced test-network'
    },

    # How much data should be synchronized (full-chain, last-10_000 or last-100 blocks)
    'sync-mode': {
        'standard': '--sync',
        'max': '--sync-mode',

        'value': True,
        'value-required': True,

        # full: everything | light: last 1_000 blocks
        'values': ['full', 'light'],

        'description': 'Set synchronization mode ("full" or "light"; default: full)'
    },

    # Whether it is a genesis validation or not
    'genesis': {
        'min': '-g',
        'standard': '--genesis',
        'max': '--genesis-validation',

        'value': False,

        'description': 'Create a new blockchain'
    },
}

# Set commands up
COMMANDS = {
    # Account management
    'account': {
        'min': 'acc',
        'standard': 'wallet',
        'max': 'account',

        'cmd-opts': {
            'create': {
                'min': 'new',
                'standard': 'create',

                'value': False,

                'description': 'Creates a new account'
            },

            'export': {
                'min': 'exp',
                'standard': 'export',

                'value': True,
                'value-name': 'save-directory',
                'value-required': False,

                'description': 'Exports an account into a file'
            },

            'import': {
                'min': 'imp',
                'standard': 'import',

                'value': False,

                'description': 'Imports an account from its private key'
            },

            'list': {
                'standard': 'list',

                'value': False,

                'description': 'Lists all accounts, that are currently saved'
            },

            'help': {
                'min': 'h',
                'standard': 'help',

                'value': False,

                'description': 'Shows this help'
            }
        },

        'description': 'Manage accounts'
    },

    'run': {
        'standard': 'run',

        'cmd-opts': {
            'validate': {
                'standard': 'validate',

                'value': True,
                'value-name': 'account-name',
                'value-required': False,

                'description': 'Run the proof-of-stake process'
            },

            'synchronize': {
                'min': 'sync',
                'standard': 'synchronize',

                'value': False,

                'description': 'Synchronize local blockchain with blockchain of the network'
            },

            'serve': {
                'standard': 'serve',

                'value': False,

                'description': 'Share data of the blockchain as rpc server'
            },

            'help': {
                'min': 'h',
                'standard': 'help',

                'value': False,

                'description': 'Shows this help'
            }
        },


        'description': 'Execute a process'
    },

    # Data archiving handler
    'export': {
        'min': 'exp',
        'standard': 'export',

        'cmd-opts': {
            'json': {
                'standard': 'json',
                'max': 'json-file',

                'value': True,
                'value-name': 'save-directory',
                'value-required': True,

                'description': 'Export blockchain to json-file'
            },

            'sqlite': {
                'min': 'db',
                'standard': 'sqlite',
                'max': 'sqlite3',

                'value': True,
                'value-name': 'save-directory',
                'value-required': True,

                'description': 'Export blockchain to sqlite3-file'
            },

            'help': {
                'min': 'h',
                'standard': 'help',

                'value': False,

                'description': 'Shows this help'
            }
        },

        'description': 'Export blockchain into a file'
    },

    'import': {
        'min': 'imp',
        'standard': 'import',

        'cmd-opts': {
            'json': {
                'standard': 'json',
                'max': 'json-file',

                'value': True,
                'value-name': 'file-path',
                'value-required': True,

                'description': 'Imports blockchain from json-file'
            },

            'sqlite': {
                'min': 'db',
                'standard': 'sqlite',
                'max': 'sqlite3',

                'value': True,
                'value-name': 'file-path',
                'value-required': True,

                'description': 'Imports blockchain from sqlite3-file'
            },

            'help': {
                'min': 'h',
                'standard': 'help',

                'value': False,

                'description': 'Shows this help'
            }
        },

        'description': 'Import blockchain from file'
    },

    # Transaction management
    'transaction': {
        'min': 'tx',
        'standard': 'transact',
        'max': 'transaction',

        'description': 'Makes a transaction'
    },

    'stake': {
        'standard': 'stake',
        'max': 'delegate',

        'description': 'Stakes a given amount to an address'
    },

    'unstake': {
        'standard': 'unstake',

        'description': 'Unstake a given previous delegated amount'
    },

    'claim': {
        'standard': 'claim',
        'max': 'earn-reward',

        'description': 'Claims a reward from successful validation'
    },

    # Versioning
    'version': {
        'min': 'v',
        'standard': 'version',

        'description': 'Shows the current version'
    },

    'version-audit': {
        'min': 'v-audit',
        'standard': 'version-audit',

        'description': 'Checks used version for vulnerabilities'
    },

    # Help
    'help': {
        'min': 'h',
        'standard': 'help',

        'description': 'Shows this page'
    }
}
