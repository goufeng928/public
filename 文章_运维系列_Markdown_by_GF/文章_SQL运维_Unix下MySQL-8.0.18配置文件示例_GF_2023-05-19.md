# 文章_SQL运维_Unix下MySQL-8.0.18配置文件示例_GF_2023-05-19

MySQL 是一个关系型数据库管理系统, 由瑞典 MySQL AB 公司开发, 属于 Oracle 旗下产品。

MySQL 是最流行的关系型数据库管理系统之一, 在 WEB 应用方面, MySQL 是最好的 RDBMS (Relational Database Management System, 关系数据库管理系统) 应用软件之一。

MySQL 是一种关系型数据库管理系统, 关系数据库将数据保存在不同的表中, 而不是将所有数据放在一个大仓库内, 这样就增加了速度并提高了灵活性。

MySQL 所使用的 SQL 语言是用于访问数据库的最常用标准化语言。

MySQL 软件采用了双授权政策，分为社区版和商业版, 由于其体积小, 速度快, 总体拥有成本低, 尤其是开放源码这一特点, 一般中小型和大型网站的开发都选择 MySQL 作为网站数据库。

## Unix 下 MySQL 8.0.18 默认配置文件 my.cnf 示例

本例中, MySQL 配置文件 my.cnf 的路径为 "/usr/local/mysql-data/conf/my.cnf"。

```txt
# MySQL 8.0.18 Default Configure File.

# ------------------------- MySQL Database Configuration -------------------------
[mysqld]

# 服务类: 监听 MySQL 服务的端口号。
port=3306

# 服务类: 启动 MySQL 服务的系统用户。
user=mysql

# 目录类: 设置 MySQL 的安装目录.
basedir=/usr/local/mysql-8.0.18

# 目录类: 设置 MySQL 数据库的数据的存放目录.
datadir=/usr/local/mysql-data/data

# 存储类: 创建新表时将使用的默认存储引擎.
default-storage-engine=INNODB

# 连接类: 允许的最大连接数.
max_connections=10000

# 连接类: 允许连接失败的次数 (防止有人从该主机试图攻击数据库系统).
max_connect_errors=10

# 字符类: 服务端使用的字符集默认为 UTF8MB4.
character-set-server=utf8mb4

# 字符类: 表名大小写不明感 (敏感为 0).
lower_case_table_names=1

# 权限类: 可无密码强制登录数据库.
#skip-grant-tables

# ------------------- MySQL Configuration for The Command Line -------------------
[mysql]

# 字符类: 设置 MySQL 命令行客户端使用的默认字符集.
default-character-set=utf8mb4

# ---------------------- MySQL Configuration for The Client ----------------------
[client]

# 连接类: 设置 MySQL 客户端连接服务端时默认使用的端口.
port=3306

# 字符类: 设置 MySQL 客户端使用的默认字符集.
default-character-set=utf8mb4
```

## Unix 下 MySQL 8.0.18 自定义配置文件 my.cnf 示例

本例中, MySQL 配置文件 my.cnf 的路径为 "/usr/local/mysql-data/conf/my.cnf"。

```txt
# MySQL 8.0.18 Custom Configure File.

# ------------------------- MySQL Database Configuration -------------------------
[mysqld]

socket = /usr/local/mysql-data/run/mysql.sock
pid_file = /usr/local/mysql-data/run/mysqld.pid
open_files_limit = 65535
explicit_defaults_for_timestamp
server_id = 1
safe_user_create
secure_file_priv=/usr/local/mysql-data/tmp
interactive_timeout = 86400
wait_timeout = 86400
sync_binlog=100
back_log=1024
max_binlog_cache_size=2147483648
max_binlog_size=524288000
default_storage_engine = InnoDB
log_slave_updates = 1

# 服务类: 监听 MySQL 服务的端口号。
port = 3306

# 服务类: 启动 MySQL 服务的系统用户。
user = mysql

# 目录类: 设置 MySQL 的安装目录.
basedir = /usr/local/mysql-8.0.18

# 目录类: 设置 MySQL 数据库的数据的存放目录.
datadir = /usr/local/mysql-data/data

# 目录类: 设置 MySQL 的临时目录.
tmpdir = /usr/local/mysql-data/tmp

# 连接类: 允许的最大连接数.
max_connections = 3000

# 连接类: 允许的最大用户连接数.
max_user_connections=2980

# 连接类: 允许连接失败的次数 (防止有人从该主机试图攻击数据库系统).
max_connect_errors = 100000

# 字符类: 服务端使用的字符集默认为 UTF8MB4.
character_set_server = utf8mb4

# 字符类: 表名大小写不明感 (敏感为 0).
lower_case_table_names = 1

# .......................... Specific Settings: INNODB ...........................
innodb_buffer_pool_size = 4096M
transaction_isolation=REPEATABLE-READ
innodb_buffer_pool_instances = 8
innodb_file_per_table = 1
innodb_data_home_dir = /usr/local/mysql-data/log/innodb_ts
innodb_data_file_path = ibdata1:2048M:autoextend
innodb_thread_concurrency = 8
innodb_log_buffer_size = 67108864
innodb_log_file_size = 1048576000
innodb_log_files_in_group = 4
innodb_max_undo_log_size=4G
innodb_undo_directory=/usr/local/mysql-data/log/undo_space/
innodb_log_group_home_dir = /usr/local/mysql-data/log/innodb_log/
innodb_adaptive_flushing=ON
innodb_flush_log_at_trx_commit = 2
innodb_max_dirty_pages_pct = 60
innodb_open_files=60000
innodb_purge_threads=1
innodb_read_io_threads=4
innodb_stats_on_metadata=OFF
innodb_flush_method=O_DIRECT

# ........................... Specific Settings: Logs ............................
log_bin = /usr/local/mysql-data/log/bin_log/mysql-bin
binlog_format= mixed
binlog_cache_size=32m
max_binlog_cache_size=64m
max_binlog_size=512m
long_query_time = 1
log_output = FILE
log_error = /usr/local/mysql-data/log/error_log/mysql-error.log
slow_query_log = 1
slow_query_log_file = /usr/local/mysql-data/log/query_log/slow_statement.log
log_queries_not_using_indexes=0
log_slave_updates=ON
log_slow_admin_statements=1
general_log = 0
general_log_file = /usr/local/mysql-data/log/general_log/general_statement.log
binlog_expire_logs_seconds = 1728000
relay_log = /usr/local/mysql-data/log/bin_log/relay-bin
relay_log_index = /usr/local/mysql-data/log/bin_log/relay-bin.index

# .................. Specific Settings: Replication New Feature ..................
master_info_repository=TABLE
relay-log-info-repository=TABLE
relay-log-recovery

# ------------------- MySQL Configuration for The Command Line -------------------
[mysql]

no-auto-rehash
default-character-set=utf8mb4
net-buffer-length=64K
unbuffered
max-allowed-packet = 2G
default-character-set = utf8mb4

#some var for mysql8
#log_error_verbosity=3
#innodb_print_ddl_logs=1
#binlog_expire_logs_seconds=259200
#innodb_dedicate_server=0
#
#innodb_status_file=1
#innodb_status_output=0
#innodb_status_output_locks=0

# -------------------------- MySQL Backup Configuration --------------------------
[mysqldump]

quick
max_allowed_packet=2G
log_error=/usr/local/mysql-data/log/error_log/mysql_dump_error.log
net_buffer_length=8k
```

## 总结

以上就是关于 SQL运维 Unix下MySQL-8.0.18配置文件示例 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
