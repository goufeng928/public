# 文章_Linux运维_Bash脚本_快速配置Apache(httpd-2.4.54)_GF_2023-03-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 编译安装程序:

Apache (httpd-2.4.54)
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动快速配置，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个快速配置结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-20 10:31

# ----------- Configure - httpd - 2.4.54 -----------
# Need Program: /opt/httpd-2.4.54

# #################################### Configure - httpd - 2.4.54 ####################################

# Function: 快速配置(Quick Configure) httpd-2.4.54
# ##################################################
function Quick_Configure_httpd_2_4_54() {

    if [[ -d "/opt/httpd-2.4.54" ]]; then
    
        local USER_NAME="None"
        local ITEM_NAME="None"
    
        # ------------------------------------------
        read -p "[Confirm] Quick Configure ( httpd-2.4.54 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi
        
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
        USER_NAME=$(cat /etc/passwd | grep -o "^apache")
        # ..........................................
        if [[ -z "$USER_NAME" && -f "/usr/sbin/adduser" ]]; then adduser apache --system --home /var/www; fi
        # ..........................................
        # 命令 useradd 一般是在 Linux 系统下创建用户所用到的 ELF 可执行程序命令。
        # 使用 useradd 时, 如果后面不添加任何参数选项, 创建出来的用户将是默认 "三无" 用户: 无 Home Directory, 无密码, 无系统 Shell。
        # useradd 选项释义:
        #     -g, --gid GROUP                          新账户主组的名称或 ID。
        #     -M, --no-create-home                     不创建用户的主目录。
        #     -s, --shell SHELL                        指定用户的默认 Shell。
        USER_NAME=$(cat /etc/passwd | grep -o "^apache")
        # ..........................................
        if [[ -z "$USER_NAME" && -f "/usr/sbin/useradd" ]]; then useradd apache -s /sbin/nologin -M; fi
        # ..........................................
        USER_NAME=$(cat /etc/passwd | grep -o "^apache")
        echo "Exists User: $USER_NAME"
        
        # ------------------------------------------
        if [[ ! -d "/var/www" ]]; then mkdir /var/www; fi

        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 将 User daemon 改为 User apache
        sed -r -i "s/^User [a-zA-Z]*/User apache/" /opt/httpd-2.4.54/conf/httpd.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="^User [a-zA-Z]*")
        echo "Edit Item: User ......                 -> $ITEM_NAME"
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 将 Group daemon 改为 Group apache
        sed -r -i "s/^Group [a-zA-Z]*/Group apache/" /opt/httpd-2.4.54/conf/httpd.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="^Group [a-zA-Z]*")
        echo "Edit Item: Group ......                -> $ITEM_NAME"
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 将 DocumentRoot "/opt/httpd-2.4.54/htdocs" 改为 DocumentRoot "/var/www"
        sed -r -i "s%^DocumentRoot \".*\"%DocumentRoot \"/var/www\"%" /opt/httpd-2.4.54/conf/httpd.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="^DocumentRoot \".*\"")
        echo "Edit Item: DocumentRoot \"......\"       -> $ITEM_NAME"
        
        # ------------------------------------------
        # 编辑 Apache (httpd) 配置文件 httpd.conf, 将 <Directory "/opt/httpd-2.4.54/htdocs"> 改为 <Directory "/var/www">
        sed -r -i "s%^<Directory \".*htdocs\">%<Directory \"/var/www\">%" /opt/httpd-2.4.54/conf/httpd.conf
        # ..........................................
        ITEM_NAME=$(cat /opt/httpd-2.4.54/conf/httpd.conf | grep --regexp="^<Directory \".*www\">")
        echo "Edit Item: <Directory \"......htdocs\">  -> $ITEM_NAME"

    else
    
        echo "[Caution] Program: ( /opt/httpd-2.4.54 ) Does Not Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # --------- Configure - httpd - 2.4.54 ---------
    Quick_Configure_httpd_2_4_54
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 快速配置Apache(httpd-2.4.54) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
