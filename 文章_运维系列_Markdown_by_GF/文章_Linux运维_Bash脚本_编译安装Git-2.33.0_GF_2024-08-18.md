# 文章_Linux运维_Bash脚本_编译安装Git-2.33.0_GF_2024-08-18

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

expat-2.5.0.tar.gz

openssl-1.1.1g.tar.gz

curl-7.71.1.tar.gz

git-2.33.0.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-08-03 01:34

# --------------------------------------------------
# Install First: 
# * GCC

# -------------- Dep for Git - 2.33.0 --------------
# Need File: zlib-1.2.13.tar.gz
# Need File: expat-2.5.0.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# Need File: curl-7.71.1.tar.gz
# ------------------ Git - 2.33.0 ------------------
# Need File: git-2.33.0.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ####################################### Dep for Git - 2.33.0 #######################################

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
            rsync -av /opt/zlib-1.2.13/lib/     /usr/local/lib/
            # ......................................
            cp /opt/zlib-1.2.13/lib/pkgconfig/zlib.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/zlib-1.2.13 && return 0
    else
    
        echo "[Caution] Program: ( /usr/include/zlib.h or /usr/local/include/zlib.h or /opt/zlib-1.2.13 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

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

# Function: 编译安装(Compile Install) cURL-7.71.1
# ##################################################
function Compile_Install_cURL_7_71_1() {

    if [[ ! -f "/usr/bin/curl" && ! -f "/usr/local/bin/curl" && ! -d "/opt/curl-7.71.1" ]]; then
    
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
            rsync -av /opt/curl-7.71.1/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/curl-7.71.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/curl-7.71.1/lib/pkgconfig/libcurl.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/curl-7.71.1 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/curl or /usr/local/bin/curl or /opt/curl-7.71.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### Git - 2.33.0 ###########################################

# Function:  编译安装(Compile Install) Git-2.33.0
# ##################################################
function Compile_Install_Git_2_33_0() {

    if [[ ! -d "/opt/git-2.33.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( git-2.33.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/git-2.33.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Method 1: 直接 make 然后 make test, 最后 make install (编译好的 Binary 文件就在当前目录)。 
        # Method 2: 没有 configure 则通过 make configure 生成 configure, 再执行 ./configure --prefix=/opt/..., 最后 make install。
        cd $STORAGE/git-2.33.0 && ./configure --prefix=/opt/git-2.33.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            ln -sf /opt/git-2.33.0/bin/git                /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/git-cvsserver      /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/gitk               /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/git-receive-pack   /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/git-shell          /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/git-upload-archive /usr/local/bin/
            ln -sf /opt/git-2.33.0/bin/git-upload-pack    /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/Git-2.33.0/libexec/ /usr/local/libexec/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/git-2.33.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/git-2.33.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {
    
    # ----------- Compilation Environment ----------
    export C_INCLUDE_PATH=/opt/openssl-1.1.1g/include
    export CPLUS_INCLUDE_PATH=/opt/openssl-1.1.1g/include
    # ..............................................
    export LIBRARY_PATH=/opt/openssl-1.1.1g/lib
    export LD_LIBRARY_PATH=/opt/openssl-1.1.1g/lib

    # ------------ Dep for Git - 2.33.0 ------------
    Compile_Install_zlib_1_2_13
    Compile_Install_expat_2_5_0
    Compile_Install_openssl_1_1_1g
    Compile_Install_cURL_7_71_1
    # ---------------- Git - 2.33.0 ----------------
    Compile_Install_Git_2_33_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Git-2.33.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
