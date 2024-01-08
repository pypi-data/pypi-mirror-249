# -*- coding: utf-8 -*-
from hamonsoft.database._impala.impala_pool import ImpalaPool
from hamonsoft.database._mysql.mysql_pool import MySQLPool
from hamonsoft.database._utils.loder import ConfigLoader


class DatabaseType:
    MYSQL = 'mysql'
    IMPALA = 'impala'


class SessionAbstract():
    version = '1_0_0'
    dbPool = None

    @classmethod
    def set_database(cls, _type, max_count=1, **kwargs):
        if _type == DatabaseType.MYSQL:
            cls.dbPool = MySQLPool(max_count=max_count, **kwargs)
        elif _type == DatabaseType.IMPALA:
            cls.dbPool = ImpalaPool(max_count=max_count, **kwargs)
        else:
            raise ValueError(f'{_type} is not supported')

    @classmethod
    def get_session(cls, timeout=1):
        return cls.dbPool.get_session(timeout)

    @classmethod
    def release_session(cls, session):
        cls.dbPool.release(session)

    @classmethod
    def init(cls, max_count=1, **kwargs):
        cls.dbPool.init(max_count=max_count, **kwargs)

    @classmethod
    def close(cls, session):
        cls.dbPool.close(session)

    @classmethod
    def check_queue_size(cls):
        return cls.dbPool.check_queue_size()


'''
MariaDB 세션 매니저
'''


class MariaDbSessionManager(SessionAbstract):
    def __init__(self):
        super().set_database(_type=DatabaseType.MYSQL, max_count=ConfigLoader.config.getint('COMMON', 'MAX_COUNT'),
                             user=ConfigLoader.config.get('MYSQL', 'USER'),
                             password=ConfigLoader.config.get('MYSQL', 'PASSWORD'),
                             host=ConfigLoader.config.get('MYSQL', 'HOST'),
                             database=ConfigLoader.config.get('MYSQL', 'DATABASE'),
                             port=ConfigLoader.config.get('MYSQL', 'PORT'), )

    def get_session(self, timeout=1):
        # 세션풀에서 사용가능한 세션을 하나 가져온다.
        # 세션매니저는 풀에서 사용가능한 하나의 세션만 가져오고 관리한다.
        # 세션풀에서 가져올 객체가 없는 경우 처리(타임아웃 기간 동안 대기) 로직 추가
        # 세션에 이상이 있는지 확인하고 재접속과 같이 처리한 이후 세션을 리턴시킨다
        session = super().get_session(timeout)
        if not session.check_connection():
            session.reconnect()

        return session

    def check_session_qsize(self):
        return super().check_queue_size()

    def release(self, session):
        if session is not None:
            super().release_session(session)

    def commit(self, session):
        if session is not None:
            session.commit()

    def rollback(self, session):
        if session is not None:
            session.rollback()

    def init(self, *args, **kwargs):
        super().init(
            **kwargs
        )

    def close(self, session):
        super().close(session)


'''
Impala 세션 매니저
IMPALA는 RDBMS와 다른 중요한 특성이 있다. 

Connection과 Session 분리:
Hive에서는 Connection과 Session을 별도로 관리한다. 
Connection은 데이터베이스 서버에 대한 연결을 나타내고, Session은 쿼리 실행 및 상태를 추적하는 데 사용된다.
커서는 쿼리를 실행하는 데 사용되며, 각각의 커서는 개별적인 세션을 가진다. 
따라서 커서를 생성할 때마다 새로운 세션을 만들어 해당 세션에서 쿼리를 실행한다.

hs2를 따르면 세션을 관리할 필요가 없다.(내부에서 알아서 한다....)
'''


class ImpalaSessionManager(SessionAbstract):
    def __init__(self):
        super().set_database(DatabaseType.IMPALA, max_count=ConfigLoader.config.getint('COMMON', 'MAX_COUNT'),
                             host=ConfigLoader.config.get('IMPALA', 'HOST'),
                             database=ConfigLoader.config.get('IMPALA', 'DATABASE'),
                             port=ConfigLoader.config.get('IMPALA', 'PORT'))

    def get_session(self, timeout=1):
        session = super().get_session(timeout)

        if not session.check_connection():
            session.reconnect()

        return session

    def check_session_qsize(self):
        return super().check_queue_size()

    def release(self, session):
        if session is not None:
            super().release_session(session)

    def commit(self, session):
        if session is not None:
            session.commit()

    def rollback(self, session):
        if session is not None:
            session.rollback()

    def init(self, *args, **kwargs):
        super().init(
            **kwargs
        )

    def close(self, session):
        super().close(session)
