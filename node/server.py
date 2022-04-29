from threading import Thread, Event
from queue import Queue

from zmq import Context, REP
from requests import get

from time import sleep as time_sleep
import json

# Add to path
from sys import path
from os.path import dirname, abspath, join

path.insert(0, join(dirname(abspath(__file__)), '..'))

# Project modules
from blockchain.block import Block
from blockchain.transaction import Transaction
from blockchain.burn_transaction import BurnTransaction

from accounts import Wallet


class Server:
    def __init__(self, processor_queue: Queue, blockchain, client, host: str = None, port: str = None, start: bool = False,
                 database=None):
        """Initializes socket for the node.

        :param host: IP-address of host (normally the public ip-address).
        :type host: str (ip-address format)
        :param port: Port of the server connection.
        :type port: int
        """
        super().__init__()

        # Set the required variables
        self.blockchain = blockchain
        self.processor_queue = processor_queue
        self.database = database
        self.client = client

        # Set host and port
        self.host = host if host else get('https://api.ipify.org').content.decode('utf-8')
        self.port = port if port else 57575  # Standard advaced tcp port: 57575

        # Set socket up
        context = Context()
        self.socket = context.socket(REP)

        # Set the server up
        self.thread = Thread(target=self.run)
        self.stop_event = Event()

        # Messages that are already broadcast
        self.broadcast_messages = []

        if start:
            self.start()

    def broadcast(self, message):
        """Broadcasts a message to all known nodes.

        :param message: Message to broadcast.
        :type message: str

        :return: Status if the broadcast was successful.
        :rtype: bool
        """

        success = self.client.send_message(message)

        # Check if the broadcast was successful
        if not success:
            return False

        return True

    def run(self):
        """Runs the server.

        :return: None
        """
        self.socket.bind(f'tcp://*:{self.port}')

        while not self.stop_event.is_set():
            # Wait for a request
            message = self.socket.recv()

            # Handle the request
            response, broadcast_message = self.handle_request(message)

            # Check if the request should be broadcast
            if broadcast_message and message not in self.broadcasted_messages:
                success = self.broadcast(message)

                # Check if the broadcast was successful
                if not success:
                    # Dev log
                    print('Failed to broadcast message')

                # Add the message to the list of broadcasted messages
                self.broadcasted_messages.append(message)

            # Send the response
            self.socket.send(response)

            # Sleep for a while
            time_sleep(.025)

    def handle_request(self, message):
        """Handles the request.

        :param message: Clients message.
        :type message: bytes

        :return: Response to the client and if the message should be broadcast.
        :rtype: bytes, bool
        """
        # Decode the message
        message = message.decode('utf-8')

        # Jsonify the message
        try:
            message = json.loads(message)

        except json.JSONDecodeError:
            return json.dumps({'success': False}).encode('utf-8'), False

        # Check if the data is complete
        if not all(key in message for key in ('type', 'data', 'sender', 'signature')):
            return json.dumps({'success': False}).encode('utf-8'), False

        # Check if the signature is valid
        if (not Wallet.valid_signature(public_key=message['sender'], signature=message['signature'],
                                       data=message['data'])):
            return json.dumps({'success': False}).encode('utf-8'), False

        # Handle the request
        if message['type'] == 'temp_block':
            # Fetch the block data from the dictionary
            block = Block()
            success = block.from_json(message['data'])

            # Check if the block was successfully created
            if not success:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Put the block into the input queue
            self.processor_queue.put({'type': 'temp_block', 'data': block})

            return json.dumps({'success': True}).encode('utf-8'), True

        elif message['type'] == 'winner_block':
            # Fetch the block data from the dictionary
            block = Block()
            success = block.from_json(message['data'])

            # Check if the block was successfully created
            if not success:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Put the block into the input queue
            self.processor_queue.put({'type': 'winner_block', 'data': block})

            return json.dumps({'success': True}).encode('utf-8'), True

        elif message['type'] == 'tx':
            # Fetch the transaction data from the dictionary
            tx = Transaction('', '', 0)
            success = tx.from_json(message['data'])

            # Check if the transaction was successfully created
            if not success:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Put the transaction into the input queue
            self.processor_queue.put({'type': 'tx', 'data': tx})

            return json.dumps({'success': True}).encode('utf-8'), True

        elif message['type'] == 'version':
            # Load json data
            try:
                data = json.loads(message['data'])
            except json.decoder.JSONDecodeError:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Check if the data is complete
            if not all(key in data for key in ('version', 'timestamp', 'public_key', 'signature')):
                return json.dumps({'success': False}).encode('utf-8'), False

            # Check if the signature is valid
            if (not Wallet.valid_signature(public_key=data['public_key'], signature=data['signature'],
                                           data=data['version'] + data['timestamp'])):
                return json.dumps({'success': False}).encode('utf-8'), False

            # Check if the data is valid
            if data['timestamp'] in self.blockchain.version_stamps:
                if data['version'] == self.blockchain.version_stamps[data['timestamp']]:
                    return json.dumps({'success': True}).encode('utf-8'), True

            # Add the version to the version stamps
            self.blockchain.add_version_stamp(data['timestamp'], data['version'], data['network'], data['public_key'],
                                              data['signature'], db_q=self.database.db_q)
        elif message['type'] == 'burn':
            # Load json data
            try:
                data = json.loads(message['data'])
            except json.decoder.JSONDecodeError:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Fetch the burn transaction data from the dictionary
            burn = BurnTransaction('', '', 0)
            success = burn.from_dict(data)

            # Check if the transaction was successfully created
            if not success:
                return json.dumps({'success': False}).encode('utf-8'), False

            # Put the transaction into the input queue
            self.processor_queue.put({'type': 'burn', 'data': burn})

            return json.dumps({'success': True}).encode('utf-8'), True

        else:
            return json.dumps({'success': False}).encode('utf-8'), False

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
