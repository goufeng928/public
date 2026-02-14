# 文章_Linux运维_Bash脚本_编译安装ncurses-5.6_GF_2024-03-05

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

ncurses-5.6.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-05 21:11

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)

# Need File: ncurses-5.6.tar.gz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) ncurses-5.6
# ##################################################
function Compile_Install_ncurses_5_6() {

    # ncurses (new curses) 是一套编程库，它提供了一系列的函数以便使用者调用它们去生成基于文本的用户界面。
    # ncurses 名字中的n意味着 "new", 因为它是 curses 的自由软件版本。由于 AT&T "臭名昭著" 的版权政策, 人们不得不在后来用 ncurses 去代替它。
    # ncurses 是 GNU 计划的一部分, 但它却是少数几个不使用 GNU GPL 或 LGPL 授权的 GNU 软件之一。
    # 其实我们对 ncurses 本身并不陌生，以下几款大名鼎鼎的软件都用到过 ncurses:
    #     * vim
    #     * emacs
    #     * lynx
    #     * screen
    # 作为嵌入式驱动开发工程师, Linux 内核的配置也离不开 ncurses 库的使用。

    if [[ ! -d "/opt/ncurses-5.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( ncurses-5.6 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/ncurses-5.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            # --------------------------------------
            # * Problem: In file included from ../c++/cursesf.h:39:0,
            #                             from ../c++/cursesf.cc:35:
            #            ../c++/cursesp.h: In member function ‘T* NCursesUserPanel<T>::UserData() const’:
            #            ../c++/cursesp.h:253:43: error: no matching function for call to ‘NCursesUserPanel<T>::get_user() const’
            #                 return reinterpret_cast<T*>(get_user ());
            #                                                       ^
            #            ../c++/cursesp.h:79:9: note: candidate: void* NCursesPanel::get_user() <near match>
            #               void *get_user()
            #                     ^~~~~~~~
            #            ../c++/cursesp.h:79:9: note:   passing ‘const NCursesUserPanel<T>*’ as ‘this’ argument discards qualifiers
            #            In file included from ../c++/cursesf.cc:35:0:
            #            ../c++/cursesf.h: In member function ‘T* NCursesUserForm<T>::UserData() const’:
            #            ../c++/cursesf.h:707:43: error: no matching function for call to ‘NCursesUserForm<T>::get_user() const’
            #                 return reinterpret_cast<T*>(get_user ());
            #                                                       ^
            #            ../c++/cursesf.h:384:16: note: candidate: void* NCursesForm::get_user() <near match>
            #               inline void *get_user() {
            #                            ^~~~~~~~
            #            ../c++/cursesf.h:384:16: note:   passing ‘const NCursesUserForm<T>*’ as ‘this’ argument discards qualifiers
            #           ............................
            #   -Solve: 出错的原因是 GCC 编译器版本过高。新版 C++ 标准中 const 成员函数不可以调用非 const 成员函数。
            #           错误提示 discards qualifiers 因为 get_user() 是非 const 的, 而 UserData() 是 const 成员函数, 不可以调用非 const 成员函数。
            #           ............................
            #           -  T* UserData (void) const
            #           +  T* UserData (void)
            #              {
            #                return reinterpret_cast<T*>(get_user ());
            #              };
            sed -i "251s/T\* UserData (void) const/T\* UserData (void)/" $STORAGE/ncurses-5.6/c++/cursesp.h
            sed -i "706s/inline T\* UserData (void) const/inline T\* UserData (void)/" $STORAGE/ncurses-5.6/c++/cursesf.h
            sed -i "662s/inline T\* UserData (void) const/inline T\* UserData (void)/" $STORAGE/ncurses-5.6/c++/cursesm.h
        fi
        
        # ------------------------------------------
        cd $STORAGE/ncurses-5.6 && ./configure --prefix=/opt/ncurses-5.6 \
                                               --enable-pc-files \
                                               --enable-shared \
                                               --with-libtool && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/terminfo" ]]; then mkdir /usr/local/lib/terminfo; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/ncurses-5.6/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/ncurses-5.6/include/ /usr/local/include/
            # ......................................
            cp -vf /opt/ncurses-5.6/include/ncurses/*.h /usr/local/include/
            # ......................................
            rsync -av /opt/ncurses-5.6/lib/ /usr/local/lib/
            # ......................................
            rsync -av /opt/ncurses-5.6/share/terminfo/ /usr/local/lib/terminfo/
            # ......................................
            cp -vf /opt/ncurses-5.6/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        ldconfig
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ncurses-5.6 && return 0
    else
        echo "[Caution] Path: ( /opt/ncurses-5.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    Compile_Install_ncurses_5_6
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装ncurses-5.6 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
