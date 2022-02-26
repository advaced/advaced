# Database handling
from sqlite3 import connect, Connection

from queue import Queue
from threading import Thread, Event

from time import sleep as time_sleep

# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '../../'))

# Path of the database
from __init__ import DATABASE_FILE


class Database():
    def __init__(self, manual=False):
        """Sets up the database connection values.

        """
        # Queue for the asynchronous handling of the database
        self.db_q = Queue()

        # Event that cuts the connection between the database and the program
        self.stop_event = Event()

        # Database-handling thread
        self.db_thread = Thread(target=self.database_handler)

        if not manual:
            self.db_thread.start()


    @staticmethod
    def execute_sql(connection: Connection, sql_command: str, executing_args: dict=None, fetch=None):
        """Execute the given sql.

        :param connection: Connection to the database.
        :type connection: :py:class:`sqlite3.Connection`
        :param sql_command: Command to execute.
        :type sql_command: str
        :param executing_args: Arguments to replace in the command.
        :type executing_args: dict
        :param fetch: Provides information about anything, that the execution wants to fetch from the database.
        :type fetch: str ('one', 'all' or None)

        :return: If fetch is not none, return the response of the database.
        """

        # Execute the command with its arguments
        cursor = connection.cursor()
        cursor.execute(sql_command, executing_args)

        # Fetch the response how the data should be delivered
        response = None

        if fetch == 'one':
            response = cursor.fetchone()

        elif fetch == 'all':
            response = cursor.fetchall()

        # Commit the changes and close the cursor
        connection.commit()
        cursor.close()

        return response


    def database_handler(self):
        """Handle incoming database-tasks from the queue.

        """

        # Set the database connection up
        connection = connect(DATABASE_FILE)

        # Run until the connection stops
        while not self.stop_event.is_set():
            # Check if the queue is empty
            if self.db_q.empty():
                time_sleep(.01)
                continue

            # Fetch the values from the queue
            sql_data = self.db_q.get()

            # If the sql_data is too small, append empty data to fill the space
            while len(sql_data) < 4:
                sql_data += (None, )

            # Execute the sql and wait for the response
            response = self.execute_sql(connection, sql_data[0], sql_data[1], sql_data[2])

            # Check if a queue was provided to push the response to
            if sql_data[3]:
                sql_data[3].put(response)


    def fetchone(self, sql_command: str, sql_data: dict):
        """Fetches one response from the database.

        :param sql_command: Command to execute.
        :type sql_command: str
        :param sql_data: Arguments to replace in the command.
        :type sql_data: dict
        """

        # Set the queue up
        query_queue =  Queue()

        # Put the data into the queue of the database
        self.db_q.put((sql_command, sql_data, 'one', query_queue))

        # Wait until the data arrives
        while query_queue.empty():
            time_sleep(.01)

        # Return the data
        return query_queue.get()


    def fetchall(self, sql_command: str, sql_data: dict):
        """Fetches the full response from the database.

        :param sql_command: Command to execute.
        :type sql_command: str
        :param sql_data: Arguments to replace in the command.
        :type sql_data: dict
        """

        # Set the queue up
        query_queue =  Queue()

        # Put the data into the queue of the database
        self.db_q.put((sql_command, sql_data, 'all', query_queue))

        # Wait until the data arrives
        while query_queue.empty():
            time_sleep(.01)

        # Return the data
        return query_queue.get()
