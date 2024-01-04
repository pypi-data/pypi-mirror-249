from database._mysql.mysql import MySQL
from database.db_pool import DBPool


class MySQLPool(DBPool):

    def init(self, *args, **kwargs):
        try:
            user = kwargs['user']
            password = kwargs['password']
            host = kwargs['host']
            database = kwargs['database']
            port = kwargs['port']
            max_count = kwargs['max_count']

            for _ in range(max_count):
                db_impl = MySQL()
                db_impl.connect(user=user, password=password, host=host, database=database, port=port)

                self.queue.put(db_impl)
                self.allList.append(db_impl)

        except Exception:
            raise
