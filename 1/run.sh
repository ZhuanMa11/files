#!/bin/bash
set -e
# 函数初始化
source ./util.sh

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
    [ -d src/mysql/projects/${project_name}/docker-compose.yml ] &&  \
        docker-compose -f src/mysql/projects/${project_name}/docker-compose.yml up -d && \
        { echo "MySQL [$project_name] started successfully"; exit 0; }

    # 安装 MySQL 的具体步骤
    echo "Installing MySQL [$project_name] ..."
    
    # 创建项目根目录
    mkdir -p src/mysql/projects/${project_name}/{initsql,conf.d}
    # 拷贝公共初始化内容
    cp -a src/mysql/initsql/* src/mysql/projects/${project_name}/initsql
    cp -a src/mysql/conf.d/* src/mysql/projects/${project_name}/conf.d
    cp -a src/mysql/.env src/mysql/projects/${project_name}/.env && \
        export envFile="$(dirname $0)/src/mysql/projects/${project_name}/.env"

    initport=$(cat .port)
    offset=$(find src/mysql/projects/ -maxdepth 1 -type d  |grep -v '\/$'|wc -l)
    setEnvItemMust MYSQL_DATABASE       $mysql_dbname $envFile
    setEnvItemMust MYSQL_USER           $mysql_username $envFile
    setEnvItemMust MYSQL_PASSWORD       $mysql_password $envFile
    setEnvItemMust MYSQL_ROOT_PASSWORD  $mysql_root_password $envFile

    cat << EOF > src/mysql/projects/${project_name}/docker-compose.yml
version: '3.9'
services:
    mysql:
        image: mysql:latest
        restart: always
        hostname: $project_name-mysql
        container_name: $project_name-mysql
        env_file:
            - $envFile
        ports:
            - "$(expr $initport - $offset):3306"
        networks:
            - $project_name
        volumes:
            - ./src/mysql/projects/${project_name}/conf.d:/etc/mysql/conf.d
            - ./src/mysql/projects/${project_name}/data:/var/lib/mysql
            - ./src/mysql/projects/${project_name}/initsql:/docker-entrypoint-initdb.d
networks:
    $project_name:
        driver: bridge
EOF

    # 使用 Docker Compose 启动 MySQL 服务
    docker-compose up -f src/mysql/projects/${project_name}/docker-compose.yml -d && \
    echo "MySQL [$project_name] installed successfully"
}

stop_mysql() {
    find src/mysql/projects/ -maxdepth 1 -type d  |grep -v '\/$'|xargs -i basename {}
    read -p "project_to_stop" name
    if [ "a$name" == "a" ] || \
        [ ! -f src/mysql/projects/$name/docker-compose.yml ]; then
        echo "invalid project name"
        exit 1
    fi

    # 停止 MySQL 的具体步骤
    echo "Stopping MySQL [$project_name] ..."
    docker-compose down -f src/mysql/projects/$name/docker-compose.yml && \
    echo "MySQL [$project_name] stopped successfully"
}

# 安装/停止 Starrocks
install_starrocks() {
    # 创建一个 docker-compose.yml 文件来定义 Starrocks 服务
    [ -d dest/sr/projects/${project_name}/docker-compose.yml ] &&  \
        docker-compose -f dest/sr/projects/${project_name}/docker-compose.yml up -d && \
        { echo "Starrocks [$project_name] started successfully"; exit 0; }

    # 安装 Starrocks 的具体步骤
    echo "Installing Starrocks [$project_name] ..."

    # 检查用户是否提供了参数
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <project_name> <starrocks_version>"
        exit 1
    fi

    # 用户传入的参数
    project_name=$1
    starrocks_version=${2:-"latest"}
    init_port=$(cat .port)
    offset=$(find dest/sr/projects/ -maxdepth 1 -type d  |grep -v '\/$'|wc -l)
    valid_port=$(expr $init_port + $[$offset*4])
    # 创建一个 docker-compose.yml 文件来定义 Starrocks 服务
    [ -d dest/sr/projects/${project_name} ] && { echo "Starrocks [$project_name] already exists"; exit 1; }
    mkdir -p dest/sr/projects/${project_name}
    cp -a dest/sr/.be.env dest/sr/projects/${project_name}
    cp -a dest/sr/.fe.env dest/sr/projects/${project_name}

    cat <<EOF > dest/sr/projects/${project_name}/docker-compose.yml
version: "3.9"
services:
    starrocks-fe-0:
        image: starrocks/fe-ubuntu:${starrocks_version}
        hostname: $project_name-starrocks-fe-0
        container_name: $project_name-starrocks-fe-0
        env_file:
            - dest/sr/projects/${project_name}/.fe.env
        command:
            - /bin/bash
            - -c
            - |
                /opt/starrocks/fe_entrypoint.sh $project_name-starrocks-fe-0
        environment:
            - HOST_TYPE=FQDN
            - TZ=Asia/Shanghai
        ports:
            - "${valid_port}:8030"
            - "$(expr $valid_port + 1):9020"
            - "$(expr $valid_port + 2):9030"
        volumes:
            - dest/sr/projects/${project_name}/fe0_data:/opt/starrocks/fe/meta
        healthcheck:
            test: ["CMD-SHELL", "netstat -tnlp|grep :9030 || exit 1"]
            interval: 10s
            timeout: 10s
            retries: 3
    starrocks-be-0:
        image: starrocks/be-ubuntu:${starrocks_version}
        hostname: $project_name-starrocks-be-0
        container_name: $project_name-starrocks-be-0
        env_file:
            - dest/sr/projects/${project_name}/.be.env
        command:
            - /bin/bash
            - -c
            - |
                /opt/starrocks/be_entrypoint.sh $project_name-starrocks-fe-0
        environment:
            - HOST_TYPE=FQDN
            - TZ=Asia/Shanghai
        ports:
            - "$(expr $valid_port + 3):8040"
        depends_on:
            - starrocks-fe-0
        healthcheck:
            test: ["CMD-SHELL", "netstat -tnlp|grep :8040 || exit 1"]
            interval: 10s
            timeout: 10s
            retries: 3
        volumes:
            - dest/sr/projects/${project_name}/be0_data:/opt/starrocks/be/storage
networks:
    $project_name:
        driver: bridge
EOF

# 使用 Docker Compose 启动 Starrocks 服务
docker-compose up -f dest/sr/projects/${project_name}/docker-compose.yml -d && \
        { echo "Starrocks [$project_name] installed successfully"; exit 0; }
}

stop_starrocks() {
    find dest/sr/projects/ -maxdepth 1 -type d  |grep -v '\/$'|xargs -i basename {}
    read -p "project_to_stop" name
    if [ "a$name" == "a" ] || \
        [ ! -f dest/sr/projects/$name/docker-compose.yml ]; then
        echo "invalid project name"
        exit 1
    fi
    # 停止 Starrocks 的具体步骤
    echo "Stopping Starrocks [$project_name] ..."
    docker-compose down -f dest/sr/projects/$name/docker-compose.yml && \
    # your stopation commands here
    echo "Starrocks [$project_name] stopped successfully"
}

# 安装/停止 Flink CDC，并配置自动同步 MySQL 的 sample 数据库到 Starrocks
install_flink_cdc() {
    # 安装 Flink CDC 的具体步骤
    echo "Installing Flink CDC..."
    # your installation commands here
    echo "Flink CDC installed successfully"

    # 配置自动同步 MySQL 的 sample 数据库到 Starrocks
    echo "Configuring automatic synchronization from MySQL to Starrocks..."
    # your configuration commands here
    echo "Automatic synchronization configured successfully"
}

stop_flink_cdc() {
    # 停止 Flink CDC 的具体步骤
    echo "Stopping Flink CDC..."
    # your stopation commands here
    echo "Flink CDC stopped successfully"
}

# 主菜单
echo "Welcome to the DevOps Tool"
echo "1. Install MySQL"
echo "2. Stop MySQL"
echo "3. Install Starrocks"
echo "4. Stop Starrocks"
echo "5. Install Flink CDC and configure synchronization"
echo "6. Stop Flink CDC"
echo "Enter your choice (1-6): "
read choice

case $choice in
    1) install_mysql "$@" ;;
    2) stop_mysql "$@";;
    3) install_starrocks "$@";;
    4) stop_starrocks "$@";;
    5) install_flink_cdc "$@";;
    6) stop_flink_cdc "$@";;
    *) echo "Invalid choice" ;;
esac
