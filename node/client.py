from threading import Thread, Event
from zmq import Context, REQ
from requests import get
from time import sleep as time_sleep
import json

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from util.database.nodes import fetch_known_nodes


class Client:
    def __init__(self, database=None):
        """Initializes the node client.

        :param database: The database to use.
        :type database: :py:class:`util.database.database.Database`
        """
        super().__init__()

        # Set the database
        self.database = database

        # Set the socket up
        context = Context()
        self.socket = context.socket(REQ)

        # Set the thread up
        self.thread = Thread(target=self.run)
        self.stop_event = Event()

    def send_message(self, message: bytes):
        """Sends a message to the nodes.

        :param message: The message to send.
        :type message: bytes

        :return: Status if the message was sent successfully.
        :rtype: bool
        """
        # Check if database is running
        if not self.thread.is_alive():
            return False

        # Send message
        try:
            self.socket.send(message)

        except:
            # Dev log
            print('Failed to send message to node')

        return True

    def run(self):
        """Runs the node client.

        :return: None
        """
        # Fetch known nodes
        known_nodes = fetch_known_nodes()

        # Check if there are any known nodes
        if not known_nodes:
            # Dev log
            print('No known nodes found')

            # TODO -> Find new nodes

            return False

        # Connect to all known nodes
        for node in known_nodes:
            if node[0] in ('localhost', '127.0.0.1', get('https://api.ipify.org').content.decode('utf8')):
                continue

            try:
                self.socket.connect(f'tcp://{node[0]}:{node[1]}')
            except:
                # Dev log
                print(f'Failed to connect to node {node[0]}:{node[1]}')

        # Run the node client
        while not self.stop_event.is_set():
            # Send keep alive message
            try:
                self.socket.send(json.dumps({'type': 'keep_alive', 'data': None}))
            except:
                # Dev log
                print('Failed to send keep alive message to node')

            # Receive response
            response = self.socket.recv()

            if not response:
                # Dev log
                print('No response from the nodes')

            # Sleep for a while
            time_sleep(20)

    def start(self):
        """Starts the node server thread.

        :return: Status if the start of the node server was successful.
        :rtype: bool
        """

        # Check if database is already running
        if self.thread.is_alive():
            return False

        # Check if stop-event is set
        if self.stop_event.is_set():
            self.stop_event = Event()
            self.thread = Thread(target=self.run)

        # Start the node thread
        self.thread.start()

        return True

    def stop(self):
        """Stops the node thread.

        :return: Status if stop was successful.
        :rtype: bool
        """
        # Check if database is not running
        if not self.thread.is_alive():
            return False

        # Stop the thread
        self.stop_event.set()

        return True

    def restart(self):
        """Restarts the thread.

        :return: Status if restart was successful.
        :rtype: bool
        """

        # Check whether the thread is running or not
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
