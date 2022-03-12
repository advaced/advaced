from platform import system
from os.path import join
from os import getcwd

# Project version
__version__ = '1.0.0'

# System to use
OS = system()

# Set the database path from used operating system
if OS == 'Linux':
    DATABASE_FILE = join('/usr', 'lib', 'advaced', 'database', 'db.db')

elif OS == 'Windows':
    DATABASE_FILE = join(getcwd(), 'db.db') # Path firstly used only for developement

elif OS == 'Darwin':
    DATABASE_FILE = join('Library', 'advaced', 'database', 'db.db')

# Socket server and client ports
SERVER_PORT = 57575
CLIENT_PORT = 67676

# RPC connection endpoint
RPC_PORT = 87878

# Set options-dict up
OPTIONS = {
    # Wich network to use
    'mainnet': {
        'min': '-mn',
        'standard': '--mainnet',
        'max': '--mainnetwork',

        'value': False,

        'description': 'Use the Advaced main-network'
    },

    'testnet': {
        'min': '-mn',
        'standard': '--mainnet',
        'max': '--mainnetwork',

        'value': False,

        'description': 'Use the Advaced test-network'
    },

    # How much data should be synchronized (full-chain, last-10_000 or last-100 blocks)
    'syncmode': {
        'standard': '--sync',
        'max': '--syncmode',

        'value': True,
        'value-required': True,

        # full: everything | light: last 1_000 blocks
        'values': [ 'full', 'light' ],

        'description': 'Set synchronization mode ("full" or "light") (default: full)'
    }
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

                'value': True,
                'value-name': 'name',
                'value-required': False,

                'description': 'Creates a new account'
            },

            'export': {
                'min': 'exp',
                'standard': 'export',

                'value': True,
                'value-name': 'save-directory',
                'value-required': True,

                'description': 'Exports an account into a file'
            },

            'import': {
                'min': 'imp',
                'standard': 'import',

                'value': True,
                'value-name': 'private-key',
                'value-required': True,

                'description': 'Imports an account from its private key'
            },

            'list': {
                'standard': 'list',

                'value': False,

                'description': 'Lists all accounts, that are currently saved'
            }
        },

        'description': 'Manage accounts'
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
            }
        },

        'description': 'Import blockchain from file'
    },

    # Transaction management
    'transaction': {
        'min': 'tx',
        'standard': 'transact',
        'max': 'transaction',

        'description': 'Makes a transaction from one of the accounts'
    },

    'stake': {
        'standard': 'stake',
        'max': 'stake-vac',

        'description': 'Stakes a given amount from one of the accounts to an address'
    },

    'unstake': {
        'standard': 'unstake',
        'max': 'unstake-vac',

        'description': 'Unstake a given previous staked amount from a address back to one of the accounts'
    },

    'claim': {
        'standard': 'claim',
        'max': 'claim-reward',

        'description': 'Claims a reward from successful validation of a block/blocks (tx: validator-address -> claiming-address | sign: validator-address)'
    },

    'burn': {
        'standard': 'burn',
        'max': 'burn-stake',

        'description': 'Manually burn stake from address, that signed and validated wrong block (normally an automatic process)'
    },

    # Versioning
    'version': {
        'min': 'v',
        'standard': 'version',

        'description': 'Show current version'
    },

    'version-audit': {
        'min': 'v-audit',
        'standard': 'version-audit',

        'description': 'Checks used version for security vulnerabilities and bugs (online)'
    },

    # Help
    'help': {
        'min': 'h',
        'standard': 'help',

        'description': 'Shows help for all commands or for only for a specific command'
    }
}
