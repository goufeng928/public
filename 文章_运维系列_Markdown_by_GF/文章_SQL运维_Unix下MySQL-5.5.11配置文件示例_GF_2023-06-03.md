# 文章_SQL运维_Unix下MySQL-5.5.11配置文件示例_GF_2023-06-03

MySQL 是一个关系型数据库管理系统, 由瑞典 MySQL AB 公司开发, 属于 Oracle 旗下产品。

MySQL 是最流行的关系型数据库管理系统之一, 在 WEB 应用方面, MySQL 是最好的 RDBMS (Relational Database Management System, 关系数据库管理系统) 应用软件之一。

MySQL 是一种关系型数据库管理系统, 关系数据库将数据保存在不同的表中, 而不是将所有数据放在一个大仓库内, 这样就增加了速度并提高了灵活性。

MySQL 所使用的 SQL 语言是用于访问数据库的最常用标准化语言。

MySQL 软件采用了双授权政策，分为社区版和商业版, 由于其体积小, 速度快, 总体拥有成本低, 尤其是开放源码这一特点, 一般中小型和大型网站的开发都选择 MySQL 作为网站数据库。

## Unix 下 MySQL 5.5.11 默认配置文件 my.cnf 示例

本例中, MySQL 配置文件 my.cnf 的路径为 "/opt/mysql-data/conf/my.cnf"。

```txt
# /opt/mysql-data/conf/my.cnf

# MySQL 5.5.11 Default Configure File.

# ------------------------- MySQL Database Configuration -------------------------
[mysqld]

# 服务类: 监听 MySQL 服务的端口号。
port=3306

# 服务类: 启动 MySQL 服务的系统用户。
user=mysql

# 目录类: 设置 MySQL 的安装目录.
basedir=/opt/mysql-5.5.11

# 目录类: 设置 MySQL 数据库的数据的存放目录.
datadir=/opt/mysql-data/data

# 存储类: 创建新表时将使用的默认存储引擎.
default-storage-engine=INNODB

# 连接类: 允许的最大连接数.
max_connections=10000

# 连接类: 允许连接失败的次数 (防止有人从该主机试图攻击数据库系统).
max_connect_errors=10

# 字符类: 服务端使用的字符集默认为 UTF-8.
character-set-server=utf8

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
default-character-set=utf8


```

## 总结

以上就是关于 SQL运维 Unix下MySQL-5.5.11配置文件示例 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
