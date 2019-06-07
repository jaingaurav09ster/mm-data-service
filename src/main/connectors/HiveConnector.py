""" Hive Database connector """

import logging
import os
import pyodbc
from src.resources.config import HIVE_CONFIG


class HiveConnector:
    """
    hive database connector class
    """

    def __init__(self):
        self.cursor = None
        self.conn = None
        self.database = HIVE_CONFIG['HIVE_SCHEMA']
        if HIVE_CONFIG['HIVE_DSN'] is not None:
            logging.debug("The HIVE_DSN environment variable is not defined.")
            self.connect_through_dsn()
        else:
            logging.debug("Attempting to connect to through user credentials")
            self.connect_through_credentials()

    def connect_through_dsn(self):
        """
        open connection
        :return: none
        """
        login_str = 'DSN={0};Server={1}'.format(HIVE_CONFIG['HIVE_DSN'], HIVE_CONFIG['HIVE_HOSTNAME'])

        self.conn = pyodbc.connect(login_str, autocommit=True)
        self.cursor = self.conn.cursor()

    def connect_through_credentials(self):
        """
        open connection
        :return: none
        """
        login_str = 'SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(HIVE_CONFIG['HIVE_HOSTNAME'],
                                                                     HIVE_CONFIG['HIVE_SCHEMA'],
                                                                     HIVE_CONFIG['HIVE_USERNAME'],
                                                                     HIVE_CONFIG['HIVE_PASSWORD'])

        self.conn = pyodbc.connect(login_str, autocommit=True, )
        self.cursor = self.conn.cursor()

    def close(self):
        """Function to close connection to database."""

        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get(self, table, columns, limit=None):
        """Function to get data from database for given table and columns"""

        query = "SELECT {0} from {1}.{2}".format(','.join(columns), self.database, table)
        print(query)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows) - limit if limit else 0:]

    def query(self, sql):
        """Function to query the database."""

        self.cursor.execute(sql)
