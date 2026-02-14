# 文章_Linux运维_Bash脚本_编译安装Apache(httpd-2.4.54)_GF_2023-03-22

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

expat-2.5.0.tar.gz

apr-1.7.0.tar.gz

apr-util-1.6.1.tar.gz

openssl-1.1.1g.tar.gz

pcre-8.37.tar.gz (Maybe Not Necessary)

httpd-2.4.54.tar.gz
  
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
# * None

# ------------------- Dependency -------------------
# Need File: expat-2.5.0.tar.gz
# Need File: apr-1.7.0.tar.gz
# Need File: apr-util-1.6.1.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# Need File: pcre-8.37.tar.gz (Maybe Not Necessary)
# ----------------- httpd - 2.4.54 -----------------
# Need File: httpd-2.4.54.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) expat-2.5.0
# ##################################################
function Compile_Install_expat_2_5_0() {

    if [[ ! -d "/opt/expat-2.5.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( expat-2.5.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/expat-2.5.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/expat-2.5.0 && ./configure --prefix=/opt/expat-2.5.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/expat-2.5.0/bin/xmlwf /usr/local/bin/
            # ......................................
            rsync -av /opt/expat-2.5.0/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/expat-2.5.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/expat-2.5.0/lib/pkgconfig/expat.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/expat-2.5.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/expat-2.5.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) apr-1.7.0
# ##################################################
function Compile_Install_apr_1_7_0() {

    if [[ ! -d "/opt/apr-1.7.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( apr-1.7.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/apr-1.7.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/apr-1.7.0 && ./configure --prefix=/opt/apr-1.7.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/apr-1.7.0/bin/apr-1-config /usr/local/bin/
            # ......................................
            rsync -av /opt/apr-1.7.0/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/apr-1.7.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/apr-1.7.0/lib/pkgconfig/apr-1.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/apr-1.7.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/apr-1.7.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) apr-util-1.6.1
# ##################################################
function Compile_Install_apr_util_1_6_1() {

    if [[ ! -d "/opt/apr-util-1.6.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( apr-util-1.6.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/apr-util-1.6.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/apr-util-1.6.1 && ./configure --prefix=/opt/apr-util-1.6.1 \
                                                  --with-apr=/opt/apr-1.7.0 && \
                                                  STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/apr-util-1.6.1/bin/apu-1-config /usr/local/bin/
            # ......................................
            rsync -av /opt/apr-util-1.6.1/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/apr-util-1.6.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/apr-util-1.6.1/lib/pkgconfig/apr-util-1.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/apr-util-1.6.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/apr-util-1.6.1 ) Already Exists."
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

# Function: 编译安装(Compile Install) pcre-8.37
# ##################################################
function Compile_Install_pcre_8_37() {

    if [[ ! -d "/opt/pcre-8.37" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( pcre-8.37 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pcre-8.37.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/pcre-8.37 && ./configure --prefix=/opt/pcre-8.37 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/pcre-8.37/bin/pcre-config /usr/local/bin/
            ln -sf /opt/pcre-8.37/bin/pcregrep    /usr/local/bin/
            ln -sf /opt/pcre-8.37/bin/pcretest    /usr/local/bin/
            # ......................................
            rsync -av /opt/pcre-8.37/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/pcre-8.37/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/pcre-8.37/lib/pkgconfig/libpcre.pc      /opt/lib/pkgconfig/
            cp -f /opt/pcre-8.37/lib/pkgconfig/libpcrecpp.pc   /opt/lib/pkgconfig/
            cp -f /opt/pcre-8.37/lib/pkgconfig/libpcreposix.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pcre-8.37 && return 0
    else
    
        echo "[Caution] Path: ( /opt/pcre-8.37 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################## httpd - 2.4.54 ##########################################

# Function: 编译安装(Compile Install) httpd-2.4.54
# ##################################################
function Compile_Install_httpd_2_4_54() {

    # ----------------------------------------------
    # Apache (httpd-2.x.x) 安装成功后, 会产生下面两个文件/目录:
    # ..............................................
    # Apache 主配置文件: /opt/httpd-2.4.54/conf/httpd.conf
    # ..............................................
    # Apache 默认网站 home 目录 (DocumentRoot): /opt/httpd-2.4.54/htdocs
    # ----------------------------------------------
    # Apache (httpd-2.x.x) 常用命令:
    # ..............................................
    # 查看 Apache 常见的模块 (包括动态和静态):
    # /usr/local/bin/apachectl -M
    # ..............................................
    # 查看 Apache 加载的静态模块:
    # /usr/local/bin/apachectl -l
    # ..............................................
    # 检查 Apache 配置文件有无语法错误:
    # /usr/local/bin/apachectl -t
    # ..............................................
    # 加载 Apache 配置文件, 但不重启:
    # /usr/local/bin/apachectl graceful
    # ..............................................
    # 启动 / 重启 / 停止 Apache 服务
    # /usr/local/bin/apachectl start/restart/stop

    if [[ ! -d "/opt/httpd-2.4.54" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( httpd-2.4.54 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/httpd-2.4.54.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Create User for httpd-2.4.54.
        local USER_NAME=$(cat /etc/passwd | grep -o apache)
        # ..........................................
        # 命令 adduser 一般是在 Unix 系统下创建用户所用到的 Perl 脚本命令。
        # 使用 adduser 时, 创建用户的过程更像是一种人机对话, 系统会提示你输入各种信息, 然后会根据这些信息帮你创建新用户。
        # adduser 选项释义:
        #     -c, --comment "COMMENT"                  设置用户的备注信息。
        #     -d, --home HOME_DIR                      指定用户的主目录路径。
        #     -s, --shell SHELL                        指定用户的默认 Shell。
        #     -g, --gid GROUP                          将用户添加到指定的用户组。
        #     -G, --groups GROUP1[,GROUP2,…[,GROUPN]]] 将用户同时添加到多个用户组。
        #     -p, --password PASSWORD                  设置用户的密码 (加密)。
        #     -e, --expiredate EXPIRE_DATE             设置用户的过期日期。
        #     -r, --system                             创建一个系统用户 (不可登录)。
        if [[ -z "$USER_NAME" && -f "/usr/bin/adduser" ]]; then adduser apache --system --home /var/www; fi
        # ..........................................
        # 命令 useradd 一般是在 Linux 系统下创建用户所用到的 ELF 可执行程序命令。
        # 使用 useradd 时, 如果后面不添加任何参数选项, 创建出来的用户将是默认 "三无" 用户: 无 Home Directory, 无密码, 无系统 Shell。
        # useradd 选项释义:
        #     -M, --no-create-home                     不创建用户的主目录。
        #     -s, --shell SHELL                        指定用户的默认 Shell。
        if [[ -z "$USER_NAME" && -f "/usr/bin/useradd" ]]; then useradd apache -s /sbin/nologin -M; fi
        
        # ------------------------------------------
        cd $STORAGE/httpd-2.4.54 && ./configure --prefix=/opt/httpd-2.4.54 \
                                                --enable-so \
                                                --enable-ssl \
                                                --enable-cgi \
                                                --enable-rewrite \
                                                --with-zlib \
                                                --with-pcre \
                                                --with-apr=/opt/apr-1.7.0 \
                                                --with-apr-util=/opt/apr-util-1.6.1 \
                                                --with-ssl=/opt/openssl-1.1.1g \
                                                --enable-modules=most \
                                                --enable-mpms-shared=all \
                                                --with-mpm=prefork && \
                                                STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .so / .a / .la (Library) File.
            # ......................................
            ln -sf /opt/httpd-2.4.54/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/httpd-2.4.54/include/ /usr/local/include/
        fi

        # ------------------------------------------
        # * Problem: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
        #   - Solve: 1. 打开 Apache (httpd) 配置文件 httpd.conf。
        #            2. 寻找 ServerName 指令。如果该指令不存在, 需要在配置文件中添加。
        #            3. 设置一个合适的域名或 IP 地址作为 ServerName 的值。例如:
        #                    ServerName yourdomain.com
        #                或者使用本机的 IP 地址:
        #                    ServerName 192.168.1.1
        #            4. 如果你不确定服务器的域名或想要临时解决这个警告, 可以使用本机的 IP 地址:
        #                    ServerName 127.0.0.1 或者 ServerName localhost
        #            5. 保存 httpd.conf 文件并重新启动 Apache (httpd)。

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/httpd-2.4.54 && return 0
    else
    
        echo "[Caution] Path: ( /opt/httpd-2.4.54 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_expat_2_5_0
    Compile_Install_apr_1_7_0
    Compile_Install_apr_util_1_6_1
    Compile_Install_openssl_1_1_1g
    Compile_Install_pcre_8_37
    # --------------- httpd - 2.4.54 ---------------
    Compile_Install_httpd_2_4_54
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Apache(httpd-2.4.54) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
