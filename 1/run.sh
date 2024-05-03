#!/bin/bash
set -e
# 函数初始化
source ./util.sh

ROOTPATH=$(cd "$(dirname $0)";pwd)

# 安装/停止 MySQL
install_mysql() {
    # 检查用户是否提供了参数
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <project_name> <mysql_username> <mysql_password> <mysql_dbname> <mysql_root_password>"
        exit 1
    fi

    project_name=$1
    mysql_username=$2
    mysql_password=$3
    mysql_dbname=$4
    mysql_root_password=$5

    # 创建一个 docker-compose.yml 文件来定义 MySQL 服务
    [ -d $ROOTPATH/src/mysql/projects/${project_name} ] &&  \
        docker-compose -f $ROOTPATH/src/mysql/projects/${project_name}/docker-compose.yml up -d && \
        { echo "MySQL [${project_name}] started successfully"; exit 0; }

    # 安装 MySQL 的具体步骤
    echo "Installing MySQL [${project_name}] ..."
    
    # 创建项目根目录
    mkdir -p $ROOTPATH/src/mysql/projects/${project_name}/{initsql,conf.d}
    # 拷贝公共初始化内容
    cp -a $ROOTPATH/src/mysql/{initsql,conf.d,.env} $ROOTPATH/src/mysql/projects/${project_name} && \
        export envFile="$ROOTPATH/src/mysql/projects/${project_name}/.env"

    initport=$(cat .port)
    offset=$(dirsInPath '*' $ROOTPATH/src/mysql/projects |wc -l)
    setEnvItemMust MYSQL_DATABASE       $mysql_dbname           $envFile
    setEnvItemMust MYSQL_HOST           ${project}_mysql_1      $envFile
    setEnvItemMust MYSQL_USER           $mysql_username         $envFile
    setEnvItemMust MYSQL_PASSWORD       $mysql_password         $envFile
    setEnvItemMust MYSQL_ROOT_PASSWORD  $mysql_root_password    $envFile

    cat << EOF > $ROOTPATH/src/mysql/projects/${project_name}/docker-compose.yml
version: '3.9'
services:
    mysql:
        image: mysql:latest
        restart: always
        env_file:
            - $envFile
        ports:
            - "$(expr $initport - $offset):3306"
        networks:
            - mysql_${project_name}
        volumes:
            - $ROOTPATH/src/mysql/projects/${project_name}/conf.d/my.cnf:/etc/mysql/conf.d/my.cnf:ro
            - $ROOTPATH/src/mysql/projects/${project_name}/data:/var/lib/mysql
            - $ROOTPATH/src/mysql/projects/${project_name}/initsql:/docker-entrypoint-initdb.d
networks:
    mysql_${project_name}:
        driver: bridge
EOF

    # 使用 Docker Compose 启动 MySQL 服务
    docker-compose -f $ROOTPATH/src/mysql/projects/${project_name}/docker-compose.yml up -d && \
    echo "MySQL [${project_name}] installed successfully"
}

stop_mysql() {
    dirsInPath '*' $ROOTPATH/src/mysql/projects/
    read -p "Select project to be stopped: " name
    [ "a$name" == "a" ] && \
        { echo "invalid project name"; exit 1; }

    [ ! -d $ROOTPATH/src/mysql/projects/$name ] && \
        { echo "project $name not found"; exit 1; }
    [ ! -f $ROOTPATH/src/mysql/projects/$name/docker-compose.yml ] && \
         { echo "Mysql unable to stop,maybe external"; exit 0; }
    echo "Stopping MySQL [${project_name}] ..."
    # 停止 MySQL 的具体步骤
    docker-compose -f $ROOTPATH/src/mysql/projects/$name/docker-compose.yml down && \
    echo "MySQL [${project_name}] stopped successfully"
}

list_mysql() {
    echo "MySQL List:"
    dirsInPath '*' $ROOTPATH/src/mysql/projects/
}

status_mysql() {
    dirsInPath '*' $ROOTPATH/src/mysql/projects/
    read -p "Select project to be checked: " name
    if [ "a$name" == "a" ] || \
        [ ! -f $ROOTPATH/src/mysql/projects/$name/docker-compose.yml ]; then
        echo "invalid project status"
        exit 1
    fi
    docker-compose -f  $ROOTPATH/src/mysql/projects/$name/docker-compose.yml ps
}

