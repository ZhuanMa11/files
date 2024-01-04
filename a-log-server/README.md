# 日志服务

## 介绍
主服务的日志服务，包含登录日志、操作日志、错误日志。

### 目录简介  

**project-template-v3**  
├─ base_addons #------------------------------------------------基础功能  
│&emsp;├─ common  #---------------------------------------------------通用功能   
│&emsp;│&emsp;├─ api_crud  #-------------------------------------删改查通用方法   
│&emsp;│&emsp;├─ api_data  #-------------------------------------表数据处理方法  
│&emsp;│&emsp;├─ api_message  #-------------------------------状态码消息方法  
│&emsp;│&emsp;└─ api_wrapper  #--------------------------------------装饰器方法  
│&emsp;├─ log_management  #---------------------------------------日志模块  
│&emsp;└─ message_api #-----------------------------------------状态码模块   
├─ dtcloud #------------------------------------------------dtcloud底层服务  
├─ dtcloud.conf #----------------------------------------------------配置文件  
├─ dtcloud-bin #-----------------------------------------------服务入口文件  
├─ README.md #--------------------------------------------系统搭建指南  
└─ requirements.txt  #----------------------------------------------依赖包名
  
###接口

接口地址:https://console-docs.apipost.cn/preview/c2c00f7a6e46553d/451c39c5ff76893d

### dtcloud.conf文件配置参数
下列参数必须齐全，根据需求可自行增加

> **基础配置参数**  
> addons_path  加载文件夹  
> admin_passwd  系统超级密码  
> data_dir   data目录, 用于存放session信息、附件、缓存文件等  
> xmlrpc_port  XML-RPC协议使用的TCP端口 （默认：8069）

> **数据库相关配置**  
> db_host  数据库ip  
> db_port   数据库端口
> db_user 数据库访问用户  
> db_password  数据库用户密码
> db_name  指定要预加载的数据库，多个以逗号分隔 
> db_maxconn 数据库最大练级额数量，默认值63
> pg_path  数据库bin文件目录地址

> **系统配置参数**  
> server_url  服务地址  


###  装饰器  
> @CommonApiRouteWrapper.response_json  
  返回信息json序列化。
 

## 安装教程

1、配置虚拟环境
File->Settings->Project->Python Interpreter  追加虚拟路径

2、Edit configuration 中配置  
&emsp;&nbsp;Script path：项目的bin路径.示例：F:\djd-v1.1\dtcloud-bin    
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
