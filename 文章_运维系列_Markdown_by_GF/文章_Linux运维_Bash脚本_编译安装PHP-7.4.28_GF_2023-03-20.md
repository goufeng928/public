# 文章_Linux运维_Bash脚本_编译安装PHP-7.4.28_GF_2023-03-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

bzip2-1.0.6.tar.gz

libxml2-2.9.1.tar.gz

libxslt-1.1.28.tar.gz

byacc-20230219.tar.gz

krb5-1.20.1.tar.gz

openssl-1.1.1g.tar.gz

sqlite-autoconf-3410200.tar.gz

curl-7.71.1.tar.gz

onig-6.9.5-rev1.tar.gz

php-7.4.28.tar.gz
  
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
# * Apache (httpd) == 2.x.x (Optional)

# ------------------- Dependency -------------------
# Need File: zlib-1.2.13.tar.gz
# Need File: bzip2-1.0.6.tar.gz
# Need File: libxml2-2.9.1.tar.gz
# Need File: libxslt-1.1.28.tar.gz
# Need File: byacc-20230219.tar.gz
# Need File: krb5-1.20.1.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# Need File: sqlite-autoconf-3410200.tar.gz
# Need File: curl-7.71.1.tar.gz
# Need File: onig-6.9.5-rev1.tar.gz
# ------------------ PHP - 7.4.28 ------------------
# Need File: php-7.4.28.tar.gz

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

