# 文件服务

### 介绍
为主服务提供文件服务，支持自动备份，自动删除没有使用的文件

### 目录简介

**xcj-file-server**  
├─ base_addons #-------------------------------------------基础功能模块  
│&emsp;├─ common #---------------------------------------------------通用功能   
│&emsp;│&emsp;├─ api_crud #-------------------------------------删改查通用方法   
│&emsp;│&emsp;├─ api_data #-------------------------------------表数据处理方法  
│&emsp;│&emsp;├─ api_excel #--------------------------------------excel处理方法  
│&emsp;│&emsp;├─ api_file #------------------------------------------文件处理方法  
│&emsp;│&emsp;├─ api_message #-------------------------------状态码消息方法  
│&emsp;│&emsp;├─ api_wrapper #--------------------------------------装饰器方法  
│&emsp;│&emsp;└─ tools #---------------------------------------------------通用工具  
│&emsp;├─ file_api #-----------------------------------------------文件管理模块  
│&emsp;└─ message_api #-----------------------------------接口状态码管理  
├─ dtcloud #------------------------------------------------dtcloud底层服务  
├─ my_addons #----------------------------------------------------业务模块  
│&emsp;└─ timed_task_management #-----------------------------定时任务  
├─ constants.py #---------------------------------------------通用配置参数  
├─ dtcloud.conf #----------------------------------------------------配置文件  
├─ dtcloud-bin #-----------------------------------------------服务入口文件  
├─ README.md #--------------------------------------------系统搭建指南  
└─ requirements.txt #-------------------------------------------------依赖包

### 重要接口

接口地址:https://console-docs.apipost.cn/preview/be4acd91b003260f/b3e89ce0b57bcb09

> **1. /api/v1/upload 上传文件**
>
**参数**：name&emsp;文件名称（不带后缀）    
&emsp;&emsp;&emsp;ext&emsp;文件后缀名  
&emsp;&emsp;&emsp;md5&emsp;文件唯一识别码  
&emsp;&emsp;&emsp;size&emsp;文件大小  
&emsp;&emsp;&emsp;access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;files&emsp;文件流

> **2. /api/v1/file_library/{int:文件id} 查询指定文件id信息**

**参数**：access_token&emsp;唯一识别码

> **3. /api/v1/check_preview/{int:文件id} 检测文件是否可以预览**

**参数**：access_token&emsp;唯一识别码

> **4. /api/v1/batch_download 检测文件是否可以预览**

**参数**：access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;data_list&emsp;打包目录结构   
&emsp;&emsp;&emsp;示例：

        [  
              {  
                "id": 6,  
                "name": "2#",  
                "category": "document",  
                "file_id": "",
                "parent_id": 0,
                "children": [
                  {
                    "id": 12,
                    "name": "图纸2",
                    "category": "drawing",
                    "file_id": "31",
                    "parent_id": 6
                  },
                  {
                    "id": 8,
                    "name": "4#",
                    "category": "document",
                    "file_id": "",
                    "parent_id": 6,
                    "children": [
                      {
                        "id": 15,
                        "name": "图纸4",
                        "category": "drawing",
                        "file_id": "32",
                        "parent_id": 8
                      }
                    ]
                  }
                ]
              },
              {
                "id": 7,
                "name": "3#",
                "category": "document",
                "file_id": "",
                "parent_id": 0
              },
              {
                "id": 16,
                "name": "图纸6",
                "category": "drawing",
                "file_id": "33",
                "parent_id": 0
              }
        ]

> **5. /api/v1/file_library 根据条件获取文件列表**

