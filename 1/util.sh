#!/bin/bash

# 仅存在即替换变量值
function setEnvItemIfExists() {
    key=$1
    newval=$2
    file=$3
    
    grep -q "^$key=" $file && sed -i "s#$key=.*#$key=$newval#g" $file
}

# 严格替换变量值
function setEnvItemMust() {
    key=$1
    newval=${2:-""}
    file=$3
    
    grep -q "^$key=" $file 2>/dev/null && sed -i "s#$key=.*#$key=$newval#g" $file || 
        echo "$key=$newval" >> $file
}

# 获取路径下的目录名称
function dirsInPath() {
    glob=$1
    path=$2
    find $path/* -maxdepth 0 -name "$1"  -type d 2> /dev/null |awk -F '/' '{print $NF}'
}

# 返回端口可用
function portUsableFromFile(){
    file=$1
    port=$(cat $file)
    while True;do
        lsof -i:$port &>/dev/null || { echo $port; break; }
        port=$(expr $port + 1 )
    done
    echo $port > $file
}