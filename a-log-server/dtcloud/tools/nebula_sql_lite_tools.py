import sqlite3


def nebula_delete_sql_lite(db_name='sbomp.db', table_name='sbomp_test_ip'):  # 删除内存表
    # 创建与数据库的连接

    conn = sqlite3.connect(db_name)
    # 删除表
    drop_sql = "drop table IF EXISTS " + table_name
    try:
        conn.execute(drop_sql)
        return True, 'ok'
    except Exception as e:
        return False, e
    finally:
        conn.close()


def nebula_create_sql_lite(create_sql, db_name='sbomp.db'):  # 创建内存表
    conn = sqlite3.connect(db_name)
    # 创建一个游标 cursor
    cur = conn.cursor()
    # 建表的sql语句
    sql_text = create_sql
    # 执行sql语句
    try:
        cur.execute(sql_text)
        return True, 'ok'
    except Exception as e:
        return False, e
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()


def nebula_select_sql_lite(select_sql, in_parameters, db_name='sbomp.db'):  # c查询记录
    conn = sqlite3.connect(db_name)
    # 创建一个游标 cursor
    cur = conn.cursor()
    # 建表的sql语句
    sql_text = select_sql
    # 执行sql语句
    try:
        cur.execute(sql_text, in_parameters)
        db_list = cur.fetchall()
        return True, db_list
    except Exception as e:
        return False, e
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()


def nebula_update_sql_lite(update_sql, in_parameters, db_name='sbomp.db'):  # 更新记录
    conn = sqlite3.connect(db_name)
    # 创建一个游标 cursor
    cur = conn.cursor()
    # 更新表的sql语句
    sql_text = update_sql
    # 执行sql语句
    try:
        cur.execute(sql_text, in_parameters)
        conn.commit()
        print(f'nebula_update_sql_lite ok')
        return True, 'ok'
    except Exception as e:
        conn.rollback()
        print(e)
        return False, e
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        conn.close()

# def get_select_sql_lite(table_name, select_values, where_values):
#     return "select {} from {} where {}".format(select_values, table_name, where_values)


# def get_update_sql_lite(table_name, set_values, where_values):
#     return "update {} set {} where {}".format(table_name, set_values, where_values)


# def get_insert_sql_lite(table_name, set_parameters):
#     parameters_list = set_parameters.split(",")
#     s = []
#     for _ in parameters_list:
#         s.append('?')
#
#     set_values = ','.join(s)
#
#     insert_sql = "insert into {} ({}) values ({})".format(table_name, set_parameters, set_values)
#     return insert_sql

# def get_create_data_sql_lite(table, data):
#     key = ','.join(data.keys())
#     value = data.values()
#     lists = ''
#     for i in value:
#         lists += "'{}',".format(i)
#
#     sql = "insert into {}({}) values({})".format(table, key, lists)
#
#     print(sql)
#     return sql
