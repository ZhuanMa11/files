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
    newval=$2
    file=$3
    
    grep -q "^$key=" $file && sed sed -i "s#$key=.*#$key=$newval#g" $file || 
        echo "$key=$newval" >> $file
}