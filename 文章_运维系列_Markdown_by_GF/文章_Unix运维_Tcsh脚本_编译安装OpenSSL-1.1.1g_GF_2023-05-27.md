# 文章_Unix运维_Tcsh脚本_编译安装OpenSSL-1.1.1g_GF_2023-05-27

csh 文件是一种 Unix Shell 脚本文件，其扩展名为 .csh 或 .tcsh。和其他 Unix Shell 脚本文件一样，它可用于执行一系列的命令，包括调用其他脚本或程序等。

通常，csh 文件中包含的命令会按照脚本文件的顺序依次执行。和其他 Shell 脚本文件相比，csh 文件具有更多的功能和优势，其中一个显著的特点是支持 C-Shell 语法。

Tcsh 是 csh 的增强版，并且完全兼容 csh。它不但具有 csh 的全部功能，还具有命令行编辑、拼写校正、可编程字符集、历史纪录、作业控制等功能，以及 C 语言风格的语法结构。

## 使用方法

* 下载源码包:

rsync-3.2.7.tar.gz

perl-5.26.1.tar.gz

openssl-1.1.1g.tar.gz
  
* 放于指定路径:

这里 Tcsh Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Tcsh Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/tcsh
# Create By GF 2023-05-27 23:16

# --------------------------------------------------
# Install First: 
# * None

# --------------------------------------------------
# FreeBSD Prepare First: 
# * Create User (Command: adduser / username: rsync / Login group: rsync / Shell: nologin / Home directory: /nonexistent)

# ------------------ rsync-3.2.7 -------------------
# Need File: rsync-3.2.7.tar.gz
# ------------------- Dependency -------------------
# Need File: perl-5.26.1.tar.gz 
# ------------------ GNU-Make-4.3 ------------------
# Need File: openssl-1.1.1g.tar.gz

# ==================================================
set STORAGE = /home/goufeng

# ########################################################################################################################################################################################################
# ############################################################################################# rsync-3.2.7 ##############################################################################################

# ====================================================================================================
# =================================== Compile Install rsync-3.2.7 ====================================

# --------------------------------------------------
# For security reasons, running the rsync server as an unprivileged user and group is encouraged.
# 出于安全考虑, 建议以无特权用户和组的身份运行 rsync 服务器。

# --------------------------------------------------
# Configuring rsync
# ..................................................
# Config Files: /etc/rsyncd.conf
# ..................................................
# Configuration Information:
#
# For client access to remote files, you may need to install the OpenSSH-9.4p1 package to connect to the remote server.
# 对于客户端访问远程文件, 您可能需要安装 OpenSSH-9.4p1 软件包才能连接到远程服务器。
#
# This is a simple download-only configuration to set up running rsync as a server. See the rsyncd.conf(5) man-page for additional options (i.e., user authentication).
# 这是一个简单的仅下载配置, 用于设置作为服务器运行的 rsync。有关其他选项 (即用户身份验证), 请参阅 rsyncd.conf(5) 手册页。
#
#    cat > /etc/rsyncd.conf << "EOF"
#    # This is a basic rsync configuration file
#    # It exports a single module without user authentication.
#    
#    motd file = /home/rsync/welcome.msg
#    use chroot = yes
#    
#    [localhost]
#        path = /home/rsync
#        comment = Default rsync module
#        read only = yes
#        list = yes
#        uid = rsyncd
#        gid = rsyncd
#    
#    EOF
# You can find additional configuration information and general documentation about rsync at https://rsync.samba.org/documentation.html.
# 您可以在以下位置找到有关 rsync 的其他配置信息和常规文档: https://rsync.samba.org/documentation.html。

if ( ! -d "/opt/rsync-3.2.7" ) then

    set VERIFY = "NULL"
    set STEP_UNZIPPED = 0
    set STEP_CONFIGURED = 0
    set STEP_MADE = 0
    set STEP_INSTALLED = 0

    # ----------------------------------------------
    echo "[Confirm] Compile and Install ( rsync-3.2.7 )? (y/n)"
    # ..............................................
    set VERIFY = $<
    # ..............................................
    if ( $VERIFY != "y" ) exit 1

    # ----------------------------------------------
    tar -zxvf $STORAGE/rsync-3.2.7.tar.gz && set STEP_UNZIPPED = 1
    
    # ----------------------------------------------
    # Default Configure Options:
    #     ./configure --prefix=/usr \
    #                 --disable-lz4 \
    #                 --disable-xxhash \
    #                 --without-included-zlib
    # ..............................................
    # *  Option: --disable-lz4: This switch disables LZ4 compression support. Note that it uses the superior 'zstd' algorithm when this switch is in use, and zstd is provided in LFS.
    #                           此选项禁用 lz4 压缩支持。请注意, 当使用此开关时, 它使用了高级的 "zstd" 算法, 并且 zstd 是在 LFS 中提供的。
    # ..............................................
    # *  Option: --disable-xxhash: This switch disables advanced xxhash checksum support. Remove this switch if you have installed xxhash.
    #                              此选项禁用高级 xxhash 校验和支持。如果已安装 xxhash, 请移除此选项。
    # ..............................................
    # *  Option: --without-included-zlib: This switch enables compilation with the system-installed zlib library.
    #                                     此选项允许使用系统安装的 zlib 库进行编译。
    # ..............................................
    cd $STORAGE/rsync-3.2.7 && ./configure --prefix=/opt/rsync-3.2.7 \
                                           --disable-lz4 \
                                           --disable-xxhash \
                                           --without-included-zlib && \
                                           set STEP_CONFIGURED = 1
    
    # ----------------------------------------------
    make && STEP_MADE = 1
    
    # ----------------------------------------------
    # If you have Doxygen-1.9.7 installed and wish to build HTML API documentation, issue:
    # 如果您安装了 Doxygen-1.9.7 并希望构建 HTML API 文档, 请使用指令:
    #     doxygen
    
    # ----------------------------------------------
    make install && set STEP_INSTALLED = 1
    
    # ----------------------------------------------
    # If you built the documentation, install it using the following commands as the root user:
    # 如果您构建了文档, 请以 root 用户身份使用以下命令进行安装:
    #     install -v -m755 -d          /usr/share/doc/rsync-3.2.7/api &&
    #     install -v -m644 dox/html/*  /usr/share/doc/rsync-3.2.7/api
     
    # ----------------------------------------------
    if ( $STEP_INSTALLED == 1 && ! -f "/bin/rsync" && ! -f "/usr/bin/rsync" ) then
        ln -sf /opt/rsync-3.2.7/bin/rsync /usr/local/bin/
    endif

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/rsync-3.2.7
else

    echo "[Caution] Path: ( /opt/rsync-3.2.7 ) Already Exists."
