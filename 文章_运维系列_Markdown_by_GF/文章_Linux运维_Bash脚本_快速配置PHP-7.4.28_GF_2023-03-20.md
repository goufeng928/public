# 文章_Linux运维_Bash脚本_快速配置PHP-7.4.28_GF_2023-03-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 编译安装程序:

Apache (httpd-2.4.54)

PHP-7.4.28
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动快速配置，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个快速配置结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-20 10:31

# ------- Configure - httpd - 2.4.54 Support -------
# Need Program: /opt/httpd-2.4.54
# ------------ Configure - PHP - 7.4.28 ------------
# Need Program: /opt/php-7.4.28

# ################################ Configure - httpd - 2.4.54 Support ################################

# Function: 快速配置(Quick Configure) httpd-2.4.54 支持
# ##################################################
function Quick_Configure_httpd_2_4_54_Support() {

    if [[ -d "/opt/httpd-2.4.54" ]]; then
    
        local User_Exists=$(cat /etc/passwd | grep -o apache)
        local ITEM_EXISTS="None"
        local ITEM_NAME="None"
    
        # ------------------------------------------
        read -p "[Confirm] Quick Configure ( httpd-2.4.54 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 写入: LoadModule php7_module modules/libphp7.so, 用于加载 PHP 模块 (加载 PHP 模块应在对 PHP 的解析之前, 否则可能无法解析 PHP)。
        # ..........................................
        ITEM_EXISTS=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep -o "LoadModule php7_module modules/libphp7.so")
        # ..........................................
        if [[ -z "$ITEM_EXISTS" ]]; then
            echo "LoadModule php7_module modules/libphp7.so" >> /opt/httpd-2.4.54/conf/httpd.conf
            # ......................................
            echo "Add Line:                                           -> httpd.conf"
            echo "Add Line: LoadModule php7_module modules/libphp7.so -> httpd.conf"
            echo "Add Line:                                           -> httpd.conf"
        fi
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 以支持 Apache 对 PHP 的解析 (对 PHP 的解析应在加载 PHP 模块之后, 否则可能无法解析 PHP)。
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 写入: <IfModule mod_php7.c>
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 写入:     AddType application/x-httpd-php .php
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 写入: </IfModule>
        # ..........................................
        ITEM_EXISTS=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep -o "AddType application/x-httpd-php .php")
        # ..........................................
        if [[ -z "$ITEM_EXISTS" ]]; then
            echo ""                                         >> /opt/httpd-2.4.54/conf/httpd.conf
            echo "<IfModule mod_php7.c>"                    >> /opt/httpd-2.4.54/conf/httpd.conf
            echo "    AddType application/x-httpd-php .php" >> /opt/httpd-2.4.54/conf/httpd.conf
            echo "</IfModule>"                              >> /opt/httpd-2.4.54/conf/httpd.conf
            echo ""                                         >> /opt/httpd-2.4.54/conf/httpd.conf
            # ......................................
            echo "Add Line:                                          -> httpd.conf"
            echo "Add Line: <IfModule mod_php7.c>                    -> httpd.conf"
            echo "Add Line:     AddType application/x-httpd-php .php -> httpd.conf"
            echo "Add Line: </IfModule>                              -> httpd.conf"
            echo "Add Line:                                          -> httpd.conf"
        fi
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 将 DirectoryIndex index.html 改为 DirectoryIndex index.html index.php
        # ..........................................
        ITEM_EXISTS=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="DirectoryIndex .*index\.php.*")
        # ..........................................
        if [[ -z "$ITEM_EXISTS" ]]; then
            sed -r -i "s/DirectoryIndex .*index\.html.*/& index.php/" /opt/httpd-2.4.54/conf/httpd.conf
            # ..........................................
            ITEM_NAME=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="DirectoryIndex .*index\.php.*")
            echo "Edit Item: DirectoryIndex ...... index.html ...... -> $ITEM_NAME"
        fi
    
    else
    
        echo "[Caution] Program: ( /opt/httpd-2.4.54 ) Does Not Exists."
        # ------------------------------------------
        return 0
    fi
}

# ###################################### Configure PHP - 7.4.28 ######################################

