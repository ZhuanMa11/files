**用于解决频繁创建和卸载Mysql/Starrocsk场景，以及满足flink cdc快速部署需求；**

***实现方式***：通过docker-compose管理，以容器形式提供用户使用，提供flink cdc流程使用；
***环境依赖***：
1. Docker
2. Docker-compose

***TODO***：
1. 控制QoS资源配额，合理分配应用资源；
2. 支持外部数据源和starrocks接入；
3. ...







### 1. Mysql流程
1.1 快速部署mysql
```bash
# Usage: ./run.sh <project_name> <mysql_username> <mysql_password> <mysql_dbname> <mysql_root_password>
bash ./run.sh demo demo 123456 sample P@ssW0rd
```

### 2. Starrocks流程
2.1 快速部署starrocks环境（多be）
``` bash
# @Param project_name 项目名称 [required]
# @Param be_num 设置be实例数 [optional]

# Usage: ./run.sh <project_name> <be_num>
bash ./run.sh demo 4
```

### 3. Flink CDC流程
3.1 快速部署flink cdc任务
```bash
# @Param project_name 项目名称 [required]
# @Param taskmanager_num taskmanager数量 [optional]
# @Param slot_num 设置每个taskmanager的slot数 [optional]

# Usage: ./run.sh <project_name> <taskmanager_num> <slot_num>
bash ./run.sh demo_cdc 1 4
```