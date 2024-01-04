import mysql.connector

from database.db_wrapper import DBWrapper


class MySQL(DBWrapper):
    def connect(self, *args, **kwargs):
        try:
            self.user = kwargs['user']
            self.password = kwargs['password']
            self.host = kwargs['host']
            self.database = kwargs['database']
            self.port = kwargs['port']

            self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                      host=self.host, database=self.database,
                                                      port=self.port)
        except:
            raise

    def reconnect(self):
        try:
            self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                      host=self.host, database=self.database,
                                                      port=self.port)
        except:
            raise

    def check_connection(self):
        try:
            return self.connection is not None and self.connection.is_connected()
        except:
            return False

    def rollback(self):
        if not self.connection.is_connected():
            try:
                conn = mysql.connector.connect(user=self.user, password=self.password, host=self.host,
                                               database=self.database, port=self.port)
                self.connection = conn
            except:
                pass
        else:
            super().rollback()

    def call_proc(self, sp, params):
        try:
            self.cursor = self.connection.cursor()
            return self.cursor.callproc(sp, params)
        except:
            raise

    def execute(self, query, bind_value=None):
        try:
            self.cursor = self.connection.cursor()
            if bind_value is None:
                self.cursor.execute(query, self.bind_value)
            else:
                self.cursor.execute(query, bind_value)

            row_count = self.cursor.rowcount
            self.cursor.close()

            return row_count
        except:
            raise

    def execute_many(self, query, bind_value):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.executemany(query, bind_value)

            row_count = self.cursor.rowcount
            self.cursor.close()

            return row_count
        except:
            raise

    def select(self, query, bind_value=None):
        try:
            self.cursor = self.connection.cursor()
            if bind_value is None:
                self.cursor.execute(query, self.bind_value)
            else:
                self.cursor.execute(query, bind_value)

            # columns = [i[0].upper() for i in self.cursor.description ]
            columns = [i[0] for i in self.cursor.description]
            rows = self.cursor.fetchall()

            new_rows = [dict(zip(columns, row)) for row in rows]

            self.cursor.close()

            return new_rows
        except:
            raise

    def select_org(self, query, bind_value=None):
        try:
            self.cursor = self.connection.cursor()
            if bind_value is None:
                self.cursor.execute(query, self.bind_value)
            else:
                self.cursor.execute(query, bind_value)

            rows = self.cursor.fetchall()

            self.cursor.close()

            return rows
        except:
            raise

    def add_bind(self, key, value):
        self.bind_value[key] = value

    def clear_bind(self):
        self.bind_value.clear()

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
