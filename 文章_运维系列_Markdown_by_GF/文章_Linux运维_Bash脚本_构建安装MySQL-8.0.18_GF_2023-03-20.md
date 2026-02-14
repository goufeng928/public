# 文章_Linux运维_Bash脚本_构建安装MySQL-8.0.18_GF_2023-03-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

libunwind-1.6.2.tar.gz

openssl-1.1.1g.tar.gz

ncurses-6.4.tar.gz

mysql-boost-8.0.18.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-20 10:31

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * GCC >= 5.3
# * CMake >= 3.8.0

# ------------------- Dependency -------------------
# Need File: zlib-1.2.13.tar.gz
# Need File: libunwind-1.6.2.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# Need File: ncurses-6.4.tar.gz
# -------- MySQL - 8.0.18 (Contains Boost) ---------
# Need File: mysql-boost-8.0.18.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) zlib-1.2.13
# ##################################################
function Compile_Install_zlib_1_2_13() {

    if [[ ! -f "/usr/include/zlib.h" && ! -f "/usr/local/include/zlib.h" && ! -d "/opt/zlib-1.2.13" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( zlib-1.2.13 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/zlib-1.2.13.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/zlib-1.2.13 && ./configure --prefix=/opt/zlib-1.2.13 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/zlib-1.2.13/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/zlib-1.2.13/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/zlib-1.2.13/lib/pkgconfig/zlib.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/zlib-1.2.13 && return 0
    else
    
        echo "[Caution] Program: ( /usr/include/zlib.h or /usr/local/include/zlib.h or /opt/zlib-1.2.13 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libunwind-1.6.2
# ##################################################
function Compile_Install_libunwind_1_6_2() {

    if [[ ! -d "/opt/libunwind-1.6.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libunwind-1.6.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libunwind-1.6.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libunwind-1.6.2 && ./configure --prefix=/opt/libunwind-1.6.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libunwind-1.6.2/bin/xmlwf /usr/local/bin/
            # ......................................
            rsync -av /opt/libunwind-1.6.2/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libunwind-1.6.2/lib/ /usr/local/lib/
            # ......................................
            cp -vf /opt/libunwind-1.6.2/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Ubuntu Linux Proprietary Command.
        ldconfig
        
        # ------------------------------------------
        # FreeBSD Unix Proprietary Command.
        /etc/rc.d/ldconfig restart

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libunwind-1.6.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libunwind-1.6.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) openssl-1.1.1g
# ##################################################
function Compile_Install_openssl_1_1_1g() {

    if [[ ! -d "/opt/openssl-1.1.1g" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( openssl-1.1.1g )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/openssl-1.1.1g.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/openssl-1.1.1g && ./config --prefix=/opt/openssl-1.1.1g \
                                               --openssldir=/opt/openssl-1.1.1g/ssl \
                                               --shared \
                                               zlib && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # 注意: 避免与系统原有的 "openssl" 发生冲突, 未将 "openssl-1.1.1g" 的二进制 bin 文件发送到 PATH 路径。
            # Caution: To avoid conflicts with the original "openssl" in the system, the binary file of "openssl-1.1.1g" was not sent to the PATH path.
            # ......................................
            # Skip # ln -sf /opt/openssl-1.1.1g/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/openssl-1.1.1g/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/openssl-1.1.1g/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/openssl-1.1.1g && return 0
    else
    
        echo "[Caution] Path: ( /opt/openssl-1.1.1g ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) ncurses-6.4
# ##################################################
function Compile_Install_ncurses_6_4() {

    # ncurses (new curses) 是一套编程库，它提供了一系列的函数以便使用者调用它们去生成基于文本的用户界面。
    # ncurses 名字中的n意味着 "new", 因为它是 curses 的自由软件版本。由于 AT&T "臭名昭著" 的版权政策, 人们不得不在后来用 ncurses 去代替它。
    # ncurses 是 GNU 计划的一部分, 但它却是少数几个不使用 GNU GPL 或 LGPL 授权的 GNU 软件之一。
    # 其实我们对 ncurses 本身并不陌生，以下几款大名鼎鼎的软件都用到过 ncurses:
    #     * vim
    #     * emacs
    #     * lynx
    #     * screen
    # 作为嵌入式驱动开发工程师, Linux 内核的配置也离不开 ncurses 库的使用。

    if [[ ! -d "/opt/ncurses-6.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( ncurses-6.4 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/ncurses-6.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/ncurses-6.4 && ./configure --prefix=/opt/ncurses-6.4 \
                                               --enable-pc-files \
                                               --enable-shared \
                                               --with-libtool && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/terminfo" ]]; then mkdir /usr/local/lib/terminfo; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/ncurses-6.4/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/ncurses-6.4/include/ /usr/local/include/
            # ......................................
            cp -vf /opt/ncurses-6.4/include/ncurses/*.h /usr/local/include/
            # ......................................
            rsync -av /opt/ncurses-6.4/lib/ /usr/local/lib/
            # ......................................
            rsync -av /opt/ncurses-6.4/share/terminfo/ /usr/local/lib/terminfo/
            # ......................................
            cp -vf /opt/ncurses-6.4/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Ubuntu Linux Proprietary Command.
        ldconfig
        
        # ------------------------------------------
        # FreeBSD Unix Proprietary Command.
        /etc/rc.d/ldconfig restart
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ncurses-6.4 && return 0
    else
        echo "[Caution] Path: ( /opt/ncurses-6.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################# MySQL - 8.0.18 (Contains Boost) ##################################

# Function: 构建安装(Build Install) MySQL-8.0.18 (Contains Boost)
# ##################################################
function Build_Install_MySQL_8_0_18_Contains_Boost() {

    # Warning: Need GCC 5.3 or newer (GCC > 5.3).
    # ..............................................
    # Warning: If it is under 5.7 and includes 5.7, still using utf8, cannot add -DDEFAULT_CHARSET=utf8mb4
    # ..............................................
    # MySQL 8.0.18 "my.cnf" Location                    : /opt/mysql8-data/conf/my.cnf (Need: chmod 644)
    # MySQL 8.0.18 Initialize                           : mysqld --defaults-file=/opt/mysql8-data/conf/my.cnf --initialize --user=mysql
    # MySQL 8.0.18 Temporary Password                   : cat /opt/mysql8-data/log/error_log/mysql-error.log | grep password
    # Log in to MySQL 8.0.18                            : mysql -uroot -pujbbqC?A+38g
    # MySQL 8.0.18 Password Modification                : mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '12345678';

    if [[ ! -d "/opt/mysql-8.0.18" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
        local GROUP_NAME="None"
        local USER_NAME="None"
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( mysql-8.0.18 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/mysql-boost-8.0.18.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Clang-11 Error Handling:
        # ..........................................
        # * Problem: /home/goufeng/mysql-8.0.18/plugin/group_replication/src/plugin.cc:548:35: error: cannot initialize return object of type 'bool' with an rvalue of type 'nullptr_t'
        #                                              NULL, NULL, NULL, NULL, NULL, NULL, NULL,
        #                                              ^~~~
        #            /home/goufeng/mysql-8.0.18/plugin/group_replication/src/plugin.cc:549:41: error: cannot initialize return object of type 'bool' with an rvalue of type 'nullptr_t'
        #                                              NULL, NULL, DEFAULT_THREAD_PRIORITY, 1, false,
        #                                                    ^~~~
        #   - Solve: Just replace NULL with false (只需将 NULL 替换为 false)。
        # ..........................................
        # Skip # sed -i ".bak" "548 s/NULL, NULL, NULL, NULL, NULL, NULL, NULL,/false, NULL, NULL, NULL, NULL, NULL, NULL,/" $STORAGE/mysql-8.0.18/plugin/group_replication/src/plugin.cc
        # Skip # sed -i ".bak" "549 s/NULL, NULL, DEFAULT_THREAD_PRIORITY, 1, false,/NULL, false, DEFAULT_THREAD_PRIORITY, 1, false,/" $STORAGE/mysql-8.0.18/plugin/group_replication/src/plugin.cc
        # ..........................................
        # * Problem: /home/goufeng/mysql-8.0.18/plugin/group_replication/src/recovery_state_transfer.cc:605:52: error: cannot initialize return object of type 'bool' with an rvalue of type 'nullptr_t'
        #                  const_cast<char *>("<NULL>"), 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
        #                                                               ^~~~
        #            /home/goufeng/mysql-8.0.18/plugin/group_replication/src/recovery_state_transfer.cc:606:25: error: cannot initialize return object of type 'bool' with an rvalue of type 'nullptr_t'
        #                  NULL, NULL, NULL, NULL, DEFAULT_THREAD_PRIORITY, 1, false, NULL, false,
        #                                    ^~~~
        #   - Solve: Just replace NULL with false (只需将 NULL 替换为 false)。
        # ..........................................
        # Skip # sed -i ".bak" "605 s/0, NULL, NULL, NULL, NULL, NULL, NULL, NULL,/0, NULL, NULL, false, NULL, NULL, NULL, NULL,/" $STORAGE/mysql-8.0.18/plugin/group_replication/src/recovery_state_transfer.cc
        # Skip # sed -i ".bak" "606 s/NULL, NULL, NULL, NULL, DEFAULT_THREAD_PRIORITY,/NULL, NULL, NULL, false, DEFAULT_THREAD_PRIORITY,/" $STORAGE/mysql-8.0.18/plugin/group_replication/src/recovery_state_transfer.cc
        
        # ------------------------------------------
        mkdir $STORAGE/mysql-8.0.18/build && STEP_CREATED=1
        
        # ------------------------------------------
        # Create Group and User For MySQL.
        GROUP_NAME=`cat /etc/group | grep -o "mysql"`
        # ..........................................
        if [[ -z "$GROUP_NAME" ]]; then addgroup --system mysql; fi
        # ..........................................
        USER_NAME=`cat /etc/passwd | grep -o "mysql"`
        # ..........................................
        # The difference between "adduser" and "useradd":
        #     "adduser" is not a standard Linux command, it is essentially a Perl script.
        #     Calling the "useradd" command in the background makes this advanced utility more efficient when creating users in Linux.
        #     "useradd" provides options for creating a home directory, setting passwords, and other parameters.
        # ..........................................
        # useradd Option Description:
        #     -c: Add note text and save it in the note column of passwd.
        #     -d: Specify the user's home directory when logging in, replace the system default value of /home/<username>.
        #     -g: Specify the group to which the user belongs. The value can be either a group name or a GID. The user group must already exist, with a default value of 100, which is users.
        #     -s: Specify the shell that the user will use after logging in. The default value is /bin/bash.
        #     -u: Specify the user ID number. This value must be unique within the system. 0~499 is reserved for the system user account by default, so the value must be greater than 499.
        #     -m: Automatically establish the user's login directory.
        #     -M: Do not automatically establish a user's login directory
        # ..........................................
        if [[ -z "$USER_NAME" ]]; then useradd mysql -s /sbin/nologin -g mysql -M; fi
        
        # ------------------------------------------
        # Create The Required Directory For MySQL.
        if [[ ! -d "/opt/mysql8-data" ]]; then
            mkdir -p /opt/mysql8-data/run
            mkdir -p /opt/mysql8-data/data
            mkdir -p /opt/mysql8-data/tmp
            mkdir -p /opt/mysql8-data/conf
            mkdir -p /opt/mysql8-data/log/bin_log
            mkdir -p /opt/mysql8-data/log/error_log
            mkdir -p /opt/mysql8-data/log/query_log
            mkdir -p /opt/mysql8-data/log/general_log
            mkdir -p /opt/mysql8-data/log/innodb_ts
            mkdir -p /opt/mysql8-data/log/undo_space
            mkdir -p /opt/mysql8-data/log/innodb_log
        fi
        
        # ------------------------------------------
        # Granting mysql8-data Permissions To MySQL Users.
        chown -R mysql:mysql /opt/mysql8-data
        
        # ------------------------------------------
        # *  Option: -DCMAKE_BUILD_TYPE=Release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                        指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # ..........................................
        # *  Option: -DWITH_BOOST=boost: Specify the path to Boost, such as "-DWITH_BOOST=/home/[UserName]/boost/boost_1_70_0",  If installing using the mysql boost x.x.x integration package, then "-DWITH_BOOST=boost" or "-DWITH_BOOST=../boost".
        #                                指定 Boost 的路径, 如: "-DWITH_BOOST=/home/[UserName]/boost/boost_1_70_0", 若使用 mysql-boost-x.x.x 集成包安装则 "-DWITH_BOOST=boost" 或者 "-DWITH_BOOST=../boost"。
        # ..........................................
        cd $STORAGE/mysql-8.0.18/build && cmake ../ -G "Unix Makefiles" \
                                                    -DCMAKE_INSTALL_PREFIX=/opt/mysql-8.0.18 \
                                                    -DWITH_BOOST=../boost \
                                                    -DMYSQL_DATADIR=/opt/mysql8-data/data \
                                                    -DMYSQL_UNIX_ADDR=/opt/mysql8-data/run/mysql.sock \
                                                    -DSYSCONFDIR=/opt/mysql8-data/conf \
                                                    -DCMAKE_C_COMPILER=/usr/bin/gcc \
                                                    -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
                                                    -DMYSQL_TCP_PORT=3306 \
                                                    -DCMAKE_BUILD_TYPE=Release \
                                                    -DCOMPILATION_COMMENT="GF Self Use Edition" \
                                                    -DDEFAULT_CHARSET=utf8mb4 \
                                                    -DDEFAULT_COLLATION=utf8mb4_general_ci \
                                                    -DEXTRA_CHARSETS=all \
                                                    -DENABLED_LOCAL_INFILE=ON \
                                                    -DWITH_INNODB_MEMCACHED=ON \
                                                    -DWITH_INNOBASE_STORAGE_ENGINE=1 \
                                                    -DWITH_FEDERATED_STORAGE_ENGINE=1 \
                                                    -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
                                                    -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
                                                    -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
                                                    -DWITH_PERFSCHEMA_STORAGE_ENGINE=1 \
                                                    -DFORCE_INSOURCE_BUILD=1 \
                                                    -DWITH_READLINE=1 \
                                                    -DWITH_SSL=system \
                                                    -DWITH_ZLIB=system && \
                                                    STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -svf /opt/mysql-8.0.18/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/mysql-8.0.18/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/mysql-8.0.18/lib/ /usr/local/lib/
            # ......................................
            cp -vf /opt/mysql-8.0.18/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Create MySQL Configure File: "my.cnf".
        if [[ $STEP_INSTALLED == 1 && ! -f "/opt/mysql8-data/conf/my.cnf" ]]; then
            touch /opt/mysql8-data/conf/my.cnf
            # ......................................
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "[mysqld]"                              >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Database Server"              >> /opt/mysql8-data/conf/my.cnf
            echo "port=3306"                             >> /opt/mysql8-data/conf/my.cnf
            echo "user=mysql"                            >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Database Directory"           >> /opt/mysql8-data/conf/my.cnf
            echo "basedir=/opt/mysql-8.0.18"             >> /opt/mysql8-data/conf/my.cnf
            echo "datadir=/opt/mysql8-data/data"         >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Database Storage"             >> /opt/mysql8-data/conf/my.cnf
            echo "default-storage-engine=INNODB"         >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Database Connection"          >> /opt/mysql8-data/conf/my.cnf
            echo "max_connections=10000"                 >> /opt/mysql8-data/conf/my.cnf
            echo "max_connect_errors=10"                 >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Database Character"           >> /opt/mysql8-data/conf/my.cnf
            echo "character-set-server=utf8mb4"          >> /opt/mysql8-data/conf/my.cnf
            echo "lower_case_table_names=1"              >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "[mysql]"                               >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: MySQL Command Line Character" >> /opt/mysql8-data/conf/my.cnf
            echo "default-character-set=utf8mb4"         >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "[client]"                              >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Client Connection"            >> /opt/mysql8-data/conf/my.cnf
            echo "port=3306"                             >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
            echo "# Class: Client Character"             >> /opt/mysql8-data/conf/my.cnf
            echo "default-character-set=utf8mb4"         >> /opt/mysql8-data/conf/my.cnf
            echo ""                                      >> /opt/mysql8-data/conf/my.cnf
        fi
        
        # ------------------------------------------
        # Copy MySQL Startup File: "mysqld".
        if   [[ $STEP_INSTALLED == 1 && -d "/etc/rc.d" ]]; then
            cp -v /opt/mysql-8.0.18/support-files/mysql.server /etc/rc.d/mysqld
            # ......................................
            sed -r -i ".bak" "s#^basedir\=.*#basedir\=/opt/mysql-8.0.18#" /etc/rc.d/mysqld
            sed -r -i ".bak" "s#^datadir\=.*#datadir\=/opt/mysql8-data/data#" /etc/rc.d/mysqld
            # ......................................
            chmod 700 /etc/rc.d/mysqld
        # ..........................................
        elif [[ $STEP_INSTALLED == 1 && -d "/etc/init.d" ]]; then
            cp -v /opt/mysql-8.0.18/support-files/mysql.server /etc/init.d/mysqld
            # ......................................
            sed -r -i "s#^basedir\=.*#basedir\=/opt/mysql-8.0.18#" /etc/init.d/mysqld
            sed -r -i "s#^datadir\=.*#datadir\=/opt/mysql8-data/data#" /etc/init.d/mysqld
            # ......................................
            chmod 700 /etc/init.d/mysqld
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/mysql-8.0.18 && return 0
    else
    
        echo "[Caution] Path: ( /opt/mysql-8.0.18 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_zlib_1_2_13
    Compile_Install_libunwind_1_6_2
    Compile_Install_openssl_1_1_1g
    Compile_Install_ncurses_6_4
    # ------ MySQL - 8.0.18 (Contains Boost) -------
    Build_Install_MySQL_8_0_18_Contains_Boost
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装MySQL-8.0.18 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
