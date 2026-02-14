# 文章_Linux运维_Bash脚本_构建安装Systemd-250_GF_2023-03-15

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

libcap-2.68.tar.xz

MarkupSafe-1.1.1.tar.gz

Jinja2-2.9.6.tar.gz

automake-1.16.tar.gz (Maybe Not Necessary)

util-linux-2.39.3.tar.xz

systemd-250.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-15 12:55

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.14.0 (Maybe Not Necessary)
# * Python == 3.x.x
# * Meson
# * Ninja

# ------------------- Dependency -------------------
# Need File: libcap-2.68.tar.xz
# --------------------- Jinja2 ---------------------
# Need File: MarkupSafe-1.1.1.tar.gz
# Need File: Jinja2-2.9.6.tar.gz
# ------------------- util-linux -------------------
# Need File: automake-1.16.tar.gz (Maybe Not Necessary)
# Need File: util-linux-2.39.3.tar.xz
# ----------------- Systemd - 250 ------------------
# Need File: systemd-250.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 制作安装(Make Install) libcap-2.68
# ##################################################
function Make_Install_libcap_2_68() {

    if [[ ! -d "/opt/libcap-2.68" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_MADE=0
        local STEP_INSTALLED=0
        local STEP_COPIED=0
        
        # ------------------------------------------
        echo "[Confirm] Make and Install ( libcap-2.68 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -Jxvf $STORAGE/libcap-2.68.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libcap-2.68 && make && STEP_MADE=1
        
        # ------------------------------------------
        # default installs the library libcap.XX.Y in /lib[64]/
        # the binaries in /sbin/
        # the header files in /usr/include
        # the {libcap,libpsx}.pc files in /usr/lib[64]/pkgconfig
        # the Go packages (if built) under /usr/share/gocode/src
        # ..........................................
        # Skip # cd $STORAGE/libcap-2.68 && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_MADE == 1 ]]; then
            if [[ ! -d "/opt/libcap-2.68" ]]; then mkdir /opt/libcap-2.68; fi
            if [[ ! -d "/opt/libcap-2.68/include" ]]; then mkdir /opt/libcap-2.68/include; fi
            if [[ ! -d "/opt/libcap-2.68/lib" ]]; then mkdir /opt/libcap-2.68/lib; fi
            if [[ ! -d "/opt/libcap-2.68/lib/pkgconfig" ]]; then mkdir /opt/libcap-2.68/lib/pkgconfig; fi
            # ......................................
            rsync -av $STORAGE/libcap-2.68/libcap/include/ /opt/libcap-2.68/include/
            # ......................................
            rm -f /opt/libcap-2.68/include/sys/psx_syscall.h && \
            cp -vf $STORAGE/libcap-2.68/psx/psx_syscall.h /opt/libcap-2.68/include/sys/
            # ......................................
            cp -vf $STORAGE/libcap-2.68/libcap/libcap.a       /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libcap.so      /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libcap.so.2    /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libcap.so.2.68 /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libpsx.a       /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libpsx.so      /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libpsx.so.2    /opt/libcap-2.68/lib/
            cp -vf $STORAGE/libcap-2.68/libcap/libpsx.so.2.68 /opt/libcap-2.68/lib/
            # ......................................
            cp -vf $STORAGE/libcap-2.68/libcap/libcap.pc /opt/libcap-2.68/lib/pkgconfig/
            cp -vf $STORAGE/libcap-2.68/libcap/libpsx.pc /opt/libcap-2.68/lib/pkgconfig/
            # ......................................
            sed -i "s%prefix\=/usr%prefix\=/opt/libcap-2.68%" /opt/libcap-2.68/lib/pkgconfig/libcap.pc
            sed -i "s%libdir\=/lib64%libdir\=\$\{prefix\}/lib%" /opt/libcap-2.68/lib/pkgconfig/libcap.pc
            sed -i "s%includedir\=/usr/include%includedir\=\$\{prefix\}/include%" /opt/libcap-2.68/lib/pkgconfig/libcap.pc
            # ......................................
            sed -i "s%prefix\=/usr%prefix\=/opt/libcap-2.68%" /opt/libcap-2.68/lib/pkgconfig/libpsx.pc
            sed -i "s%libdir\=/lib64%libdir\=\$\{prefix\}/lib%" /opt/libcap-2.68/lib/pkgconfig/libpsx.pc
            sed -i "s%includedir\=/usr/include%includedir\=\$\{prefix\}/include%" /opt/libcap-2.68/lib/pkgconfig/libpsx.pc
            # ......................................
            STEP_COPIED=1
        fi
        
        # ------------------------------------------
        if [[ $STEP_COPIED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libcap-2.68/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libcap-2.68/lib/ /usr/local/lib/
            # ......................................
            cp -vf /opt/libcap-2.68/lib/pkgconfig/libcap.pc /opt/lib/pkgconfig/
            cp -vf /opt/libcap-2.68/lib/pkgconfig/libpsx.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libcap-2.68 && return 0
    else
        echo "[Caution] Path: ( /opt/libcap-2.68 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################## Jinja2 ##############################################

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

# Function: 构建安装(Build Install) Jinja2-2.9.6 (by Python3)
# ##################################################
function Build_Install_Jinja2_2_9_6_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    # ..............................................
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "Jinja2")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "Jinja2")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "2.9.6")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( Jinja2-2.9.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/Jinja2-2.9.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/Jinja2-2.9.6 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/Jinja2-2.9.6 && python3 setup.py install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/Jinja2-2.9.6 && return 0
    else
    
        echo "[Caution] Python Program: ( Jinja2-2.9.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################ util-linux ############################################

# Function: 编译安装(Compile Install) automake-1.16
# ##################################################
function Compile_Install_automake_1_16() {

    if [[ ! -d "/opt/automake-1.16" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( automake-1.16 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf automake-1.16.tar.gz && STEP_UNZIPPED=1

        # ------------------------------------------
        cd $STORAGE/automake-1.16 && ./configure --prefix=/opt/automake-1.16 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/automake-1.16/bin/aclocal       /usr/local/bin/
            ln -sf /opt/automake-1.16/bin/aclocal-1.16  /usr/local/bin/
            ln -sf /opt/automake-1.16/bin/automake      /usr/local/bin/
            ln -sf /opt/automake-1.16/bin/automake-1.16 /usr/local/bin/
        fi
        # ..........................................
        if [[ $STEP_INSTALLED == 1 && -d "/opt/libtool-2.4.6" ]]; then
            cp -vf /opt/libtool-2.4.6/share/aclocal/*.m4 /opt/automake-1.16/share/aclocal/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/automake-1.16 && return 0
    else
    
        echo "[Caution] Path: ( /opt/automake-1.16 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) util-linux-2.39.3
# ##################################################
function Compile_Install_util_linux_2_39_3() {

    # util-linux-2.39.3 Provide: blkid           (Sys Binary File)
    # util-linux-2.39.3 Provide: fdisk           (Sys Binary File)
    # util-linux-2.39.3 Provide: mount           (Binary File)
    # util-linux-2.39.3 Provide: uuidd           (Sys Binary File)
    # util-linux-2.39.3 Provide: libblkid.a      (Static Libraries)
    # util-linux-2.39.3 Provide: libblkid.so     (Shared Libraries)
    # util-linux-2.39.3 Provide: libfdisk.a      (Static Libraries)
    # util-linux-2.39.3 Provide: libfdisk.so     (Shared Libraries)
    # util-linux-2.39.3 Provide: libmount.a      (Static Libraries)
    # util-linux-2.39.3 Provide: libmount.so     (Shared Libraries)
    # util-linux-2.39.3 Provide: libsmartcols.a  (Static Libraries)
    # util-linux-2.39.3 Provide: libsmartcols.so (Shared Libraries)
    # util-linux-2.39.3 Provide: libuuid.a       (Static Libraries)
    # util-linux-2.39.3 Provide: libuuid.so      (Shared Libraries)

    if [[ ! -d "/opt/util-linux-2.39.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( util-linux-2.39.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -Jxvf $STORAGE/util-linux-2.39.3.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # First, disable a problematic test:
        # 首先, 禁用有问题的测试:
        #     sed -i '/test_mkfds/s/^/#/' tests/helpers/Makemodule.am
        # Skip # sed -i '/test_mkfds/s/^/#/' $STORAGE/util-linux-2.39.3/tests/helpers/Makemodule.am
        
        # ------------------------------------------
        # 1. Installation of Util-linux:
        # 
        #     ./configure --bindir=/usr/bin    \
        #                 --libdir=/usr/lib    \
        #                 --runstatedir=/run   \
        #                 --sbindir=/usr/sbin  \
        #                 --disable-chfn-chsh  \
        #                 --disable-login      \
        #                 --disable-nologin    \
        #                 --disable-su         \
        #                 --disable-setpriv    \
        #                 --disable-runuser    \
        #                 --disable-pylibmount \
        #                 --disable-static     \
        #                 --without-python     \
        #                 --without-systemd    \
        #                 --without-systemdsystemunitdir        \
        #                 ADJTIME_PATH=/var/lib/hwclock/adjtime \
        #                 --docdir=/usr/share/doc/util-linux-2.39.3
        #     The --disable and --without options prevent warnings about building components that either require packages not in LFS, or are inconsistent with programs installed by other packages.
        #     --disable 和 --without 选项可防止有关构建组件的警告, 这些组件要么需要不在 LFS 中的程序包, 要么与其他程序包安装的程序不一致。
        # ..........................................
        # 2. Installation of Util-linux - 32-bit:
        #     Move a tool out of the way which is optionally used by configure but will report invalid pathes for multilib builds.
        #     将一个工具移到可供 configure 选择使用的位置, 但该工具将报告多分支生成的无效路径。
        #     
        #         mv /usr/bin/ncursesw6-config{,.tmp}
        # 
        #     CC="gcc -m32" \
        #     ./configure ADJTIME_PATH=/var/lib/hwclock/adjtime   \
        #                 --host=i686-pc-linux-gnu \
        #                 --libdir=/usr/lib32      \
        #                 --docdir=/usr/share/doc/util-linux-2.39.3 \
        #                 --disable-chfn-chsh      \
        #                 --disable-login          \
        #                 --disable-nologin        \
        #                 --disable-su             \
        #                 --disable-setpriv        \
        #                 --disable-runuser        \
        #                 --disable-pylibmount     \
        #                 --disable-static         \
        #                 --without-python         \
        #                 --without-systemd        \
        #                 --without-systemdsystemunitdir
        #     Restore the tool previously moved away:
        #     恢复以前移走的工具:
        #     
        #         mv /usr/bin/ncursesw6-config{.tmp,}
        #     After "make", install the package:
        #     
        #         make DESTDIR=$PWD/DESTDIR install
        #         cp -Rv DESTDIR/usr/lib32/* /usr/lib32
        #         rm -rf DESTDIR
        # ..........................................
        # 3. Installation of Util-linux - x32-bit
        #     Move a tool out of the way which is optionally used by configure but will report invalid pathes for multilib builds.
        #     将一个工具移到可供 configure 选择使用的位置, 但该工具将报告多分支生成的无效路径。
        #     
        #         mv /usr/bin/ncursesw6-config{,.tmp}
        # 
        #     CC="gcc -mx32" \
        #     ./configure ADJTIME_PATH=/var/lib/hwclock/adjtime   \
        #                 --host=x86_64-pc-linux-gnux32 \
        #                 --libdir=/usr/libx32 \
        #                 --docdir=/usr/share/doc/util-linux-2.39.3 \
        #                 --disable-chfn-chsh  \
        #                 --disable-login      \
        #                 --disable-nologin    \
        #                 --disable-su         \
        #                 --disable-setpriv    \
        #                 --disable-runuser    \
        #                 --disable-pylibmount \
        #                 --disable-static     \
        #                 --without-python     \
        #                 --without-systemd    \
        #                 --without-systemdsystemunitdir
        #     Restore the tool previously moved away:
        #     恢复以前移走的工具:
        #     
        #         mv /usr/bin/ncursesw6-config{.tmp,}
        #     After "make", install the package:
        #     
        #         make DESTDIR=$PWD/DESTDIR install
        #         cp -Rv DESTDIR/usr/libx32/* /usr/libx32
        #         rm -rf DESTDIR
        # ..........................................
        cd $STORAGE/util-linux-2.39.3 && ./configure --prefix=/opt/util-linux-2.39.3 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        # If desired, run the test suite as a non-root user:
        # 如果需要, 请以非 root 用户身份运行测试套件:
        #     Warning
        #     Running the test suite as the root user can be harmful to your system.
        #     To run it, the CONFIG_SCSI_DEBUG option for the kernel must be available in the currently running system and must be built as a module.
        #     Building it into the kernel will prevent booting. For complete coverage, other BLFS packages must be installed.
        #     If desired, this test can be run by booting into the completed LFS system and running:
        #     以 root 用户身份运行测试套件可能会对系统有害。
        #     要运行它, 内核的 CONFIG_SCSI_DEBUG 选项必须在当前运行的系统中可用, 并且必须作为模块构建。
        #     将其构建到内核中会阻止启动。为了实现完全覆盖, 必须安装其他 BLFS 软件包。
        #     如果需要, 可以通过引导到完整的 LFS 系统并运行以下程序来运行此测试:
        # 
        #         bash tests/run.sh --srcdir=$PWD --builddir=$PWD
        # 
        # chown -R tester .
        # su tester -c "make -k check"
        #
        # The hardlink tests will fail if the host's kernel does not have the option CONFIG_CRYPTO_USER_API_HASH enabled or does not have any options providing a SHA256 implementation (for example, CONFIG_CRYPTO_SHA256, or CONFIG_CRYPTO_SHA256_SSSE3 if the CPU supports Supplemental SSE3) enabled.
        # In addition, two sub-tests from misc: mbsencode and one sub-test from script: replay are known to fail.
        # 如果主机内核未启用选项 CONFIG_CRYPTO_USER_API_HASH 或未启用任何提供 SHA256 实现的选项 (例如, 如果 CPU 支持补充 SSE3, 则为 CONFIG_CRYPTO_SHA256 或 CONFIG_CRYPTO_SHA256_SSSE3), 则硬链接测试将失败。
        # 此外, 来自 misc:mbsencode 的两个子测试和来自 script:replay 的一个子测试都失败了。
        
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/sbin" ]]; then mkdir /usr/local/sbin; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/util-linux-2.39.3/bin/* /usr/local/bin/
            # ......................................
            # Skip # ln -sf /opt/util-linux-2.39.3/sbin/* /usr/local/sbin/
            # ......................................
            # Skip # rsync -av /opt/util-linux-2.39.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/util-linux-2.39.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/util-linux-2.39.3/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/util-linux-2.39.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/util-linux-2.39.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################## Systemd - 250 ###########################################

# Function: 构建安装(Build Install) Systemd-250
# ##################################################
function Build_Install_Systemd_250() {

    # Recommended
    #     Linux-PAM is not strictly required to build systemd, but the main reason to rebuild systemd in BLFS (it's already built in LFS anyway) is for the systemd-logind daemon and the pam_systemd.so PAM module.
    #     Linux-PAM is required for them. All packages in BLFS book with a dependency on systemd expects it has been rebuilt with Linux-PAM.
    # 推荐
    #     构建 systemd 并不严格要求 Linux-PAM, 但在 BLFS 中重建 systemd (无论如何, 它已经在LFS中构建) 的主要原因是 systemd-logind 守护进程和 PAM_systemd.so PAM 模块。
    #     它们需要 Linux PAM。BLFS 书中所有依赖 systemd 的包都希望它已经用 Linux-PAM 重新构建。
    # ..............................................
    # Configuring systemd
    #     The /etc/pam.d/system-session file needs to be modified and a new file needs to be created in order for systemd-logind to work correctly. Run the following commands as the root user:
    #     
    #         grep 'pam_systemd' /etc/pam.d/system-session ||
    #         cat >> /etc/pam.d/system-session << "EOF"
    #         # Begin Systemd addition
    #         
    #         session  required    pam_loginuid.so
    #         session  optional    pam_systemd.so
    #         
    #         # End Systemd addition
    #         EOF
    #         
    #         cat > /etc/pam.d/systemd-user << "EOF"
    #         # Begin /etc/pam.d/systemd-user
    #         
    #         account  required    pam_access.so
    #         account  include     system-account
    #         
    #         session  required    pam_env.so
    #         session  required    pam_limits.so
    #         session  required    pam_loginuid.so
    #         session  optional    pam_keyinit.so force revoke
    #         session  optional    pam_systemd.so
    #         
    #         auth     required    pam_deny.so
    #         password required    pam_deny.so
    #         
    #         # End /etc/pam.d/systemd-user
    #         EOF
    # ..............................................
    # Important
    #     Now ensure Shadow-4.14.5 has been already rebuilt with Linux-PAM-1.6.0 support first, then logout, and login again.
    #     This ensures the running login session registered with systemd-logind and a per-user systemd instance running for each user owning a login session.
    #     Many BLFS packages listing Systemd as a dependency needs the systemd-logind integration and/or a running per-user systemd instance.
    # 特别重要
    #    现在, 请先确保 Shadow-4.14.5 已经重建并支持 Linux-PAM-1.6.0, 然后注销并再次登录。
    #    这确保了使用 systemd-logind 注册的正在运行的登录会话, 以及为每个拥有登录会话的用户运行的每个用户的 systemd 实例。
    #    许多将 Systemd 列为依赖项的 BLFS 包需要 systemd-logind 集成 和/或 按用户运行的 Systemd 实例。
    # ..............................................
    # Warning
    #     If upgrading from a previous version of systemd and an initrd is used for system boot, you should generate a new initrd before rebooting the system.
    # 警告
    #     如果从以前版本的 systemd 升级并使用 initrd 进行系统引导, 则应在重新启动系统之前生成新的 initrd。

    if [[ ! -d "/opt/sandbox-systemd/systemd-250" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( systemd-250 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/systemd-250.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # Remove two unneeded groups, render and sgx, from the default udev rules:
            # 从默认 udev 规则中删除两个不需要的组件 render 和 sgx:
            #     sed -i -e 's/GROUP="render"/GROUP="video"/' \
            #            -e 's/GROUP="sgx", //' rules.d/50-udev-default.rules.in
            # ......................................
            sed -i "143s/MOUNT_ATTR_RDONLY/MOUNT_ATTR_IDMAP/" $STORAGE/systemd-250/src/shared/mount-util.c
            sed -i "146s/MOUNT_ATTR_NOSUID/MOUNT_ATTR_IDMAP/" $STORAGE/systemd-250/src/shared/mount-util.c
            sed -i "149s/MOUNT_ATTR_NODEV/MOUNT_ATTR_IDMAP/" $STORAGE/systemd-250/src/shared/mount-util.c
            sed -i "152s/MOUNT_ATTR_NOEXEC/MOUNT_ATTR_IDMAP/" $STORAGE/systemd-250/src/shared/mount-util.c
        fi
        
        # ------------------------------------------
        # Default Build Options:
        #     meson setup ..                \
        #           --prefix=/usr           \
        #           --buildtype=release     \
        #           -Ddefault-dnssec=no     \
        #           -Dfirstboot=false       \
        #           -Dinstall-tests=false   \
        #           -Dldconfig=false        \
        #           -Dman=auto              \
        #           -Dsysusers=false        \
        #           -Drpmmacrosdir=no       \
        #           -Dhomed=false           \
        #           -Duserdb=false          \
        #           -Dmode=release          \
        #           -Dpam=false             \
        #           -Dpamconfdir=/etc/pam.d \
        #           -Ddev-kvm-mode=0660     \
        #           -Dnobody-group=nogroup  \
        #           -Ddocdir=/usr/share/doc/systemd-250
        # ..........................................
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        # ..........................................
        # *  Option: --prefix=/usr: Installation prefix. The installation prefix must be below the root prefix.
        #                           安装的前缀(路径)。安装前缀(路径)必须在根目录前缀(路径)之下。
        # ..........................................
        # *  Option: -Dmode=developer: autoenable features suitable for systemd development/release builds (default 'developer').
        #                             适用于 systemd development/release 版本的 autoenable 功能 (默认 "developer")。
        # ..........................................
        # *  Option: -Dpamconfdir=/etc/pam.d: Forces the PAM files to be installed in /etc/pam.d rather than /usr/lib/pam.d.
        # ..........................................
        # *  Option: -Drootprefix=/: override the root prefix [default '/' if split-usr and '/usr' otherwise]. The installation prefix must be below the root prefix.
        #                            覆盖根目录前缀(路径)[如果系统是 split-usr 则默认为 "/", 否则为 "/usr"]。安装前缀(路径)必须在根目录前缀(路径)之下。
        # ..........................................
        # *  Option: -Duserdb=false: Removes a daemon that does not offer any use under a BLFS configuration. If you wish to enable the userdbd daemon, replace "false" with "true" in the above meson command.
        # ..........................................
        # *  Option: -Dhomed=false: Removes a daemon that does not offer any use under a traditional BLFS configuration, especially using accounts created with useradd.
        #                           To enable systemd-homed, first ensure that you have cryptsetup-2.7.0 and libpwquality-1.4.5 installed, and then change "false" to "true" in the above meson setup command.
        #                           删除在传统BLFS配置下不提供任何用途的守护程序, 尤其是使用使用 useradd 创建的帐户。
        #                           要启用 systemd-homed, 首先确保安装了 cryptsetup-2.7.0 和 libpwquality-1.4.5, 然后在上述介子设置命令中将 "false" 更改为 "true"。
        # ..........................................
        # * Attention:
        #   此处安装 Systemd 时, 为了不影响系统原有的 Systemd 环境, 采用隔离安装。根目录设置 -Drootprefix=/opt/sandbox-systemd, Systemd 安装目录设置 --prefix=/opt/sandbox-systemd/systemd-250。
        cd $STORAGE/systemd-250 && meson build/ --prefix=/opt/sandbox-system/opt/systemd-250 \
                                                --pkg-config-path=/opt/lib/pkgconfig \
                                                -Drootprefix=/opt/sandbox-system \
                                                -Dmode=release && \
                                                STEP_BUILDED=1
        
        # ------------------------------------------
        # * Problem: ../src/shared/mount-util.c:143:22: error: ‘MOUNT_ATTR_RDONLY’ undeclared (first use in this function); did you mean ‘MOUNT_ATTR_IDMAP’?
        #                             f |= MOUNT_ATTR_RDONLY;
        #                                  ^~~~~~~~~~~~~~~~~
        #                                  MOUNT_ATTR_IDMAP
        #            ../src/shared/mount-util.c:143:22: note: each undeclared identifier is reported only once for each function it appears in
        #            ../src/shared/mount-util.c:146:22: error: ‘MOUNT_ATTR_NOSUID’ undeclared (first use in this function); did you mean ‘MOUNT_ATTR_RDONLY’?
        #                             f |= MOUNT_ATTR_NOSUID;
        #                                  ^~~~~~~~~~~~~~~~~
        #                                  MOUNT_ATTR_RDONLY
        #            ../src/shared/mount-util.c:149:22: error: ‘MOUNT_ATTR_NODEV’ undeclared (first use in this function); did you mean ‘MOUNT_ATTR_NOSUID’?
        #                             f |= MOUNT_ATTR_NODEV;
        #                                  ^~~~~~~~~~~~~~~~
        #                                  MOUNT_ATTR_NOSUID
        #            ../src/shared/mount-util.c:152:22: error: ‘MOUNT_ATTR_NOEXEC’ undeclared (first use in this function); did you mean ‘MOUNT_ATTR_NODEV’?
        #                             f |= MOUNT_ATTR_NOEXEC;
        #                                  ^~~~~~~~~~~~~~~~~
        #                                  MOUNT_ATTR_NODEV
        #            [338/1802] Compiling C object src/shared/libsystemd-shared-250.a.p/mount-setup.c.o
        #            ninja: build stopped: subcommand failed.
        #   - Solve: 按照提示修改:
        #                MOUNT_ATTR_RDONLY 改为: MOUNT_ATTR_IDMAP
        #                MOUNT_ATTR_NOSUID 改为: MOUNT_ATTR_IDMAP
        #                MOUNT_ATTR_NODEV  改为: MOUNT_ATTR_IDMAP
        #                MOUNT_ATTR_NOEXEC 改为: MOUNT_ATTR_IDMAP
        cd $STORAGE/systemd-250 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # After configured, As the root user, replace the running systemd manager (the init process) with the systemd executable newly built and installed:
        # 配置完成后, 作为 root 用户, 用新构建和安装的 systemd 可执行文件替换正在运行的 systemd 管理器 (init进程):
        #    systemctl daemon-reexec
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # ......................................
            # Regular synchronization file path.
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/sandbox-system/opt/systemd-250/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/sandbox-system/opt/systemd-250/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/sandbox-system/opt/systemd-250/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/sandbox-system/opt/systemd-250/lib/pkgconfig/libsystemd.pc /opt/lib/pkgconfig/
            # Skip # cp -f /opt/sandbox-system/opt/systemd-250/lib/pkgconfig/libudev.pc /opt/lib/pkgconfig/
            # ......................................
            # Sandbox system synchronization file path.
            if [[ ! -d "/opt/sandbox-system/lib" ]]; then mkdir /opt/sandbox-system/lib; fi
            if [[ ! -d "/opt/sandbox-system/lib/pkgconfig" ]]; then mkdir /opt/sandbox-system/lib/pkgconfig; fi
            # ......................................
            cp -f /opt/sandbox-system/opt/systemd-250/lib/pkgconfig/libsystemd.pc /opt/sandbox-system/lib/pkgconfig/
            # Skip # cp -f /opt/sandbox-system/opt/systemd-250/lib/pkgconfig/libudev.pc /opt/sandbox-system/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/systemd-250 && return 0
    else
    
        echo "[Caution] Path: ( /opt/sandbox-systemd/systemd-250 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 Systemd 时需要引入 libcap 的 include 头文件。
    # >>>>>>>>>>>>>>>>>>>>>>> PCRE2 的 include 头文件。
    export C_INCLUDE_PATH=/opt/libcap-2.68/include:/opt/pcre2-10.43/include
    export CPLUS_INCLUDE_PATH=/opt/libcap-2.68/include:/opt/pcre2-10.43/include
    # ..............................................
    # 编译 Systemd 时需要引入 PCRE2 的 lib 库文件。
    export LIBRARY_PATH=/opt/pcre2-10.43/lib
    export LD_LIBRARY_PATH=/opt/pcre2-10.43/lib

    # ----------------- Dependency -----------------
    Make_Install_libcap_2_68
    # ------------------- Jinja2 -------------------
    Build_Install_MarkupSafe_1_1_1_by_Python3
    Build_Install_Jinja2_2_9_6_by_Python3
    # ----------------- util-linux -----------------
    Compile_Install_automake_1_16
    Compile_Install_util_linux_2_39_3
    # --------------- Systemd - 250 ----------------
    Build_Install_Systemd_250
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 构建安装Systemd-250 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
