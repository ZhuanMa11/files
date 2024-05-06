#!/bin/bash
envFile=$1
cat $envFile |sed  's#^#export #g' > ${envFile}~
source ${envFile}~
echo "[db]
type = mysql
host = $MYSQL_HOST
port = ${MYSQL_PORT:-3306}
user = ${MYSQL_USER:-root}
password = ${MYSQL_PASSWORD:-$MYSQL_ROOT_PASSWORD}"
