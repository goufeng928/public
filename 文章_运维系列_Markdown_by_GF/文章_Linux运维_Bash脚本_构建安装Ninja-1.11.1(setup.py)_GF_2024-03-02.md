# 文章_Linux运维_Bash脚本_构建安装Ninja-1.11.1(setup.py)_GF_2024-03-02

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

cmake-3.28.3.tar.gz

wheel-0.42.0.tar.gz

packaging-23.2.tar.gz

distro-1.9.0.tar.gz

setuptools-41.2.0.zip

setuptools_scm-1.17.0.tar.gz

scikit-build-0.15.0.tar.gz

ninja-1.11.1.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-03 00:05

# --------------------- CMake ----------------------
# Need File: cmake-3.28.3.tar.gz
# ------------ Ninja - 1.11.1 - setup.py -----------
# Need File: wheel-0.42.0.tar.gz
# Need File: packaging-23.2.tar.gz
# Need File: distro-1.9.0.tar.gz
# Need File: setuptools-41.2.0.zip
# Need File: setuptools_scm-1.17.0.tar.gz
# Need File: scikit-build-0.15.0.tar.gz
# Need File: ninja-1.11.1.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################## CMake ###############################################

# Function: 编译安装(Compile Install) CMake-3.28.3
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

# ##################################### Ninja - 1.11.1 - setup.py ####################################

# Function: 构建安装(Build Install) Wheel-0.42.0 (by Python3)
# ##################################################
function Build_Install_Wheel_0_42_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "wheel")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "wheel")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "0.42.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( Wheel-0.42.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/wheel-0.42.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/wheel-0.42.0 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/wheel-0.42.0 && python3 setup.py install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/Python-3.8.0/bin/wheel /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/wheel-0.42.0 && return 0
    else
    
        echo "[Caution] Python Program: ( wheel-0.42.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) Packaging-23.2 (by Python3)
# ##################################################
function Pip_Install_Packaging_23_2_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "packaging")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "packaging")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "23.2")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( packaging-23.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/packaging-23.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/packaging-23.2 && pip3 install . && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/packaging-23.2 && return 0
    else
    
        echo "[Caution] Python Program: ( packaging-23.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: Pip安装(Pip Install) Distro-1.9.0 (by Python3)
# ##################################################
function Pip_Install_Distro_1_9_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "distro")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "distro")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.9.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Pip Install ( distro-1.9.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/distro-1.9.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # 如果项目位于其他目录, 则需要将其路径 "." 替换。
        # pip 工具会根据项目中的 pyproject.toml 文件自动安装相应的依赖项。
        cd $STORAGE/distro-1.9.0 && pip3 install . && STEP_INSTALLED=1
        
        # ------------------------------------------
        # * Caution: 安装 Distro, 其实就是让系统在需要的时候能找到 Distro 这个二进制文件并运行。
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf $STORAGE/ninja-1.11.1/distro /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/distro-1.9.0 && return 0
    else
    
        echo "[Caution] Python Program: ( distro-1.9.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) SetupTools-41.2.0 (by Python3)
# ##################################################
function Build_Install_SetupTools_41_2_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "setuptools")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "setuptools")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "41.2.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( packaging-23.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        unzip $STORAGE/setuptools-41.2.0.zip && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/setuptools-41.2.0 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/setuptools-41.2.0 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/setuptools-41.2.0 && return 0
    else
    
        echo "[Caution] Python Program: ( setuptools-41.2.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) SetupTools-SCM-1.17.0 (by Python3)
# ##################################################
function Build_Install_SetupTools_SCM_1_17_0_by_Python3() {

    # * Caution: 安装 SetupTools-SCM-1.17.0 完成后, 其版本号为 0.0.0 而不是 1.17.0。

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "setuptools-scm")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "setuptools-scm")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.17.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( setuptools-scm-1.17.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/setuptools_scm-1.17.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/setuptools_scm-1.17.0 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/setuptools_scm-1.17.0 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/setuptools_scm-1.17.0 && return 0
    else
    
        echo "[Caution] Python Program: ( setuptools-scm-1.17.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Scikit-Build-0.15.0 (by Python3)
# ##################################################
function Build_Install_Scikit_Build_0_15_0_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "scikit-build")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "scikit-build")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "0.0.0")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( scikit-build-0.15.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/scikit-build-0.15.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/scikit-build-0.15.0 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/scikit-build-0.15.0 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/scikit-build-0.15.0 && return 0
    else
    
        echo "[Caution] Python Program: ( scikit-build-0.15.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Ninja-1.11.1-by-Py-Setup (by Python3)
# ##################################################
function Build_Install_Ninja_1_11_1_by_Py_Setup_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "ninja")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "ninja")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "1.11.1")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        # Ninja 工具一般配合 Meson 工具使用。
        # Meson 可以使用 Python 的 Pip 工具安装: pip install --user meson
        # Meson 可以从源码进行构建安装: python3 setup.py build 以及 python3 setup.py install
        # Ninja 可以使用 Python 的 Pip 工具安装: pip install --user ninja
        # Ninja 可以从源码进行构建安装: python3 setup.py build 以及 python3 setup.py install (需要下载含有 setup.py 的源码包)
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( ninja-1.11.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/ninja-1.11.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 && ! -f "$STORAGE/ninja-1.11.1/setup.py" ]]; then
            echo "[Caution] Python Source Code: ( ninja-1.11.1.tar.gz ) is Not installing Through ( setup.py )."
            # ......................................
            exit 1
        fi
        
        # ------------------------------------------
        cd $STORAGE/ninja-1.11.1 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/ninja-1.11.1 && python3 setup.py install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # * Caution: 安装 Ninja, 其实就是让系统在需要的时候能找到 Ninja 这个二进制文件并运行。
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf $STORAGE/ninja-1.11.1/ninja /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ninja-1.11.1 && return 0
    else
    
        echo "[Caution] Python Program: ( ninja-1.11.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ------------------- CMake --------------------
    Compile_Install_CMake_3_28_3
    # ---------- Ninja - 1.11.1 - setup.py ---------
    Build_Install_Wheel_0_42_0_by_Python3
    Pip_Install_Packaging_23_2_by_Python3
    Pip_Install_Distro_1_9_0_by_Python3
    Build_Install_SetupTools_41_2_0_by_Python3
    Build_Install_SetupTools_SCM_1_17_0_by_Python3
    Build_Install_Scikit_Build_0_15_0_by_Python3
    Build_Install_Ninja_1_11_1_by_Py_Setup_by_Python3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装Ninja-1.11.1(setup.py) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