**参数**：access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;domain&emsp;帅选条件    
&emsp;&emsp;&emsp;示例：`[('ext','in',['3dm', '3ds', '3dxml', 'asm', 'catpart', 'catproduct', 'dae', 'dgn', 'dwf', 'dwfx', 'dxf', 'fbx','gbg', 'gbq', 'gcl', 'gdq', 'ggj', 'gjg', 'gmp', 'gpb', 'gpv', 'gqi', 'gsc', 'gsh', 'gtb', 'gtj', 'gzb','iam', 'ifc', 'igms', 'ipt', 'jt', 'nwc', 'nwd', 'obj', 'osgb', 'ply', 'prt', 'rfa', 'rte', 'rvm', 'rvt','shp', 'skp', 'sldasm', 'sldprt', 'step', 'stl', 'stp'])]`

> **6. /api/v1/parse_model 获取构件tree**

**参数**：access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;data&emsp;文件目录   
&emsp;&emsp;&emsp;示例:

    [
        {
            "building_name": "1#",
            "model_list": [
                {
                    "category": "building",
                    "model_ids": ['35']}, 
                {
                    "category": "component", 
                    "model_ids": ['31']
                }
            ]
        },
        {
            "building_name": "2#",
            "model_list": [
                {
                    "category": "building", 
                    "model_ids": ['31', '35']}, 
                {
                    "category": "component", 
                    "model_ids": ['32']}
                ]
            }
    ]

> **7. /api/v1/build_properties 获取构件属性**

**参数**：access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;file_id&emsp;文件id   
&emsp;&emsp;&emsp;guid&emsp;构建id

> **8. /api/v1/PC_build_properties 获取PC构件**

**参数**：access_token&emsp;唯一识别码  
&emsp;&emsp;&emsp;file_ids&emsp;文件id列表   
&emsp;&emsp;&emsp;where_data&emsp;查询条件&emsp;示例：`AND T1.value = 'PCB' AND T3.value = '2F_2.9' AND T2.value like '%2F%'`

### dtcloud.conf文件配置参数

下列参数必须齐全，根据需求可自行增加

> **基础配置参数**  
> addons_path 加载文件夹  
> admin_passwd 系统超级密码  
> data_dir data目录, 用于存放session信息、附件、缓存文件等  
> xmlrpc_port XML-RPC协议使用的TCP端口 （默认：8069）

> **数据库相关配置**  
> db_host 数据库ip  
> db_port 数据库端口
> db_user 数据库访问用户  
> db_password 数据库用户密码
> db_name 指定要预加载的数据库，多个以逗号分隔
> db_maxconn 数据库最大练级额数量，默认值63
> pg_path 数据库bin文件目录地址

> **系统配置参数**  
> server_url 服务地址  
> main_server_url 主服务地址    
> file_convert_url 转换服务地址   
> rvt_middle_dir 模型转换中间文件存放地址

### 装饰器

> @CommonApiRouteWrapper.response_json  
> 实现功能：调用接口认证、返回信息json序列化。

## 安装教程

1、配置虚拟环境
File->Settings->Project->Python Interpreter 追加虚拟路径

2、Edit configuration 中配置  
&emsp;&nbsp;Script path：项目的bin路径,示例:F:\djd-v1.1\dtcloud-bin    
&emsp;&nbsp;Parameter：执行conf 数据库设定  
&emsp;&nbsp;Python Interpreter ： 选择上面配置的虚拟路径

3、Terminal中执行：pip install -r requirements.txt -i https://pypi.douban.com/simple/

4、如果需要加入单个的包，执行：pip install 包名    
&emsp;&nbsp;如果需要指定版本，执行 pip install 包名==版本号

5、dtcloud.conf 中修改数据库的信息

```bash
国内镜像:
https://pypi.douban.com/simple/ 豆瓣
https://mirrors.aliyun.com/pypi/simple/ 阿里
https://pypi.hustunique.com/simple/ 华中理工大学
https://pypi.sdutlinux.org/simple/ 山东理工大学
https://pypi.mirrors.ustc.edu.cn/simple/ 中国科学技术大学
https://pypi.tuna.tsinghua.edu.cn/simple 清华

引申：更新pip
python -m pip install --index-url https://pypi.douban.com/simple --upgrade pip
```
