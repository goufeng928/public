# 文章_Linux运维_Bash脚本_编译安装Linux-PAM-1.3.1_GF_2023-03-21

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

rpcsvc-proto-1.4.3.tar.xz (Maybe Not Necessary)

libtirpc-1.3.3.tar.bz2

Linux-PAM-1.3.1.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-21 16:22

# --------------------------------------------------
# Install First: 
# * None

# ------------------- Dependency -------------------
# Need File: zlib-1.2.13.tar.gz
# Need File: rpcsvc-proto-1.4.3.tar.xz (Maybe Not Necessary)
# Need File: libtirpc-1.3.3.tar.bz2
# --------------- Linux-PAM - 1.3.1 ----------------
# Need File: Linux-PAM-1.3.1.tar.xz

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

# Function: 编译安装(Compile Install) rpcsvc-proto-1.4.3
# ##################################################
function Compile_Install_rpcsvc_proto_1_4_3() {

    if [[ ! -d "/opt/rpcsvc-proto-1.4.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( rpcsvc-proto-1.4.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/rpcsvc-proto-1.4.3.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Configure Options:
        #     ./configure --prefix=/usr/local/rpcsvc-proto-1.4.3 \
        #                 --sysconfdir=/etc   
        cd $STORAGE/rpcsvc-proto-1.4.3 && ./configure --prefix=/opt/rpcsvc-proto-1.4.3 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            rsync -av /opt/rpcsvc-proto-1.4.3/bin/rpcgen /usr/local/bin/
            # ......................................
            rsync -av /opt/rpcsvc-proto-1.4.3/include/ /usr/local/include/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/rpcsvc-proto-1.4.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/rpcsvc-proto-1.4.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libtirpc-1.3.3
# ##################################################
function Compile_Install_libtirpc_1_3_3() {

    if [[ ! -d "/opt/libtirpc-1.3.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libtirpc-1.3.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/libtirpc-1.3.3.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Configure Options:
        #     ./configure --prefix=/usr/local/tirpc-1.3.3 \
        #                 --sysconfdir=/etc \
        #                 --disable-static \
        #                 --disable-gssapi
        cd $STORAGE/libtirpc-1.3.3 && ./configure --prefix=/opt/libtirpc-1.3.3 \
                                                  --disable-static \
                                                  --disable-gssapi && \
                                                  STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            cp -f /opt/tirpc-1.3.3/include/tirpc/netconfig.h /opt/libtirpc-1.3.3/include/
            # ......................................
            # Create a subdirectory "rpc" for Include.
            if [[ ! -d "/opt/libtirpc-1.3.3/include/rpc" ]]; then mkdir /opt/libtirpc-1.3.3/include/rpc; fi
            # ......................................
            cp -f /opt/tirpc-1.3.3/include/tirpc/rpc/*.h /opt/libtirpc-1.3.3/include/rpc/
            # ......................................
            # Create a subdirectory "rpcsvc" for Include.
            if [[ ! -d "/opt/libtirpc-1.3.3/include/rpcsvc" ]]; then mkdir /opt/libtirpc-1.3.3/include/rpcsvc; fi
            # ......................................
            cp -f /opt/tirpc-1.3.3/include/tirpc/rpcsvc/crypt.h  /opt/libtirpc-1.3.3/include/rpcsvc/
            # ......................................
            # Regular synchronization file path.
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libtirpc-1.3.3/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libtirpc-1.3.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libtirpc-1.3.3/lib/pkgconfig/libtirpc.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libtirpc-1.3.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libtirpc-1.3.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ######################################## Linux-PAM - 1.3.1 #########################################

# Function: 编译安装(Compile Install) Linux-PAM-1.3.1
# ##################################################
function Compile_Install_Linxu_PAM_1_3_1() {

    if [[ ! -d "/opt/Linux-PAM-1.3.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_MADE=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( Linux-PAM-1.3.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/Linux-PAM-1.3.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Default Configure Options:
        # ./configure --prefix=/usr \
        #             --sbindir=/usr/sbin \
        #             --sysconfdir=/etc \
        #             --libdir=/usr/lib  \
        #             --enable-securedir=/usr/lib/security \
        #             --docdir=/usr/share/doc/Linux-PAM-1.3.1
        cd $STORAGE/Linux-PAM-1.3.1 && ./configure --prefix=/opt/Linux-PAM-1.3.1 \
                                                   --enable-read-both-confs && \
                                                   STEP_CONFIGURED=1
        
        # ------------------------------------------
        make LIBS="-ltirpc" && STEP_MADE=1
        
        # ------------------------------------------
        make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Create a subdirectory "security" for Include.
            if [[ ! -d "/opt/Linux-PAM-1.3.1/include/security" ]]; then mkdir /opt/Linux-PAM-1.3.1/include/security; fi
            # ......................................
            cp -f /opt/Linux-PAM-1.3.1/include/*.h /opt/Linux-PAM-1.3.1/include/security/
            # ......................................
            # Regular synchronization file path.
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            # Skip # ln -sf /opt/Linux-PAM-1.3.1/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/Linux-PAM-1.3.1/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/Linux-PAM-1.3.1/lib/ /usr/local/lib/
        fi
        
        # ------------------------------------------
        # 将 PAM 加入系统服务 (for Ubuntu 18.04)。
        # Skip # ln -s /opt/Linux-PAM-1.3.1/lib/systemd/system/pam_namespace.service /lib/systemd/system/pam.service
        # ..........................................
        # 将 PAM 配置文件复制到 root 目录下的 etc 。
        # cp $STORAGE/Linux-PAM-1.3.1/conf/pam.conf /etc/pam.conf

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/Linux-PAM-1.3.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/Linux-PAM-1.3.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_zlib_1_2_13
    Compile_Install_rpcsvc_proto_1_4_3
    Compile_Install_libtirpc_1_3_3
    # ------------- Linux-PAM - 1.3.1 --------------
    Compile_Install_Linxu_PAM_1_3_1
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Linux-PAM-1.3.1 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
