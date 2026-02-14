# 文章_Linux运维_Bash脚本_编译安装Wayland-1.22.0_GF_2024-02-29

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

libffi-3.4.4.tar.gz

libxml2-2.9.1.tar.gz

expat-2.5.0.tar.gz

libxslt-1.1.28.tar.gz

xmlto-0.0.28.tar.bz2

docbook-xsl-1.79.1.tar.bz2

docbook-xsl-doc-1.79.1.tar.bz2

pixman-0.43.4.tar.gz

cairo-1.18.0.tar.xz

fribidi-1.0.13.tar.xz

graphite2-1.3.14.tgz

harfbuzz-8.3.0.tar.xz

freetype-2.12.0.tar.gz (Recompile and Reinstall)

fontconfig-2.15.0.tar.xz (Recompile and Reinstall)

pango-1.51.2.tar.xz

gts-0.7.6.tar.gz

graphviz-8.1.0.tar.gz

doxygen-1.10.0.src.tar.gz

wayland-1.22.0.tar.gz

wayland-protocols-1.32.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-29 00:06

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.14.x
# * Python == 3.x.x
# * Meson
# * Ninja
# * X11
# * libGD >= 2.3.x (Compiled by: freetype, libpng, jpeg)

# ------------------- Dependency -------------------
# Need File: libffi-3.4.4.tar.gz
# ------------------- XML Tools --------------------
# Need File: libxml2-2.9.1.tar.gz
# Need File: expat-2.5.0.tar.gz
# Need File: libxslt-1.1.28.tar.gz
# Need File: xmlto-0.0.28.tar.bz2
# ----- XML Tools (XSL Stylesheets) DocBook-XSL ----
# Need File: docbook-xsl-1.79.1.tar.bz2
# Need File: docbook-xsl-doc-1.79.1.tar.bz2
# --------- Graphviz Dep: Cairo (Optional) ---------
# Need File: pixman-0.43.4.tar.gz
# Need File: cairo-1.18.0.tar.xz
# --------- Graphviz Dep: Pango (Optional) ---------
# Need File: fribidi-1.0.13.tar.xz
# Need File: graphite2-1.3.14.tgz
# Need File: harfbuzz-8.3.0.tar.xz
# Need File: freetype-2.12.0.tar.gz (Recompile and Reinstall)
# Need File: fontconfig-2.15.0.tar.xz (Recompile and Reinstall)
# Need File: pango-1.51.2.tar.xz
# ---------- Graphviz Dep: GTS (Optional) ----------
# Need File: gts-0.7.6.tar.gz
# -------------------- Graphviz --------------------
# Need File: graphviz-8.1.0.tar.gz
# -------------------- Doxygen ---------------------
# Need File: doxygen-1.10.0.src.tar.gz
# -------------------- Wayland ---------------------
# Need File: wayland-1.22.0.tar.gz
# -------------- Wayland - Protocols ---------------
# Need File: wayland-protocols-1.32.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 编译安装(Compile Install) libffi-3.4.4 (for Linux)
# ##################################################
function Compile_Install_libffi_3_4_4_for_Linux() {

    if [[ ! -d "/opt/libffi-3.4.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( libffi-3.4.4 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/libffi-3.4.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libffi-3.4.4 && ./configure --prefix=/opt/libffi-3.4.4 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/libffi-3.4.4/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/libffi-3.4.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libffi-3.4.4/lib/pkgconfig/libffi.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libffi-3.4.4 && return 0
    else
        echo "[Caution] Path: ( /opt/libffi-3.4.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################ XML Tools #############################################

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

# Function: 编译安装(Compile Install) xmlto-0.0.28
# ##################################################
function Compile_Install_xmlto_0_0_28() {

    if [[ ! -d "/opt/xmlto-0.0.28" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( xmlto-0.0.28 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -jxvf $STORAGE/xmlto-0.0.28.tar.bz2 && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/xmlto-0.0.28 && ./configure --prefix=/opt/xmlto-0.0.28 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/xmlto-0.0.28/bin/xmlif /usr/local/bin/
            ln -sf /opt/xmlto-0.0.28/bin/xmlto /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/xmlto-0.0.28 && return 0
    else
    
        echo "[Caution] Path: ( /opt/xmlto-0.0.28 ) Already Exists."
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

# ################################## Graphviz Dep: Cairo (Optional) ##################################

# Function: 构建安装(Build Install) Pixman-0.43.4
# ##################################################
function Build_Install_Pixman_0_43_4() {

    # Pixman 是由三星工程师开发的像素操作库, 广泛应用于矢量图形 Cario 和 X 服务器等。
    # Pixman 能够提供低级像素处理能力, 同时具备图像合成、图形变化以及光栅化等功能。

    if [[ ! -d "/opt/pixman-0.43.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( pixman-0.43.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/pixman-0.43.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/pixman-0.43.4 && meson build/ --prefix=/opt/pixman-0.43.4 \
                                                  --pkg-config-path=/opt/lib/pkgconfig && \
                                                  STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/pixman-0.43.4 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/pixman-0.43.4/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/pixman-0.43.4/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/pixman-0.43.4/lib/pkgconfig/pixman-1.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pixman-0.43.4 && return 0
    else
    
        echo "[Caution] Path: ( /opt/pixman-0.43.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Cairo-1.18.0
# ##################################################
function Build_Install_Cairo_1_18_0() {

    # Attention: may conflict with the original "Cairo" in the system. Especially Ubuntu.
    # 注意: 可能与系统原有的 "Cairo" 冲突。尤其是 Ubuntu。

    if [[ ! -d "/opt/cairo-1.18.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( cairo-1.18.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/cairo-1.18.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: Run-time dependency gobject-2.0 found: NO (tried pkgconfig and cmake)
        #            Looking for a fallback subproject for the dependency gobject-2.0
        #            Downloading glib source from https://download.gnome.org/sources/glib/2.74/glib-2.74.0.tar.xz
        #   - Solve: 方法 A. 编译 Glib 库。
        #            方法 B. meson Build 添加 -Dglib=disabled 选项, 此选项禁用了 Glib, 因为特别是含有 Gnome 的发行版 Linux 中 Glib 是 Gnome 的基础, glib 已集成到系统, 没有完整的 Glib 供调用。
        # ..........................................
        # *  Option: -Dxlib-xcb=enabled: This switch enables several experimental Xlib/XCB functions used by some window managers.
        #                                此选项启用了一些窗口管理器使用的几个实验性 Xlib/XCB 函数。
        cd $STORAGE/cairo-1.18.0 && meson build/ --prefix=/opt/cairo-1.18.0 \
                                                 --buildtype=release \
                                                 --pkg-config-path=/opt/lib/pkgconfig \
                                                 -Dxlib=enabled && \
                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/cairo-1.18.0 && ninja -C build/ install && STEP_INSTALLED=1

        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/cairo-1.18.0/bin/cairo-trace /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/cairo-1.18.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/cairo-1.18.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/cairo-1.18.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/cairo-1.18.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/cairo-1.18.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################## Graphviz Dep: Pango (Optional) ##################################

# Function: 构建安装(Build Install) FriBidi-1.0.13
# ##################################################
function Build_Install_FriBidi_1_0_13() {

    # Attention: may conflict with the original "FriBidi" in the system. Especially Ubuntu.
    # 注意: 可能与系统原有的 "FriBidi" 冲突。尤其是 Ubuntu。

    if [[ ! -d "/opt/fribidi-1.0.13" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( fribidi-1.0.13 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/fribidi-1.0.13.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/fribidi-1.0.13 && meson build/ --prefix=/opt/fribidi-1.0.13 \
                                                   --buildtype=release \
                                                   --pkg-config-path=/opt/lib/pkgconfig && \
                                                   STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/fribidi-1.0.13 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/fribidi-1.0.13/bin/fribidi /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/fribidi-1.0.13/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/fribidi-1.0.13/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/fribidi-1.0.13/lib/pkgconfig/fribidi.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/fribidi-1.0.13 && return 0
    else
    
        echo "[Caution] Path: ( /opt/fribidi-1.0.13 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Graphite2-1.3.14
# ##################################################
function Build_Install_Graphite2_1_3_14() {

    if [[ ! -d "/opt/graphite2-1.3.14" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_MADE=0
        local STEP_DOCUMENTED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( graphite2-1.3.14 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/graphite2-1.3.14.tgz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # Some tests fail if FontTools (Python 3 module) is not installed. These tests can be removed with:
        # 如果未安装 FontTools (Python3 模块), 某些测试将失败。这些测试可以通过以下方式删除：
        if [[ $STEP_UNZIPPED == 1 ]]; then
            sed -i '/cmptest/d' $STORAGE/graphite2-1.3.14/tests/CMakeLists.txt
        fi
        
        # ------------------------------------------
        mkdir $STORAGE/graphite2-1.3.14/build && STEP_CREATED=1
        
        # ------------------------------------------
        # *  Option: -DCMAKE_VERBOSE_MAKEFILE=ON: This switch turns on build verbose mode.
        #                                         此选项打开将生成详细模式。
        cd $STORAGE/graphite2-1.3.14/build && cmake ../ -G "Unix Makefiles" \
                                                        -DCMAKE_INSTALL_PREFIX=/opt/graphite2-1.3.14 \
                                                        -DCMAKE_BUILD_TYPE=Release && \
                                                        STEP_BUILDED=1
                                                        
        # ------------------------------------------
        make && STEP_MADE=1

        # ------------------------------------------
        # If you wish to build the documentation, issue: make docs
        # 如果您希望构建文档, 请使用指令: make docs
        # Skip # make docs && STEP_DOCUMENTED=1
        
        # ------------------------------------------
        # To test the results, issue: make test. One test named nametabletest is known to fail.
        # 要测试结果, 请使用指令: 进行测试。已知有一个名为 nametabletest 的测试失败。
        make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # If you built the documentation, install, as the root user:
        # 如果您构建了文档, 请以 root 用户身份安装:
        if [[ $STEP_DOCUMENTED == 1 ]]; then
            install -v -d -m755 /usr/share/doc/graphite2-1.3.14 &&
            
            cp      -v -f    doc/{GTF,manual}.html \
                                /usr/share/doc/graphite2-1.3.14 &&
            cp      -v -f    doc/{GTF,manual}.pdf \
                                /usr/share/doc/graphite2-1.3.14
        fi
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/graphite2-1.3.14/bin/gr2fonttest /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/graphite2-1.3.14/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/graphite2-1.3.14/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/graphite2-1.3.14/lib/pkgconfig/graphite2.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/graphite2-1.3.14 && return 0
    else
    
        echo "[Caution] Path: ( /opt/graphite2-1.3.14 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) HarfBuzz-8.3.0
# ##################################################
function Build_Install_HarfBuzz_8_3_0() {

    # Attention: may conflict with the original "HarfBuzz" in the system. Especially Ubuntu.
    # 注意: 可能与系统原有的 "HarfBuzz" 冲突。尤其是 Ubuntu。

    if [[ ! -d "/opt/harfbuzz-8.3.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( harfbuzz-8.3.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/harfbuzz-8.3.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                 指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        #            ...............................
        #            -Dgraphite2=enabled: This switch enables Graphite2 support, which is required for building texlive-20230313 or LibreOffice-24.2.1.2 with system harfbuzz.
        #                                 此选项启用 Graphite2 支持, 这是使用系统 harfbuzz 构建 texlive-20230313 或 LibreOffice-24.1.2 所必需的。
        #            ...............................
        #            -Ddocs=disabled: If GTK-Doc-1.34.0 is installed, the documentation is built and installed. This switch prevents that.
        #                             如果安装了GTK-Doc-1.34.0, 则生成并安装文档。这个选项可以防止这种情况发生。
        #            ...............................
        # * Problem: Program glib-mkenums mkenums found: NO
        #            src/meson.build:902:2: ERROR: Program 'glib-mkenums mkenums' not found or not executable
        #   - Solve: 找不到可执行文件 glib-mkenums (由于 glib 可执行文件和库文件加载进系统可能造成内核崩溃, 只在需要时调用)。
        #            编译前使用指令: export PATH=$PATH:/opt/glib-2.78.4/bin
        # ..........................................
        # * Problem: /usr/bin/ld: warning: libpcre2-8.so.0, needed by /opt/glib-2.78.4/lib/libglib-2.0.so, not found (try using -rpath or -rpath-link)
        #            /opt/glib-2.78.4/lib/libglib-2.0.so：对‘pcre2_get_ovector_count_8’未定义的引用
        #   - Solve: 找不到 PCRE2 的 libpcre2-8.so.0 库文件 (由于 PCRE2 库文件加载进系统可能造成内核崩溃, 只在需要时调用)。
        #            编译前使用指令: export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/pcre2-10.43/lib
        cd $STORAGE/harfbuzz-8.3.0 && meson setup build/ --prefix=/opt/harfbuzz-8.3.0 \
                                                         --buildtype=release \
                                                         --pkg-config-path=/opt/lib/pkgconfig \
                                                         -Dgraphite2=enabled && \
                                                         STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/harfbuzz-8.3.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/harfbuzz-8.3.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/harfbuzz-8.3.0/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/harfbuzz-8.3.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/harfbuzz-8.3.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
            # ......................................
            # 重新编译安装 (Recompile Reinstall) 第 1 步: 重新编译安装 FreeType-2.12.0。
            # After HarfBuzz-8.3.0 is installed, reinstall FreeType-2.12.0
            # 安装 HarfBuzz-8.3.0 后, 重新安装 FreeType-2.12.0。
            if [[ -d "/opt/freetype-2.12.0" ]]; then rm -rf /opt/freetype-2.12.0; fi
            # ......................................
            # 重新编译安装 (Recompile Reinstall) 第 2 步: 重新编译安装 Fontconfig-2.15.0。
            # Fontconfig-2.15.0 must be built with FreeType-2.12.0 using HarfBuzz-8.3.0
            # Fontconfig-2.15.0 必须使用 HarfBuzz-8.3.0 构建的 FreeType-2.12.0。
            if [[ -d "/opt/fontconfig-2.15.0" ]]; then rm -rf /opt/fontconfig-2.15.0; fi
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/harfbuzz-8.3.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/harfbuzz-8.3.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) freetype-2.12.0
# ##################################################
function Compile_Install_freetype_2_12_0() {

    if [[ ! -d "/opt/freetype-2.12.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( freetype-2.12.0 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/freetype-2.12.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: /usr/bin/ld: //usr/local/lib/libbz2.a(blocksort.o): relocation R_X86_64_PC32 against symbol `stderr@@GLIBC_2.2.5' can not be used when making a shared object; recompile with -fPIC
        #            /usr/bin/ld: final link failed: Bad value
        #            collect2: error: ld returned 1 exit status
        #            config.mk:55: recipe for target '/home/goufeng/freetype-2.12.0/objs/libfreetype.la' failed
        #   - Solve: 在对 bzip2 执行 make 前, 修改 Makefile。
        #                # To assist in cross-compiling
        #                CC=gcc -fPIC # -> 第 1 处修改, 加上 -fPIC。
        #                AR=ar
        #                RANLIB=ranlib
        #                LDFLAGS=
        #                
        #                BIGFILES=-D_FILE_OFFSET_BITS=64
        #                CFLAGS=-Wall -Winline -O2 -fPIC -g $(BIGFILES) # -> 第 2 处修改, 加上 -fPIC。
        #            (第 1 处貌似是外层, 我先是在第 2 处修改后依旧不起作用的时候, 在第 1 处也添加了)
        #            然后进行 make -f Makefile-libbz2_so (在当前目录生成 Shared Library libbz2.so) 或者 make install。
        cd $STORAGE/freetype-2.12.0 && ./configure --prefix=/opt/freetype-2.12.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            rsync -av /opt/freetype-2.12.0/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/freetype-2.12.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/freetype-2.12.0/lib/pkgconfig/freetype2.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/freetype-2.12.0 && return 0
    else
        echo "[Caution] Path: ( /opt/freetype-2.12.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) fontconfig-2.15.0
# ##################################################
function Compile_Install_fontconfig_2_15_0() {

    if [[ ! -d "/opt/fontconfig-2.15.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( fontconfig-2.15.0 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -xvJf $STORAGE/fontconfig-2.15.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/fontconfig-2.15.0 && ./configure --prefix=/opt/fontconfig-2.15.0 \
                                                     PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                     STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/fontconfig-2.15.0/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/fontconfig-2.15.0/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/fontconfig-2.15.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/fontconfig-2.15.0/lib/pkgconfig/fontconfig.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/fontconfig-2.15.0 && return 0
    else
        echo "[Caution] Path: ( /opt/fontconfig-2.15.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) Pango-1.51.2
# ##################################################
function Build_Install_Pango_1_51_2() {

    # Attention: may conflict with the original "Pango" in the system. Especially Ubuntu.
    # 注意: 可能与系统原有的 "Pango" 冲突。尤其是 Ubuntu。

    if [[ ! -d "/opt/pango-1.51.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( pango-1.51.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/pango-1.51.2.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --wrap-mode=nofallback: This switch prevents meson from using subproject fallbacks for any dependency declarations in the build files,
        #                                    stopping it downloading any optional dependency which is not installed on the system.
        #                                    这个选项防止 Meson 对构建文件中的任何依赖项声明使用子项目回退, 从而阻止它下载任何未安装在系统上的可选依赖项。
        cd $STORAGE/pango-1.51.2 && meson build/ --prefix=/opt/pango-1.51.2 \
                                                 --buildtype=release \
                                                 --wrap-mode=nofallback \
                                                 --pkg-config-path=/opt/lib/pkgconfig && \
                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/pango-1.51.2 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/pango-1.51.2/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/pango-1.51.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/pango-1.51.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/pango-1.51.2/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/pango-1.51.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/pango-1.51.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ################################### Graphviz Dep: GTS (Optional) ###################################

# Function: 编译安装(Compile Install) GTS-0.7.6
# ##################################################
function Compile_Install_GTS_0_7_6() {

    # Attention: may conflict with the original "GTS" in the system. Especially Ubuntu.
    # 注意: 可能与系统原有的 "GTS" 冲突。尤其是 Ubuntu。

    if [[ ! -d "/opt/gts-0.7.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( gts-0.7.6 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/gts-0.7.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gts-0.7.6 && ./configure --prefix=/opt/gts-0.7.6 \
                                             PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                             STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gts-0.7.6/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gts-0.7.6/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/gts-0.7.6/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/gts-0.7.6/lib/pkgconfig/gts.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gts-0.7.6 && return 0
    else
        echo "[Caution] Path: ( /opt/gts-0.7.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# Graphviz #############################################

# Function: 编译安装(Compile Install) Graphviz-8.1.0
# ##################################################
function Compile_Install_Graphviz_8_1_0() {

    # Graphviz 默认不能识别 .png 和 .jpeg 格式, 需要安装编译有 libpng 和 jpeg 支持的 libGD 库。
    # Graphviz does not recognize .png and .jpeg formats by default, and requires the installation and compilation of libGD libraries supported by libpng and jpeg.

    if [[ ! -d "/opt/graphviz-8.1.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
        
        # ------------------------------------------
        echo "[Confirm] Compile and Install ( graphviz-8.1.0 )? (y/n)"
        # ..........................................
        read VERIFY
        # ..........................................
        if [[ $VERIFY != "y" ]]; then exit 1; fi
        
        # ------------------------------------------
        tar -zxvf $STORAGE/graphviz-8.1.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/graphviz-8.1.0 && ./configure --prefix=/opt/graphviz-8.1.0 \
                                                  PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                  STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/graphviz-8.1.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/graphviz-8.1.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/graphviz-8.1.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/graphviz-8.1.0 && return 0
    else
        echo "[Caution] Path: ( /opt/graphviz-8.1.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# Doxygen ##############################################

# Function: 构建安装(Build Install) Doxygen-1.10.0
# ##################################################
function Build_Install_Doxygen_1_10_0() {

    if [[ ! -d "/opt/doxygen-1.10.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( doxygen-1.10.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/doxygen-1.10.0.src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        mkdir $STORAGE/doxygen-1.10.0/build && STEP_CREATED=1
        
        # ------------------------------------------
        # * Problem: [ 15%] Built target xml
        #            [ 16%] Generating ../generated_src/configvalues.h
        #            No module named 'pyexpat'
        #   - Solve: 查找路径问题, cp -r /usr/local/Python-3.8.0/lib/python3.8 /usr/local/lib/
        # ..........................................
        # * Problem: CMake Error at /opt/cmake-3.28.3/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
        #              Could NOT find Iconv (missing: ICONV_COMPILES)
        #   - Solve: 回溯有关 iconv 的配置信息:
        #            ......
        #            -- Looking for iconv_open
        #            -- Looking for iconv_open - found
        #            -- Found Iconv: In glibc
        #            -- Performing Test ICONV_COMPILES
        #            -- Performing Test ICONV_COMPILES - Failed
        #            ......
        #            如果其中有 "-- Found Iconv: In glibc" 后面还出现 "Could NOT find Iconv (missing: ICONV_COMPILES)", 则说明系统原有的 iconv 和新装的 iconv 冲突了。
        #            系统调用的是包含在 glibc 中的 iconv (iconv 是 glibc 中的内容) 却被新装的 iconv 的 include 或 library 抢占了加载优先级, 导致 iconv 测试失败。
        #            相关资料 (http://en.wikipedia.org/wiki/Iconv):
        #                All recent Linux distributions contain a free implementation of iconv() as part of the GNU C Library which is the C library for current Linux systems.
        #                To use it, the GNU glibc locales need to be installed, which are provided as a separate package (usually named glibc-locale) normally installed by default.
        #            移除新装的 iconv 后问题解决。
        cd $STORAGE/doxygen-1.10.0/build && cmake ../ -G "Unix Makefiles" \
                                                      -DCMAKE_BUILD_TYPE=Release \
                                                      -DCMAKE_INSTALL_PREFIX=/opt/doxygen-1.10.0 && \
                                                      STEP_BUILDED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/doxygen-1.10.0/bin/doxygen /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/doxygen-1.10.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/doxygen-1.10.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# Wayland ##############################################

# Function: 构建安装(Build Install) Wayland-1.22.0
# ##################################################
function Build_Install_Wayland_1_22_0() {

    if [[ ! -d "/opt/wayland-1.22.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( wayland-1.22.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/wayland-1.22.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: Program dot found: NO
        #            doc/meson.build:5:0: ERROR: Program 'dot' not found or not executable
        #   - Solve: Install Graphviz, 或者如果您不需要构建文档, 构建时添加 -Ddocumentation=false 选项就会关闭文档, 则不需要 dot。
        # ..........................................
        # * Problem: Message: doxygen: 1.10.0 (GIT-NOTFOUND)
        #            Message: dot: dot - graphviz version 8.1.0 (20230707.0739)
        #            doc/meson.build:27:1: ERROR: Problem encountered: The style sheet for man pages providing "http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl" was not found.
        #   - Solve: Install DocBook-XSL.
        cd $STORAGE/wayland-1.22.0 && meson build/ --prefix=/opt/wayland-1.22.0 \
                                                   --pkg-config-path=/opt/lib/pkgconfig && \
                                                   STEP_BUILDED=1
        
        # ------------------------------------------
        # * Problem: [16/108] Generating doc/doxygen/xml/wayland-architecture.png with a custom command
        #            FAILED: doc/doxygen/xml/wayland-architecture.png
        #            /usr/local/bin/dot -Tpng -odoc/doxygen/xml/wayland-architecture.png ../doc/doxygen/dot/wayland-architecture.gv
        #            Format: "png" not recognized. Use one of: canon cmap cmapx cmapx_np dot dot_json eps fig gv imap imap_np ismap json json0 mp pic plain plain-ext pov ps ps2 svg svgz tk xdot xdot1.2 xdot1.4 xdot_json
        #   - Solve: Install libGD.
        cd $STORAGE/wayland-1.22.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            ln -sf /opt/wayland-1.22.0/bin/* /usr/local/bin/
            # ......................................
            rsync -av /opt/wayland-1.22.0/include/ /usr/local/include/
            # ......................................
            rsync -av /opt/wayland-1.22.0/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/wayland-1.22.0/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/wayland-1.22.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/wayland-1.22.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ####################################### Wayland - Protocols ########################################

# Function: 构建安装(Build Install) Wayland-Protocols-1.32
# ##################################################
function Build_Install_Wayland_Protocols_1_32() {

    if [[ ! -d "/opt/wayland-protocols-1.32" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( wayland-protocols-1.32 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/wayland-protocols-1.32.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/wayland-protocols-1.32 && meson build/ --prefix=/opt/wayland-protocols-1.32 \
                                                           --pkg-config-path=/opt/lib/pkgconfig && \
                                                           STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/wayland-protocols-1.32 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            cp -f /opt/wayland-protocols-1.32/share/pkgconfig/wayland-protocols.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/wayland-protocols-1.32 && return 0
    else
    
        echo "[Caution] Path: ( /opt/wayland-protocols-1.32 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    export C_INCLUDE_PATH=/opt/sandbox-X11/include
    export CPLUS_INCLUDE_PATH=/opt/sandbox-X11/include
    # ..............................................
    export LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/sandbox-glib/lib:/opt/fribidi-1.0.13/lib
    export LD_LIBRARY_PATH=/opt/sandbox-X11/lib:/opt/sandbox-glib/lib:/opt/fribidi-1.0.13/lib
    # ..............................................
    export PATH=$PATH:/opt/sandbox-glib/bin
    
    # ----------------- Dependency -----------------
    Compile_Install_libffi_3_4_4
    # ----------------- XML Tools ------------------
    Compile_Install_libxml2_2_9_1
    Compile_Install_expat_2_5_0
    Compile_Install_libxslt_1_1_28
    Compile_Install_xmlto_0_0_28
    # --- XML Tools (XSL Stylesheets) DocBook-XSL --
    Deploy_Install_XSL_Stylesheets_DocBook_XSL_1_79_1
    # ------- Graphviz Dep: Cairo (Optional) -------
    Build_Install_Pixman_0_43_4
    Build_Install_Cairo_1_18_0
    # ------- Graphviz Dep: Pango (Optional) -------
    Build_Install_FriBidi_1_0_13
    Build_Install_Graphite2_1_3_14
    Build_Install_HarfBuzz_8_3_0
    Compile_Install_freetype_2_12_0
    Compile_Install_fontconfig_2_15_0
    Build_Install_Pango_1_51_2
    # -------- Graphviz Dep: GTS (Optional) --------
    Compile_Install_GTS_0_7_6
    # ------------------ Graphviz ------------------
    Compile_Install_Graphviz_8_1_0
    # ------------------ Doxygen -------------------
    Build_Install_Doxygen_1_10_0
    # ------------------ Wayland -------------------
    Build_Install_Wayland_1_22_0
    # ------------ Wayland - Protocols -------------
    Build_Install_Wayland_Protocols_1_32
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Wayland-1.22.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
