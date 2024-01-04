# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud360
# QQ:35350428
# 邮件:35350428@qq.com
# 手机：13584935775
# 作者：'扶程星云'
# 公司网址： http://www.dtcloud360.com/
# Copyright 中亿丰信息科技(苏州)有限公司
# 日期：2021/10/15
# 功能： 针对 sqlite3的操作
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


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


def nebula_select_sql_lite(select_sql, in_parameters, db_name='sbomp.db'):  # 查询记录
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