# Function: 制作安装(Make Install) bzip2-1.0.6
# ##################################################
function Make_Install_bzip2_1_0_6() {

    # Attention: may conflict with the original "bzip2" in the system.
    # 注意: 可能与系统原有的 "bzip2" 冲突。

    if [[ ! -d "/opt/bzip2-1.0.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Make and Install ( bzip2-1.0.6 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/bzip2-1.0.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i "18s/CC\=gcc/CC\=gcc \-fPIC/" $STORAGE/bzip2-1.0.6/Makefile
            sed -i "24s/CFLAGS\=\-Wall \-Winline \-O2 \-g \$(BIGFILES)/CFLAGS\=\-Wall \-Winline \-O2 \-fPIC \-g \$(BIGFILES)/" $STORAGE/bzip2-1.0.6/Makefile
        fi
        
        # ------------------------------------------
        cd $STORAGE/bzip2-1.0.6 && make install PREFIX=/opt/bzip2-1.0.6 && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # ln -sf /opt/bzip2-1.0.6/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/bzip2-1.0.6/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/bzip2-1.0.6/lib/ /usr/local/lib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/bzip2-1.0.6 && return 0
    else
        echo "[Caution] Path: ( /opt/bzip2-1.0.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxml2-2.9.1
# ##################################################
function Compile_Install_libxml2_2_9_1() {

    if [[ ! -d "/opt/libxml2-2.9.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( libxml2-2.9.1 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/libxml2-2.9.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxml2-2.9.1 && ./configure --prefix=/opt/libxml2-2.9.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libxml2-2.9.1/bin/xml2-config /usr/local/bin/
            ln -sf /opt/libxml2-2.9.1/bin/xmlcatalog  /usr/local/bin/
            ln -sf /opt/libxml2-2.9.1/bin/xmllint     /usr/local/bin/
            # ......................................
            rsync -av /opt/libxml2-2.9.1/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libxml2-2.9.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxml2-2.9.1/lib/pkgconfig/libxml-2.0.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxml2-2.9.1 && return 0
    else
        echo "[Caution] Path: ( /opt/libxml2-2.9.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxslt-1.1.28
# ##################################################
function Compile_Install_libxslt_1_1_28() {

    if [[ ! -d "/opt/libxslt-1.1.28" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libxslt-1.1.28 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libxslt-1.1.28.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxslt-1.1.28 && ./configure --prefix=/opt/libxslt-1.1.28 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libxslt-1.1.28/bin/xslt-config /usr/local/bin/
            ln -sf /opt/libxslt-1.1.28/bin/xsltproc    /usr/local/bin/
            # ......................................
            rsync -av /opt/libxslt-1.1.28/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libxslt-1.1.28/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxslt-1.1.28/lib/pkgconfig/libexslt.pc /opt/lib/pkgconfig/
            cp -f /opt/libxslt-1.1.28/lib/pkgconfig/libxslt.pc  /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxslt-1.1.28 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxslt-1.1.28 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) byacc-20230219
# ##################################################
function Compile_Install_byacc_20230219() {

    if [[ ! -d "/opt/byacc-20230219" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( byacc-20230219 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/byacc-20230219.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/byacc-20230219 && ./configure --prefix=/opt/byacc-20230219 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .h (Include) File.
            # ......................................
            # Default None .so / .a / .la (Library) File.
            # ......................................
            ln -sf /opt/byacc-20230219/bin/yacc /usr/local/bin/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/byacc-20230219 && return 0
    else
    
        echo "[Caution] Path: ( /opt/byacc-20230219 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) krb5-1.20.1
# ##################################################
function Compile_Install_krb5_1_20_1() {

    if [[ ! -d "/opt/krb5-1.20.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( krb5-1.20.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/krb5-1.20.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/krb5-1.20.1/src && ./configure --prefix=/opt/krb5-1.20.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/krb5-1.20.1/bin/* /usr/local/bin/
            # ......................................
            # Skip # ln -sf /opt/krb5-1.20.1/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/krb5-1.20.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/krb5-1.20.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/krb5-1.20.1/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/krb5-1.20.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/krb5-1.20.1 ) Already Exists."
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

# Function: 编译安装(Compile Install) SQLite-3.41.2
# ##################################################
function Compile_Install_SQLite_3_41_2() {

    if [[ ! -d "/opt/SQLite-3.41.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( sqlite-autoconf-3410200 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/sqlite-autoconf-3410200.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/sqlite-autoconf-3410200 && ./configure --prefix=/opt/SQLite-3.41.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/SQLite-3.41.2/bin/sqlite3 /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/SQLite-3.41.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/SQLite-3.41.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/SQLite-3.41.2/lib/pkgconfig/sqlite3.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/sqlite-autoconf-3410200 && return 0
    else
    
        echo "[Caution] Path: ( /opt/SQLite-3.41.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) cURL-7.71.1
# ##################################################
function Compile_Install_cURL_7_71_1() {

    if [[ ! -d "/opt/curl-7.71.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( curl-7.71.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/curl-7.71.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/curl-7.71.1 && ./configure --prefix=/opt/curl-7.71.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/curl-7.71.1/bin/curl        /usr/local/bin/
            ln -sf /opt/curl-7.71.1/bin/curl-config /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/curl-7.71.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/curl-7.71.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/curl-7.71.1/lib/pkgconfig/libcurl.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/curl-7.71.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/curl-7.71.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) onig-6.9.5-rev1
# ##################################################
function Compile_Install_onig_6_9_5_rev1() {

    if [[ ! -d "/opt/onig-6.9.5-rev1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( onig-6.9.5-rev1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/onig-6.9.5-rev1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/onig-6.9.5 && ./configure --prefix=/opt/onig-6.9.5-rev1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/onig-6.9.5-rev1/bin/onig-config /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/onig-6.9.5-rev1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/onig-6.9.5-rev1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/onig-6.9.5-rev1/lib/pkgconfig/oniguruma.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/onig-6.9.5-rev1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/onig-6.9.5-rev1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### PHP - 7.4.28 ###########################################

# Function: 编译安装(Compile Install) PHP-7.4.28
# ##################################################
function Compile_Install_PHP_7_4_28() {

    # 配置 Apache2 + PHP7 (Optional):
    # 1. 安装 Apache (httpd)。
    # 2. 查看 apxs 二进制 Bin 文件所在路径, 用于编译 PHP 时生成 /etc/httpd/modules/libphp7.so, 若没有这个依赖, Apache 无法解析 PHP 代码。
    # 3. 执行 PHP 的配置命令, 不要遗漏 apxs 路径的配置, 如: --with-apxs2=/usr/local/bin/apxs。

    if [[ ! -d "/opt/php-7.4.28" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( php-7.4.28 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/php-7.4.28.tar.gz  && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/php-7.4.28 && ./configure --prefix=/opt/php-7.4.28 \
                                              --with-config-file-path=/opt/php-7.4.28/etc \
                                              --with-fpm-user=php \
                                              --with-fpm-group=php \
                                              --with-apxs2=/usr/local/bin/apxs \
                                              --with-curl \
                                              --with-freetype-dir \
                                              --with-gd \
                                              --with-gettext \
                                              --with-iconv-dir \
                                              --with-kerberos \
                                              --with-libdir=lib64 \
                                              --with-libxml-dir  \
                                              --with-mysqli \
                                              --with-openssl \
                                              --with-pcre-regex \
                                              --with-pdo-mysql \
                                              --with-pdo-sqlite \
                                              --with-pear \
                                              --with-png-dir \
                                              --with-jpeg-dir \
                                              --with-xmlrpc \
                                              --with-xsl \
                                              --with-zlib \
                                              --with-bz2 \
                                              --with-mhash \
                                              --enable-fpm \
                                              --enable-bcmath \
                                              --enable-libxml \
                                              --enable-inline-optimization \
                                              --enable-mbregex \
                                              --enable-mbstring \
                                              --enable-opcache \
                                              --enable-pcntl \
                                              --enable-shmop \
                                              --enable-soap \
                                              --enable-sockets \
                                              --enable-sysvsem \
                                              --enable-sysvshm \
                                              --enable-xml \
                                              --enable-zip \
                                              --enable-fpm \
                                              PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                              STEP_CONFIGURED=1
        
        # ------------------------------------------
        # * Problem: undefined reference to `xmlFreeParserCtxt'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -lxml2
        # ..........................................
        # * Problem: undefined reference to `EVP_PKEY_free'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/openssl-1.1.1g/lib -lssl
        # ..........................................
        # * Problem: ...libcrypto.so.1.1: error adding symbols: DSO missing from command line
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/openssl-1.1.1g/lib -lcrypto
        # ..........................................
        # * Problem: undefined reference to `xsltSaveResultToString'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/libxslt-1.1.28/lib -lxslt
        # ..........................................
        # * Problem: undefined reference to `sqlite3_reset'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/SQLite-3.41.2/lib -lsqlite3
        # ..........................................
        # * Problem: undefined reference to `curl_share_strerror'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/curl-7.71.1/lib -lcurl
        # ..........................................
        # * Problem: undefined reference to `OnigEncodingASCII'
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -L/opt/onig-6.9.5-rev1/lib -lonig
        # ..........................................
        # * Problem: undefined reference to `__dn_expand' | Handle : EXTRA_LIBS = -lresolv | From Glibc-2.17
        #            collect2: error: ld returned 1 exit status
        #   - Solve: 在 php-7.4.28/Makefile 中的 EXTRA_LIBS 变量添加: -lresolv (来自 Glibc 2.17)
        # ..........................................
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            ln -sf /opt/php-7.4.28/bin/* /usr/local/bin/
            # ......................................
            ln -sf /opt/php-7.4.28/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/php-7.4.28/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/php-7.4.28/lib/ /usr/local/lib/
        fi
        
        # ------------------------------------------
        # Copy / Deploy Configure File.
        # ..........................................
        cp -v $STORAGE/php-7.4.28/php.ini-production /opt/php-7.4.28/etc/php.ini
        # ..........................................
        cp -v /opt/php-7.4.28/etc/php-fpm.conf.default /opt/php-7.4.28/etc/php-fpm.conf
        # ..........................................
        cp -v /opt/php-7.4.28/etc/php-fpm.d/www.conf.default /opt/php-7.4.28/etc/php-fpm.d/www.conf
        # ..........................................
        sed -i "s#^;pid = run/php-fpm.pid#pid = /var/run/php-fpm.pid#" /opt/php-7.4.28/etc/php-fpm.conf
        # ..........................................
        sed -i "s#^;error_log = log/php-fpm.log#error_log = /var/log/php-fpm.log#" /opt/php-7.4.28/etc/php-fpm.conf
        
        # ------------------------------------------
        # Copy / Deploy) init.d Boot File (Optional).
        # ..........................................
        cp -v $STORAGE/php-7.4.28/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
        # ..........................................
        chmod +x /etc/init.d/php-fpm
        
        # ------------------------------------------
        # Copy / Deploy Systemctl Boot File (Optional).
        # ..........................................
        # Skip # cp -v $STORAGE/php-7.4.28/sapi/fpm/php-fpm.service /lib/systemd/system/php-fpm.service
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/php-7.4.28 && return 0
    else
    
        echo "[Caution] Path: ( /opt/php-7.4.28 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_zlib_1_2_13
    Make_Install_bzip2_1_0_6
    Compile_Install_libxml2_2_9_1
    Compile_Install_libxslt_1_1_28
    Compile_Install_byacc_20230219
    Compile_Install_krb5_1_20_1
    Compile_Install_openssl_1_1_1g
    Compile_Install_SQLite_3_41_2
    Compile_Install_cURL_7_71_1
    Compile_Install_onig_6_9_5_rev1
    # ---------------- PHP - 7.4.28 ----------------
    Compile_Install_PHP_7_4_28
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装PHP-7.4.28 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
