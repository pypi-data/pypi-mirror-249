# -*- coding: utf-8 -*-

import impala.dbapi

from database.db_wrapper import DBWrapper


class Impala(DBWrapper):

    def reconnect(self):
        pass

    def check_connection(self):
        pass

    def select_org(self, query, bind_value=None):
        pass

    def select(self, query, bind_value=None):
        pass

    def execute(self, query, bind_value=None):
        pass

    def add_bind(self, key, value):
        pass

    def close(self):
        pass

    def clear_bind(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def __init__(self):
        super().__init__()

    def __del__(self):
        pass

    def connect(self, host, port=21050, database=None):
        try:
            self.connection = impala.dbapi.connect(host, port, database=database)
        except:
            raise

    def is_connected(self):
        if self.connection is None:
            return False

        return self.connection.is_connected()

    def execute_many(self, query, bind_value):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.executemany(query, bind_value)

            row_count = self.cursor.rowcount
            self.cursor.close()

            return row_count
        except:
            raise
