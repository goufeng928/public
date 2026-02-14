# 文章_Linux运维_Bash脚本_交叉编译Flex-2.6.4_GF_2023-03-24

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

m4-1.4.18.tar.gz

autoconf-2.69.tar.gz

automake-1.15.tar.gz

libtool-2.4.6.tar.gz

gettext-0.19.7.tar.gz

flex-2.6.4.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2023-03-24 23:39

# Need File: m4-1.4.18.tar.gz
# Need File: autoconf-2.69.tar.gz
# Need File: automake-1.15.tar.gz
# Need File: libtool-2.4.6.tar.gz
# Need File: gettext-0.19.7.tar.gz
# Need File: flex-2.6.4.tar.gz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) m4-1.4.18-for-GCC-7.5.0
# ##################################################
function compile_install_m4_1_4_18_for_gcc_7_5_0() {

    if [[ ! -f "/usr/local/bin/m4" ]]; then
    
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
        cd $STORAGE/m4-1.4.18 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
	    
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/m4-1.4.18 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/m4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) autoconf-2.69
# ##################################################
function compile_install_autoconf_2_69() {

    if [[ ! -f "/usr/local/bin/autoconf" ]]; then
    
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
        cd $STORAGE/autoconf-2.69 && ./configure && STEP_CONFIGURED=1
	    
        # ------------------------------------------
        make && make install && STEP_INSTALLED=0
	    
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/autoconf-2.69 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/autoconf ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) automake-1.15 (for Ubuntu)
# ##################################################
function compile_install_automake_1_15_for_ubuntu() {

    if [[ ! -f "/usr/local/bin/automake" ]]; then
    
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
        cd $STORAGE/automake-1.15 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=0
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/automake-1.15 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/automake ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libtool-2.4.6
# ##################################################
function compile_install_libtool_2_4_6() {

    if [[ ! -f "/usr/local/bin/libtool" ]]; then
    
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
        cd $STORAGE/libtool-2.4.6 && ./configure && STEP_CONFIGURED=1
	    
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libtool-2.4.6 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/libtool ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) gettext-0.19.7
# ##################################################
function compile_install_gettext_0_19_7() {

    if [[ ! -f "/usr/local/bin/gettext" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gettext-0.19.7 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf gettext-0.19.7.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gettext-0.19.7 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gettext-0.19.7 && return 0
	    
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/gettext ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 交叉编译安装(Cross Compile Install) flex-2.6.4 (for ARM)
# ##################################################
function cross_compile_install_flex_2_6_4_for_arm() {
    
    if [[ ! -f "/usr/local/bin/flex" ]]; then
    
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
        export PATH=/opt/arm-4.8.1/bin:$PATH
        
        # ------------------------------------------
        cd $STORAGE/flex-2.6.4 && ./autogen.sh && ./configure --host=arm-none-linux-gnueabi && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/flex-2.6.4 && return 0
    else
    
        echo "[Caution] Bin: ( /usr/local/bin/flex ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    compile_install_m4_1_4_18_for_gcc_7_5_0
    compile_install_autoconf_2_69
    compile_install_automake_1_15_for_ubuntu
    compile_install_libtool_2_4_6
    compile_install_gettext_0_19_7
    cross_compile_install_flex_2_6_4_for_arm
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Flex-2.6.4 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