# 安装/停止 Starrocks
install_starrocks() {
    # 创建一个 docker-compose.yml 文件来定义 Starrocks 服务
    [ -d $ROOTPATH/dest/sr/projects/${project_name}/docker-compose.yml ] &&  \
        docker-compose -f $ROOTPATH/dest/sr/projects/${project_name}/docker-compose.yml up -d && \
        { echo "Starrocks [${project_name}] started successfully"; exit 0; }

    # 安装 Starrocks 的具体步骤
    echo "Installing Starrocks [${project_name}] ..."

    # 检查用户是否提供了参数
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <project_name> <starrocks_version> <be_num>"
        exit 1
    fi

    # 用户传入的参数
    project_name=$1
    starrocks_version=${2:-"latest"}
    be_num=${3:-"1"}
    init_port=$(cat .port)
    offset=$(dirsInPath '*' $ROOTPATH/dest/sr/projects |wc -l)
    valid_port=$(expr $init_port + $[$offset*4])
    # 创建一个 docker-compose.yml 文件来定义 Starrocks 服务
    [ -d $ROOTPATH/dest/sr/projects/${project_name} ] && { echo "Starrocks [${project_name}] already exists"; exit 1; }
    mkdir -p $ROOTPATH/dest/sr/projects/${project_name}
    cp -a $ROOTPATH/dest/sr/{.be.env,.fe.env,conf.d} $ROOTPATH/dest/sr/projects/${project_name} && \
        export envFile="$ROOTPATH/dest/sr/projects/${project_name}/.env"

    setEnvItemMust BE_NUM           ${be_num}                                           $envFile
    setEnvItemMust FE_USER          "root"                                              $envFile
    setEnvItemMust FE_PASSWORD      ""                                                  $envFile
    setEnvItemMust FE_HTTP_PORT     8030                                                $envFile
    setEnvItemMust FE_QUERY_PORT    9030                                                $envFile
    setEnvItemMust FE_HOST          ${project_name}_starrocks-fe_1                      $envFile
    setEnvItemMust OUTPUT_DIR       $ROOTPATH/dest/sr/projects/${project_name}/.output  $envFile

    cat <<EOF > $ROOTPATH/dest/sr/projects/${project_name}/docker-compose.yml
version: "3.9"
services:
    starrocks-fe:
        image: starrocks/fe-ubuntu:${starrocks_version}
        env_file:
            - $ROOTPATH/dest/sr/projects/${project_name}/.fe.env
        command:
            - /bin/bash
            - -c
            - |
                /opt/starrocks/fe_entrypoint.sh ${project_name}_starrocks-fe_1
        networks:
            - sr_${project_name}
        ports:
            - "${valid_port}:8030"
            - "$(expr $valid_port + 1):9020"
            - "$(expr $valid_port + 2):9030"
        volumes:
            - $ROOTPATH/dest/sr/projects/${project_name}/fe0_data:/opt/starrocks/fe/meta
            - $ROOTPATH/dest/sr/projects/${project_name}/conf.d/fe.conf:/opt/starrocks/fe/conf/fe.conf:ro
        healthcheck:
            test: ["CMD-SHELL", "netstat -tnlp|grep :9030 || exit 1"]
            interval: 10s
            timeout: 10s
            retries: 3
    starrocks-be:
        image: starrocks/be-ubuntu:${starrocks_version}
        env_file:
            - $ROOTPATH/dest/sr/projects/${project_name}/.be.env
        command:
            - /bin/bash
            - -c
            - |
                /opt/starrocks/be_entrypoint.sh ${project_name}_starrocks-fe_1
        ports:
            - "$(expr $valid_port + 3):8040"
        networks:
            - sr_${project_name}
        depends_on:
            - starrocks-fe
        deploy:
            replicas: ${be_num}
        healthcheck:
            test: ["CMD-SHELL", "netstat -tnlp|grep :8040 || exit 1"]
            interval: 10s
            timeout: 10s
            retries: 3
        volumes:
            - $ROOTPATH/dest/sr/projects/${project_name}/be0_data:/opt/starrocks/be/storage
            - $ROOTPATH/dest/sr/projects/${project_name}/conf.d/be.conf:/opt/starrocks/be/conf/be.conf:ro
networks:
    sr_${project_name}:
        driver: bridge
EOF

    # 使用 Docker Compose 启动 Starrocks 服务
    docker-compose -f $ROOTPATH/dest/sr/projects/${project_name}/docker-compose.yml up -d && \
        { echo "Starrocks [${project_name}] installed successfully"; exit 0; }
}

