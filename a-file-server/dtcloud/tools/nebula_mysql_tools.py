import pymysql


def nebula_connect_mysql(connect_db_dict):  # 连接mysql
    # 打开数据库连接
    ip = connect_db_dict.get('ip', '127.0.0.1')

    port = connect_db_dict.get('port', 3389)
    if type(port) == str:
        port = int(port)
    user = connect_db_dict.get('user', 'test')

    passwd = connect_db_dict.get('passwd', 'test')

    db_name = connect_db_dict.get('db_name', 'test')

    try:
        conn = pymysql.connect(host=ip, user=user, port=port, passwd=passwd, db=db_name)  # # 打开数据库连接
        cursor = conn.cursor()  # 获取游标
        return conn, cursor
    except Exception as e:
        print(f'连接mysql出错!错误信息:{e}')
        nebula_close_connect_mysql(cursor, conn)
        return None, e


def nebula_close_connect_mysql(cursor, conn):  # 关闭链接
    cursor.close()
    conn.close()
