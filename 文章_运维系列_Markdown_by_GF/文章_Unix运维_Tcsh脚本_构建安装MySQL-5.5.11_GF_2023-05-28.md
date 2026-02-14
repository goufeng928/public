# 文章_Unix运维_Tcsh脚本_构建安装MySQL-5.5.11_GF_2023-05-28

csh 文件是一种 Unix Shell 脚本文件，其扩展名为 .csh 或 .tcsh。和其他 Unix Shell 脚本文件一样，它可用于执行一系列的命令，包括调用其他脚本或程序等。

通常，csh 文件中包含的命令会按照脚本文件的顺序依次执行。和其他 Shell 脚本文件相比，csh 文件具有更多的功能和优势，其中一个显著的特点是支持 C-Shell 语法。

Tcsh 是 csh 的增强版，并且完全兼容 csh。它不但具有 csh 的全部功能，还具有命令行编辑、拼写校正、可编程字符集、历史纪录、作业控制等功能，以及 C 语言风格的语法结构。

## 使用方法

* 下载源码包:

cmake-2.8.5.tar.gz

mysql-5.5.11.tar.gz
  
* 放于指定路径:

这里 Tcsh Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Tcsh Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/tcsh
# Create By GF 2023-05-28 10:33

# --------------------------------------------------
# Install First: 
# * GCC / Clang

# --------------------------------------------------
# FreeBSD Prepare First: 
# * Create User (Command: adduser / username: mysql / Login group: mysql / Shell: nologin / Home directory: /nonexistent)

# ---------------- Compiler - CMake ----------------
# Need File: cmake-2.8.5.tar.gz
# ----------------- MySQL - 5.5.11 -----------------
# Need File: mysql-5.5.11.tar.gz

# ==================================================
# C11 标准(ISO/IEC 9899:2011): Year 2011 / GCC 4.9 (或更高) / Clang 3.3 (或更高) / Visual Studio 2019 版本 16.8 (或更高)
# ..................................................
# C17 标准(ISO/IEC 9899:2018): Year 2018 / GCC 9.0 (或更高) / Clang 6.0 (或更高) / Visual Studio 2019 版本 16.8 (或更高)
# --------------------------------------------------
set CHECK_C_STD = 11

# ==================================================
# C++11 标准 (ISO/IEC 14882:2011): Year 2011 / GCC 4.8.1 (或更高) / Clang 3.3 (或更高) / Visual Studio 2010 版本 2.0  (或更高)
# ..................................................
# C++17 标准 (ISO/IEC 14882:2017): Year 2017 / GCC 7.0   (或更高) / Clang 5.0 (或更高) / Visual Studio 2017 版本 15.3 (或更高)
# --------------------------------------------------
set CHECK_CPP_STD = 17

# ==================================================
set STORAGE = /home/goufeng

# ########################################################################################################################################################################################################
# ########################################################################################### Compiler - CMake ###########################################################################################

# ====================================================================================================
# =================================== Compile Install CMake-2.8.5 ====================================

if ( ! -d "/opt/cmake-2.8.5" ) then

    set VERIFY = "NULL"
    set STEP_UNZIPPED = 0
    set STEP_CONFIGURED = 0
    set STEP_INSTALLED = 0

    # ----------------------------------------------
    echo "[Confirm] Compile and Install ( cmake-2.8.5 )? (y/n)"
    # ..............................................
    set VERIFY = $<
    # ..............................................
    if ( $VERIFY != "y" ) exit 1

    # ----------------------------------------------
    tar -zxvf $STORAGE/cmake-2.8.5.tar.gz && set STEP_UNZIPPED = 1
    
    # ----------------------------------------------
    cd $STORAGE/cmake-2.8.5 && ./configure --prefix=/opt/cmake-2.8.5 && set STEP_CONFIGURED = 1
    
    # ----------------------------------------------
    make && make install && set STEP_INSTALLED = 1
     
    # ----------------------------------------------
    if ( $STEP_INSTALLED == 1 ) then
        # Skip # ln -sf /opt/cmake-2.8.5/bin/cmake /usr/local/bin/
        echo "Skip the Establishing of CMake Symbolic Link."
    endif

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/cmake-2.8.5
else

    echo "[Caution] Path: ( /opt/cmake-2.8.5 ) Already Exists."
