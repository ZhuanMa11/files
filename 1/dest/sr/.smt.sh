echo "[other]
# number of backends in StarRocks
be_num = ${BE_NUM}
# `decimal_v3` is supported since StarRocks-1.18.1
use_decimal_v3 = false
# file to save the converted DDL SQL
output_dir = ${OUTPUT_DIR}

[table-rule.1]
# pattern to match databases for setting properties
database = ${DB_PATTERN}
# pattern to match tables for setting properties
table = ${TABLE_PATTERN}
schema = ^.*$

############################################
### flink sink configurations
### DO NOT set `connector`, `table-name`, `database-name`, they are auto-generated
############################################
flink.starrocks.jdbc-url=jdbc:mysql://${FE_HOST}:${FE_QUERY_PORT}>
flink.starrocks.load-url= ${FE_HOST}:${FE_HTTP_PORT}
flink.starrocks.username=${FE_USER}
flink.starrocks.password=${FE_PASSWORD}
flink.starrocks.sink.max-retries=10
flink.starrocks.sink.properties.format=csv
flink.starrocks.sink.properties.column_separator=\x01
flink.starrocks.sink.properties.row_delimiter=\x02
flink.starrocks.sink.buffer-flush.interval-ms=15000"