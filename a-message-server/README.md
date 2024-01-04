# 项目框架_3.0

## 软件架构
![img.png](./base_addons/common/tools/系统架构图.png)软件架构说明


## 介绍

### 目录简介  

**project-template-v3**  
├─ base_addons #------------------------------------------------基础功能  
├─ dtcloud #------------------------------------------------dtcloud底层服务  
├─ my_addons #----------------------------------------------------业务服务  
│&emsp;├─ common  #---------------------------------------------------通用功能   
│&emsp;│&emsp;├─ api_crud  #-------------------------------------删改查通用方法   
│&emsp;│&emsp;├─ api_data  #-------------------------------------表数据处理方法  
│&emsp;│&emsp;├─ api_excel  #--------------------------------------excel处理方法  
│&emsp;│&emsp;├─ api_file  #------------------------------------------文件处理方法  
│&emsp;│&emsp;├─ api_message  #-------------------------------状态码消息方法  
│&emsp;│&emsp;├─ api_wrapper  #--------------------------------------装饰器方法  
│&emsp;│&emsp;└─ tools  #---------------------------------------------------通用工具  
│&emsp;├─ file_api  #-----------------------------------------------文件管理模块  
│&emsp;├─ interface_status_code_management  #-----接口状态码管理  
│&emsp;└─ login_api #---------------------------------------------------登录模块   
├─ constants.py #---------------------------------------------通用配置参数  
├─ dtcloud.conf #----------------------------------------------------配置文件  
├─ dtcloud-bin #-----------------------------------------------服务入口文件  
├─ index.md #-------------------------------------------------------框架介绍  
├─ README.md #--------------------------------------------系统搭建指南  
└─ requirements.txt  #----------------------------------------------依赖包名
  
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
> file_convert_url 文件转换服务地址  
> log_serve_url   日志服务地址   
> get_create_operate_log  get方法是否启用操作日志，默认为False
> rvt_middle_dir  模型转换中间文件存放地址
> log_file_path  日志存放地址


###  装饰器  
> @CommonApiLoginWrapper.login  
  实现功能：密码解密、登录验证、登录日志、错误日志、返回信息json序列化。

> @CommonApiRouteWrapper.access_token_check  
  实现功能：访问用户存在验证、用户唯一识别码验证、业务实体、操作日志、错误日志、返回信息json序列化。
  
> @CommonApiRouteWrapper.response_json  
  错误日志、返回信息json序列化。
 


## 安装教程

1、配置虚拟环境
File->Settings->Project->Python Interpreter  追加虚拟路径

2、Edit configuration 中配置
Script path：项目的bin路径：
     F:\djd-v1.1\dtcloud-bin
Parameter：执行conf 数据库设定
Python Interpreter ： 选择上面配置的虚拟路径

3、Terminal中执行：pip install -r requirements.txt -i https://pypi.douban.com/simple/

4、如果需要加入单个的包，执行：pip install 包名
     如果需要指定版本，执行 pip install 包名==版本号

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
