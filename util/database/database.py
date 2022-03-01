# Database handling
from distutils.log import error
from sqlite3 import connect, Connection

from queue import Queue
from threading import Thread, Event

from time import sleep as time_sleep

# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd()))

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
    

    @classmethod
    def push_to_db(cls,  sql_command: str, sql_data: dict):
        """Executes the input to the database.

        :param sql_command: Command to execute.
        :type sql_command: str
        :param sql_data: Arguments to replace in the command.
        :type sql_data: dict

        :return: Status wether the execution was successful or not.
        """
        # Set the database connection up
        connection = connect(DATABASE_FILE)

        # Try to execute the sql and wait for the response
        try:
            cls.execute_sql(connection, sql_command, sql_data)
        
        except error:
            # Development Log
            print(error)

            return False

        return True
    

    @classmethod
    def fetchone_from_db(cls, sql_command: str, sql_data: dict):
        """Fetches one response from the database.

        :param sql_command: Command to execute.
        :type sql_command: str
        :param sql_data: Arguments to replace in the command.
        :type sql_data: dict

        :return: Response of the database.
        """

        # Set the database connection up
        connection = connect(DATABASE_FILE)

        # Execute the sql and wait for the response
        response = cls.execute_sql(connection, sql_command, sql_data, 'one')

        return response


    @classmethod
    def fetchall_from_db(cls, sql_command: str, sql_data: dict):
        """Fetches the full response from the database.

        :param sql_command: Command to execute.
        :type sql_command: str
        :param sql_data: Arguments to replace in the command.
        :type sql_data: dict

        :return: Response of the database.
        """

        # Set the database connection up
        connection = connect(DATABASE_FILE)

        # Execute the sql and wait for the response
        response = cls.execute_sql(connection, sql_command, sql_data, 'all')

        return response


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

        :return: Response of the database.
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

        :return: Response of the database.
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


    def start(self):
        """Starts the database-thread manually.

        :return: Status if database start was successful.
        :rtype: bool
        """

        # Check if database is already running
        if self.db_thread.is_alive():
            return False

        # Check if stop-event is set
        if self.stop_event.is_set():
            self.stop_event = Event()
            self.db_thread = Thread(target=self.database_handler)

        # Start the database-handler
        self.db_thread.start()

        return True


    def stop(self):
        """Stops the database-thread manually.

        :return: Status if database stop was successful.
        :rtype: bool
        """
        # Check if database is not running
        if not self.db_thread.is_alive():
            return False

        # Check if stop-event is set
        # if self.stop_event.is_set():
        #     return False

        # Stop the database-handler
        self.stop_event.set()

        return True


    def restart(self):
        """Restarts the database-thread manually.

        :return: Status if database restart was successful.
        :rtype: bool
        """

        # Check wether the database-thread is running or not
        if not self.db_thread.is_alive():
            return False

        # Stop the database
        self.stop()

        # Wait until stop is injected
        while self.db_thread.is_alive():
            time_sleep(.01)

        # Start the database
        self.start()

        # Check if restart was not successful
        if not self.db_thread.is_alive():
            return False

        return True
