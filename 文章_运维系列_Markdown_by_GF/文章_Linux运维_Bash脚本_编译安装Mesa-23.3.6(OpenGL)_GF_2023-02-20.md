# 文章_Linux运维_Bash脚本_编译安装Mesa-23.3.6(OpenGL)_GF_2023-02-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

expat-2.5.0.tar.gz

libdrm-2.4.120.tar.xz

MarkupSafe-1.1.1.tar.gz (Python 源码)

Mako-1.1.6.tar.gz (Python 源码)

llvm-project-15.0.7.src.tar.xz

glslang-main-linux-Release.zip

fixesproto-5.0.tar.gz

libXfixes-5.0.3.tar.gz

libxshmfence_1.3.orig.tar.gz

glproto-1.4.17.tar.gz

dri2proto-2.8.tar.gz

xf86vidmodeproto-2.3.tar.gz

libXxf86vm-1.1.4.tar.gz

randrproto-1.5.0.tar.bz2

libXrandr-1.5.2.tar.gz

mesa-23.3.6.tar.xz

libXi-1.7.6.tar.gz

glu-9.0.3.tar.xz

freeglut-3.4.0.tar.gz

glew-2.2.0.tgz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-20 21:42

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.13.4
# * Python == 3.x.x
# * Meson
# * Ninja
# * X11 (Needed by Wayland)
# * Wayland >= 1.22.0 (Contains: Wayland-Protocols)

# ------------------- Dependency -------------------
# Need File: expat-2.5.0.tar.gz
# Need File: libdrm-2.4.120.tar.xz
# ------------------ Mako - 1.1.6 ------------------
# Need File: MarkupSafe-1.1.1.tar.gz -> Python 源码
# Need File: Mako-1.1.6.tar.gz -> Python 源码
# ----------------- LLVM >= 15.0.0 -----------------
# Need File: llvm-project-15.0.7.src.tar.xz
# --------------------- Glslang --------------------
# Need File: glslang-main-linux-Release.zip
# ------------- Special X11 Dependency -------------
# Need File: fixesproto-5.0.tar.gz
# Need File: libXfixes-5.0.3.tar.gz
# Need File: libxshmfence_1.3.orig.tar.gz
# Need File: glproto-1.4.17.tar.gz
# Need File: dri2proto-2.8.tar.gz
# Need File: xf86vidmodeproto-2.3.tar.gz
# Need File: libXxf86vm-1.1.4.tar.gz
# Need File: randrproto-1.5.0.tar.bz2
# Need File: libXrandr-1.5.2.tar.gz
# ------------------ Mesa - 23.3.6 -----------------
# Need File: mesa-23.3.6.tar.xz
# ---------------- freeGlut - 3.4.0 ----------------
# Need File: libXi-1.7.6.tar.gz
# Need File: glu-9.0.3.tar.xz
# Need File: freeglut-3.4.0.tar.gz
# ------------------ GLEW - 2.2.0 ------------------
# Need File: glew-2.2.0.tgz

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

# Function: 构建安装(Build Install) libdrm-2.4.120
# ##################################################
function Build_Install_libdrm_2_4_120() {

    # Attention: may conflict with the original "drm" in the system.
    # 注意: 可能与系统原有的 "drm" 冲突。

    if [[ ! -d "/opt/libdrm-2.4.120" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libdrm-2.4.120 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libdrm-2.4.120.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libdrm-2.4.120 && meson build --prefix=/opt/libdrm-2.4.120 && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libdrm-2.4.120 && ninja -C build install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libdrm-2.4.120/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libdrm-2.4.120/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libdrm-2.4.120/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libdrm-2.4.120 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libdrm-2.4.120 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### Mako - 1.1.6 ###########################################

# Function: 构建安装(Build Install) MarkupSafe-1.1.1 (by Python3)
# ##################################################
function Build_Install_MarkupSafe_1_1_1_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    # ..............................................
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "MarkupSafe")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "MarkupSafe")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.1.1")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( MarkupSafe-1.1.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/MarkupSafe-1.1.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/MarkupSafe-1.1.1 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/MarkupSafe-1.1.1 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/MarkupSafe-1.1.1 && return 0
    else
    
        echo "[Caution] Python Package: ( MarkupSafe-1.1.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Mako-1.1.6 (by Python3)
# ##################################################
function Build_Install_Mako_1_1_6_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    # ..............................................
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "Mako")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "Mako")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.1.6")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( Mako-1.1.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/Mako-1.1.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/Mako-1.1.6 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/Mako-1.1.6 && python3 setup.py install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/Python-3.8.0/bin/mako-render /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/Mako-1.1.6 && return 0
    else
    
        echo "[Caution] Python Package: ( Mako-1.1.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################## LLVM >= 15.0.0 ##########################################