endif

# ########################################################################################################################################################################################################
# ############################################################################################## Dependency ##############################################################################################

# ====================================================================================================
# =================================== Compile Install perl-5.26.1 ====================================

if ( ! -d "/opt/perl-5.26.1" ) then

    set VERIFY = "NULL"
    set STEP_UNZIPPED = 0
    set STEP_CONFIGURED = 0
    set STEP_INSTALLED = 0

    # ----------------------------------------------
    echo "[Confirm] Compile and Install ( perl-5.26.1 )? (y/n)"
    # ..............................................
    set VERIFY = $<
    # ..............................................
    if ( $VERIFY != "y" ) exit 1

    # ----------------------------------------------
    tar -zxvf $STORAGE/perl-5.26.1.tar.gz && set STEP_UNZIPPED = 1
    
    # ----------------------------------------------
    cd $STORAGE/perl-5.26.1 && ./Configure -des \
                                           -Dprefix=/opt/perl-5.26.1 \
                                           -Duseshrplib && \
                                           set STEP_CONFIGURED = 1
    
    # ----------------------------------------------
    make && make install && set STEP_INSTALLED = 1
     
    # ----------------------------------------------
    if ( $STEP_INSTALLED == 1 ) then
        ln -sf /opt/perl-5.26.1/bin/* /usr/local/bin/
        # ..........................................
        # Skip # rsync -av /opt/perl-5.26.1/lib/ /usr/local/lib/
    endif

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/perl-5.26.1
else

    echo "[Caution] Path: ( /opt/perl-5.26.1 ) Already Exists."
endif

# ########################################################################################################################################################################################################
# ############################################################################################ OpenSSL-1.1.1g ############################################################################################

# ====================================================================================================
# ================================== Compile Install OpenSSL-1.1.1g ==================================

if ( ! -d "/opt/openssl-1.1.1g" ) then

    set VERIFY = "NULL"
    set STEP_UNZIPPED = 0
    set STEP_CONFIGURED = 0
    set STEP_INSTALLED = 0

    # ----------------------------------------------
    echo "[Confirm] Compile and Install ( openssl-1.1.1g )? (y/n)"
    # ..............................................
    set VERIFY = $<
    # ..............................................
    if ( $VERIFY != "y" ) exit 1

    # ----------------------------------------------
    tar -zxvf $STORAGE/openssl-1.1.1g.tar.gz && set STEP_UNZIPPED = 1
    
    # ----------------------------------------------
    cd $STORAGE/openssl-1.1.1g && ./config --prefix=/opt/openssl-1.1.1g \
                                           --openssldir=/opt/openssl-1.1.1g/ssl \
                                           --shared \
                                           zlib && \
                                           STEP_CONFIGURED = 1
    
    # ----------------------------------------------
    make && make install && set STEP_INSTALLED = 1
     
    # ----------------------------------------------
    if ( $STEP_INSTALLED == 1 ) then
        if ( ! -d "/usr/local/lib" ) mkdir /usr/local/lib
        if ( ! -d "/usr/local/lib/pkgconfig" ) mkdir /usr/local/lib/pkgconfig
        # ..........................................
        ln -sf /opt/openssl-1.1.1g/bin/openssl /usr/local/bin/
        # ..........................................
        rsync -av /opt/openssl-1.1.1g/include/ /usr/local/include/
        # ..........................................
        rsync -av /opt/openssl-1.1.1g/lib/ /usr/local/lib/
        # ..........................................
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /usr/local/lib/pkgconfig/
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /usr/local/lib/pkgconfig/
        cp -f /opt/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /usr/local/lib/pkgconfig/
    endif

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/openssl-1.1.1g
else

    echo "[Caution] Path: ( /opt/openssl-1.1.1g ) Already Exists."
endif

# ########################################################################################################################################################################################################
# ################################################################################################## Ends ################################################################################################

```

## 总结

以上就是关于 Unix运维 Tcsh脚本 编译安装OpenSSL-1.1.1g 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
