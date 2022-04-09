# Processor execution
from threading import Thread, Event
from queue import Queue

# Scheduling
from time import sleep as time_sleep
from datetime import datetime, timezone, timedelta

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from validator.validator import Validator
from util.database.database import Database

from blockchain.transaction import Transaction
from blockchain.block import Block
from blockchain.blockchain import Blockchain

from rpc.server import RPCServer
from accounts import Wallet


class Processor:
    def __init__(self, private_key, start=False, genesis_validation=False):
        super().__init__()

        self.private_key = private_key
        self.genesis_validation = genesis_validation

        self.stop_event = Event()
        self.thread = Thread(target=self.run)

        # Input of the rpc server and the other nodes
        self.input_queue = Queue()

        # Transactions to add to chain (list of:py::class:`blockchain.Transaction`)
        self.tx = []

        # Temporary blocks for the next epoch
        self.next_epoch = []

        if start:
            self.start()

    def run(self):
        # 1. Synchronize with other nodes (via rpc server of these nodes)

        # 2. Set the validator up
        self.validator = Validator(self.private_key)

        # 3. Check if enough VAC is staked to become a validator
        if Wallet.stake(self.validator.wallet.public_key, self.blockchain) < 4_096:
            return False

        # 4. Advertise to the network

        # 5. Connect to other nodes

        # 6. Slide into validating process

        # 7. Listen to new data and validate blocks
        while not self.stop_event.is_set():
            print('Creating new block...')

            # Fetch the transactions for this block
            if self.tx:
                tx = self.tx[0:2048] if len(self.tx) >= 2048 else self.tx[0:len(self.tx)]

                self.tx = list(set(self.tx) - set(tx))

            else:
                tx = []

            # Create own block
            block = Block(tx, self.blockchain.last_blocks[0])

            if self.blockchain.last_blocks[0].timestamp + timedelta(0, 32) > datetime.now(timezone.utc):
                block.timestamp = self.blockchain.last_blocks[0].timestamp + timedelta(0, 32)

            else:
                block.timestamp = datetime.now(timezone.utc)

            # Sign the block
            block, success = self.validator.validate_block(block)

            # Check if the block is valid
            if not block.is_valid(self.blockchain):
                # Dev log
                print('Error occurred! Stopping program (Own block is invalid)')

                # TODO -> Change behaviour when block is invalid

                return False

            # Add blocks fetched previously
            self.validator.temp_blocks = self.next_epoch
            self.next_epoch = []

            # Add block to own temp block
            self.validator.temp_blocks.append(block)

            # TODO -> Emit block to other nodes

            # Collect all temporary blocks and transactions from queue, until time is over (32 seconds)
            while datetime.now().timestamp() <= self.blockchain.last_blocks[0].timestamp.timestamp() + 32:
                if not self.input_queue.empty():
                    # Fetch item from queue
                    item_queue = self.input_queue.get()

                    # Check if the item is a transaction
                    if item_queue['type'] == 'tx':
                        self.tx.append(item_queue['data'])

                    # Check if the item is a block
                    elif item_queue['type'] == 'block':
                        # Check if the block is for this round
                        if item_queue['data'].index == block.index:
                            exists = False

                            for tmp in self.validator.temp_blocks:
                                if tmp.validator == item_queue['data'].validator:
                                    exists = True
                                    break

                            if not exists:
                                self.validator.temp_blocks.append(item_queue['data'])

                        # Check if the block is for the next round
                        elif item_queue['data'].index == block.index + 1:
                            self.next_epoch.append(item_queue['data'])

                    # TODO -> Share the block with other nodes

                else:
                    time_sleep(.01)

            # Select the winner block of the temporary blocks
            winner_block = self.validator.select_winner(self.blockchain, True)

            # Share winner with other nodes, fetch their winner
            # TODO -> Wait 5 seconds until all possible winners arrived at the input_queue, then select the one with
            #  most of the "votes"

            # Add block to the blockchain
            success = self.blockchain.add_block(winner_block)

            if not success:
                # Dev log
                print('Error occurred! Stopping program (add_block was not successful)')

                return False

            print('Added block successfully:', winner_block.index)

            # Reset temporary blocks
            self.validator.temp_blocks = []

            # Every 10 blocks check if whole chain is valid
            if winner_block.index % 10 == 0:
                if not self.blockchain.is_valid:
                    # TODO -> Find the error and resync the chain with other nodes

                    # Dev log
                    print('Error occurred! Stopping program (Chain is invalid)')

                    return False

                else:
                    # Dev log
                    print('Chain is valid')

        # 8. Turn all processes off

    def start(self):
        """Starts the processor-thread.

        :return: Status if processor start was successful.
        :rtype: bool
        """

        # Check if database is already running
        if self.thread.is_alive():
            return False

        # Check if stop-event is set
        if self.stop_event.is_set():
            self.stop_event = Event()
            self.db_thread = Thread(target=self.run)

        # Start database handler
        self.database = Database()

        # Initialize the blockchain
        if not self.genesis_validation:
            self.blockchain = Blockchain()

        else:
            # Test values
            test_tx = Transaction(
                '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                '690ec29bae1791c134acfa0a5f49ebcc43491493e41f751ed319a67db8f75d6dc2acc288b7e7d160ed3362c9490b40ff399047e639a9a0862f6dcd227fbd9f99',
                4_096, tx_type='stake')
            test_tx.signature = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

            self.blockchain = Blockchain(genesis_tx=[test_tx])

        # Start the rpc server
        self.rpc_server = RPCServer(self.blockchain, processor_queue=self.input_queue, start=True,
                                    db_q=self.database.db_q)

        # Start the database-handler
        self.thread.start()

        return True

    def stop(self):
        """Stops the processor thread.

        :return: Status if stop was successful.
        :rtype: bool
        """
        # Check if database is not running
        if not self.thread.is_alive():
            return False

        # Check if stop-event is set
        # if self.stop_event.is_set():
        #     return False

        # Stop the thread
        self.stop_event.set()

        # Cut the socket and rpc connections
        self.rpc_server.stop()
        self.rpc_server = None

        return True

    def restart(self):
        """Restarts the thread.

        :return: Status if restart was successful.
        :rtype: bool
        """

        # Check wether the thread is running or not
        if not self.thread.is_alive():
            return False

        # Stop the processor
        self.stop()

        # Wait until stop is injected
        while self.thread.is_alive():
            time_sleep(.01)

        # Start the processor
        self.start()

        # Check if restart was not successful
        if not self.thread.is_alive():
            return False

        return True
