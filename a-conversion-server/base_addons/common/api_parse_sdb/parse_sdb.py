# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/28
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import sqlite3


class ParseSdb:
    @staticmethod
    def parse_sdb_get_model_tree(sdb_path):
        """
        获取构建树
        :param sdb_path:
        :return:
        """
        sql3 = sqlite3.connect(sdb_path)

        def _get_first_point():
            a = sql3.execute("""
            select
            name.id, name.value, name.external_id, "", category.value
            from
            (select _objects_id.id, _objects_id.external_id, _objects_attr.category, _objects_val.value  from _objects_eav
            inner join _objects_id
            on _objects_id.id = _objects_eav.entity_id
            inner join _objects_val
            on _objects_eav.value_id = _objects_val.id
            inner join _objects_attr
            on _objects_eav.attribute_id = _objects_attr.id
            where _objects_id.id = 1
            and name = 'name') as name
            inner
            join
            (select _objects_eav.id, _objects_id.external_id, _objects_attr.category, _objects_val.value  from _objects_eav
            inner join _objects_id
            on _objects_id.id = _objects_eav.entity_id
            inner join _objects_val
            on _objects_eav.value_id = _objects_val.id
            inner join _objects_attr
            on _objects_eav.attribute_id = _objects_attr.id
            where _objects_id.id = 1
            and name = 'Category'
             ) as category
            on
            name.external_id = category.external_id""")
            info = a.fetchall()
            dic_info = {}
            if info:
                parent_info = info[0]
                dic_info = {
                    "id": parent_info[0],
                    "name": parent_info[1],
                    "guid": parent_info[2],
                    "parent_id": parent_info[3] if parent_info[3] else None,
                    "category": parent_info[4],
                    "revit_level": "",
                }
            a.close()
            return dic_info

        def _get_revit_level():
            # 获取所有得name = revit level
            a = sql3.execute(""" select level.id,level.节点索引,level.属性的值,level.构建GUID,level.name,level.category, name.属性的值 from 
         (select _objects_eav.id as 'id',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
               inner join _objects_attr
               on _objects_eav.attribute_id = _objects_attr.id
               inner join _objects_id
               on _objects_id.id = _objects_eav.entity_id
               inner join _objects_val
               on _objects_eav.value_id = _objects_val.id
               where value = 'Revit Level') as level
            inner join
           (select _objects_eav.id as 'ID',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
               inner join _objects_attr
               on _objects_eav.attribute_id = _objects_attr.id
               inner join _objects_id
               on _objects_id.id = _objects_eav.entity_id
               inner join _objects_val
               on _objects_eav.value_id = _objects_val.id
               where name = 'name') as name
         on level.节点索引 = name.节点索引""")
            dict_list = list()
            for info in a.fetchall():
                dic_info = {
                    "id": info[1],
                    "name": info[6],
                }
                dict_list.append(dic_info)
            a.close()
            return dict_list

        def _get_revit_group(data_list):
            a = sql3.execute("""  select level_group.id,level_group.节点索引,level_group.属性的值,level_group.构建GUID,name.属性的值,Category_level.属性的值 from 
         (select _objects_eav.id,_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
               inner join _objects_attr
               on _objects_eav.attribute_id = _objects_attr.id
               inner join _objects_id
               on _objects_id.id = _objects_eav.entity_id
               inner join _objects_val
               on _objects_eav.value_id = _objects_val.id
               where name = '参照标高') level_group
             inner join
           (select _objects_eav.id as 'ID',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
               inner join _objects_attr
               on _objects_eav.attribute_id = _objects_attr.id
               inner join _objects_id
               on _objects_id.id = _objects_eav.entity_id
               inner join _objects_val
               on _objects_eav.value_id = _objects_val.id
               where name = 'name') as name
         on level_group.节点索引 = name.节点索引
          inner join      
               (select _objects_eav.id as 'ID',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
               inner join _objects_attr
               on _objects_eav.attribute_id = _objects_attr.id
               inner join _objects_id
               on _objects_id.id = _objects_eav.entity_id
               inner join _objects_val
               on _objects_eav.value_id = _objects_val.id
               where name = 'Category') as Category_level
         on    Category_level.节点索引 = level_group.节点索引""")
            revit_level_list = _get_revit_level()
            data_dic = {}
            # 获取revit_level
            for d in revit_level_list:
                data_dic[d.get("name")] = d  # 以name为key创建新得字典
            for info in a.fetchall():
                if info[2] in data_dic:
                    parent_id = data_dic[info[2]]["id"]
                    dic_info = {
                        "id": info[1],
                        "name": info[4],
                        "guid": info[3],
                        "parent_id": parent_id,
                        "category": info[5],
                        "revit_level": parent_id,
                    }
                    data_list.append(dic_info)
            a.close()
            return data_list

        def _get_parent_info_by_parent_id(parent_id, parent_list, revit_level):
            a = sql3.execute("""
             select name.id,name.value,name.external_id,parent.value,category.value from 
             (select _objects_id.id,_objects_id.external_id,_objects_attr.category,_objects_val.value  from _objects_eav 
                   inner join _objects_id
                   on _objects_id.id = _objects_eav.entity_id
                   inner join _objects_val
                   on _objects_eav.value_id = _objects_val.id
                   inner join _objects_attr
                   on _objects_eav.attribute_id = _objects_attr.id
                     where _objects_id.id = {0}
                    and  name = 'name') as name
              inner join
              (select _objects_eav.id,_objects_id.external_id,_objects_attr.category,_objects_val.value  from _objects_eav 
                   inner join _objects_id
                   on _objects_id.id = _objects_eav.entity_id
                   inner join _objects_val
                   on _objects_eav.value_id = _objects_val.id
             inner join _objects_attr
                   on _objects_eav.attribute_id = _objects_attr.id
              where _objects_id.id = {0}
                    and  name = 'Category'
                    ) as category
                    on name.external_id = category.external_id
              inner join (
               select _objects_eav.id,_objects_id.external_id,_objects_attr.category,_objects_val.value  from _objects_eav 
                   inner join _objects_id
                   on _objects_id.id = _objects_eav.entity_id
                   inner join _objects_val
                   on _objects_eav.value_id = _objects_val.id
             inner join _objects_attr
                   on _objects_eav.attribute_id = _objects_attr.id
              where _objects_id.id = {0}
                    and  name = 'parent'
                    ) as parent
                    on name.external_id = parent.external_id
            """.format(parent_id))
            info = a.fetchall()
            a.close()
            if info:
                parent_info = info[0]
                if parent_info[3] == 1:
                    parent_dict_info = {
                        "id": parent_info[0],
                        "name": parent_info[1],
                        "guid": parent_info[2],
                        "parent_id": revit_level,
                        "category": parent_info[4],
                        "revit_level": revit_level,
                    }
                    parent_list.append(parent_dict_info)
                    return parent_list
                else:
                    parent_dict_info = {
                        "id": parent_info[0],
                        "name": parent_info[1],
                        "guid": parent_info[2],
                        "parent_id": parent_info[3],
                        "category": parent_info[4],
                        "revit_level": revit_level,
                    }
                    parent_list.append(parent_dict_info)
                    return _get_parent_info_by_parent_id(parent_info[3], parent_list, revit_level)
            else:
                return parent_list

        def _get_json():
            b = sql3.execute("""
                          select name_level.节点索引 as '节点ID',name_level.属性的值 as '属性的值', name_level.构建GUID as 'GUID',Category_level.属性的值,name.节点索引 as '节点ID',name.属性的值 as '属性的值', name.构建GUID as 'GUID',parent.属性的值,Category.属性的值 from 
                          (select _objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值' from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'Component' 
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id ) as component
                           inner join
                           (select _objects_eav.id as 'ID',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'name'
                               inner join _objects_id
                               on _objects_id.id = _objects_eav.entity_id
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id
                        ) as name
                         on name.节点索引 = component.属性的值
                            inner join
                           (select _objects_eav.id as 'ID',_objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值',_objects_id.external_id as '构建GUID',_objects_attr.name,_objects_attr.category  from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'name'
                               inner join _objects_id
                               on _objects_id.id = _objects_eav.entity_id
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id
                            ) as name_level
                         on name_level.节点索引 = component.节点索引
                          inner join 
                               (select _objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值' from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'parent'
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id
                              ) as parent
                        on parent.节点索引 = component.属性的值
                              inner join 
                               (select _objects_eav.entity_id as '节点索引' from _objects_eav        
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'Category'
                                ) as viewable_in
                        on viewable_in.节点索引 = component.属性的值
                        inner join      
                               (select _objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值'  from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'Category'
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id
                               ) as Category
                         on    Category.节点索引 = component.属性的值
                         inner join      
                               (select _objects_eav.entity_id as '节点索引',_objects_val.value as '属性的值' from _objects_eav 
                               inner join _objects_attr
                               on _objects_eav.attribute_id = _objects_attr.id
                               and name = 'Category'
                               inner join _objects_val
                               on _objects_eav.value_id = _objects_val.id
                               ) as Category_level
                         on    Category_level.节点索引 = component.节点索引
                         order  by name_level.节点索引, parent.属性的值
                        """)

            dict_list = list()
            dict_list.append(_get_first_point())
            revit_level = ""
            parent_id = ""
            for info in b.fetchall():
                if info[0] != revit_level:
                    revit_level = info[0]
                    dict_info = {
                        "id": info[0],
                        "name": info[1],
                        "guid": info[2],
                        "parent_id": 1,
                        "category": info[3],
                        "revit_level": revit_level,
                    }
                    dict_list.append(dict_info)
                    parent_id = ""
                if info[7] != parent_id:
                    parent_id = info[7]
                    dict_children_info = {
                        "id": info[4],
                        "name": info[5],
                        "guid": info[6],
                        "parent_id": info[7],
                        "category": info[8],
                        "revit_level": revit_level,
                    }
                    dict_list.append(dict_children_info)
                    parent_info_list = _get_parent_info_by_parent_id(info[7], list(), revit_level)
                    for parent_info in parent_info_list:
                        dict_list.append(parent_info)
                else:
                    dict_children_info = {
                        "id": info[4],
                        "name": info[5],
                        "guid": info[6],
                        "parent_id": info[7],
                        "category": info[8],
                        "revit_level": revit_level,
                    }
                    dict_list.append(dict_children_info)

            dict_list = _get_revit_group(dict_list)
            b.close()
            return dict_list

        def _get_trees(dic):
            key_column = 'id'  # 常量id
            parent_column = 'parent_id'  # 常量父id
            child_column = 'children'  #
            data_dic = {}
            for d in dic:
                data_dic[str(d.get(key_column)) + '-' + str(d.get("revit_level"))] = d  # 以自己的权限主键为键,以新构建的字典为值,构造新的字典
            data_tree_list = []  # 整个数据大列表
            for d_id, d_dic in data_dic.items():
                pid = d_dic.get(parent_column)  # 取每一个字典中的父id
                if pid is None:  # 父id=0，就直接加入数据大列表
                    d_dic[parent_column] = 0
                    data_tree_list.append(d_dic)
                else:  # 父id>0 就加入父id队对应的那个的节点列表
                    try:  # 判断异常代表有子节点，增加子节点列表=[]
                        d_dic[parent_column] = pid
                        if pid == 1:
                            data_dic[str(pid) + '-'][child_column].append(d_dic)
                        else:
                            data_dic[str(pid) + '-' + str(d_dic.get("revit_level"))][child_column].append(d_dic)
                    except KeyError:
                        try:
                            if pid == 1:
                                data_dic[str(pid) + '-'][child_column] = []
                                data_dic[str(pid) + '-'][child_column].append(d_dic)
                            else:
                                data_dic[str(pid) + '-' + str(d_dic.get("revit_level"))][child_column] = []
                                data_dic[str(pid) + '-' + str(d_dic.get("revit_level"))][child_column].append(d_dic)
                        except KeyError:
                            continue
            return data_tree_list

        dic = _get_json()
        if str(dic) != '[{}]':
            dic = [dict(t) for t in set([tuple(d.items()) for d in dic])]
            dic.sort(key=lambda x: x["id"])
        return _get_trees(dic)