# Function: 构建安装(Build Install) LLVM-Project-15.0.7
# ##################################################
function Build_Install_LLVM_Project_15_0_7() {

    # Linux 查看 LLVM 版本: llvm-as --version

    if [[ ! -f "/usr/local/bin/llvm-as" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( LLVM-Project-15.0.7 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/llvm-project-15.0.7.src.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        mkdir $STORAGE/llvm-project-15.0.7.src/llvm/build && STEP_CREATED=1
        
        # ------------------------------------------
        # 通过以下方式构建 LLVM:
        # cd llvm-project-15.0.7.src
        # ..........................................
        # cmake -S llvm -B build -G <Generator> [options]
        #     常见的构建系统生成器 <Generator> 包括:
        #         1) Ninja - 用于生成 Ninja 构建文件。大多数 LLVM 开发人员都使用 Ninja。
        #         2) Unix Makefiles - 用于生成与 make 兼容的并行 makefiles 生成文件。
        #         3) Visual Studio - 用于生成 Visual Studio 项目和解决方案。
        #         4) Xcode - 用于生成 Xcode 项目。
        #         5) 有关更全面的 List 列表, 请参阅 CMake 文档。
        # ..........................................
        # cmake -S llvm -B build -G Ninja -DCMAKE_BUILD_TYPE=[Type]
        #     [Type] 的类型有:
        #         1) Release - 普通使用 Release 就行。
        #         2) Debug - 通常是为了开发, 如果是 Debug, 请准备足够的内存和硬盘空间。
        #         3) RelWithDebInfo
        #         4) MinSizeRel
        # ..........................................
        # cmake -S llvm -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_PROJECTS='[Proj1];[Proj2]'
        #     [Proj1];[Proj2] 要额外构建的 LLVM 子项目的 semicolon-separated 分号分隔列表。可以包括以下任何一项:
        #         1) clang
        #         2) clang-tools-extra
        #         3) lldb
        #         4) lld
        #         5) polly
        #     或跨项目测试: cross-project-tests
        #     例如, 构建 LLVM, Clang 和 LLD, 请使用 -DLLVM_ENABLE_PROJECTS="clang;lld"
        # ..........................................
        # cmake -S llvm -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=[Directory]
        #     [Directory] 指定要安装的 LLVM 工具和库的完整路径名 (Default 默认路径为: /usr/local)。
        cd $STORAGE/llvm-project-15.0.7.src/llvm/build && cmake -G "Unix Makefiles" \
                                                                -DCMAKE_C_COMPILER=/usr/bin/gcc \
                                                                -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
                                                                -DLLVM_ENABLE_PROJECTS=clang \
                                                                -DCMAKE_BUILD_TYPE=Release \
                                                                ../ && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/llvm-project-15.0.7.src && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/llvm-as ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################## Glslang #############################################

# Function: 部署(Deploy) glslang-main-linux-Release
# ##################################################
function Deploy_glslang_main_linux_Release() {

    # OpenGL / OpenGL ES Reference Compiler
    # Glslang is the official reference compiler front end for the OpenGL ES and OpenGL shading languages. 
    # It implements a strict interpretation of the specifications for these languages. 
    # It is open and free for anyone to use, either from a command line or programmatically. 
    # The OpenGL and OpenGL ES working groups are committed to maintaining consistency between the reference compiler and the corresponding shading language specifications.
    # OpenGL / OpenGL ES 参考编译器
    # Glslang 是 OpenGL 和 OpenGL ES 着色语言的官方参考编译器前端。
    # 它对这些语言的规范进行了严格的解释。
    # 它是开放的, 任何人都可以自由使用, 无论是从命令行还是通过编程方式。
    # OpenGL 和 OpenGL ES 工作组致力于保持参考编译器和相应着色语言规范之间的一致性。
    # ..............................................
    # Purpose
    # The primary purpose of the reference compiler is to identify shader portability issues. 
    # If glslang accepts a shader without errors, then all OpenGL and OpenGL ES implementations claiming to support the shader's language version should also accept the shader without errors. 
    # Likewise, if glslang reports an error when compiling a shader, all OpenGL and OpenGL ES implementations for that language version should report errors, unless the glslang errors are caused by differences in implementation-defined limits or extension support (see below).
    # 目的
    # 引用编译器的主要目的是识别着色器的可移植性问题。
    # 如果 glslang 无错误地接受着色器, 那么所有声称支持着色器语言版本的 OpenGL 和 OpenGL ES 实现也应无错误地接收着色器。
    # 同样, 如果 glslang 在编译着色器时报告错误, 则该语言版本的所有 OpenGL 和 OpenGL ES 实现都应报告错误, 除非 glslang 错误是由实现定义的限制或扩展支持的差异引起的 (见下文)。
    # ..............................................
    # Secondarily, glslang is also suitable for programmatic use in a tool chain or a driver, translating the input source into an abstract syntax tree that can be translated into an intermediate representation for machine-independent processing and lowering to machine-specific code. 
    # Glslang can also return (even from the command line) uniform variable reflection information (before optimization).
    # 其次, glslang 也适用于工具链或驱动程序中的程序化使用, 将输入源翻译成抽象语法树, 该抽象语法树可以翻译成用于机器独立处理的中间表示, 并降低到机器特定代码。
    # Glslash还可以 (甚至从命令行) 返回统一的变量反射信息 (在优化之前)。

    if [[ ! -f "/usr/local/bin/glslang" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_DEPLOYED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( glslang-main-linux-Release )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        unzip $STORAGE/glslang-main-linux-Release.zip && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sudo cp -r $STORAGE/bin/*     /usr/local/bin/
            sudo cp -r $STORAGE/include/* /usr/local/include/
            sudo cp -r $STORAGE/lib/*     /usr/local/lib/ && STEP_DEPLOYED=1
        fi
        
        # ------------------------------------------
        if [[ $STEP_DEPLOYED == 1 ]]; then
            rm -rf $STORAGE/bin
            rm -rf $STORAGE/include
            rm -rf $STORAGE/lib
            return 0
        fi
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/glslang ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ###################################### Special X11 Dependency ######################################

# Function: 编译安装(Compile Install) fixesproto-5.0
# ##################################################
function Compile_Install_fixesproto_5_0() {

    if [[ ! -d "/opt/fixesproto-5.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( fixesproto-5.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/fixesproto-5.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/fixesproto-5.0 && ./configure --prefix=/opt/fixesproto-5.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/fixesproto-5.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/fixesproto-5.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/fixesproto-5.0/lib/pkgconfig/fixesproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/fixesproto-5.0/ /opt/sandbox-X11/
            # ......................................
            # fixesproto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/fixesproto-5.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/fixesproto-5.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXfixes-5.0.3
# ##################################################
function Compile_Install_libXfixes_5_0_3() {

    if [[ ! -d "/opt/libXfixes-5.0.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXfixes-5.0.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXfixes-5.0.3.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXfixes-5.0.3 && ./configure --prefix=/opt/libXfixes-5.0.3 \
                                                   PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                   STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXfixes-5.0.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXfixes-5.0.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXfixes-5.0.3/lib/pkgconfig/xfixes.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXfixes-5.0.3/ /opt/sandbox-X11/
            # ......................................
            # libXfixes 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXfixes-5.0.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXfixes-5.0.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxshmfence-1.3
# ##################################################
function Compile_Install_libxshmfence_1_3() {

    if [[ ! -d "/opt/libxshmfence-1.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libxshmfence-1.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libxshmfence_1.3.orig.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxshmfence-1.3 && ./configure --prefix=/opt/libxshmfence-1.3 \
                                                    PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                    STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libxshmfence-1.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libxshmfence-1.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxshmfence-1.3/lib/pkgconfig/xshmfence.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libxshmfence-1.3/ /opt/sandbox-X11/
            # ......................................
            # libxshmfence 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxshmfence-1.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxshmfence-1.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) glproto-1.4.17
# ##################################################
function Compile_Install_glproto_1_4_17() {

    if [[ ! -d "/opt/glproto-1.4.17" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( glproto-1.4.17 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/glproto-1.4.17.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/glproto-1.4.17 && ./configure --prefix=/opt/glproto-1.4.17 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/glproto-1.4.17/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/glproto-1.4.17/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/glproto-1.4.17/lib/pkgconfig/glproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/glproto-1.4.17/ /opt/sandbox-X11/
            # ......................................
            # glproto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/glproto-1.4.17 && return 0
    else
    
        echo "[Caution] Path: ( /opt/glproto-1.4.17 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) dri2proto-2.8
# ##################################################
function Compile_Install_dri2proto_2_8() {

    if [[ ! -d "/opt/dri2proto-2.8" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( dri2proto-2.8 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/dri2proto-2.8.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/dri2proto-2.8 && ./configure --prefix=/opt/dri2proto-2.8 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/dri2proto-2.8/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/dri2proto-2.8/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/dri2proto-2.8/lib/pkgconfig/dri2proto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/dri2proto-2.8/ /opt/sandbox-X11/
            # ......................................
            # dri2proto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/dri2proto-2.8 && return 0
    else
    
        echo "[Caution] Path: ( /opt/dri2proto-2.8 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) xf86vidmodeproto-2.3
# ##################################################
function Compile_Install_xf86vidmodeproto_2_3() {

    if [[ ! -d "/opt/xf86vidmodeproto-2.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xf86vidmodeproto-2.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/xf86vidmodeproto-2.3.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xf86vidmodeproto-2.3 && ./configure --prefix=/opt/xf86vidmodeproto-2.3 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/xf86vidmodeproto-2.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/xf86vidmodeproto-2.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/xf86vidmodeproto-2.3/lib/pkgconfig/xf86vidmodeproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/xf86vidmodeproto-2.3/ /opt/sandbox-X11/
            # ......................................
            # xf86vidmodeproto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xf86vidmodeproto-2.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xf86vidmodeproto-2.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXxf86vm-1.1.4
# ##################################################
function Compile_Install_libXxf86vm_1_1_4() {

    if [[ ! -d "/opt/libXxf86vm-1.1.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXxf86vm-1.1.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXxf86vm-1.1.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXxf86vm-1.1.4 && ./configure --prefix=/opt/libXxf86vm-1.1.4 \
                                                    PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                    STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXxf86vm-1.1.4/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXxf86vm-1.1.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXxf86vm-1.1.4/lib/pkgconfig/xxf86vm.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXxf86vm-1.1.4/ /opt/sandbox-X11/
            # ......................................
            # libXxf86vm 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXxf86vm-1.1.4 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXxf86vm-1.1.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) randrproto-1.5.0
# ##################################################
function Compile_Install_randrproto_1_5_0() {

    if [[ ! -d "/opt/randrproto-1.5.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( randrproto-1.5.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/randrproto-1.5.0.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/randrproto-1.5.0 && ./configure --prefix=/opt/randrproto-1.5.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/randrproto-1.5.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/randrproto-1.5.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/randrproto-1.5.0/lib/pkgconfig/randrproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/randrproto-1.5.0/ /opt/sandbox-X11/
            # ......................................
            # randrproto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/randrproto-1.5.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/randrproto-1.5.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXrandr-1.5.2
# ##################################################
function Compile_Install_libXrandr_1_5_2() {

    if [[ ! -d "/opt/libXrandr-1.5.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXrandr-1.5.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXrandr-1.5.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXrandr-1.5.2 && ./configure --prefix=/opt/libXrandr-1.5.2 \
                                                   PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                   STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXrandr-1.5.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXrandr-1.5.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXrandr-1.5.2/lib/pkgconfig/xrandr.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXrandr-1.5.2/ /opt/sandbox-X11/
            # ......................................
            # libXrandr 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXrandr-1.5.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXrandr-1.5.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### Mesa - 23.3.6 ##########################################

# Function: 编译安装(Compile Install) mesa-23.3.6
# ##################################################
function Compile_Install_Mesa_23_3_6() {

    # Kernel Configuration
    # Enable the following options in the kernel configuration and recompile the kernel if necessary:
    # 内核配置
    # 在内核配置中启用以下选项, 并在必要时重新编译内核:
    #     Device Drivers --->
    #       Graphics support --->
    #         <*/M>   Direct Rendering Manager (XFree86 4.1.0 and higher DRI support) --->
    #                                                                           ...  [DRM]
    #         # For r300 or r600:
    #         < /*/M> ATI Radeon                                              [DRM_RADEON]
    #         # For radeonsi:
    #         < /*/M> AMD GPU                                                 [DRM_AMDGPU]
    #         [*]       Enable amdgpu support for SI parts                 [DRM_AMDGPU_SI]
    #         [*]       Enable amdgpu support for CIK parts               [DRM_AMDGPU_CIK]
    #           Display Engine Configuration --->
    #           [*]   AMD DC - Enable new display engine                      [DRM_AMD_DC]
    #         # For nouveau:
    #         < /*/M> Nouveau (NVIDIA) cards                                 [DRM_NOUVEAU]
    #         # For i915, crocus, or iris:
    #         < /*/M> Intel 8xx/9xx/G3x/G4x/HD Graphics                         [DRM_I915]
    #         # For swrast:
    #         < /*/M> Virtual GEM provider                                      [DRM_VGEM]
    #         # For svga:
    #         < /*/M> DRM driver for VMware Virtual GPU                       [DRM_VMWGFX]
    
    # NOTE:
    # 
    # The corresponding Mesa Gallium3D driver name is provided as the comment for the configuration entries. If you don't know the name of the Mesa Gallium3D driver for your GPU, see Mesa Gallium3D Drivers below.
    # (相应的 Mesa Gallium3D 驱动程序名称作为配置条目的注释提供。如果您不知道 GPU 的 Mesa Gallium3D 驱动程序的名称, 请参阅下面的 Mesa Galium3D 驱动器。)
    # 
    # CONFIG_DRM_RADEON, CONFIG_DRM_AMDGPU, CONFIG_DRM_NOUVEAU, and CONFIG_DRM_I915 may require firmware. See About Firmware for details.
    # (CONFIG_DRM_RADEON, CONFIG_DRM_AMDGPU, CONFIG_DRM_NOUVEAU 和 CONFIG_DRM_I915 可能需要固件。有关详细信息, 请参阅关于固件。)
    # 
    # Selecting CONFIG_DRM_RADEON or CONFIG_DRM_AMDGPU as "y" is not recommended. If it is, any required firmware must be built as a part of the kernel image or the initramfs for the driver to function correctly.
    # (不建议将 CONFIG_DRM_RADEON 或 CONFIG_DRM_AMDGPU 选择为 "y"。如果是, 则必须将任何所需的固件构建为内核映像或 initramfs 的一部分, 以便驱动程序正常工作。)
    # 
    # The sub-entries under CONFIG_DRM_AMDGPU are used to ensure the AMDGPU kernel driver supports all GPUs using the radeonsi driver. They are not needed if you won't need CONFIG_DRM_AMDGPU itself. They may be unneeded for some GPU models.
    # CONFIG_DRM_AMDGPU 下的子条目用于确保 AMDGPU 内核驱动程序支持使用 radeonsi 驱动程序的所有 GPU。如果不需要 CONFIG_DRM_AMDGPU 本身, 则不需要它们。对于某些 GPU 型号来说, 它们可能是不需要的。
    # 
    # For swrast, CONFIG_DRM_VGEM is not strictly needed but recommended as an optimization.
    # 对于 swrast, CONFIG_DRM_VGEM 不是严格需要的, 但建议作为优化。

    if [[ ! -d "/opt/mesa-23.3.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_NINJA=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( mesa-23.3.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/mesa-23.3.6.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --buildtype=release: This switch ensures a fully-optimized build, and disables debug assertions which will severely slow down the libraries in certain use-cases. Without this switch, build sizes can span into the 2GB range.
        #                                 此选项确保了完全优化的构建, 并禁用调试断言, 这将在某些用例中严重降低库的运行速度。如果没有此交换机, 构建大小可以扩展到 2GB 范围。
        # ..........................................
        # *  Option: -Dgallium-drivers=auto: This parameter controls which Gallium3D drivers should be built.
        #                                    auto selects all Gallium3D drivers available for x86: 
        #                                        r300 (for ATI Radeon 9000 or Radeon X series),
        #                                        r600 (for AMD/ATI Radeon HD 2000-6000 series),
        #                                        radeonsi (for AMD Radeon HD 7000 or newer AMD GPU models),
        #                                        nouveau (for Supported NVIDIA GPUs, they are listed as all "3D features" either "DONE" or "N/A" in the Nouveau status page),
        #                                        virgl (for QEMU virtual GPU with virglrender support; note that BLFS qemu-8.1.0 is not built with virglrender),
        #                                        svga (for VMWare virtual GPU),
        #                                        swrast (using CPU for 3D rasterisation; note that it's much slower than using a modern 3D-capable GPU, so it should be only used if the GPU is not supported by other drivers),
        #                                        iris (for Intel GPUs shipped with Broadwell or newer CPUs),
        #                                        crocus (for Intel GMA 3000, X3000 series, 4000 series, or X4000 series GPUs shipped with chipsets, or Intel HD GPUs shipped with pre-Broadwell CPUs),
        #                                        i915 (for Intel GMA 900, 950, 3100, or 3150 GPUs shipped with chipsets or Atom D/N 4xx/5xx CPUs).
        #                                    You may replace auto with a comma-separated list to build only a subset of these drivers if you precisely know which drivers you need, for example -Dgallium-drivers=radeonsi,iris,swrast.
        #                                    此参数控制应构建哪些 Gallium3D 驱动程序。
        #                                    自动选择所有适用于 x86 的 Gallium3D 驱动程序：
        #                                        r300 (用于 ATI Radeon 9000 或 Radeon X 系列), 
        #                                        r600 (用于 AMD/ATI Radeon HD 2000-6000 系列), 
        #                                        radeonsi (适用于 AMD Radeon HD 7000 或更新的 AMD GPU 型号), 
        #                                        nouveau (对于支持的 NVIDIA GPU, 在 Nouveau 状态页中它们被列为所有 "3D 功能" ("DONE" 或 "N/A")), 
        #                                        virgl (用于支持 virglrender 的 QEMU 虚拟 GPU; 请注意, BLFS QEMU-81.1.0 不是使用 virglrend 构建的), 
        #                                        svga (用于 VMWare 虚拟 GPU), 
        #                                        swrast (使用 CPU 进行 3D 光栅化; 请注意, 它比使用现代 3D GPU 慢得多, 因此只有在其他驱动程序不支持 GPU 的情况下才能使用), 
        #                                        iris (用于 Broadwell 或更新 CPU 附带的 Intel GPU), 
        #                                        crocus (适用于芯片组附带的 Intel GMA 3000, X3000 系列, 4000 系列或 X4000 系列 GPU, 或 Broadwell CPU 之前附带的 Intel HD GPU), 
        #                                        i915 (适用于芯片组或 Atom D/N 4xx/5xx CPUs 附带的英特尔 GMA 900, 950, 3100, 或 3150 GPUs)。
        #                                    如果你确切地知道你需要哪些驱动程序, 你可以用逗号分隔的列表来代替auto, 只构建这些驱动程序的一个子集, 例如-Dgala drivers=radeonsi, iris, swrast。
        # ..........................................
        # *  Option: -Dplatforms="...": This parameter controls which windowing systems will be supported. Available linux platforms are x11 and wayland.
        #                               此参数控制将支持哪些窗口系统。可用的 linux 平台有 x11 和 wayland。
        # ..........................................
        # *  Option: -Dvulkan-drivers="": This switch allows choosing which Vulkan drivers are built. The default is auto, but this requires the optional dependencies glslang and Vulkan-Loader. 
        #                                 Vulkan is a newer API designed for utilizing the GPUs with a performance better than OpenGL, but nothing in BLFS benefits from it for now.
        #                                 So we pass an empty list in order to remove the need for these dependencies.
        #                                 此选项允许选择构建的 Vulkan 驱动程序。默认为 auto, 但这需要可选的依赖关系 glslang 和 Vulkan Loader。
        #                                 Vulkan 是一款新的 API, 专为使用 GPU 而设计, 其性能优于 OpenGL, 但 BLFS 目前没有从中受益。
        #                                 因此, 我们传递一个空列表, 以消除对这些依赖项的需求。
        # ..........................................
        # *  Option: -Dvalgrind=disabled: This parameter disables the usage of Valgrind during the build process. Remove this parameter if you have Valgrind installed, and wish to check for memory leaks.
        #                                 此参数禁止在构建过程中使用 Valgrind。如果已经安装了 Valgrind 并希望检查内存是否泄漏, 请移除此参数。
        # ..........................................
        # *  Option: -Dlibunwind=disabled: This parameter disables the usage of libunwind.
        #                                  此参数可禁用 libunwind 的使用。
        # ..........................................
        # *  Option: meson configure -Dbuild-tests=true: This command will reconfigure the build to set -Dbuild-tests=true, but keep the other options specified in the meson setup command unchanged.
        #                                                It allows ninja test to build and run unit tests.
        #                                                此命令将重新配置生成以设定 -Dbuild-tests=true, 但保持 Meson 设置命令中指定的其他选项不变。
        #                                                它允许 ninja 测试构建和运行单元测试。
        # ..........................................
        # *  Option: -Degl-native-platform="...": This parameter controls which Embedded Graphics Library support will be built. Available linux options are auto (default), x11, wayland, surfaceless, and drm.
        #                                         此参数控制将构建哪些嵌入式图形库支持。可用的 linux 选项有 auto (默认), x11, wayland, surfaceless 和 drm。
        # ..........................................
        # * Problem: Run-time dependency LLVM (modules: amdgpu, bitreader, bitwriter, core, engine, executionengine, instcombine, ipo, mcdisassembler, mcjit, native, scalaropts, transformutils, coroutines, lto) found: NO (tried config-tool)
        #            Looking for a fallback subproject for the dependency llvm (modules: bitwriter, engine, mcdisassembler, mcjit, core, executionengine, scalaropts, transformutils, instcombine, amdgpu, bitreader, ipo, native)
        #            Building fallback subproject with default_library=shared
        #            meson.build:1714:2: ERROR: Neither a subproject directory nor a llvm.wrap file was found.
        #   - Solve: meson build Add -Dshared-llvm=disabled -Dcpp_rtti=false
        # ..........................................
        cd $STORAGE/mesa-23.3.6 && meson build/ --prefix=/opt/mesa-23.3.6 \
                                                --buildtype=release \
                                                -Dplatforms=x11,wayland \
                                                -Dgallium-drivers=swrast \
                                                -Dvulkan-drivers="" \
                                                -Dvalgrind=disabled \
                                                -Dlibunwind=disabled \
                                                -Dshared-llvm=disabled \
                                                -Dcpp_rtti=false \
                                                --pkg-config-path="/opt/lib/pkgconfig" && \
                                                STEP_BUILDED=1

        # ------------------------------------------
        cd $STORAGE/mesa-23.3.6 && ninja && STEP_NINJA=1
                                                
        # ------------------------------------------
        # To test the results, issue: "meson configure -Dbuild-tests=true && ninja test". Three tests related to mesa:intel are known to fail.
        # 要测试结果, 请使用指令："meson configure -Dbuild-tests=true && ninja test"。与 mesa:intel 相关的三项测试都失败了。
        
        # ------------------------------------------
        cd $STORAGE/mesa-23.3.6 && ninja -C build install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # If desired, install the optional documentation by running the following commands as the root user:
        # 如果需要, 请以 root 用户身份运行以下命令来安装可选文档:
        # install -v -dm755 /usr/share/doc/mesa-23.1.6 &&
        # cp -rfv ../docs/* /usr/share/doc/mesa-23.1.6
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/mesa-23.3.6/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/mesa-23.3.6/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/mesa-23.3.6/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # Mesa 属于 OpenGL 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/graphics/OpenGL/include
            #    /opt/graphics/OpenGL/lib
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/mesa-23.3.6 && return 0
    else
    
        echo "[Caution] Path: ( /opt/mesa-23.3.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ######################################### freeGlut - 3.4.0 #########################################

# Function: 编译安装(Compile Install) libXi-1.7.6
# ##################################################
function Compile_Install_libXi_1_7_6() {

    if [[ ! -d "/opt/libXi-1.7.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXi-1.7.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXi-1.7.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXi-1.7.6 && ./configure --prefix=/opt/libXi-1.7.6 \
                                               PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXi-1.7.6/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXi-1.7.6/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXi-1.7.6/lib/pkgconfig/xi.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXi-1.7.6/ /opt/sandbox-X11/
            # ......................................
            # libXi 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXi-1.7.6 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXi-1.7.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) GLU-9.0.3
# ##################################################
function Compile_Install_GLU_9_0_3() {

    if [[ ! -d "/opt/glu-9.0.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( glu-9.0.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/glu-9.0.3.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/glu-9.0.3 && meson build/ --prefix=/opt/glu-9.0.3 \
                                              --buildtype=release \
                                              -Dgl_provider=gl \
                                              --pkg-config-path="/opt/lib/pkgconfig" && \
                                              STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/glu-9.0.3 && ninja -C build install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # After installation is completed, as the root user:
        # rm -vf /usr/lib/libGLU.a
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/glu-9.0.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/glu-9.0.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/glu-9.0.3/lib/pkgconfig/glu.pc /opt/lib/pkgconfig/
            # ......................................
            # GLU 属于 OpenGL 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/graphics/OpenGL/include
            #    /opt/graphics/OpenGL/lib
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/glu-9.0.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/glu-9.0.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) freeGlut-3.4.0
# ##################################################
function Build_Install_freeGlut_3_4_0() {

    # freeGLUT Require: Mesa
    # ----------------------------------------------
    # freeGLUT 是 GLUT (OpenGL Utility Toolkit) 的一个免费开源替代库。在程序中负责创建窗口, 初始化 OpenGL 上下文和处理输入事件所需的所有系统特定的杂务, 从而允许创建真正可移植的 OpenGL 程序。
    # GLUT 最初是 <<OpenGL 红皮书 (第二版)>> (Mark Kilgard 著) 中的示例程序。自那以后, GLUT 简单, 跨平台的特点, 使其在各种实际应用中广泛应用。

    if [[ ! -d "/opt/freeglut-3.4.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( freeglut-3.4.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/freeglut-3.4.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i "3i SET(CMAKE_INCLUDE_PATH /opt/sandbox-X11/include /opt/mesa-23.3.6/include)" $STORAGE/freeglut-3.4.0/CMakeLists.txt
            sed -i "4i SET(CMAKE_LIBRARY_PATH /opt/sandbox-X11/lib /opt/mesa-23.3.6/lib)" $STORAGE/freeglut-3.4.0/CMakeLists.txt
        fi
        
        # ------------------------------------------
        mkdir $STORAGE/freeglut-3.4.0/build && STEP_CREATED=1
        
        # ------------------------------------------
        # *  Option: -DFREEGLUT_BUILD_DEMOS=OFF: Disable building optional demo programs. Note that if you choose to build them, their installation must be done manually.
        #                                        The demo programs are limited and installation is not recommended.
        #                                        禁用构建可选演示程序。请注意, 如果您选择构建它们, 则必须手动完成它们的安装。
        #                                        演示程序是有限的, 不建议安装。
        # ..........................................
        # *  Option: -DFREEGLUT_BUILD_STATIC_LIBS=OFF: Do not build the static library.
        #                                              不要构建静态库。
        # ..........................................
        # * Problem: CMake Error at CMakeLists.txt:277 (MESSAGE):
        #              Missing X11's XInput2.h (X11/extensions/XInput2.h)
        #   - Solve: libXi 的路径查找问题, 只把 libXi 的 include 内文件复制到系统路径如 /usr/local/include 仍不能解决, 还需要把 lib 内文件复制到系统路径如 /usr/local/lib
        # ..........................................
        # * Problem: [  2%] Building C object CMakeFiles/freeglut.dir/src/fg_callbacks.c.o
        #            In file included from /home/goufeng/freeglut-3.4.0/include/GL/freeglut.h:17:0,
        #                             from /home/goufeng/freeglut-3.4.0/src/fg_callbacks.c:28:
        #            /home/goufeng/freeglut-3.4.0/include/GL/freeglut_std.h:144:13: fatal error: GL/glu.h: No such file or directory
        #             #   include <GL/glu.h>
        #                         ^~~~~~~~~~
        #            compilation terminated.
        #   - Solve: The include file <GL/glu.h> is part of "libGLU" package. Install "GLU-9.x.x"
        # ..........................................
        # * Problem: CMake Error at /opt/cmake-3.28.3/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
        #              Could NOT find X11 (missing: X11_X11_LIB)
        #   - Solve: 根据 CMakeLists.txt 中 "FIND_PACKAGE(X11 REQUIRED)" 可知, 查找 X11 路径的信息保存在 "/opt/cmake-3.28.3/share/cmake-3.28/Modules/FindX11.cmake"。
        #            ...............................
        #            方法1. 修改 .cmake 文件 (不推荐)
        #                在 "X11_INC_SEARCH_PATH" 变量中加入 X11 的头文件实际路径, 形如 "set(X11_INC_SEARCH_PATH 路径1 路径2 /opt/sandbox-X11/include)"。
        #                在 "X11_LIB_SEARCH_PATH" 变量中加入 X11 的库文件实际路径, 形如 "set(X11_LIB_SEARCH_PATH 路径1 路径2 /opt/sandbox-X11/lib)"。
        #            ...............................
        #            方法2. 使用 "CMAKE_INCLUDE_PATH" 和 "CMAKE_LIBRARY_PATH" 环境变量 (推荐)
        #                要添加的头文件查找路径只有一个, 只需要在编译时使用 "-DCMAKE_INCLUDE_PATH=/opt/sandbox-X11/include"。
        #                要添加的库文件查找路径只有一个, 只需要在编译时使用 "-DCMAKE_LIBRARY_PATH=/opt/sandbox-X11/lib"。
        #                要添加的头文件查找路径有很多, 则需要在 CMakeLists.txt 中的 PROJECT(freeglut C) 之后配置变量, 如:
        #                    SET(CMAKE_INCLUDE_PATH /opt/sandbox-X11/include /opt/mesa-23.3.6/include)
        #                要添加的库文件查找路径有很多, 则需要在 CMakeLists.txt 中的 PROJECT(freeglut C) 之后配置变量, 如:
        #                    SET(CMAKE_LIBRARY_PATH /opt/sandbox-X11/lib /opt/mesa-23.3.6/lib)
        cd $STORAGE/freeglut-3.4.0/build && cmake -G "Unix Makefiles" \
                                                  -DCMAKE_INSTALL_PREFIX=/opt/freeglut-3.4.0 \
                                                  -DCMAKE_BUILD_TYPE=Release \
                                                  -DFREEGLUT_BUILD_DEMOS=OFF \
                                                  -DFREEGLUT_BUILD_STATIC_LIBS=OFF \
                                                  -Wno-dev \
                                                  ../ && STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/freeglut-3.4.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/freeglut-3.4.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/freeglut-3.4.0/lib/pkgconfig/glut.pc /opt/lib/pkgconfig/
            # ......................................
            # freeGLUT 属于 OpenGL 开发套件, 其 CMake 默认可查找路径为:
            #    /opt/graphics/OpenGL/include
            #    /opt/graphics/OpenGL/lib
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/freeglut-3.4.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/freeglut-3.4.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################### GLEW - 2.2.0 ###########################################

# Function: 制作安装(Make Install) GLEW-2.2.0
# ##################################################
function Make_Install_GLEW_2_2_0() {

    # GLEW OpenGL 扩展库是个简单的工具, 用于帮助 C/C++ 开发者初始化扩展 (OpenGL 扩展功能) 并书写可移植的应用程序。GLEW 当前支持各种各样的操作系统, 包含 Windows, Linux, Darwin, Irix 与 Solaris。

    if [[ ! -f "/usr/bin/glewinfo" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CHANGE_DIRECTORY=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Make and Install ( glew-2.2.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/glew-2.2.0.tgz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/glew-2.2.0 && STEP_CHANGE_DIRECTORY=1
        
        # ------------------------------------------
        # * Explain: sed -i 's%lib64%lib%g' ...: This ensures that the library is installed in /usr/lib.
        #                                        这样可以确保库安装在 /usr/lib 中。
        # ..........................................
        # * Explain: sed -i -e '/glew.lib.static:/d' ...: This suppresses the static library.
        #                                                 这将抑制静态库。
        if [[ $STEP_CHANGE_DIRECTORY == 1 ]]; then
            sed -i 's%lib64%lib%g' config/Makefile.linux &&
            sed -i -e '/glew.lib.static:/d' \
                   -e '/0644 .*STATIC/d'    \
                   -e 's/glew.lib.static//' Makefile
        fi
        
        # ------------------------------------------
        # * Explain: make install.all: This installs the programs as well as the library.
        #                              这将安装程序和库。
        make && make install.all && STEP_INSTALLED=1
        
        # ------------------------------------------
        # GLEW 属于 OpenGL 开发套件, 其 CMake 默认可查找路径为:
        #    /opt/graphics/OpenGL/include
        #    /opt/graphics/OpenGL/lib

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/glew-2.2.0 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/bin/glewinfo ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # 1. 创建 OpenGL 项目并测试
    #
    #     (1) 创建 VS 项目, 例如 OpglTest
    #     
    #     (2) 右键项目 -> 属性 -> VC++ 目录 ->
    #     
    #         1) 在 Include 目录添加 .../freeglut/include 和 .../glew/include
    #     
    #         2) 在 Library 目录添加 .../freeglut/lib 和 .../glew/lib
    #     
    #     (3) 新建 OpglTest.cpp 文件, 输入以下代码: 
    #     
    #         #include <GL/glew.h>
    #         #include <GL/freeglut.h>
    #         
    #         void Display()
    #         {
    #             glClear(GL_COLOR_BUFFER_BIT);
    #             glRectf(-0.6f, -0.6f, 0.6f, 0.6f);
    #             glFlush();
    #         }
    #         
    #         int main(int argc, char* argv[])
    #         {
    #             glutInit(&argc, argv);
    #             glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE);
    #             glutInitWindowPosition(100, 100);
    #             glutInitWindowSize(500, 500);
    #             glutCreateWindow("OpenGL test");
    #             glutDisplayFunc(&Display);
    #             glutMainLoop();
    #             return 0;
    #         }
    # 
    # 2. freeglutd.lib 的错误提示处理
    # 
    #     如果弹出错误提示说 "找不到freeglutd.lib文件", 打开 .../freeglut/include/GL/ 目录中的 freeglut_std.h 文件
    #     
    #     找到 pragma comment (lib, "freeglutd.lib"), 改成 pragma comment (lib, "freeglut.lib"), 就是说把末尾的 d 去掉
    #     
    #     重新编译即可。
    
    # ----------- Compilation Environment ----------
    export C_INCLUDE_PATH=/opt/sandbox-X11/include
    export CPLUS_INCLUDE_PATH=/opt/sandbox-X11/include
    # ..............................................
    export LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/mesa-23.3.6/lib
    export LD_LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/mesa-23.3.6/lib

    # ----------------- Dependency -----------------
    Compile_Install_expat_2_5_0
    Build_Install_libdrm_2_4_120
    # ---------------- Mako - 1.1.6 ----------------
    Build_Install_MarkupSafe_1_1_1_by_Python3
    Build_Install_Mako_1_1_6_by_Python3
    # --------------- LLVM >= 15.0.0 ---------------
    Build_Install_LLVM_Project_15_0_7
    # ------------------- Glslang ------------------
    Deploy_glslang_main_linux_Release
    # ----------- Special X11 Dependency -----------
    Compile_Install_fixesproto_5_0
    Compile_Install_libXfixes_5_0_3
    Compile_Install_libxshmfence_1_3
    Compile_Install_glproto_1_4_17
    Compile_Install_dri2proto_2_8
    Compile_Install_xf86vidmodeproto_2_3
    Compile_Install_libXxf86vm_1_1_4
    Compile_Install_randrproto_1_5_0
    Compile_Install_libXrandr_1_5_2
    # ---------------- Mesa - 23.3.6 ---------------
    Compile_Install_Mesa_23_3_6
    # -------------- freeGlut - 3.4.0 --------------
    Compile_Install_libXi_1_7_6
    Compile_Install_GLU_9_0_3
    Build_Install_freeGlut_3_4_0
    # ---------------- GLEW - 2.2.0 ----------------
    Make_Install_GLEW_2_2_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Mesa-23.3.6(OpenGL) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
