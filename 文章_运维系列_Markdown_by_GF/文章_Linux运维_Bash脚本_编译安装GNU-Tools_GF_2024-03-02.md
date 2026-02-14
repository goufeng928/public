# 文章_Linux运维_Bash脚本_编译安装GNU-Tools_GF_2024-03-02

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

pkg-config-0.29.2.tar.gz

m4-1.4.18.tar.gz

autoconf-2.69.tar.gz

automake-1.15.tar.gz

libtool-2.4.6.tar.gz

gettext-0.22.4.tar.xz

flex-2.6.4.tar.gz

bison-3.7.5.tar.gz

libiconv-1.14.tar.gz (Not Recommended for Installation)

make-4.3.tar.gz (GNU Source)
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-02 14:41

# --------------------------------------------------
# Install First: 
# * None

# ------------------- PKG-Config -------------------
# Need File: pkg-config-0.29.2.tar.gz
# ---------------------- Flex ----------------------
# Need File: m4-1.4.18.tar.gz
# Need File: autoconf-2.69.tar.gz
# Need File: automake-1.15.tar.gz
# Need File: libtool-2.4.6.tar.gz
# Need File: gettext-0.22.4.tar.xz
# Need File: flex-2.6.4.tar.gz
# ---------------------- Bison ---------------------
# Need File: bison-3.7.5.tar.gz
# -------------------- libiconv --------------------
# Need File: libiconv-1.14.tar.gz (Not Recommended for Installation)
# -------------------- GNU Make --------------------
# Need File: make-4.3.tar.gz (GNU Source)

# ##################################################
STORAGE=/home/goufeng

# ######################################### PKG-Config ###############################################

