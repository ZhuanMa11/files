from dtcloud.tools import config


def connect_mongo_table(mongo_db_collection='sbomp_energy_log', only_read=True):  # 连接mongo_db 返回表,默认只读
    re = False
    used_mongo_db = config.get('used_mongo_db', False)
    # used_mongo_db_clusters = config.get('used_mongo_db_clusters', False)
    if used_mongo_db:
        import pymongo
        mongo_db_host = config.get('mongo_db_host', 'localhost')
        mongo_db_name = config.get('mongo_db_name', 'demo14_db_new')
        mongo_db_user = config.get('mongo_db_user')
        mongo_db_password = config.get('mongo_db_password')
        mongo_db_port = config.get('mongo_db_port', 27017)
        print(f'mongo_db_host:{mongo_db_host},mongo_db_name:{mongo_db_name},mongo_db_user:{mongo_db_user},mongo_db_password:{mongo_db_password},mongo_db_port:{mongo_db_port}')
        if only_read:  # 只读情况下，看有无只读服务器
            used_mongo_db_read = config.get('used_mongo_db_read', 'False')
            if used_mongo_db_read:  # 有只读服务器
                mongo_db_host = config.get('mongo_db_host_read', 'localhost')
                mongo_db_name = config.get('mongo_db_name_read', 'demo14_db_new')
                mongo_db_user = config.get('mongo_db_user_read')
                mongo_db_password = config.get('mongo_db_password_read')
                mongo_db_port = config.get('mongo_db_port_read', 27017)
                print(f'only_read mongo_db_host:{mongo_db_host},mongo_db_name:{mongo_db_name},mongo_db_user:{mongo_db_user},mongo_db_password:{mongo_db_password},mongo_db_port:{mongo_db_port}')

        if isinstance(mongo_db_port, str):
            mongo_db_port = int(mongo_db_port)

        # if used_mongo_db_clusters:
        #     used_mongo_db_clusters = 'mongodb://' + used_mongo_db_clusters
        #     my_client = pymongo.MongoClient(used_mongo_db_clusters)
        # else:
        my_client = pymongo.MongoClient(host=mongo_db_host, port=mongo_db_port)  # 连接数据库

        try:
            my_db = my_client[mongo_db_name]  # 打开指定的数据库
            if mongo_db_user and mongo_db_password:  # 如果有密码则登录
                auth_type = 'SCRAM-SHA-1'
                my_db.authenticate(mongo_db_user, mongo_db_password, mechanism=auth_type)
            my_table = my_db[mongo_db_collection]  # 连接集合（数据库表）
            re = my_table
        except Exception as exception:
            print(f'****** connect_mongo_table error : {exception}')
    return re


def insert_mongo_db_one(mongo_table, in_dict):  # 在表里插入记录
    re = False
    if mongo_table:
        try:
            re = mongo_table.insert_one(in_dict)
            print(f'insert_mongo_db ok : {re}')
        except Exception as exception:
            print(f'****** insert_mongo_db error : {exception}')
    return re


def insert_mongo_db_many(mongo_table, in_list):  # 在表里插入记录
    re = False
    if mongo_table:
        try:
            re = mongo_table.insert_many(in_list)
            print(f'insert_mongo_db ok : {re}')
        except Exception as exception:
            print(f'****** insert_mongo_db error : {exception}')
    return re


def insert_used_mongo_db(in_dict, mongo_db_collection='sbomp_energy_log'):
    my_table = connect_mongo_table(mongo_db_collection, only_read=False)
    return insert_mongo_db_one(my_table, in_dict)


def check_mongo_key(my_table, in_index_list=[('log_local_time', 1)]):
    # in_index_list = [('log_local_time', 1)]  转换成 in_index_dict={'log_local_time': 1}
    in_index_dict = dict(in_index_list)

    _find = False
    for index_tuple in my_table.list_indexes():  # 查找
        index_dict = dict(index_tuple)
        if 'key' in index_dict:
            key_tuple = index_dict['key']
            key_dict = dict(key_tuple)
            if key_dict == in_index_dict:
                _find = True
                break
    if not _find:
        my_table.create_index(in_index_list, background=True)


if __name__ == "__main__":
    print('192.168.3.242:502')

    # ip_port_list: ["'192.168.3.3", "503'"]
    # in_ip: '192.168.3.3:503'
