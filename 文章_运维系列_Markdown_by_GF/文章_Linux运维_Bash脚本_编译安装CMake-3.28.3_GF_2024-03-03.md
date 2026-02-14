# 文章_Linux运维_Bash脚本_编译安装CMake-3.28.3_GF_2024-03-03

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

openssl-1.1.1g.tar.gz

cmake-3.28.3.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-03 20:22

# --------------------------------------------------
# Install First: 
# * None

# ------------------- Dependency -------------------
# Need File: zlib-1.2.13.tar.gz
# Need File: openssl-1.1.1g.tar.gz
# ------------------ CMake 3.28.3 ------------------
# Need File: cmake-3.28.3.tar.gz

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
            rsync -av /opt/zlib-1.2.13/include/ /usr/local/include/
            rsync -av /opt/zlib-1.2.13/lib/     /usr/local/lib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/zlib-1.2.13 && return 0
    else
    
        echo "[Caution] Program: ( /usr/include/zlib.h or /usr/local/include/zlib.h or /opt/zlib-1.2.13 ) Already Exists."
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
            rsync -av /opt/openssl-1.1.1g/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/openssl-1.1.1g/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /opt/lib/pkgconfig/
            cp -f /opt/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/openssl-1.1.1g && return 0
    else
    
        # ------------------------------------------
        # 注意: 避免与系统原有的 "openssl" 发生冲突, 未将 "openssl-1.1.1g" 的二进制 bin 文件发送到 PATH 路径。
        # Caution: To avoid conflicts with the original "openssl" in the system, the binary file of "openssl-1.1.1g" was not sent to the PATH path.
        # ..........................................
        # Skip # ln -sf /opt/openssl-1.1.1g/bin/* /usr/local/bin/
        # ..........................................
        rsync -av /opt/openssl-1.1.1g/include/ /usr/local/include/
        # ..........................................
        rsync -av /opt/openssl-1.1.1g/lib/ /usr/local/lib/
        # ..........................................
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /opt/lib/pkgconfig/
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /opt/lib/pkgconfig/
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /opt/lib/pkgconfig/
        # ------------------------------------------
        echo "[Caution] Path: ( /opt/openssl-1.1.1g ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### CMake 3.28.3 ###########################################

# Function: 编译安装(Compile Install) cmake-3.28.3
# ##################################################
function Compile_Install_CMake_3_28_3() {

    if [[ ! -d "/opt/cmake-3.28.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( cmake-3.28.3 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/cmake-3.28.3.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/cmake-3.28.3 && ./configure --prefix=/opt/cmake-3.28.3 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/cmake-3.28.3/bin/cmake /usr/local/bin/cmake
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/cmake-3.28.3 && return 0
    else
        echo "[Caution] Path: ( /opt/cmake-3.28.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- Dependency -----------------
    Compile_Install_zlib_1_2_13
    Compile_Install_openssl_1_1_1g
    # ---------------- CMake 3.28.3 ----------------
    Compile_Install_CMake_3_28_3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装CMake-3.28.3 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
