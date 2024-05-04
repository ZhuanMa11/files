envFile=$1
cat $envFile |sed  's#^#export #g' > ${envFile}~
source ${envFile}~
echo "[db]
type = mysql
host = $MYSQL_HOST
port = $MYSQL_PORT
user = $MYSQL_USER
password = $MYSQL_PASSWORD"