# Function: 编译安装(Compile Install) pkg-config-0.29.2
# ##################################################
function Compile_Install_pkg_config_0_29_2() {

    if [[ ! -f "/usr/bin/pkg-config" && ! -f "/usr/local/bin/pkg-config" && ! -d "/opt/pkg-config-0.29.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( pkg-config-0.29.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/pkg-config-0.29.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/pkg-config-0.29.2 && ./configure --prefix=/opt/pkg-config-0.29.2 \
                                                     --with-internal-glib && \
                                                     STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/pkg-config-0.29.2/bin/pkg-config /usr/local/bin/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pkg-config-0.29.2 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/pkg-config or /usr/local/bin/pkg-config or /opt/pkg-config-0.29.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################ Flex ##################################################

# Function: 编译安装(Compile Install) m4-1.4.18 (for GCC-7.5.0)
# ##################################################
function Compile_Install_m4_1_4_18_for_GCC_7_5_0() {

    if [[ ! -f "/usr/bin/m4" && ! -f "/usr/local/bin/m4" && ! -d "/opt/m4-1.4.18" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( m4-1.4.18 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/m4-1.4.18.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: patch 方法.
            #            cd /opt/m4-1.4.18
            #            patch -p1 < /opt/0003-c-stack-stop-using-SIGSTKSZ.patch
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 1).
            #            m4-1.4.18/lib/c-stack.c
            #             #if ! HAVE_STACK_T && ! defined stack_t
            #             typedef struct sigaltstack stack_t;
            #             #endif
            #            -#ifndef SIGSTKSZ
            #            -# define SIGSTKSZ 16384
            #            -#elif HAVE_LIBSIGSEGV && SIGSTKSZ < 16384
            #            -/* libsigsegv 2.6 through 2.8 have a bug where some architectures use
            #            -   more than the Linux default of an 8k alternate stack when deciding
            #            -   if a fault was caused by stack overflow.  */
            #            -# undef SIGSTKSZ
            #            -# define SIGSTKSZ 16384
            #            -#endif
            #            +/* Storage for the alternate signal stack.
            #            +   64 KiB is not too large for Gnulib-using apps, and is large enough
            #            +   for all known platforms.  Smaller sizes may run into trouble.
            #            +   For example, libsigsegv 2.6 through 2.8 have a bug where some
            #            +   architectures use more than the Linux default of an 8 KiB alternate
            #            +   stack when deciding if a fault was caused by stack overflow.  */
            #            +static max_align_t alternate_signal_stack[(64 * 1024
            #            +                                           + sizeof (max_align_t) - 1)
            #            +                                          / sizeof (max_align_t)];
            sed -i "53,61d" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "53i\\/\* Storage for the alternate signal stack\." $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "54i\   64 KiB is not too large for Gnulib\-using apps\, and is large enough" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "55i\   for all known platforms\.  Smaller sizes may run into trouble\." $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "56i\   For example, libsigsegv 2\.6 through 2\.8 have a bug where some" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "57i\   architectures use more than the Linux default of an 8 KiB alternate" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "58i\   stack when deciding if a fault was caused by stack overflow\.  \*\/" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "59i\static max_align_t alternate_signal_stack\[\(64 \* 1024" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "60i\                                           \+ sizeof \(max_align_t\) \- 1\)" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "61i\                                          \/ sizeof \(max_align_t\)\]\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 2).
            #            m4-1.4.18/lib/c-stack.c
            #            -/* Storage for the alternate signal stack.  */
            #            -static union
            #            -{
            #            -  char buffer[SIGSTKSZ];
            #            -
            #            -  /* These other members are for proper alignment.  There's no
            #            -     standard way to guarantee stack alignment, but this seems enough
            #            -     in practice.  */
            #            -  long double ld;
            #            -  long l;
            #            -  void *p;
            #            -} alternate_signal_stack;
            sed -i "131,142d" $STORAGE/m4-1.4.18/lib/c-stack.c
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 3).
            #            m4-1.4.18/lib/c-stack.c
            #               /* Always install the overflow handler.  */
            #               if (stackoverflow_install_handler (overflow_handler,
            #            -                                     alternate_signal_stack.buffer,
            #            -                                     sizeof alternate_signal_stack.buffer))
            #            +                                     alternate_signal_stack,
            #            +                                     sizeof alternate_signal_stack))
            sed -i "196,197d" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "196i\                                     alternate_signal_stack\," $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "197i\                                     sizeof alternate_signal_stack\)\)" $STORAGE/m4-1.4.18/lib/c-stack.c
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 4).
            #            m4-1.4.18/lib/c-stack.c
            #               stack_t st;
            #               struct sigaction act;
            #               st.ss_flags = 0;
            #            +  st.ss_sp = alternate_signal_stack;
            #            +  st.ss_size = sizeof alternate_signal_stack;
            sed -i "270i\  st\.ss_sp \= alternate_signal_stack\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "271i\  st\.ss_size \= sizeof alternate_signal_stack\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 5).
            #            m4-1.4.18/lib/c-stack.c
            #             # if SIGALTSTACK_SS_REVERSED
            #               /* Irix mistakenly treats ss_sp as the upper bound, rather than
            #                  lower bound, of the alternate stack.  */
            #            -  st.ss_sp = alternate_signal_stack.buffer + SIGSTKSZ - sizeof (void *);
            #            -  st.ss_size = sizeof alternate_signal_stack.buffer - sizeof (void *);
            #            -# else
            #            -  st.ss_sp = alternate_signal_stack.buffer;
            #            -  st.ss_size = sizeof alternate_signal_stack.buffer;
            #            +  st.ss_size -= sizeof (void *);
            #            +  char *ss_sp = st.ss_sp;
            #            +  st.ss_sp = ss_sp + st.ss_size;
            #             # endif
            sed -i "275,279d" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "275i\  st\.ss_size \-\= sizeof \(void \*\)\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "276i\  char \*ss_sp \= st\.ss_sp\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            sed -i "277i\  st\.ss_sp \= ss_sp \+ st\.ss_size\;" $STORAGE/m4-1.4.18/lib/c-stack.c
            # ......................................
            # * Problem: # c-stack.c:55:26: error: missing binary operator before token "("
            #   - Solve: sed 方法 (Part 6).
            #            m4-1.4.18/lib/c-stack.h
            #                ACTION must be async-signal-safe.  ACTION together with its callees
            #            -   must not require more than SIGSTKSZ bytes of stack space.  Also,
            #            +   must not require more than 64 KiB bytes of stack space.  Also,
            #                ACTION should not call longjmp, because this implementation does
            #                not guarantee that it is safe to return to the original stack.
            sed -i "37d" $STORAGE/m4-1.4.18/lib/c-stack.h
            sed -i "37i\   must not require more than 64 KiB bytes of stack space\.  Also\," $STORAGE/m4-1.4.18/lib/c-stack.h
            # ......................................
            # * Problem: -freadahead.c: In function ‘freadahead’
            #   - Solve: sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' /opt/m4-1.4.18/lib/*.c
            #            echo "#define _IO_IN_BACKUP 0x100" >> /opt/m4-1.4.18/lib/stdio-impl.h
            cd $STORAGE/m4-1.4.18 && sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' ./lib/*.c
            cd $STORAGE/m4-1.4.18 && echo "#define _IO_IN_BACKUP 0x100" >> ./lib/stdio-impl.h
        fi
        
        # ------------------------------------------
        cd $STORAGE/m4-1.4.18 && ./configure --prefix=/opt/m4-1.4.18 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/m4-1.4.18/bin/m4 /usr/local/bin/
        fi
	    
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/m4-1.4.18 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/m4 or /usr/local/bin/m4 or /opt/m4-1.4.18 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) autoconf-2.69
# ##################################################
function Compile_Install_autoconf_2_69() {

    if [[ ! -f "/usr/bin/autoconf" && ! -f "/usr/local/bin/autoconf" && ! -d "/opt/autoconf-2.69" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( autoconf-2.69 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf autoconf-2.69.tar.gz && STEP_UNZIPPED=1
	    
        # ------------------------------------------
        cd $STORAGE/autoconf-2.69 && ./configure --prefix=/opt/autoconf-2.69 && STEP_CONFIGURED=1
	    
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/autoconf-2.69/bin/autoconf   /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/autoheader /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/autom4te   /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/autoreconf /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/autoscan   /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/autoupdate /usr/local/bin/
            ln -sf /opt/autoconf-2.69/bin/ifnames    /usr/local/bin/
        fi
	    
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/autoconf-2.69 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/autoconf or /usr/local/bin/autoconf or /opt/autoconf-2.69 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) automake-1.15 (for Ubuntu)
# ##################################################
function Compile_Install_automake_1_15_for_Ubuntu() {

    if [[ ! -f "/usr/bin/automake" && ! -f "/usr/local/bin/automake" && ! -d "/opt/automake-1.15" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( automake-1.15 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf automake-1.15.tar.gz && STEP_UNZIPPED=1
        
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # * Problem: Makefile:3687: recipe for target 'doc/automake-1.15.1' failed
            #   - Solve: sed -i 's/\$\(update_mans\) automake\-\$\(APIVERSION\)/\$\(update_mans\) automake\-\$\(APIVERSION\) \-\-no\-discard\-stderr/' /opt/automake-1.15/Makefile
            sed -i 's/\$\(update_mans\) automake\-\$\(APIVERSION\)/\$\(update_mans\) automake\-\$\(APIVERSION\) \-\-no\-discard\-stderr/' $STORAGE/automake-1.15/Makefile
            # ......................................
            # * Problem: Unescaped left brace in regex is illegal here in regex; marked by <-- HERE in m/\${ <-- HERE ([^ \t=:+{}]+)}/ at /usr/local/bin/automake line 3936.
            #   - Solve: 按照提示行数, 将第一个遇到的 { 用 [ ] 括住.
            #            automake-1.15/bin/automake.in
            #               my ($text) = @_;
            #            -  $text =~ s/\${([^ \t=:+{}]+)}/substitute_ac_subst_variables_worker ($1)/ge;
            #            +  $text =~ s/\$[{]([^ \t=:+{}]+)}/substitute_ac_subst_variables_worker ($1)/ge;
            #               return $text;
            sed -i "3881d" $STORAGE/automake-1.15/bin/automake.in
            sed -i "3881i\  \$text =~ s/\\\\$\[\{\]\(\[\^ \\\t\=\:\+\{\}\]\+\)\}/substitute_ac_subst_variables_worker \(\$1\)/ge;" $STORAGE/automake-1.15/bin/automake.in
        fi

        # ------------------------------------------
        cd $STORAGE/automake-1.15 && ./configure --prefix=/opt/automake-1.15 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/automake-1.15/bin/aclocal       /usr/local/bin/
            ln -sf /opt/automake-1.15/bin/aclocal-1.15  /usr/local/bin/
            ln -sf /opt/automake-1.15/bin/automake      /usr/local/bin/
            ln -sf /opt/automake-1.15/bin/automake-1.15 /usr/local/bin/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/automake-1.15 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/automake or /usr/local/bin/automake or /opt/automake-1.15 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libtool-2.4.6
# ##################################################
function Compile_Install_libtool_2_4_6() {

    # ----------------------------------------------
    # * Problem: Makefile.am:477: error: Libtool library used but 'LIBTOOL' is undefined
    #            Makefile.am:477:   The usual way to define 'LIBTOOL' is to add 'LT_INIT'
    #            Makefile.am:477:   to 'configure.ac' and run 'aclocal' and 'autoconf' again.
    #            Makefile.am:477:   If 'LT_INIT' is in 'configure.ac', make sure
    #            Makefile.am:477:   its definition is in aclocal's search path.
    #            autoreconf: automake failed with exit status: 1
    #   - Solve: 原因是 automake 和 libtool 没有安装在同一目录中, 导致 aclocal 在路径中找不到 .m4 文件。
    #            解决方法 (1):
    #                1. 执行 aclocal --print-ac-dir 查看 aclocal 的路径, 例如显示 /opt/automake-1.15/share/aclocal
    #                2. 将 libtool 的 share/aclocal 目录中的 .m4 文件复制到 /opt/automake-1.15/share/aclocal (cp /opt/libtool-2.4.6/share/aclocal/*.m4 /opt/automake-1.15/share/aclocal/)
    #                3. 再次执行 autoreconf, 问题解决。
    #            解决方法 (2):
    #                1. 确保二进制 bin 文件: "aclocal" (包含在 automake 中) 和 "libtoolize" (包含在 libtool 中) 在可找到 PATH 中 (最好是同一路径下)
    #                2. 先执行 libtoolize, 会在当前目录自动生成要用到的 .m4 文件, 再执行 autoreconf, 问题解决。

    if [[ ! -f "/usr/bin/libtool" && ! -f "/usr/local/bin/libtool" && ! -d "/opt/libtool-2.4.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libtool-2.4.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf libtool-2.4.6.tar.gz && STEP_UNZIPPED=1
	    
        # ------------------------------------------
        cd $STORAGE/libtool-2.4.6 && ./configure --prefix=/opt/libtool-2.4.6 && STEP_CONFIGURED=1
	    
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/libtool-2.4.6/bin/libtool    /usr/local/bin/
            ln -sf /opt/libtool-2.4.6/bin/libtoolize /usr/local/bin/
            # ......................................
            cp /opt/libtool-2.4.6/share/aclocal/*.m4 /opt/automake-1.15/share/aclocal/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libtool-2.4.6 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/libtool or /usr/local/bin/libtool or /opt/libtool-2.4.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) gettext-0.22.4 (for Linux)
# ##################################################
function Compile_Install_gettext_0_22_4_for_Linux() {

    # **********************************************
    if [[ -f "/usr/bin/gettext" && ! -f "/usr/bin/autopoint" ]]; then
        mv /usr/bin/gettext /usr/bin/gettext.bak
    fi

    # **********************************************
    if [[ ! -f "/usr/bin/gettext" && ! -f "/usr/local/bin/gettext" && ! -d "/opt/gettext-0.22.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gettext-0.22.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/gettext-0.22.4.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Must Be "Shared (--enable-shared)" To Be Called By Other Programs.
        cd $STORAGE/gettext-0.22.4 && ./configure --prefix=/opt/gettext-0.22.4 \
                                                  --enable-shared && \
                                                  STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            rsync -av /opt/gettext-0.22.4/bin/     /usr/local/bin/
            rsync -av /opt/gettext-0.22.4/include/ /usr/local/include/
            rsync -av /opt/gettext-0.22.4/lib/     /usr/local/lib/
        fi
        
        # ------------------------------------------
        ldconfig

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gettext-0.22.4 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/gettext or /usr/local/bin/gettext or /opt/gettext-0.22.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) flex-2.6.4 (for Ubuntu)
# ##################################################
function Compile_Install_flex_2_6_4_for_Ubuntu() {
    
    if [[ ! -f "/usr/bin/flex" && ! -f "/usr/local/bin/flex" && ! -d "/opt/flex-2.6.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( flex-2.6.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf flex-2.6.4.tar.gz && STEP_UNZIPPED=1

        # ------------------------------------------
        # * Problem: Can't exec "autopoint": No such file or directory at /opt/autoconf-2.69/share/autoconf/Autom4te/FileUtils.pm line 345.
        #            autoreconf: failed to run autopoint: No such file or directory
        #            autoreconf: autopoint is needed because this package uses Gettext
        #   - Solve: autopoint 在 gettext 的 bin/ 下面, 但系统原有的 gettext 可能没有 autopoint。
        #            autopoint is located under the bin/ of the gettext, but the original system gettext may not have autopoint. 
        #            备份系统原有的 gettext (mv /usr/bin/gettext /usr/bin/gettext.bak) 并重新编译安装 gettext.
        #            Back up the original system gettext (mv /usr/bin/gettext /usr/bin/gettext.bak) and recompile and install the gettext
        cd $STORAGE/flex-2.6.4 && ./autogen.sh && ./configure --prefix=/opt/flex-2.6.4 \
                                                              CFLAGS=-D_GNU_SOURCE && \
                                                              STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/flex-2.6.4/bin/flex /usr/local/bin/
            ln -sf /opt/flex-2.6.4/bin/flex /usr/local/bin/flex++
            # ......................................
            rsync -av /opt/flex-2.6.4/include/ /usr/local/include/
            rsync -av /opt/flex-2.6.4/lib/     /usr/local/lib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/flex-2.6.4 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/flex or /usr/local/bin/flex or /opt/flex-2.6.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################### Bison ##############################################

# Function: 编译安装(Compile Install) bison-3.7.5
# ##################################################
function Compile_Install_bison_3_7_5() {

    if [[ ! -f "/usr/bin/bison" && ! -f "/usr/local/bin/bison" && ! -d "/opt/bison-3.7.5" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( bison-3.7.5 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/bison-3.7.5.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/bison-3.7.5 && ./configure --prefix=/opt/bison-3.7.5 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/bison-3.7.5/bin/bison /usr/local/bin/
            ln -sf /opt/bison-3.7.5/bin/yacc  /usr/local/bin/
            # ......................................
            rsync -av /opt/bison-3.7.5/lib/ /usr/local/lib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/bison-3.7.5 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/bison or /usr/local/bin/bison or /opt/bison-3.7.5 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# libiconv #############################################

# Function: 编译安装(Compile Install) libiconv-1.14 (for GCC-7.5.0)
# ##################################################
function Compile_Install_libiconv_1_14_for_GCC_7_5_0() {

    # Not Recommended for Installation
    # 一般不建议安装 iconv, 因为 iconv 是默认包含在 glibc 中的一部分, 多个 iconv 存在可能引起调用问题。
    # 相关资料 (http://en.wikipedia.org/wiki/Iconv):
    #     All recent Linux distributions contain a free implementation of iconv() as part of the GNU C Library which is the C library for current Linux systems.
    #     To use it, the GNU glibc locales need to be installed, which are provided as a separate package (usually named glibc-locale) normally installed by default.
    
    local SKIP=1

    if [[ ! -f "/usr/bin/iconv" && ! -f "/usr/local/bin/iconv" && ! -d "/opt/libiconv-1.14" && $SKIP == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libiconv-1.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libiconv-1.14.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # * Problem: In file included from progname.c:26:0:
            #            ./stdio.h:1010:1: error: ‘gets’ undeclared here (not in a function); did you mean ‘fgets’?
            #             _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
            #   - Solve: patch 方法.
            #            1. 把 Patch 补丁拷贝到 libiconv-1.14/srclib (cp libiconv-glibc-2.16.patch libiconv-1.14/srclib)
            #            2. cd libiconv-1.14/srclib
            #            3. patch -p1 < libiconv-glibc-2.16.patch
            # ......................................
            # * Problem: In file included from progname.c:26:0:
            #            ./stdio.h:1010:1: error: ‘gets’ undeclared here (not in a function); did you mean ‘fgets’?
            #             _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
            #   - Solve: sed 方法.
            #            --- srclib/stdio.in.h.orig      2011-08-07 16:42:06.000000000 +0300
            #            +++ srclib/stdio.in.h   2013-01-10 15:53:03.000000000 +0200
            #            @@ -695,7 +695,9 @@
            #             /* It is very rare that the developer ever has full control of stdin,
            #                so any use of gets warrants an unconditional warning.  Assume it is
            #                always declared, since it is required by C89.  */
            #            -_GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
            #            +#if defined(__GLIBC__) && !defined(__UCLIBC__) && !__GLIBC_PREREQ(2, 16)
            #            + _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
            #            +#endif
            #             #endif
            sed -i "698d" $STORAGE/libiconv-1.14/srclib/stdio.in.h
            sed -i "698i\\#if defined\(__GLIBC__\) \&\& \!defined\(__UCLIBC__\) \&\& \!__GLIBC_PREREQ\(2\, 16\)" $STORAGE/libiconv-1.14/srclib/stdio.in.h
            sed -i "699i\ _GL_WARN_ON_USE \(gets\, \"gets is a security hole \- use fgets instead\"\)\;" $STORAGE/libiconv-1.14/srclib/stdio.in.h
            sed -i "670i\\#endif" $STORAGE/libiconv-1.14/srclib/stdio.in.h
        fi
        
        # ------------------------------------------
        cd $STORAGE/libiconv-1.14 && ./configure --prefix=/opt/libiconv-1.14 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/libiconv-1.14/bin/iconv /usr/local/bin/
            # ......................................
            rsync -av /opt/libiconv-1.14/include/ /usr/local/include/
            rsync -av /opt/libiconv-1.14/lib/     /usr/local/lib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libiconv-1.14 && return 0
    else
    
        echo "[Caution] Program: ( /usr/bin/iconv or /usr/local/bin/iconv or /opt/libiconv-1.14 or Skipped) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# GNU Make #############################################

# Function: 编译安装(Compile Install) GNU-Make-4.3
# ##################################################
function Compile_Install_GNU_Make_4_3() {

    if [[ ! -d "/opt/gnu-make-4.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gnu-make-4.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/make-4.3.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 && ! -f "$STORAGE/make-4.3/src/gnumake.h" ]]; then
            echo "[Caution] Source Code: ( make-4.3.tar.gz ) is Not The GNU Make Source Code."
            # ......................................
            exit 1
        fi
        
        # ------------------------------------------
        cd $STORAGE/make-4.3 && ./configure --prefix=/opt/gnu-make-4.3 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/gnu-make-4.3/bin/make /usr/local/bin/gnu-make
            # ......................................
            cp -f /opt/gnu-make-4.3/include/gnumake.h /usr/local/include/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/make-4.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gnu-make-4.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------------- PKG-Config -----------------
    Compile_Install_pkg_config_0_29_2
    # -------------------- Flex --------------------
    Compile_Install_m4_1_4_18_for_GCC_7_5_0
    Compile_Install_autoconf_2_69
    Compile_Install_automake_1_15_for_Ubuntu
    Compile_Install_libtool_2_4_6
    Compile_Install_gettext_0_22_4_for_Linux
    Compile_Install_flex_2_6_4_for_Ubuntu
    # -------------------- Bison -------------------
    Compile_Install_bison_3_7_5
    # ------------------ libiconv ------------------
    # Skip # Compile_Install_libiconv_1_14_for_GCC_7_5_0
    # ------------------ GNU Make ------------------
    Compile_Install_GNU_Make_4_3
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装GNU-Tools 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