stop_starrocks() {
    dirsInPath '*' $ROOTPATH/dest/sr/projects/
    read -p "Select project to be stopped: " name
    if [ "a$name" == "a" ] || \
        [ ! -f $ROOTPATH/dest/sr/projects/$name/docker-compose.yml ]; then
        echo "invalid project name"
        exit 1
    fi
    # 停止 Starrocks 的具体步骤
    echo "Stopping Starrocks [${project_name}] ..."
    docker-compose -f $ROOTPATH/dest/sr/projects/$name/docker-compose.yml down && \
        echo "Starrocks [${project_name}] stopped successfully"
}

list_starrocks() {
    echo "Starrocks List:"
    dirsInPath '*' $ROOTPATH/dest/sr/projects/
}

status_starrocks() {
    dirsInPath '*' $ROOTPATH/dest/sr/projects/
    read -p "Select project to be checked: " name
    if [ "a$name" == "a" ] || \
        [ ! -f $ROOTPATH/dest/sr/projects/$name/docker-compose.yml ]; then
        echo "invalid project status"
        exit 1
    fi
    docker-compose -f  $ROOTPATH/dest/sr/projects/$name/docker-compose.yml ps
}

# 安装/停止 Flink CDC，并配置自动同步 MySQL 的 sample 数据库到 Starrocks
install_flink_cdc() {
    [ -d $ROOTPATH/flink/projects/${project_name}/docker-compose.yml ] &&  \
        docker-compose -f $ROOTPATH/flink/projects/${project_name}/docker-compose.yml up -d && \
        { echo "Flink CDC [${project_name}] started successfully"; exit 0; }

    read -p "Datasource type to submit, choose one: [$(dirsInPath '*' $ROOTPATH/src|xargs |tr ' ' '|')]: " sourceType && \
        [ -d $ROOTPATH/src/$sourceType ] || { echo "source type $sourceType not found";exit 1; }
    read -p "Please type source project:
        $(dirsInPath '*' $ROOTPATH/src/$sourceType|xargs -n 1)
    >>> Selected: " sourceProject && \
        [ -d $ROOTPATH/src/$sourceType/$sourceProject ] || { echo "source project $sourceProject not found with type $sourceType ";exit 1; }
    
    read -p "Please type starrocks project:
        $(dirsInPath '*' $ROOTPATH/dest/sr/projects|xargs -n 1)
    >>> Selected: " srProject && \
        [ -d $ROOTPATH/dest/sr/project/$srProject ] || { echo "starrocks project $srProject not found";exit 1; }

    echo "Installing Flink CDC [${project_name}] ..."
    # 安装 Flink CDC 的具体步骤
    cat <<EOF > $ROOTPATH/flink/projects/${project_name}/docker-compose.yml
    version: "3.9"
    services:
        jobmanager:
            image: flink:1.14.4-scala_2.11
            ports:
            - "8081:8081"
            command: jobmanager
            env_file:
                - $ROOTPATH/flink/.env
            volumes:
                - $ROOTPATH/flink/projects/${project_name}/checkpoint:/opt/flink/checkpoint
                - $ROOTPATH/flink/projects/${project_name}/savepoint:/opt/flink/savepoint
            networks:
                - ${sourceType}_${sourceProject}
                - sr_${srProject}
            environment:
            - |
                FLINK_PROPERTIES=
                jobmanager.rpc.address: ${project_name}_jobmanager_1
        taskmanager:
            image: flink:1.14.4-scala_2.11
            depends_on:
            - jobmanager
            command: taskmanager
            deploy:
                replicas: 1
            networks:
                - ${sourceType}_${sourceProject}
                - sr_${srProject}
            environment:
            - |
                FLINK_PROPERTIES=
                jobmanager.rpc.address: ${project_name}_jobmanager_1
                taskmanager.numberOfTaskSlots: 4
EOF
    docker-compose -f $ROOTPATH/flink/projects/${project_name}/docker-compose.yml up -d && \
        { echo "Flink CDC [$project_name] installed successfully"; exit 0; }

    # 配置自动同步 MySQL 的 sample 数据库到 Starrocks
    echo "Configuring automatic synchronization from MySQL to Starrocks..."

    echo "Database patterns: "
    read DB_PATTERN
    echo "Table patterns: "
    read TABLE_PATTERN

    source $ROOTPATH/src/$sourceType/$sourceProject/.env
    source $ROOTPATH/dest/sr/projects/$srProject/.env

    [ ! -f $ROOTPATH/flink/tools/smt/starrocks-migrate-tool ] && \
        wget https://cdn-thirdparty.starrocks.com/smt.tar.gz && \
        tar -xzvf smt.tar.gz -C $ROOTPATH/flink/tools

    SMTCONF=$ROOTPATH/flink/projects/${project_name}/smt.conf

    sh $ROOTPATH/src/$sourceType/$sourceProject/.smt.sh >   $SMTCONF
    sh $ROOTPATH/dest/sr/$srProject/.smt.sh             >>  $SMTCONF
    $ROOTPATH/flink/tools/smt/starrocks-migrate-tool -c     $SMTCONF

    docker cp $OUTPUT_DIR ${srProject}_starrocks-fe_1:/tmp
    docker cp $OUTPUT_DIR ${project_name}_jobmanager_1:/tmp
    docker exec -ti ${srProject}_starrocks-fe_1 \
        "mysql -u $FE_USER -h $FE_HOST -P $FE_QUERY_PORT -p$FE_PASSWORD < /tmp/.output/starrocks-create.all.sql"
    docker exec -ti ${project_name}_jobmanager_1 bash -c " \
        bin/sql-client.sh < /tmp/.output/flink-create.all.sql && bin/flink list"

    # your configuration commands here
    echo "Automatic synchronization configured successfully"
}