endif

# ########################################################################################################################################################################################################
# ############################################################################################# MySQL-5.5.11 #############################################################################################

# ====================================================================================================
# ==================================== Build Install MySQL-5.5.11 ====================================

# Warning: If it is under 5.7 and includes 5.7, still using utf8, cannot add -DDEFAULT_CHARSET=utf8mb4
# ..............................................
# 在 MySQL 5.7 以前, 使用 SET PASSWORD 语句来修改密码, 从 MySQL 5.7 开始, 推荐使用 ALTER USER 语句来修改密码。
# ..............................................
# MySQL 5.5.11 "my.cnf" Location                    : /opt/mysql-data/conf/my.cnf && Need: chmod 644
# MySQL 5.5.11 Initialize                           : /opt/mysql-5.5.11/scripts/mysql_install_db --basedir=/opt/mysql-5.5.11 --user=mysql
# MySQL 5.5.11 Manually Copying Startup Files       : cp /opt/mysql-5.5.11/support-files/mysql.server [/etc/rc.d | /etc/init.d]
# MySQL 5.5.11 Root Initial Password                : Empty(空), 直接使用 mysql -uroot -p 登录, 提示输入密码, 直接 Enter 键。
# MySQL 5.5.11 View Password Verification VARIABLES : mysql> SHOW VARIABLES LIKE 'validate_password%'; (如果 "my.cnf" 中没有密码相关环境变量的设定, 则无法查询出相关信息)
# MySQL 5.5.11 Password Modification Policy         : mysql> set global validate_password.policy=0; (Optional: 0 or LOW / 1 or MEDIUM / 2 or STRONG | 直接设置为临时生效, 永久生效需要写入 "my.cnf") 
# MySQL 5.5.11 Modify Password Length               : mysql> set global validate_password.length=6; (直接设置为临时生效, 永久生效需要写入 "my.cnf") 
# MySQL 5.5.11 Password Modification                : mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('gf123456');
# MySQL 5.5.11 Refresh Privileges                   : mysql> FLUSH PRIVILEGES; (必要步骤, 否则新密码可能不会立即生效)

