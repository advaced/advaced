# Processor execution
from threading import Thread, Event
from queue import Queue

from time import sleep as time_sleep

# Add to path
from sys import path
from os.path import dirname, abspath, join
path.insert(0, join(dirname(abspath(__file__)), '..'))

# Database handler
from util.database.database import Database

# Blockchain classes
from blockchain import Block, Transaction
from blockchain.blockchain import Blockchain

# RPC server
from rpc import RPCServer


class Processor():
    def __init__(self, private_key, start=False):
        self.stop_event = Event()
        self.thread = Thread(target=self.run)

        # Input of the rpc server and the other nodes
        self.input_queue = Queue()

        if start:
            self.start()


    def run(self):
        # 1. Synchronize with other nodes (via rpc server of these nodes)


        # 2. Setup the validator


        # 3. Check if enough VAC is staked to become a validator


        # 4. Advertise to the network


        # 5. Connect to other nodes



        # 6. Slide into validating process


        # 7. Listen to new data and validate blocks
        while not self.stop_event.is_set():
            pass
            #

            # TODO -> Add the processor


        # 8. Cut the socket and rpc connections


        # 9. Turn all processes off


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
        self.blockchain = Blockchain()

        # Start the rpc server
        self.rpc_server = RPCServer(blockchain, start=True, db_q=self.database.db_q)

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
