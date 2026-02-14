# 文章_Linux运维_Bash脚本_编译安装Glib-2.78.4_GF_2024-03-05

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

bzip2-1.0.6.tar.gz

libxml2-2.9.1.tar.gz

libxslt-1.1.28.tar.gz

docbook-xml-4.5.zip

docbook-xsl-1.79.1.tar.bz2

docbook-xsl-doc-1.79.1.tar.bz2

ncurses-6.4.tar.gz

readline-8.2.tar.gz

pcre2-10.43.tar.bz2

glib-2.78.4.tar.xz
  
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
# * Python >= 3.x
# * Meson
# * Ninja

# ------------------- Dependency -------------------
# Need File: bzip2-1.0.6.tar.gz
# Need File: libxml2-2.9.1.tar.gz
# Need File: libxslt-1.1.28.tar.gz
# --------- XML Tools (XML DTD) DocBook-XML --------
# Need File: docbook-xml-4.5.zip
# ----- XML Tools (XSL Stylesheets) DocBook-XSL ----
# Need File: docbook-xsl-1.79.1.tar.bz2
# Need File: docbook-xsl-doc-1.79.1.tar.bz2
# -------------------- ReadLine --------------------
# Need File: ncurses-6.4.tar.gz
# Need File: readline-8.2.tar.gz
# --------------------- PCRE2 ----------------------
# Need File: pcre2-10.43.tar.bz2
# ----------------- Glib - 2.78.4 ------------------
# Need File: glib-2.78.4.tar.xz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 制作安装(Make Install) bzip2-1.0.6
# ##################################################
function Make_Install_bzip2_1_0_6() {

    # Attention: may conflict with the original "bzip2" in the system.
    # 注意: 可能与系统原有的 "bzip2" 冲突。

    if [[ ! -d "/opt/bzip2-1.0.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Make and Install ( bzip2-1.0.6 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/bzip2-1.0.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i "18s/CC\=gcc/CC\=gcc \-fPIC/" $STORAGE/bzip2-1.0.6/Makefile
            sed -i "24s/CFLAGS\=\-Wall \-Winline \-O2 \-g \$(BIGFILES)/CFLAGS\=\-Wall \-Winline \-O2 \-fPIC \-g \$(BIGFILES)/" $STORAGE/bzip2-1.0.6/Makefile
        fi
        
        # ------------------------------------------
        cd $STORAGE/bzip2-1.0.6 && make install PREFIX=/opt/bzip2-1.0.6 && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Default None .pc (Pkg-Config) File.
            # ......................................
            # Skip # ln -sf /opt/bzip2-1.0.6/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/bzip2-1.0.6/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/bzip2-1.0.6/lib/ /usr/local/lib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/bzip2-1.0.6 && return 0
    else
        echo "[Caution] Path: ( /opt/bzip2-1.0.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxml2-2.9.1
# ##################################################
function Compile_Install_libxml2_2_9_1() {

    if [[ ! -d "/opt/libxml2-2.9.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( libxml2-2.9.1 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/libxml2-2.9.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxml2-2.9.1 && ./configure --prefix=/opt/libxml2-2.9.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libxml2-2.9.1/bin/xml2-config /usr/local/bin/
            ln -sf /opt/libxml2-2.9.1/bin/xmlcatalog  /usr/local/bin/
            ln -sf /opt/libxml2-2.9.1/bin/xmllint     /usr/local/bin/
            # ......................................
            rsync -av /opt/libxml2-2.9.1/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libxml2-2.9.1/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxml2-2.9.1/lib/pkgconfig/libxml-2.0.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxml2-2.9.1 && return 0
    else
        echo "[Caution] Path: ( /opt/libxml2-2.9.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libxslt-1.1.28
# ##################################################
function Compile_Install_libxslt_1_1_28() {

    if [[ ! -d "/opt/libxslt-1.1.28" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libxslt-1.1.28 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libxslt-1.1.28.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxslt-1.1.28 && ./configure --prefix=/opt/libxslt-1.1.28 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/libxslt-1.1.28/bin/xslt-config /usr/local/bin/
            ln -sf /opt/libxslt-1.1.28/bin/xsltproc    /usr/local/bin/
            # ......................................
            rsync -av /opt/libxslt-1.1.28/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libxslt-1.1.28/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libxslt-1.1.28/lib/pkgconfig/libexslt.pc /opt/lib/pkgconfig/
            cp -f /opt/libxslt-1.1.28/lib/pkgconfig/libxslt.pc  /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxslt-1.1.28 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxslt-1.1.28 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################## XML Tools (XML DTD) DocBook-XML #################################

# Function: 部署安装(Deploy Install) XML-DTD: DocBook-XML-4.5
# ##################################################
function Deploy_Install_XML_DTD_DocBook_XML_4_5() {

    if [[ ! -d "/usr/share/xml/docbook/xml-dtd-4.5" ]]; then
    
        # 安装目录: /etc/xml 和 /usr/share/xml/docbook/xml-dtd-4.5
        # Installed Directories: /etc/xml and /usr/share/xml/docbook/xml-dtd-4.5

        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
        local STEP_CONFIGURED=0
    
        # ------------------------------------------
        read -p "[Confirm] Deploy and Install ( XML-DTD: DocBook-XML-4.5)? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        unzip $STORAGE/docbook-xml-4.5.zip -d docbook-xml-4.5 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/docbook-xml-4.5
        
        # ------------------------------------------
        # 安装 DocBook XML DTD
        # Installation of DocBook XML DTD
        install -v -d -m755 /usr/share/xml/docbook/xml-dtd-4.5 &&
        install -v -d -m755 /etc/xml &&
        cp -v -af --no-preserve=ownership docbook.cat *.dtd ent/ *.mod \
            /usr/share/xml/docbook/xml-dtd-4.5
        
        # ------------------------------------------
        # 配置 DocBook XML DTD
        # Configuring DocBook XML DTD
        # ..........................................
        # 创建 (或更新) 并填充 /etc/xml/docbook 目录文件:
        if [ ! -e /etc/xml/docbook ]; then
            xmlcatalog --noout --create /etc/xml/docbook
        fi &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//DTD DocBook XML V4.5//EN" \
            "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/calstblx.dtd" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/soextblx.dtd" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/dbpoolx.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/dbhierx.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/htmltblx.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/dbnotnx.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/dbcentx.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "public" \
            "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5/dbgenent.mod" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "rewriteSystem" \
            "http://www.oasis-open.org/docbook/xml/4.5" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5" \
            /etc/xml/docbook &&
        xmlcatalog --noout --add "rewriteURI" \
            "http://www.oasis-open.org/docbook/xml/4.5" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5" \
            /etc/xml/docbook
        # ..........................................
        # 创建 (或更新) 并填充 /etc/xml/catalog 目录文件:
        if [ ! -e /etc/xml/catalog ]; then
            xmlcatalog --noout --create /etc/xml/catalog
        fi &&
        xmlcatalog --noout --add "delegatePublic" \
            "-//OASIS//ENTITIES DocBook XML" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog &&
        xmlcatalog --noout --add "delegatePublic" \
            "-//OASIS//DTD DocBook XML" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog &&
        xmlcatalog --noout --add "delegateSystem" \
            "http://www.oasis-open.org/docbook/" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog &&
        xmlcatalog --noout --add "delegateURI" \
            "http://www.oasis-open.org/docbook/" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog
        
        # ------------------------------------------
        # 创建 DocBook XML DTD 系统标识符, 以便于请求任何 4.x 版本时使用 DocBook XML DTD V4.5 (Glib-2.78.4 要求 XML DTD V4.2):
        for DTDVERSION in 4.1.2 4.2 4.3 4.4
        do
          xmlcatalog --noout --add "public" \
            "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
            /etc/xml/docbook
          xmlcatalog --noout --add "rewriteSystem" \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5" \
            /etc/xml/docbook
          xmlcatalog --noout --add "rewriteURI" \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
            "file:///usr/share/xml/docbook/xml-dtd-4.5" \
            /etc/xml/docbook
          xmlcatalog --noout --add "delegateSystem" \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog
          xmlcatalog --noout --add "delegateURI" \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
            "file:///etc/xml/docbook" \
            /etc/xml/catalog
        done

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/docbook-xml-4.5 && return 0
    else
    
        echo "[Caution] Path: ( /usr/share/xml/docbook/xml-dtd-4.5 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################## XML Tools (XSL Stylesheets) DocBook-XSL #############################

# Function: 部署安装(Deploy Install) XSL-Stylesheets: DocBook-XSL-1.79.1
# ##################################################
function Deploy_Install_XSL_Stylesheets_DocBook_XSL_1_79_1() {

    if [[ ! -d "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" ]]; then
    
        # 安装目录: /usr/share/xml/docbook/xsl-stylesheets-1.79.1 和 /usr/share/doc/docbook-xsl-1.79.1
        # Installed Directories: /usr/share/xml/docbook/xsl-stylesheets-1.79.1 and /usr/share/doc/docbook-xsl-1.79.1

        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_INSTALLED=0
        local STEP_CONFIGURED=0
    
        # ------------------------------------------
        read -p "[Confirm] Deploy and Install ( XSL-Stylesheets: DocBook-XSL-1.79.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/docbook-xsl-1.79.1.tar.bz2 && \
        tar -jxvf $STORAGE/docbook-xsl-doc-1.79.1.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/docbook-xsl-1.79.1
        
        # ------------------------------------------
        # 安装 DocBook XSL 样式表
        # Installation of DocBook XSL Stylesheets
        install -v -m755 -d /usr/share/xml/docbook/xsl-stylesheets-1.79.1 &&

        cp -v -R VERSION assembly common eclipse epub epub3 extensions fo        \
                 highlighting html htmlhelp images javahelp lib manpages params  \
                 profiling roundtrip slides template tests tools webhelp website \
                 xhtml xhtml-1_1 xhtml5                                          \
            /usr/share/xml/docbook/xsl-stylesheets-1.79.1 &&
        
        ln -s VERSION /usr/share/xml/docbook/xsl-stylesheets-1.79.1/VERSION.xsl &&
        
        install -v -m644 -D README \
                            /usr/share/doc/docbook-xsl-1.79.1/README.txt &&
        install -v -m644    RELEASE-NOTES* NEWS* \
                            /usr/share/doc/docbook-xsl-1.79.1
        
        # ------------------------------------------
        cd $STORAGE/docbook-xsl-doc-1.79.1
        
        # ------------------------------------------
        # 如果下载了可选的源码文档 tarball, 请以 root 用户身份发出以下命令来安装源码文档: 
        # If you downloaded the optional documentation tarball, install the documentation by issuing the following command as the root user:
        cp -v -R doc/* /usr/share/doc/docbook-xsl-1.79.1
        
        # ------------------------------------------
        # 配置 DocBook XSL 样式表
        # Configuring DocBook XSL Stylesheets
        if [ ! -d /etc/xml ]; then install -v -m755 -d /etc/xml; fi &&
        if [ ! -f /etc/xml/catalog ]; then
            xmlcatalog --noout --create /etc/xml/catalog
        fi &&
        
        xmlcatalog --noout --add "rewriteSystem" \
                   "http://docbook.sourceforge.net/release/xsl/1.79.1" \
                   "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
            /etc/xml/catalog &&
        
        xmlcatalog --noout --add "rewriteURI" \
                   "http://docbook.sourceforge.net/release/xsl/1.79.1" \
                   "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
            /etc/xml/catalog &&
        
        xmlcatalog --noout --add "rewriteSystem" \
                   "http://docbook.sourceforge.net/release/xsl/current" \
                   "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
            /etc/xml/catalog &&
        
        xmlcatalog --noout --add "rewriteURI" \
                   "http://docbook.sourceforge.net/release/xsl/current" \
                   "/usr/share/xml/docbook/xsl-stylesheets-1.79.1" \
            /etc/xml/catalog

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/docbook-xsl-1.79.1 && \
        cd $STORAGE && rm -rf $STORAGE/docbook-xsl-doc-1.79.1 && return 0
    else
    
        echo "[Caution] Path: ( /usr/share/xml/docbook/xsl-stylesheets-1.79.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# ReadLine #############################################

# Function: 编译安装(Compile Install) ncurses-6.4
# ##################################################
function Compile_Install_ncurses_6_4() {

    # ncurses (new curses) 是一套编程库，它提供了一系列的函数以便使用者调用它们去生成基于文本的用户界面。
    # ncurses 名字中的n意味着 "new", 因为它是 curses 的自由软件版本。由于 AT&T "臭名昭著" 的版权政策, 人们不得不在后来用 ncurses 去代替它。
    # ncurses 是 GNU 计划的一部分, 但它却是少数几个不使用 GNU GPL 或 LGPL 授权的 GNU 软件之一。
    # 其实我们对 ncurses 本身并不陌生，以下几款大名鼎鼎的软件都用到过 ncurses:
    #     * vim
    #     * emacs
    #     * lynx
    #     * screen
    # 作为嵌入式驱动开发工程师, Linux 内核的配置也离不开 ncurses 库的使用。

    if [[ ! -d "/opt/ncurses-6.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( ncurses-6.4 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/ncurses-6.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/ncurses-6.4 && ./configure --prefix=/opt/ncurses-6.4 \
                                               --enable-pc-files \
                                               --enable-shared \
                                               --with-libtool && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/ncurses-6.4/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/ncurses-6.4/include/ /usr/local/include/
            # ......................................
            cp -f /opt/ncurses-6.4/include/ncurses/*.h /usr/local/include/
            # ......................................
            rsync -av /opt/ncurses-6.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/ncurses-6.4/lib/pkgconfig/form.pc      /opt/lib/pkgconfig/
            cp -f /opt/ncurses-6.4/lib/pkgconfig/menu.pc      /opt/lib/pkgconfig/
            cp -f /opt/ncurses-6.4/lib/pkgconfig/ncurses.pc   /opt/lib/pkgconfig/
            cp -f /opt/ncurses-6.4/lib/pkgconfig/ncurses++.pc /opt/lib/pkgconfig/
            cp -f /opt/ncurses-6.4/lib/pkgconfig/panel.pc     /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        ldconfig
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/ncurses-6.4 && return 0
    else
        echo "[Caution] Path: ( /opt/ncurses-6.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) readline-8.2
# ##################################################
function Compile_Install_readline_8_2() {

    # 编译安装 readline 之前, 需要确保 ncurses 已经存在并可调用, 因为 readline can be called when ncurses lib is installed.
    # 所以 ncurses 是 readline 的依赖软, 虽然不安装 ncurses 也能将 readline 编译通过, 但 readline 不能被调用, 没有意义。

    if [[ ! -d "/opt/readline-8.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( readline-8.2 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/readline-8.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/readline-8.2 && ./configure --prefix=/opt/readline-8.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/readline-8.2/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/readline-8.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/readline-8.2/lib/pkgconfig/history.pc  /opt/lib/pkgconfig/
            cp -f /opt/readline-8.2/lib/pkgconfig/readline.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/readline-8.2 && return 0
    else
        echo "[Caution] Path: ( /opt/readline-8.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################## PCRE2 ###############################################

# Function: 编译安装(Compile Install) PCRE2-10.43
# ##################################################
function Compile_Install_PCRE2_10_43() {

    if [[ ! -d "/opt/pcre2-10.43" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( pcre2-10.43 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -jxvf $STORAGE/pcre2-10.43.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: ** Cannot --enable-pcre2test-readline because readline library was not found.
        #   - Solve: 回溯 Configure 过程:
        #            ......
        #            checking for readline/readline.h... yes
        #            checking for readline/history.h... yes
        #            checking for readline in -lreadline... no
        #            checking for readline in -lreadline... no
        #            checking for readline in -lreadline... no
        #            checking for readline in -lreadline... no
        #            checking for readline in -lreadline... no
        #            checking for readline in -lreadline... no
        #            ......
        #            说明 readline 的库在链接验证的过程中失败了, 如果已经正确安装了 readline, 库文件存在, 则需要检查 ncurses 是否存在并先于 readline 安装, 以确保 readline 函数能够被调用。
        # ..........................................
        # * Configure Option Description:
        # --enable-unicode: This switch enables Unicode support and includes the functions for handling UTF-8/16/32 character strings in the library.
        #                   此选项启用 Unicode 支持, 并包括处理库中 UTF-8/16/32 字符串的功能。
        # ..........................................
        # --enable-pcre2-16: This switch enables 16 bit character support.
        #                    此选项支持 16 位字符。
        # ..........................................
        # --enable-pcre2-32: This switch enables 32 bit character support.
        #                    此选项支持 32 位字符。
        # ..........................................
        # --enable-pcre2grep-libz: This switch adds support for reading .gz compressed files to pcre2grep.
        #                          此选项增加了对将 .gz 压缩文件读取到 pcre2grep 的支持。
        # ..........................................
        # --enable-pcre2grep-libbz2: This switch adds support for reading .bz2 compressed files to pcre2grep.
        #                            此选项增加了对将 .bz2 压缩文件读取到 pcre2grep 的支持。
        # ..........................................
        # --enable-pcre2test-libreadline: This switch adds line editing and history features to the pcre2test program.
        #                                 此选项为 pcre2test 程序添加了行编辑和历史记录功能。
        # ..........................................
        # --disable-static: This switch prevents installation of static versions of the libraries.
        #                   此选项可防止安装库的静态版本。
        # ..........................................
        # --enable-jit: This option enables Just-in-time compiling, which can greatly speed up pattern matching.
        #               此选项启用实时编译, 这可以大大加快模式匹配的速度。
        cd $STORAGE/pcre2-10.43 && ./configure --prefix=/opt/pcre2-10.43 \
                                               --enable-unicode \
                                               --enable-jit \
                                               --enable-pcre2-16 \
                                               --enable-pcre2-32 \
                                               --enable-pcre2grep-libz \
                                               --enable-pcre2grep-libbz2 \
                                               --enable-pcre2test-libreadline \
                                               --disable-static && \
                                               STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/pcre2-10.43/pcre2-config /usr/local/bin/
            # Skip # ln -sf /opt/pcre2-10.43/pcre2grep    /usr/local/bin/
            # Skip # ln -sf /opt/pcre2-10.43/pcre2test    /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/pcre2-10.43/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/pcre2-10.43/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/pcre2-10.43/lib/pkgconfig/libpcre2-8.pc     /opt/lib/pkgconfig/
            cp -f /opt/pcre2-10.43/lib/pkgconfig/libpcre2-16.pc    /opt/lib/pkgconfig/
            cp -f /opt/pcre2-10.43/lib/pkgconfig/libpcre2-32.pc    /opt/lib/pkgconfig/
            cp -f /opt/pcre2-10.43/lib/pkgconfig/libpcre2-posix.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/pcre2-10.43/ /opt/sandbox-glib/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pcre2-10.43 && return 0
    else
        echo "[Caution] Path: ( /opt/pcre2-10.43 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ########################################## Glib - 2.78.4 ###########################################

# Function: 构建安装(Build Install) Glib-2.78.4
# ##################################################
function Build_Install_Glib_2_78_4() {

    # Glib 库是 Linux 平台下最常用的 C语言 函数库, 它具有很好的可移植性和实用性。
    # Glib 是 Gtk+ 库和 Gnome 的基础。Glib 可以在多个平台下使用, 比如 Linux、Unix、Windows 等。Glib为许多标准的、常用的 C语言 结构提供了相应的替代物。

    if [[ ! -d "/opt/glib-2.78.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( glib-2.78.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/glib-2.78.4.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # If desired, apply the optional patch. 
        # In many cases, applications that use this library, either directly or indirectly via other libraries such as GTK+-3.24.41, output numerous warnings when run from the command line. 
        # This patch enables the use of an environment variable, GLIB_LOG_LEVEL, that suppresses unwanted messages. 
        # The value of the variable is a digit that corresponds to:
        #     1 Alert
        #     2 Critical
        #     3 Error
        #     4 Warning
        #     5 Notice
        # For instance export GLIB_LOG_LEVEL=4 will skip output of Warning and Notice messages (and Info/Debug messages if they are turned on). 
        # If GLIB_LOG_LEVEL is not defined, normal message output will not be affected.
        # 如果需要, 请应用可选的修补程序。
        # 在许多情况下, 直接或间接通过其他库 (如 GTK+-3.24.41) 使用此库的应用程序在从命令行运行时会输出大量警告。
        # 此修补程序允许使用环境变量 GLIB_LOG_LEVEL 来抑制不需要的消息。变量的值是一个数字，对应于：
        #     1 警报
        #     2 关键
        #     3 错误
        #     4 警告
        #     5 通知
        # 例如, 导出 GLIB_LOG_LEVEL=4 将跳过 "警告" 和 "通知" 消息 (以及 "信息/调试" 消息 (如果已打开)) 的输出。
        # 如果未定义 GLIB_LOG_LEVEL, 则不会影响正常的消息输出。
        # ..........................................
        # * 方法一 (1st Method): patch 方法.
        #                        patch -Np1 -i ../glib-skip_warnings-1.patch
        # ..........................................
        # * 方法二 (2nd Method): sed 方法.
        #                        --- glib-2.68.0.orig/glib/gmessages.c	2021-03-18 08:28:31.909625000 -0500
        #                        +++ glib-2.68.0/glib/gmessages.c	2021-04-01 20:32:23.517596280 -0500
        #                        @@ -528,6 +528,34 @@ static GDestroyNotify log_writer_user_da
        #                         /* --- functions --- */
        #                         
        #                        +/* skip_message
        #                        + *
        #                        + * This internal function queries an optional environment variable,
        #                        + * GLIB_LOG_LEVEL and converts it to a value consistent
        #                        + * with the type GLogLevelFlags. If the value is equal to
        #                        + * or greater than the integer equivalent of the log_level,
        #                        + * then the function returns a boolean that indicates that
        #                        + * logging the output should be skipped.
        #                        + */
        #                        +
        #                        +static gboolean skip_message( GLogLevelFlags log_level);
        #                        +
        #                        +static gboolean skip_message( GLogLevelFlags log_level) 
        #                        +{
        #                        +   char*    user_log_level;
        #                        +   int      user_log_int;
        #                        +   gboolean skip = FALSE;
        #                        +
        #                        +   user_log_level = getenv( "GLIB_LOG_LEVEL" );
        #                        +
        #                        +   user_log_int = ( user_log_level != NULL ) ? atoi( user_log_level ) : 0;
        #                        +   user_log_int = ( user_log_level != 0 ) ? 1 << user_log_int         : 0;
        #                        +
        #                        +   if ( user_log_int >= log_level ) skip = TRUE;
        #                        +
        #                        +   return skip;
        #                        +}
        #                        +
        #                         static void _g_log_abort (gboolean breakpoint);
        #                         
        #                         static void
        sed -i "525i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "526i\\/\* skip_message" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "527i\ \*" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "528i\ \* This internal function queries an optional environment variable\," $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "529i\ \* GLIB_LOG_LEVEL and converts it to a value consistent" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "530i\ \* with the type GLogLevelFlags\. If the value is equal to" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "531i\ \* or greater than the integer equivalent of the log_level\," $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "532i\ \* then the function returns a boolean that indicates that" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "533i\ \* logging the output should be skipped\." $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "534i\ \*\/" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "535i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "536i\static gboolean skip_message\( GLogLevelFlags log_level\)\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "537i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "538i\static gboolean skip_message\( GLogLevelFlags log_level\)" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "539i\\{" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "540i\   char\*    user_log_level\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "541i\   int      user_log_int\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "542i\   gboolean skip \= FALSE\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "543i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "544i\   user_log_level \= getenv\( \"GLIB_LOG_LEVEL\" \)\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "545i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "546i\   user_log_int \= \( user_log_level \!\= NULL \) \? atoi\( user_log_level \) \: 0\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "547i\   user_log_int \= \( user_log_level \!\= 0 \) \? 1 \<\< user_log_int         \: 0\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "548i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "549i\   if \( user_log_int \>\= log_level \) skip \= TRUE\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "550i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "551i\   return skip\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "552i\\}" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "553i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        #                        ...................
        #                        --- glib-2.68.0.orig/glib/gmessages.c	2021-03-18 08:28:31.909625000 -0500
        #                        +++ glib-2.68.0/glib/gmessages.c	2021-04-01 20:32:23.517596280 -0500
        #                        @@ -2591,6 +2619,9 @@ g_log_writer_standard_streams (GLogLevel
        #                           g_return_val_if_fail (fields != NULL, G_LOG_WRITER_UNHANDLED);
        #                           g_return_val_if_fail (n_fields > 0, G_LOG_WRITER_UNHANDLED);
        #                         
        #                        +  /* If the user does not want this message level, just return */
        #                        +  if ( skip_message( log_level) ) return G_LOG_WRITER_HANDLED;
        #                        +
        #                           stream = log_level_to_file (log_level);
        #                           if (!stream || fileno (stream) < 0)
        #                             return G_LOG_WRITER_UNHANDLED;
        sed -i "2626i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2627i\  \/\* If the user does not want this message level\, just return \*\/" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2628i\  if \( skip_message\( log_level\) \) return G_LOG_WRITER_HANDLED\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2629i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        #                        ...................
        #                        --- glib-2.68.0.orig/glib/gmessages.c	2021-03-18 08:28:31.909625000 -0500
        #                        +++ glib-2.68.0/glib/gmessages.c	2021-04-01 20:32:23.517596280 -0500
        #                        @@ -2818,6 +2849,9 @@ _g_log_writer_fallback (GLogLevelFlags
        #                           FILE *stream;
        #                           gsize i;
        #                         
        #                        +  /* If the user does not want this message level, just return */
        #                        +  if ( skip_message( log_level) ) return G_LOG_WRITER_HANDLED;
        #                        +
        #                           /* we cannot call _any_ GLib functions in this fallback handler,
        #                            * which is why we skip UTF-8 conversion, etc.
        #                            * since we either recursed or ran out of memory, we're in a pretty
        sed -i "2859i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2860i\  \/\* If the user does not want this message level\, just return \*\/" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2861i\  if \( skip_message\( log_level\) \) return G_LOG_WRITER_HANDLED\;" $STORAGE/glib-2.78.4/glib/gmessages.c
        sed -i "2862i\ " $STORAGE/glib-2.78.4/glib/gmessages.c
        
        # ------------------------------------------
        # * Configure Option Description:
        # --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                      指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # -Dman=true: This switch causes the build to create and install the package man pages.
        #             此选项使得构建源码时创建并安装软件包手册页。
        # -Dgtk_doc=true: This switch causes the build to create and install the API documentation.
        #                 此选项使得构建源码时创建并安装 API 文档。
        cd $STORAGE/glib-2.78.4 && meson setup build/ --prefix=/opt/glib-2.78.4 \
                                                      --buildtype=release \
                                                      --pkg-config-path=/opt/lib/pkgconfig \
                                                      -Dman=true && \
                                                      STEP_BUILDED=1
        
        # ------------------------------------------
        # * Problem: [1480/1495] Generating docs/reference/gio/glib-compile-schemas-man with a custom command
        #            Error: no ID for constraint linkend: "GSettings"
        #   Explain: 如果安装了 libxslt-1.1.28, 则在安装手册页时, 以下命令可能会指示几个 (约 33 个) 错误, 这些错误以 "Error: no ID for constraint linkend:" 开头。这些是无害的。
        #            If libxslt-1.1.33 is installed, the following command may indicate several (about 33) errors that start with "Error: no ID for constraint linkend:" when installing the man pages. These are harmless.
        cd $STORAGE/glib-2.78.4 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/glib-2.78.4/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/glib-2.78.4/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/glib-2.78.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gio-2.0.pc               /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gio-unix-2.0.pc          /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/glib-2.0.pc              /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gmodule-2.0.pc           /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gmodule-export-2.0.pc    /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gmodule-no-export-2.0.pc /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gobject-2.0.pc           /opt/lib/pkgconfig/
            cp -f /opt/glib-2.78.4/lib/pkgconfig/gthread-2.0.pc           /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/glib-2.78.4/ /opt/sandbox-glib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/glib-2.78.4 && return 0
    else
    
        echo "[Caution] Path: ( /opt/glib-2.78.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    export PATH=$PATH:/opt/sandbox-glib/bin

    # ----------------- Dependency -----------------
    Make_Install_bzip2_1_0_6
    Compile_Install_libxml2_2_9_1
    Compile_Install_libxslt_1_1_28
    # ------- XML Tools (XML DTD) DocBook-XML ------
    Deploy_Install_XML_DTD_DocBook_XML_4_5
    # --- XML Tools (XSL Stylesheets) DocBook-XSL --
    Deploy_Install_XSL_Stylesheets_DocBook_XSL_1_79_1
    # ------------------ ReadLine ------------------
    Compile_Install_ncurses_6_4
    Compile_Install_readline_8_2
    # ------------------- PCRE2 --------------------
    Compile_Install_PCRE2_10_43
    # --------------- Glib - 2.78.4 ----------------
    Build_Install_Glib_2_78_4
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Glib-2.78.4 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
