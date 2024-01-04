from database._impala.impala import Impala
from database.db_pool import DBPool


class ImpalaPool(DBPool):
    def __init__(self):
        super().__init__()

    def init(self, *args, **kwargs):
        try:
            host = kwargs['host']
            port = kwargs['port']
            database = kwargs['database'] if 'database' in kwargs else None
            max_count = kwargs['max_count']

            for _ in range(max_count):
                db_impl = Impala()
                db_impl.connect(host=host, port=port, database=database)

                self.queue.put(db_impl)
                self.allList.append(db_impl)

        except Exception:
            raise