# Function: 快速配置(Quick Configure) PHP-7.4.28
# ##################################################
function Quick_Configure_PHP_7_4_28() {

    if [[ -d "/opt/php-7.4.28" ]]; then
    
        local GROUP_NAME="None"
        local USER_NAME="None"
        local ITEM_NAME="None"
    
        # ------------------------------------------
        read -p "[Confirm] Quick Configure ( php-7.4.28 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        GROUP_NAME=$(cat /etc/group | grep -o "^php")
        # ..........................................
        if [[ -z "$GROUP_NAME" && -f "/usr/sbin/addgroup" ]]; then addgroup --system php; fi
        # ..........................................
        GROUP_NAME=$(cat /etc/group | grep -o "^php")
        # ..........................................
        if [[ -z "$GROUP_NAME" && -f "/usr/sbin/groupadd" ]]; then groupadd --system php; fi
        # ..........................................
        GROUP_NAME=$(cat /etc/group | grep -o "^php")
        echo "Exists Group: $GROUP_NAME"
        
        # ------------------------------------------
        # 命令 adduser 一般是在 Unix 系统下创建用户所用到的 Perl 脚本命令。
        # 使用 adduser 时, 创建用户的过程更像是一种人机对话, 系统会提示你输入各种信息, 然后会根据这些信息帮你创建新用户。
        # adduser 选项释义:
        #     -c, --comment "COMMENT"                  设置用户的备注信息。
        #     -d, --home HOME_DIR                      指定用户的主目录路径。
        #     -s, --shell SHELL                        指定用户的默认 Shell。
        #     -g, --gid GROUP                          将用户添加到指定的用户组。
        #     -p, --password PASSWORD                  设置用户的密码 (加密)。
        #     -e, --expiredate EXPIRE_DATE             设置用户的过期日期。
        #     -r, --system                             创建一个系统用户 (不可登录)。
        USER_NAME=$(cat /etc/passwd | grep -o "^php")
        # ..........................................
        if [[ -z "$USER_NAME" && -f "/usr/sbin/adduser" ]]; then adduser php --system --home /var/www && adduser php php; fi
        # ..........................................
        # 命令 useradd 一般是在 Linux 系统下创建用户所用到的 ELF 可执行程序命令。
        # 使用 useradd 时, 如果后面不添加任何参数选项, 创建出来的用户将是默认 "三无" 用户: 无 Home Directory, 无密码, 无系统 Shell。
        # useradd 选项释义:
        #     -g, --gid GROUP                          新账户主组的名称或 ID。
        #     -M, --no-create-home                     不创建用户的主目录。
        #     -s, --shell SHELL                        指定用户的默认 Shell。
        USER_NAME=$(cat /etc/passwd | grep -o "^php")
        # ..........................................
        if [[ -z "$USER_NAME" && -f "/usr/sbin/useradd" ]]; then useradd php -s /sbin/nologin -g php -M; fi
        # ..........................................
        USER_NAME=$(cat /etc/passwd | grep -o "^php")
        echo "Exists User: $USER_NAME"
        
        # ------------------------------------------
        # 复制 PHP-FPM 配置文件 php-fpm.conf, 将 php-fpm.conf.default 复制为 /opt/php-7.4.28/etc/php-fpm.conf 使其生效。
        if [[ ! -f "/opt/php-7.4.28/etc/php-fpm.conf" ]]; then
            cp -v /opt/php-7.4.28/etc/php-fpm.conf.default /opt/php-7.4.28/etc/php-fpm.conf
            # ......................................
            echo "Copy File: php-fpm.conf.default -> php-fpm.conf"
        fi
        
        # ------------------------------------------
        # 编辑 PHP-FPM 脚本文件 php-fpm, 将 php_fpm_PID= ...... /php-fpm.pid 改为 php_fpm_PID=/var/run/php-fpm.pid (应与 php-fpm.conf 中的 php-fpm.pid 路径相同)。
        sed -r -i "s#^php_fpm_PID\=.*php-fpm\.pid#php_fpm_PID\=/var/run/php-fpm\.pid#" /etc/init.d/php-fpm
        # ..........................................
        ITEM_NAME=$(cat /etc/init.d/php-fpm | grep --regexp="^php_fpm_PID\=.*php-fpm\.pid")
        echo "Edit Item: php_fpm_PID= ...... /php-fpm.pid -> $ITEM_NAME"

        # ------------------------------------------
        # 编辑 PHP-FPM 配置文件 php-fpm.conf, 将 ;pid = run/php-fpm.pid 取消注释, 改为 pid = /var/run/php-fpm.pid (应与 /etc/init.d/php-fpm 中的 php-fpm.pid 路径相同)。
        sed -i "s#^;pid = run/php-fpm.pid#pid = /var/run/php-fpm.pid#" /opt/php-7.4.28/etc/php-fpm.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/php-7.4.28/etc/php-fpm.conf | grep --regexp="^pid \= .*php-fpm.pid")
        echo "Edit Item: ;pid = run/php-fpm.pid -> $ITEM_NAME"
        
        # ------------------------------------------
        # 编辑 PHP-FPM 配置文件 php-fpm.conf, 将 ;error_log = log/php-fpm.log 取消注释, 改为 error_log = /var/log/php-fpm.log
        sed -i "s#^;error_log = log/php-fpm.log#error_log = /var/log/php-fpm.log#" /opt/php-7.4.28/etc/php-fpm.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/php-7.4.28/etc/php-fpm.conf | grep --regexp="^error_log \= .*php-fpm.log")
        echo "Edit Item: ;error_log = log/php-fpm.log -> $ITEM_NAME"
        
        # ------------------------------------------
        # 编辑 PHP 配置文件 php.ini, 将 short_open_tag = Off 改为 short_open_tag = On (如果为 Off, 可能会打不开 phpinfo(); 测试代码页面)。
        sed -r -i "s#^short_open_tag.*#short_open_tag = On#" /opt/php-7.4.28/etc/php.ini
        # ..........................................
        ITEM_NAME=$(cat /opt/php-7.4.28/etc/php.ini | grep --regexp="^short_open_tag")
        echo "Edit Item: short_open_tag = ... -> $ITEM_NAME"

    else
    
        echo "[Caution] Program: ( /opt/php-7.4.28 ) Does Not Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----- Configure - httpd - 2.4.54 Support -----
    Quick_Configure_httpd_2_4_54_Support
    # ---------- Configure - PHP - 7.4.28 ----------
    Quick_Configure_PHP_7_4_28
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 快速配置PHP-7.4.28 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
