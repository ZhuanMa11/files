# StarRocks migrate tool

1. Modify the configurations in `conf/config_prod.conf`.
2. Execute the binary `sh starrocks-migrate-tool` to generate DDL SQL.
3. Results are generted in `./result` by default for creating tables in both `flink-sql` and `StarRocks`.
