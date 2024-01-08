from database._utils.loder import ConfigLoader
from database.session_manager import MariaDbSessionManager, ImpalaSessionManager, DatabaseType

DATABASE_TYPE='impala'

try:
    config_file = "C:\\Users\\전석\\Desktop\\keti\\config\\Database.cfg"
    ConfigLoader.load(config_file)
    
    session_manager = None
    
    if DATABASE_TYPE.lower() == DatabaseType.MYSQL:
        session_manager = MariaDbSessionManager()
    elif DATABASE_TYPE.lower() == DatabaseType.IMPALA:
        session_manager = ImpalaSessionManager()
    else:
        raise ValueError(f'{DATABASE_TYPE} is not supported')
    
    print(f'데이터 베이스 타입 {DATABASE_TYPE}, DB POOL REMAIN : {session_manager.check_session_qsize()}')
    connection = session_manager.get_session()
    print(f'데이터 베이스 타입 {DATABASE_TYPE}, DB POOL REMAIN : {session_manager.check_session_qsize()}')
    
    # 테스트를 위해 세션 CLOSE
    connection.close() #또는 session_manager.close(connection)
    
    #close상태인 세션을 pool에 반환
    session_manager.release(connection)
    
    print(f'데이터 베이스 타입 {DATABASE_TYPE}, DB POOL REMAIN : {session_manager.check_session_qsize()}')
    
    # session_manager에서 가져올때 검사.
    # get_session() 내부에서 세션 검사. 세션에 문제가 있을 때 reconnection
    
    connection = session_manager.get_session()
    print(f'데이터 베이스 {DATABASE_TYPE}, 풀에서 가져온 세션 상태 : {connection.check_connection()}, DB POOL REMAIN : {session_manager.check_session_qsize()}')
    session_manager.release(connection)
    
except Exception as e:
    print(f'error {e}')
