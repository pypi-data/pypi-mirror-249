# -*- coding: utf-8 -*-
from database._mysql.mysql_pool import MySQLPool
from database._utils.loder import CommConfig


class MariaDbSessionAbstract():
    version = '1_0_0'
    dbPool = MySQLPool()

    @classmethod
    def get_session(cls):
        return cls.dbPool.get_session()

    @classmethod
    def release_session(cls, session):
        cls.dbPool.release(session)

    @classmethod
    def init(cls, *args, **kwargs):
        cls.dbPool.init(
            **kwargs
        )

    @classmethod
    def close(cls, session):
        cls.dbPool.close(session)

    @classmethod
    def check_queue_size(cls):
        return cls.dbPool.check_queue_size()


class MariaDbSessionManager(MariaDbSessionAbstract):
    def __init__(self):
        self.init(
            user=CommConfig.config.get('MYSQL', 'USER'),
            password=CommConfig.config.get('MYSQL', 'PASSWORD'),
            host=CommConfig.config.get('MYSQL', 'HOST'),
            database=CommConfig.config.get('MYSQL', 'DATABASE'),
            port=CommConfig.config.get('MYSQL', 'PORT'),
            max_count=CommConfig.config.getint('COMMON', 'MAX_COUNT')
        )

    def get_session(self):
        # 세션풀에서 사용가능한 세션을 하나 가져온다.
        # 세션매니저는 풀에서 사용가능한 하나의 세션만 가져오고 관리한다.
        session = super().get_session()

        if session is None:
            raise Exception('Could not make session')

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


class MariaDbSessionManager2(MariaDbSessionAbstract):
    def __init__(self):
        #
        self.session = None
