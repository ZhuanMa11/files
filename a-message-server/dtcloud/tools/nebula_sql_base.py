# 返回标准的SQL语句

# where_values = 'ip_address=? and port=?'
# select_sql = get_select_sql_base(table_name=table_name, select_values='id,connect_state,reconnect_datetime',
#                                  where_values=where_values)
# re_state, db_list = nebula_select_sql_lite(select_sql, db_name=db_name, in_parameters=in_parameters)
def get_select_sql_base(table_name, select_values, where_values):  # 获取记录语句
    return "select {} from {} where {}".format(select_values, table_name, where_values)


def get_select_sql_order_base(table_name, select_values, where_values, order_str):  # 获取记录语句
    return "select {} from {} where {} order by {}".format(select_values, table_name, where_values, order_str)


def get_select_sql_order_limit(table_name, select_values, where_values, order_str, limit_value):  # 获取记录语句
    return "select {} from {} where {} order by {} limit 0,{}".format(select_values, table_name, where_values, order_str, limit_value)

# 更新记录语句方法
# set_values = 'connect_datetime=?,reconnect_datetime=?,connect_state=?'
# where_values = 'ip_address=? and port=?'
# update_sql = get_update_sql_base(table_name=table_name, set_values=set_values,
#                                  where_values=where_values)
# set_values = 'connect_datetime=?,reconnect_datetime=?,connect_state=?'
# update_sql = get_update_sql_base(table_name=table_name, set_values=set_values,
#                                  where_values=where_values)
# in_parameters = (connect_datetime, reconnect_datetime, connect_state, ip_address, str_port)
# re_state, re_info = nebula_update_sql_lite(update_sql, db_name=db_name, in_parameters=in_parameters)

def get_update_sql_base(table_name, set_values, where_values):  # 更新记录语句
    return "update {} set {} where {}".format(table_name, set_values, where_values)


# set_parameters = 'ip_address,port,connect_datetime,reconnect_datetime,connect_state'
# insert_sql = get_insert_sql_base(table_name=table_name, set_parameters=set_parameters)
# in_parameters = (ip_address, str_port, connect_datetime, reconnect_datetime, connect_state)
# re_state, re_info = nebula_update_sql_lite(update_sql=insert_sql, db_name=db_name,
#                                            in_parameters=in_parameters)
def get_insert_sql_base(table_name, set_parameters):  # 插入一条记录语句
    parameters_list = set_parameters.split(",")
    s = []
    for _ in parameters_list:
        s.append('?')

    set_values = ','.join(s)

    insert_sql = "insert into {} ({}) values ({})".format(table_name, set_parameters, set_values)
    return insert_sql