stop_flink_cdc() {
    # 停止 Flink CDC 的具体步骤
    echo "Stopping Flink CDC..."
    # your stopation commands here
    echo "Flink CDC stopped successfully"
}

list_flink_cdc() {
    echo "Flink CDC List:"
    dirsInPath '*' $ROOTPATH/flink/projects/
}

status_flink_cdc() {
    dirsInPath '*' $ROOTPATH/flink/projects/
    read -p "Select project to be checked: " name
    if [ "a$name" == "a" ] || \
        [ ! -f $ROOTPATH/flink/projects/$name/docker-compose.yml ]; then
        echo "invalid project status"
        exit 1
    fi
    docker-compose -f  $ROOTPATH/flink/projects/$name/docker-compose.yml ps
}

# 主菜单
echo "Welcome to the DevOps Tool"
echo "<<< Mysql >>>"
echo "1. Install MySQL"
echo "2. Stop MySQL"
echo "3. List MySQL"
echo "4. Status MySQL"
echo ""
echo "<<< Starrocks >>>"
echo "5. Install Starrocks"
echo "6. Stop Starrocks"
echo "7. List Starrocks"
echo "8. Status Starrocks"
echo ""
echo "<<< Flink CDC >>>"
echo "9. Install Flink CDC and configure synchronization"
echo "10. Stop Flink CDC"
echo "11. List Flink CDC"
echo "12. Status Flink CDC"
echo ""
echo "Enter your choice (1-12): "
read choice

case $choice in
    # mysql 
    1) install_mysql "$@" ;;
    2) stop_mysql "$@";;
    3) list_mysql "$@";;
    4) status_mysql "$@";;

    # starrocks
    5) install_starrocks "$@";;
    6) stop_starrocks "$@";;
    7) list_starrocks "$@";;
    8) status_starrocks "$@";;

    # flink cdc
    9) install_flink_cdc "$@";;
    10) stop_flink_cdc "$@";;
    11) list_flink_cdc "$@";;
    12) status_flink_cdc "$@";;
    *) echo "Invalid choice" ;;
esac