if ( ! -d "/opt/mysql-5.5.11" ) then

    set VERIFY = "NULL"
    set STEP_UNZIPPED = 0
    set STEP_CREATED = 0
    set STEP_BUILDED = 0
    set STEP_INSTALLED = 0

    # ----------------------------------------------
    echo "[Confirm] Build and Install ( mysql-5.5.11 )? (y/n)"
    # ..............................................
    set VERIFY = $<
    # ..............................................
    if ( $VERIFY != "y" ) exit 1

    # ----------------------------------------------
    tar -zxvf $STORAGE/mysql-5.5.11.tar.gz && set STEP_UNZIPPED = 1
    
    
    # ----------------------------------------------
    # C++11 Error Handling:
    if ( $CHECK_CPP_STD >= 11 ) then
        # ..........................................
        # * Problem: Cerror: ISO C++11 does not allow access declarations; use using declarations instead
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/log.h 中 351 行的 "MYSQL_LOG" 改为 "using MYSQL_LOG"。
        #            将 mysql-5.5.11/sql/log.h 中 352 行的 "MYSQL_LOG" 改为 "using MYSQL_LOG"。
        # ..........................................
        sed -i ".bak" "351 s/MYSQL_LOG/using MYSQL_LOG/" $STORAGE/mysql-5.5.11/sql/log.h
        sed -i ".bak" "352 s/MYSQL_LOG/using MYSQL_LOG/" $STORAGE/mysql-5.5.11/sql/log.h
        # ..........................................
        # * Problem: error: constant expression evaluates to -1 which cannot be narrowed to type 'unsigned long' [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 10980 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 11087 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 11149 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 11211 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 11216 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/storage/innobase/handler/ha_innodb.cc 中 11226 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            ...............................
        #            将 mysql-5.5.11/plugin/semisync/semisync_master_plugin.cc 中 182 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            将 mysql-5.5.11/plugin/semisync/semisync_master_plugin.cc 中 196 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        #            ...............................
        #            将 mysql-5.5.11/plugin/semisync/semisync_slave_plugin.cc 中 164 行的 "~0L" 改为 "static_cast<unsigned long>(~0L)"。
        # ..........................................
        sed -i ".bak" "10980 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        sed -i ".bak" "11087 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        sed -i ".bak" "11149 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        sed -i ".bak" "11211 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        sed -i ".bak" "11216 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        sed -i ".bak" "11226 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/storage/innobase/handler/ha_innodb.cc
        #            ...............................
        sed -i ".bak" "182 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/plugin/semisync/semisync_master_plugin.cc
        sed -i ".bak" "196 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/plugin/semisync/semisync_master_plugin.cc
        #            ...............................
        sed -i ".bak" "164 s/~0L/static_cast<unsigned long>(~0L)/" $STORAGE/mysql-5.5.11/plugin/semisync/semisync_slave_plugin.cc
        # ..........................................
        # * Problem: error: constant expression evaluates to 18446744073709551615 which cannot be narrowed to type 'longlong' (aka 'long long') [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/mysqld.cc 中 5731 行的 "ULONG_MAX" 改为 "static_cast<longlong>(ULONG_MAX)"。
        #            将 mysql-5.5.11/sql/mysqld.cc 中 5859 行的 "ULONG_MAX" 改为 "static_cast<longlong>(ULONG_MAX)"。
        #            ...............................
        #            将 mysql-5.5.11/client/mysql.cc 中 1553 行的 "ULONG_MAX" 改为 "static_cast<longlong>(ULONG_MAX)"。
        #            将 mysql-5.5.11/client/mysql.cc 中 1557 行的 "ULONG_MAX" 改为 "static_cast<longlong>(ULONG_MAX)"。
        #            ...............................
        #            将 mysql-5.5.11/client/mysqlbinlog.cc 中 1141 行的 "(ulonglong)(~(my_off_t)0)" 改为 "static_cast<longlong>((ulonglong)(~(my_off_t)0))"。
        #            将 mysql-5.5.11/client/mysqlbinlog.cc 中 1142 行的 "(ulonglong)(~(my_off_t)0)" 改为 "static_cast<longlong>((ulonglong)(~(my_off_t)0))"。
        # ..........................................
        sed -i ".bak" "5731 s/ULONG_MAX/static_cast<longlong>(ULONG_MAX)/" $STORAGE/mysql-5.5.11/sql/mysqld.cc
        sed -i ".bak" "5859 s/ULONG_MAX/static_cast<longlong>(ULONG_MAX)/" $STORAGE/mysql-5.5.11/sql/mysqld.cc
        #            ...............................
        sed -i ".bak" "1553 s/ULONG_MAX/static_cast<longlong>(ULONG_MAX)/" $STORAGE/mysql-5.5.11/client/mysql.cc
        sed -i ".bak" "1557 s/ULONG_MAX/static_cast<longlong>(ULONG_MAX)/" $STORAGE/mysql-5.5.11/client/mysql.cc
        #            ...............................
        sed -i ".bak" "1141 s/(ulonglong)(~(my_off_t)0)/static_cast<longlong>((ulonglong)(~(my_off_t)0))/" $STORAGE/mysql-5.5.11/client/mysqlbinlog.cc
        sed -i ".bak" "1142 s/(ulonglong)(~(my_off_t)0)/static_cast<longlong>((ulonglong)(~(my_off_t)0))/" $STORAGE/mysql-5.5.11/client/mysqlbinlog.cc
        # ..........................................
        # * Problem: error: cannot initialize a parameter of type 'HA_CREATE_INFO *' (aka 'st_ha_create_information *') with an rvalue of type 'ulonglong' (aka 'unsigned long long')
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/sql_partition.cc 中 283 行的 "(ulonglong)0" 改为 "(HA_CREATE_INFO *)0"。
        # ..........................................
        sed -i ".bak" "283 s/(ulonglong)0/(HA_CREATE_INFO *)0/" $STORAGE/mysql-5.5.11/sql/sql_partition.cc
        # ..........................................
        # * Problem: error: non-constant-expression cannot be narrowed from type 'int' to 'size_t' (aka 'unsigned long') in initializer list [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/sql_plugin.cc 中 682 行的 "len" 改为 "static_cast<size_t>(len)"。
        # ..........................................
        sed -i ".bak" "682 s/len/static_cast<size_t>(len)/" $STORAGE/mysql-5.5.11/sql/sql_plugin.cc
        # ..........................................
        # * Problem: error: non-constant-expression cannot be narrowed from type 'size_t' (aka 'unsigned long') to 'int' in initializer list [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/sql_trigger.cc 中 193 行的 "my_offsetof(class Table_triggers_list, definitions_list)"      改为 "static_cast<int>(my_offsetof(class Table_triggers_list, definitions_list))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 198 行的 "my_offsetof(class Table_triggers_list, definition_modes_list)" 改为 "static_cast<int>(my_offsetof(class Table_triggers_list, definition_modes_list))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 203 行的 "my_offsetof(class Table_triggers_list, definers_list)"         改为 "static_cast<int>(my_offsetof(class Table_triggers_list, definers_list))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 208 行的 "my_offsetof(class Table_triggers_list, client_cs_names)"       改为 "static_cast<int>(my_offsetof(class Table_triggers_list, client_cs_names))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 213 行的 "my_offsetof(class Table_triggers_list, connection_cl_names)"   改为 "static_cast<int>(my_offsetof(class Table_triggers_list, connection_cl_names))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 218 行的 "my_offsetof(class Table_triggers_list, db_cl_names)"           改为 "static_cast<int>(my_offsetof(class Table_triggers_list, db_cl_names))"。
        #            将 mysql-5.5.11/sql/sql_trigger.cc 中 227 行的 "my_offsetof(class Table_triggers_list, definition_modes_list)" 改为 "static_cast<int>(my_offsetof(class Table_triggers_list, definition_modes_list))"。
        #            ...............................
        #            将 mysql-5.5.11/sql/sql_view.cc 中 726 行的 "my_offsetof(TABLE_LIST, select_stmt)"             改为 "static_cast<int>(my_offsetof(TABLE_LIST, select_stmt))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 729 行的 "my_offsetof(TABLE_LIST, md5)"                     改为 "static_cast<int>(my_offsetof(TABLE_LIST, md5))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 732 行的 "my_offsetof(TABLE_LIST, updatable_view)"          改为 "static_cast<int>(my_offsetof(TABLE_LIST, updatable_view))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 735 行的 "my_offsetof(TABLE_LIST, algorithm)"               改为 "static_cast<int>(my_offsetof(TABLE_LIST, algorithm))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 738 行的 "my_offsetof(TABLE_LIST, definer.user)"            改为 "static_cast<int>(my_offsetof(TABLE_LIST, definer.user))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 741 行的 "my_offsetof(TABLE_LIST, definer.host)"            改为 "static_cast<int>(my_offsetof(TABLE_LIST, definer.host))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 744 行的 "my_offsetof(TABLE_LIST, view_suid)"               改为 "static_cast<int>(my_offsetof(TABLE_LIST, view_suid))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 747 行的 "my_offsetof(TABLE_LIST, with_check)"              改为 "static_cast<int>(my_offsetof(TABLE_LIST, with_check))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 750 行的 "my_offsetof(TABLE_LIST, timestamp)"               改为 "static_cast<int>(my_offsetof(TABLE_LIST, timestamp))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 753 行的 "my_offsetof(TABLE_LIST, file_version)"            改为 "static_cast<int>(my_offsetof(TABLE_LIST, file_version))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 756 行的 "my_offsetof(TABLE_LIST, source)"                  改为 "static_cast<int>(my_offsetof(TABLE_LIST, source))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 759 行的 "my_offsetof(TABLE_LIST, view_client_cs_name)"     改为 "static_cast<int>(my_offsetof(TABLE_LIST, view_client_cs_name))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 762 行的 "my_offsetof(TABLE_LIST, view_connection_cl_name)" 改为 "static_cast<int>(my_offsetof(TABLE_LIST, view_connection_cl_name))"。
        #            将 mysql-5.5.11/sql/sql_view.cc 中 765 行的 "my_offsetof(TABLE_LIST, view_body_utf8)"          改为 "static_cast<int>(my_offsetof(TABLE_LIST, view_body_utf8))"。
        # ..........................................
        sed -i ".bak" "193 s/my_offsetof(class Table_triggers_list, definitions_list)/static_cast<int>(my_offsetof(class Table_triggers_list, definitions_list))/"           $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "198 s/my_offsetof(class Table_triggers_list, definition_modes_list)/static_cast<int>(my_offsetof(class Table_triggers_list, definition_modes_list))/" $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "203 s/my_offsetof(class Table_triggers_list, definers_list)/static_cast<int>(my_offsetof(class Table_triggers_list, definers_list))/"                 $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "208 s/my_offsetof(class Table_triggers_list, client_cs_names)/static_cast<int>(my_offsetof(class Table_triggers_list, client_cs_names))/"             $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "213 s/my_offsetof(class Table_triggers_list, connection_cl_names)/static_cast<int>(my_offsetof(class Table_triggers_list, connection_cl_names))/"     $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "218 s/my_offsetof(class Table_triggers_list, db_cl_names)/static_cast<int>(my_offsetof(class Table_triggers_list, db_cl_names))/"                     $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        sed -i ".bak" "227 s/my_offsetof(class Table_triggers_list, definition_modes_list)/static_cast<int>(my_offsetof(class Table_triggers_list, definition_modes_list))/" $STORAGE/mysql-5.5.11/sql/sql_trigger.cc
        #            ...............................
        sed -i ".bak" "726 s/my_offsetof(TABLE_LIST, select_stmt)/static_cast<int>(my_offsetof(TABLE_LIST, select_stmt))/"                         $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "729 s/my_offsetof(TABLE_LIST, md5)/static_cast<int>(my_offsetof(TABLE_LIST, md5))/"                                         $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "732 s/my_offsetof(TABLE_LIST, updatable_view)/static_cast<int>(my_offsetof(TABLE_LIST, updatable_view))/"                   $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "735 s/my_offsetof(TABLE_LIST, algorithm)/static_cast<int>(my_offsetof(TABLE_LIST, algorithm))/"                             $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "738 s/my_offsetof(TABLE_LIST, definer.user)/static_cast<int>(my_offsetof(TABLE_LIST, definer.user))/"                       $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "741 s/my_offsetof(TABLE_LIST, definer.host)/static_cast<int>(my_offsetof(TABLE_LIST, definer.host))/"                       $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "744 s/my_offsetof(TABLE_LIST, view_suid)/static_cast<int>(my_offsetof(TABLE_LIST, view_suid))/"                             $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "747 s/my_offsetof(TABLE_LIST, with_check)/static_cast<int>(my_offsetof(TABLE_LIST, with_check))/"                           $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "750 s/my_offsetof(TABLE_LIST, timestamp)/static_cast<int>(my_offsetof(TABLE_LIST, timestamp))/"                             $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "753 s/my_offsetof(TABLE_LIST, file_version)/static_cast<int>(my_offsetof(TABLE_LIST, file_version))/"                       $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "756 s/my_offsetof(TABLE_LIST, source)/static_cast<int>(my_offsetof(TABLE_LIST, source))/"                                   $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "759 s/my_offsetof(TABLE_LIST, view_client_cs_name)/static_cast<int>(my_offsetof(TABLE_LIST, view_client_cs_name))/"         $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "762 s/my_offsetof(TABLE_LIST, view_connection_cl_name)/static_cast<int>(my_offsetof(TABLE_LIST, view_connection_cl_name))/" $STORAGE/mysql-5.5.11/sql/sql_view.cc
        sed -i ".bak" "765 s/my_offsetof(TABLE_LIST, view_body_utf8)/static_cast<int>(my_offsetof(TABLE_LIST, view_body_utf8))/"                   $STORAGE/mysql-5.5.11/sql/sql_view.cc
        # ..........................................
        # * Problem: error: non-constant-expression cannot be narrowed from type 'unsigned int' to 'int' in initializer list [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/sql/sql_profile.cc 中  92 行的 "profile_options & PROFILE_CPU"         改为 "static_cast<int>(profile_options & PROFILE_CPU)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  93 行的 "profile_options & PROFILE_CPU"         改为 "static_cast<int>(profile_options & PROFILE_CPU)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  94 行的 "profile_options & PROFILE_CONTEXT"     改为 "static_cast<int>(profile_options & PROFILE_CONTEXT)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  95 行的 "profile_options & PROFILE_CONTEXT"     改为 "static_cast<int>(profile_options & PROFILE_CONTEXT)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  96 行的 "profile_options & PROFILE_BLOCK_IO"    改为 "static_cast<int>(profile_options & PROFILE_BLOCK_IO)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  97 行的 "profile_options & PROFILE_BLOCK_IO"    改为 "static_cast<int>(profile_options & PROFILE_BLOCK_IO)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  98 行的 "profile_options & PROFILE_IPC"         改为 "static_cast<int>(profile_options & PROFILE_IPC)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中  99 行的 "profile_options & PROFILE_IPC"         改为 "static_cast<int>(profile_options & PROFILE_IPC)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 100 行的 "profile_options & PROFILE_PAGE_FAULTS" 改为 "static_cast<int>(profile_options & PROFILE_PAGE_FAULTS)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 101 行的 "profile_options & PROFILE_PAGE_FAULTS" 改为 "static_cast<int>(profile_options & PROFILE_PAGE_FAULTS)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 102 行的 "profile_options & PROFILE_SWAPS"       改为 "static_cast<int>(profile_options & PROFILE_SWAPS)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 103 行的 "profile_options & PROFILE_SOURCE"      改为 "static_cast<int>(profile_options & PROFILE_SOURCE)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 104 行的 "profile_options & PROFILE_SOURCE"      改为 "static_cast<int>(profile_options & PROFILE_SOURCE)"。
        #            将 mysql-5.5.11/sql/sql_profile.cc 中 105 行的 "profile_options & PROFILE_SOURCE"      改为 "static_cast<int>(profile_options & PROFILE_SOURCE)"。
        # ..........................................
        sed -i ".bak" "92 s/profile_options \& PROFILE_CPU/static_cast<int>(profile_options \& PROFILE_CPU)/"                  $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "93 s/profile_options \& PROFILE_CPU/static_cast<int>(profile_options \& PROFILE_CPU)/"                  $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "94 s/profile_options \& PROFILE_CONTEXT/static_cast<int>(profile_options \& PROFILE_CONTEXT)/"          $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "95 s/profile_options \& PROFILE_CONTEXT/static_cast<int>(profile_options \& PROFILE_CONTEXT)/"          $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "96 s/profile_options \& PROFILE_BLOCK_IO/static_cast<int>(profile_options \& PROFILE_BLOCK_IO)/"        $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "97 s/profile_options \& PROFILE_BLOCK_IO/static_cast<int>(profile_options \& PROFILE_BLOCK_IO)/"        $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "98 s/profile_options \& PROFILE_IPC/static_cast<int>(profile_options \& PROFILE_IPC)/"                  $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "99 s/profile_options \& PROFILE_IPC/static_cast<int>(profile_options \& PROFILE_IPC)/"                  $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "100 s/profile_options \& PROFILE_PAGE_FAULTS/static_cast<int>(profile_options \& PROFILE_PAGE_FAULTS)/" $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "101 s/profile_options \& PROFILE_PAGE_FAULTS/static_cast<int>(profile_options \& PROFILE_PAGE_FAULTS)/" $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "102 s/profile_options \& PROFILE_SWAPS/static_cast<int>(profile_options \& PROFILE_SWAPS)/"             $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "103 s/profile_options \& PROFILE_SOURCE/static_cast<int>(profile_options \& PROFILE_SOURCE)/"           $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "104 s/profile_options \& PROFILE_SOURCE/static_cast<int>(profile_options \& PROFILE_SOURCE)/"           $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        sed -i ".bak" "105 s/profile_options \& PROFILE_SOURCE/static_cast<int>(profile_options \& PROFILE_SOURCE)/"           $STORAGE/mysql-5.5.11/sql/sql_profile.cc
        # ..........................................
        # * Problem: error: constant expression evaluates to 239 which cannot be narrowed to type 'char' [-Wc++11-narrowing]
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/plugin/semisync/semisync.cc 中 30 行的 "ReplSemiSyncBase::kPacketMagicNum" 改为 "static_cast<char>(ReplSemiSyncBase::kPacketMagicNum)"。
        # ..........................................
        sed -i ".bak" "30 s/ReplSemiSyncBase::kPacketMagicNum/static_cast<char>(ReplSemiSyncBase::kPacketMagicNum)/" $STORAGE/mysql-5.5.11/plugin/semisync/semisync.cc
        # ..........................................
        # * Problem: error: incompatible integer to pointer conversion assigning to 'char *' from 'char'
        #            ...............................
        #   - Solve: 将 mysql-5.5.11/client/mysql.cc 中 2627 行的 "field_names[i][num_fields*2]= '\0';" 改为 "field_names[i][num_fields*2]= 0;"。
        # ..........................................
        sed -r -i ".bak" "2627 s/field_names\[i\]\[num_fields\*2\]= .*;/field_names\[i\]\[num_fields\*2\]= 0;/" $STORAGE/mysql-5.5.11/client/mysql.cc
    endif
    
    # ----------------------------------------------
    mkdir $STORAGE/mysql-5.5.11/my-build && set STEP_CREATED = 1
    
    # ----------------------------------------------
    # Create The Required Directory For MySQL.
    if ( ! -d "/opt/mysql5-data" ) then
        mkdir -p /opt/mysql5-data/run
        mkdir -p /opt/mysql5-data/data
        mkdir -p /opt/mysql5-data/tmp
        mkdir -p /opt/mysql5-data/conf
        mkdir -p /opt/mysql5-data/log/bin_log
        mkdir -p /opt/mysql5-data/log/error_log
        mkdir -p /opt/mysql5-data/log/query_log
        mkdir -p /opt/mysql5-data/log/general_log
        mkdir -p /opt/mysql5-data/log/innodb_ts
        mkdir -p /opt/mysql5-data/log/undo_space
        mkdir -p /opt/mysql5-data/log/innodb_log
    endif
    
    # ----------------------------------------------
    # Granting mysql5-data Permissions To MySQL Users.
    chown -R mysql:mysql /opt/mysql5-data
    
    # ----------------------------------------------
    # *  Option: -DCMAKE_BUILD_TYPE=Release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
    #                                        指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
    # ..............................................
    cd $STORAGE/mysql-5.5.11/my-build && /opt/cmake-2.8.5/bin/cmake ../ -G "Unix Makefiles" \
                                                                        -DCMAKE_INSTALL_PREFIX=/opt/mysql-5.5.11 \
                                                                        -DMYSQL_DATADIR=/opt/mysql5-data/data \
                                                                        -DMYSQL_UNIX_ADDR=/opt/mysql5-data/run/mysql.sock \
                                                                        -DSYSCONFDIR=/opt/mysql5-data/conf \
                                                                        -DMYSQL_TCP_PORT=3306 \
                                                                        -DCMAKE_BUILD_TYPE=Release \
                                                                        -DCOMPILATION_COMMENT="GF Self Use Edition" \
                                                                        -DWITH_INNOBASE_STORAGE_ENGINE=1 \
                                                                        -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
                                                                        -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
                                                                        -DWITH_PERFSCHEMA_STORAGE_ENGINE=1 \
                                                                        -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
                                                                        -DDEFAULT_CHARSET=utf8 \
                                                                        -DDEFAULT_COLLATION=utf8_general_ci \
                                                                        -DWITH_EXTRA_CHARSETS=ALL && \
                                                                        STEP_BUILDED=1
    
    # ----------------------------------------------
    make && make install && set STEP_INSTALLED = 1
    
    # ----------------------------------------------
    if ( $STEP_INSTALLED == 1 ) then
        # Default None .pc (Pkg-Config) File.
        # ..........................................
        ln -svf /opt/mysql-5.5.11/bin/* /usr/local/bin/
        # ..........................................
        # Skip # rsync -av /opt/mysql-5.5.11/include/ /usr/local/include/
        # ..........................................
        # Skip # rsync -av /opt/mysql-5.5.11/lib/ /usr/local/lib/
    endif
    
    # ----------------------------------------------
    # Copy or Create MySQL Configure File: "my.cnf".
    # Skip # cp /opt/mysql-5.5.11/support-files/my-medium.cnf /opt/mysql5-data/conf/my.cnf
    # ..............................................
    if ( $STEP_INSTALLED == 1 && ! -f "/opt/mysql5-data/conf/my.cnf" ) then
        touch /opt/mysql5-data/conf/my.cnf
        # ..........................................
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "[mysqld]"                              >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Database Server"              >> /opt/mysql5-data/conf/my.cnf
        echo "port=3306"                             >> /opt/mysql5-data/conf/my.cnf
        echo "user=mysql"                            >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Database Directory"           >> /opt/mysql5-data/conf/my.cnf
        echo "basedir=/opt/mysql-5.5.11"             >> /opt/mysql5-data/conf/my.cnf
        echo "datadir=/opt/mysql5-data/data"         >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Database Storage"             >> /opt/mysql5-data/conf/my.cnf
        echo "default-storage-engine=INNODB"         >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Database Connection"          >> /opt/mysql5-data/conf/my.cnf
        echo "max_connections=10000"                 >> /opt/mysql5-data/conf/my.cnf
        echo "max_connect_errors=10"                 >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Database Character"           >> /opt/mysql5-data/conf/my.cnf
        echo "character-set-server=utf8mb4"          >> /opt/mysql5-data/conf/my.cnf
        echo "lower_case_table_names=1"              >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "[mysql]"                               >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: MySQL Command Line Character" >> /opt/mysql5-data/conf/my.cnf
        echo "default-character-set=utf8"            >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "[client]"                              >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Client Connection"            >> /opt/mysql5-data/conf/my.cnf
        echo "port=3306"                             >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
        echo "# Class: Client Character"             >> /opt/mysql5-data/conf/my.cnf
        echo "default-character-set=utf8"            >> /opt/mysql5-data/conf/my.cnf
        echo ""                                      >> /opt/mysql5-data/conf/my.cnf
    endif
    
    # ----------------------------------------------
    # Copy MySQL Startup File: "mysqld".
    if   ( $STEP_INSTALLED == 1 && -d "/etc/rc.d" ) then
        cp -v /opt/mysql-5.5.11/support-files/mysql.server /etc/rc.d/mysqld
        # ..........................................
        sed -r -i ".bak" "s#^basedir\=.*#basedir\=/opt/mysql-5.5.11#" /etc/rc.d/mysqld
        sed -r -i ".bak" "s#^datadir\=.*#datadir\=/opt/mysql5-data/data#" /etc/rc.d/mysqld
        # ..........................................
        chmod 700 /etc/rc.d/mysqld
    # ..............................................
    else if ( $STEP_INSTALLED == 1 && -d "/etc/init.d" ) then
        cp -v /opt/mysql-5.5.11/support-files/mysql.server /etc/init.d/mysqld
        # ..........................................
        sed -r -i "s#^basedir\=.*#basedir\=/opt/mysql-5.5.11#" /etc/init.d/mysqld
        sed -r -i "s#^datadir\=.*#datadir\=/opt/mysql5-data/data#" /etc/init.d/mysqld
        # ..........................................
        chmod 700 /etc/init.d/mysqld
    endif

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/mysql-5.5.11
else

    echo "[Caution] Path: ( /opt/mysql-5.5.11 ) Already Exists."
endif

# ########################################################################################################################################################################################################
# ################################################################################################## Ends ################################################################################################

```

## 总结

以上就是关于 Unix运维 Tcsh脚本 构建安装MySQL-5.5.11 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
