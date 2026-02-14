# 文章_Linux运维_Bash脚本_编译安装GTK+-3.24.41_GF_2023-02-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

shared-mime-info-2.2.tar.gz

libjpeg-turbo-3.0.0.tar.gz

docutils-0.20.1.tar.gz (Python 源码)

gdk-pixbuf-2.42.10.tar.xz

libepoxy-1.5.10.tar.xz

gobject-introspection-1.78.1.tar.xz

atk-2.35.1.tar.xz

dbus-1.14.10.tar.xz

recordproto-1.14.2.tar.gz (Part of X11)

libXtst-1.2.3.tar.gz (Part of X11)

at-spi2-core-2.38.0.tar.xz

at-spi2-atk-2.20.1.tar.xz

libxkbcommon-1.6.0.tar.xz

gir-file-for-gtk+-20190203.tar.gz

gtk+-3.24.41.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-09 01:22

# --------------------------------------------------
# Install First: 
# * GNU-Tools (Contains: pkg-config, m4, autoconf, automake, libtool, gettext, flex, bison, libiconv, make)
# * CMake >= 3.14.0
# * Python == 3.x.x
# * Meson
# * Ninja
# * X11
# * Glib
# * libGD == 2.3.x (Compiled by: freetype, libpng, jpeg)
# * Mesa(OpenGL) == 23.3.x

# ------------------- Dependency -------------------
# Need File: shared-mime-info-2.2.tar.gz
# Need File: libjpeg-turbo-3.0.0.tar.gz
# Need File: docutils-0.20.1.tar.gz (Python 源码)
# Need File: gdk-pixbuf-2.42.10.tar.xz
# Need File: libepoxy-1.5.10.tar.xz
# Need File: gobject-introspection-1.78.1.tar.xz
# Need File: atk-2.35.1.tar.xz
# Need File: dbus-1.14.10.tar.xz
# Need File: recordproto-1.14.2.tar.gz
# Need File: libXtst-1.2.3.tar.gz
# Need File: at-spi2-core-2.38.0.tar.xz
# Need File: at-spi2-atk-2.20.1.tar.xz
# Need File: libxkbcommon-1.6.0.tar.xz
# --------------- gir-file-for-gtk+ ----------------
# Need File: gir-file-for-gtk+-20190203.tar.gz
# ---------------------- GTK+ ----------------------
# Need File: gtk+-3.24.41.tar.xz

# ##################################################
STORAGE=/home/goufeng

# ############################################ Dependency ############################################

# Function: 构建安装(Build Install) Shared-Mime-Info-2.2
# ##################################################
function Build_Install_Shared_Mime_Info_2_2() {

    if [[ ! -d "/opt/shared-mime-info-2.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( shared-mime-info-2.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/shared-mime-info-2.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # If you wish to run the test suite, you must first extract the xdgmime tarball into the current directory, and compile it so that meson can find it:
        # 如果您希望运行测试套件, 您必须首先将 xdgmime 的 Tarball 压缩包提取到当前目录中, 并对其进行编译, 以便 Meson 能够找到它:
        # tar -xf ../xdgmime.tar.xz &&
        # make -C xdgmime
        
        # ------------------------------------------
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                 指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # ..........................................
        # *  Option: -Dupdate-mimedb=true: This parameter tells the build system to run update-mime-database during installation. Otherwise, this must be done manually in order to be able to use the MIME database.
        #                                  此参数告诉构建系统在安装期间运行 update-mime-database。否则, 必须手动执行此操作才能使用 MIME 数据库。
        cd $STORAGE/shared-mime-info-2.2 && meson build/ --prefix=/opt/shared-mime-info-2.2 \
                                                         --buildtype=release \
                                                         -Dupdate-mimedb=true \
                                                         --pkg-config-path=/opt/lib/pkgconfig && \
                                                         STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/shared-mime-info-2.2 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/shared-mime-info-2.2/bin/update-mime-database /usr/local/bin/
            # ......................................
            cp -f /opt/shared-mime-info-2.2/share/pkgconfig/shared-mime-info.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/shared-mime-info-2.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/shared-mime-info-2.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libjpeg-turbo-3.0.0
# ##################################################
function Build_Install_libjpeg_turbo_3_0_0() {

    if [[ ! -d "/opt/libjpeg-turbo-3.0.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CREATED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libjpeg-turbo-3.0.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libjpeg-turbo-3.0.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        mkdir $STORAGE/libjpeg-turbo-3.0.0/build && STEP_CREATED=1
        
        # ------------------------------------------
        # 默认选项 (Default Option):
        # cmake -DCMAKE_INSTALL_PREFIX=/usr
        # -DCMAKE_BUILD_TYPE=RELEASE
        # -DENABLE_STATIC=FALSE
        # -DCMAKE_INSTALL_DOCDIR=/usr/share/doc/libjpeg-turbo-3.0.0
        # -DCMAKE_INSTALL_DEFAULT_LIBDIR=lib
        # ..........................................
        # *  Option: -DWITH_JPEG8=ON: This switch enables compatibility with libjpeg version 8.
        #            此选项启用与 libjpeg 版本 8 的兼容性。
        cd $STORAGE/libjpeg-turbo-3.0.0/build && cmake ../ -G "Unix Makefiles" \
                                                           -DCMAKE_INSTALL_PREFIX=/opt/libjpeg-turbo-3.0.0 \
                                                           -DCMAKE_BUILD_TYPE=Release \
                                                           -DENABLE_STATIC=FALSE && \
                                                           STEP_BUILDED=1

        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/libjpeg-turbo-3.0.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libjpeg-turbo-3.0.0/include/ /usr/local/include/
            # Skip # rsync -av /opt/libjpeg-turbo-3.0.0/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libjpeg-turbo-3.0.0/lib/pkgconfig/libjpeg.pc      /opt/lib/pkgconfig/
            cp -f /opt/libjpeg-turbo-3.0.0/lib/pkgconfig/libturbojpeg.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libjpeg-turbo-3.0.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libjpeg-turbo-3.0.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) docutils-0.20.1 (by Python3)
# ##################################################
function Build_Install_docutils_0_20_1_by_Python3() {

    # 使用 expr index "$string" "$substring" 来判断字符串 $string 中是否包含子字符串 $substring。
    # Use the expr index "$string" and "$substring" to determine whether the string $string contains a substring $substring.
    
    # 如果子字符串存在, 则返回子字符串在原字符串中的位置 (从 1 开始), 否则返回 0。
    # If the substring exists, return the position of the substring in the original string (starting from 1), otherwise return 0.
    
    local EXISTS_LINE=$(pip3 list | grep "docutils")
    local EXISTS_NAME=$(expr index "$EXISTS_LINE" "docutils")
    local EXISTS_VERSION=$(expr index "$EXISTS_LINE" "0.20.1")

    if [[ $EXISTS_NAME == 0 && $EXISTS_VERSION == 0 ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( docutils-0.20.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/docutils-0.20.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/docutils-0.20.1 && python3 setup.py build && STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/docutils-0.20.1 && python3 setup.py install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            ln -sf /opt/Python-3.8.0/bin/docutils /usr/local/bin/
            # ......................................
            cp -f /opt/Python-3.8.0/bin/rst2html4.py          /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2html5.py          /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2html.py           /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2latex.py          /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2man.py            /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2odt_prepstyles.py /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2odt.py            /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2pseudoxml.py      /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2s5.py             /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2xetex.py          /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rst2xml.py            /usr/local/bin/
            cp -f /opt/Python-3.8.0/bin/rstpep2html.py        /usr/local/bin/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/docutils-0.20.1 && return 0
    else
    
        echo "[Caution] Python Program: ( docutils-0.20.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) GDK-Pixbuf-2.42.10
# ##################################################
function Build_Install_GDK-Pixbuf_2_42_10() {

    # runtime dependency, needed for loading symbolic icons: librsvg-2.56.3
    # runtime dependency, needed for loading TIFF images: libtiff-4.5.1
    # runtime dependency, needed for loading XPM images: gdk-pixbuf-xlib-2.40.2
    # runtime dependency, needed for loading AVIF images: libavif-0.11.1
    # runtime dependency, needed for loading WebP images: webp-pixbuf-loader-0.2.4
    # Required if building GNOME: gobject-introspection-1.76.1

    if [[ ! -d "/opt/gdk-pixbuf-2.42.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local NINJA=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gdk-pixbuf-2.42.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/gdk-pixbuf-2.42.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                 指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # ..........................................
        # *  Option: --wrap-mode=nofallback: This switch prevents meson from using subproject fallbacks for any dependency declarations in the build files, stopping it downloading any optional dependency which is not installed on the system.
        #                                    此选项可防止 Meson 对构建文件中的任何依赖项声明使用子项目回退, 从而阻止其下载任何未安装在系统上的可选依赖项。
        # ..........................................
        # *  Option: -Dman=false: Use this option if you do not want to generate manual pages, or if you do not want to install docutils-0.20.1.
        #                         如果您不想生成手动页面, 或者不想安装 docutils-0.20.1, 请使用此选项。
        # ..........................................
        # * Problem: Program rst2man rst2man.py found: NO
        #            docs/meson.build:70:2: ERROR: Problem encountered: No rst2man found, but man pages were explicitly enabled
        #   - Solve: 安装 Python3 模块 docutil。
        cd $STORAGE/gdk-pixbuf-2.42.10 && meson build/ --prefix=/opt/gdk-pixbuf-2.42.10 \
                                                       --buildtype=release \
                                                       --wrap-mode=nofallback \
                                                       --pkg-config-path=/opt/lib/pkgconfig && \
                                                       STEP_BUILDED=1
                                                       
        # ------------------------------------------
        ninja && NINJA=1
        
        # ------------------------------------------
        # If you have Gi-DocGen-2023.1 installed and wish to build the API documentation for this package, issue:
        # 如果您安装了 Gi-DocGen-2023.1, 并希望为此软件包构建 API 文档, 请使用以下指令:
        # sed "/docs_dir =/s@\$@ / 'gdk-pixbuf-2.42.10'@" -i ../docs/meson.build &&
        # meson configure -Dgtk_doc=true                                         &&
        # ninja
        
        # ------------------------------------------
        # To test the results, issue: "ninja test". The tests make a heavy use of disk.
        # 要测试结果, 请使用指令: "ninja test"。测试大量使用磁盘。
        
        # ------------------------------------------
        cd $STORAGE/gdk-pixbuf-2.42.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gdk-pixbuf-2.42.10/bin/gdk-pixbuf-csource       /usr/local/bin/
            # Skip # ln -sf /opt/gdk-pixbuf-2.42.10/bin/gdk-pixbuf-pixdata       /usr/local/bin/
            # Skip # ln -sf /opt/gdk-pixbuf-2.42.10/bin/gdk-pixbuf-query-loaders /usr/local/bin/
            # Skip # ln -sf /opt/gdk-pixbuf-2.42.10/bin/gdk-pixbuf-thumbnailer   /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gdk-pixbuf-2.42.10/include/ /usr/local/include/
            # Skip # rsync -av /opt/gdk-pixbuf-2.42.10/lib/     /usr/local/lib/
            # Skip # rsync -av /opt/gdk-pixbuf-2.42.10/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/gdk-pixbuf-2.42.10/lib/pkgconfig/gdk-pixbuf-2.0.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # If you installed the package on to your system using a "DESTDIR" method, an important file was not installed and should be copied and/or generated. Generate it using the following command as the root user:
        # 如果您使用 "DESTDIR" 方法将程序包安装到系统上, 则表明未安装重要文件, 应复制 和/或 生成该文件。作为 root 用户使用以下命令生成它:
        # gdk-pixbuf-query-loaders --update-cache

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gdk-pixbuf-2.42.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gdk-pixbuf-2.42.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libepoxy-1.5.10
# ##################################################
function Build_Install_libepoxy_1_5_10() {

    if [[ ! -d "/opt/libepoxy-1.5.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libepoxy-1.5.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libepoxy-1.5.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: --buildtype=release: Specify a buildtype suitable for stable releases of the package, as the default may produce unoptimized binaries.
        #                                 指定一个适用于包的稳定版本的构建类型, 因为默认情况下可能会生成未优化的二进制文件。
        # ..........................................
        # *  Option: -Ddocs=true: If you have Doxygen-1.9.7 installed, add this option to generate additional documentation.
        #                         如果安装了 Doxygen-1.9.7, 请添加此选项以生成附加文档。
        cd $STORAGE/libepoxy-1.5.10 && meson build/ --prefix=/opt/libepoxy-1.5.10 \
                                                    --buildtype=release \
                                                    --pkg-config-path=/opt/lib/pkgconfig && \
                                                    STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libepoxy-1.5.10 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libepoxy-1.5.10/include/ /usr/local/include/
            # Skip # rsync -av /opt/libepoxy-1.5.10/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/libepoxy-1.5.10/lib/pkgconfig/epoxy.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libepoxy-1.5.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libepoxy-1.5.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) GObject-Introspection-1.78.1
# ##################################################
function Build_Install_GObject_Introspection_1_78_1() {

    # GObject Introspection (缩写为 G-I) 是一个从 C 代码中提取 API 并生成二进制类型库的系统, 非 C语言 绑定和其他工具可以使用该库来 Introspection 或包装原始 C 库。
    # 它使用 C 代码中文档注释中的注释系统来公开关于 API 的额外信息, 这些信息不是代码本身的机器可读信息。
    # GObject introspection (abbreviated G-I) is a system which extracts APIs from C code and produces binary type libraries which can be used by non-C language bindings, and other tools, to introspect or wrap the original C libraries.
    # It uses a system of annotations in documentation comments in the C code to expose extra information about the APIs which is not machine readable from the code itself.
    # ..............................................
    # GLib 和 GObject Introspection 之间存在一个依赖循环。
    # There is a dependency cycle between GLib and GObject-Introspection. 

    if [[ ! -d "/opt/gobject-introspection-1.78.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_NINJA=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gobject-introspection-1.78.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/gobject-introspection-1.78.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: -Dgtk_doc=true: Build and install the documentation.
        #                            构建并安装文档。
        # ..........................................
        # *  Option: -Dcairo=enabled: Use cairo for tests.
        #                             使用 cairo 进行测试。
        # ..........................................
        # *  Option: -Ddoctool=enabled: Install g-ir-doc-tool and run related tests.
        #                               安装g-ir-doc-tool并运行相关测试。
        cd $STORAGE/gobject-introspection-1.78.1 && meson build/ --prefix=/opt/gobject-introspection-1.78.1 \
                                                                 --buildtype=release \
                                                                 --pkg-config-path=/opt/lib/pkgconfig && \
                                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        # To test the results, fix an incompatibility of the test suite with Python 3.12 or later and then run the test suite:
        # 要测试结果, 请修复测试套件与 Python 3.12 或更高版本的不兼容性, 然后运行测试套件:
        # sed "/PYTHONPATH/a'/usr/lib/python3.12'," -i ../tests/warn/meson.build &&
        # ninja test
        ninja && STEP_NINJA=1
        
        # ------------------------------------------
        cd $STORAGE/gobject-introspection-1.78.1 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/gobject-introspection-1.78.1/bin/     /usr/local/bin/
            # Skip # rsync -av /opt/gobject-introspection-1.78.1/include/ /usr/local/include/
            # Skip # rsync -av /opt/gobject-introspection-1.78.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/gobject-introspection-1.78.1/lib/pkgconfig/gobject-introspection-1.0.pc           /opt/lib/pkgconfig/
            cp -f /opt/gobject-introspection-1.78.1/lib/pkgconfig/gobject-introspection-no-export-1.0.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/gobject-introspection-1.78.1/ /opt/sandbox-glib/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gobject-introspection-1.78.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gobject-introspection-1.78.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) ATK-2.35.1
# ##################################################
function Build_Install_ATK_2_35_1() {

    if [[ ! -d "/opt/atk-2.35.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( atk-2.35.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/atk-2.35.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/atk-2.35.1 && meson build/ --prefix=/opt/atk-2.35.1 \
                                               --buildtype=release \
                                               --pkg-config-path=/opt/lib/pkgconfig && \
                                               STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/atk-2.35.1 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/atk-2.35.1/include/ /usr/local/include/
            # Skip # rsync -av /opt/atk-2.35.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/atk-2.35.1/lib/pkgconfig/atk.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/atk-2.35.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/atk-2.35.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) dbus-1.14.10
# ##################################################
function Compile_Install_dbus_1_14_10() {

    if [[ ! -d "/opt/dbus-1.14.10" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( dbus-1.14.10 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/dbus-1.14.10.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Explain: sed -i ... ltmain.sh: This sed silences several useless and obsolete warnings generated from libtool.
        #                                  这个 sed 使 libtool 生成的几个无用和过时的警告静音。
        # sed -i "/seems to be moved/s/^/#/" config/ltmain.sh
        
        # ------------------------------------------
        # Default Configure Options:
        # ./configure --prefix=/usr \
        #             --sysconfdir=/etc \
        #             --localstatedir=/var \
        #             --runstatedir=/run \
        #             --disable-doxygen-docs \
        #             --disable-xml-docs \
        #             --disable-static \
        #             --with-systemduserunitdir=no \
        #             --with-systemdsystemunitdir=no \
        #             --docdir=/usr/share/doc/dbus-1.14.10 \
        #             --with-system-socket=/run/dbus/system_bus_socket
        # ..........................................
        # *  Option: --disable-doxygen-docs: This switch disables doxygen documentation build and install, if you have doxygen installed. If doxygen is installed, and you wish to build them, remove this parameter.
        #                                    如果安装了 doxygen, 则此开关将禁用 doxygen 文档的构建和安装。如果安装了doxygen, 并且您希望构建它们, 请删除此参数。
        # ..........................................
        # *  Option: --disable-xml-docs: This switch disables html documentation build and install, if you have xmlto installed. If xmlto is installed, and you wish to build them, remove this parameter.
        #                                如果安装了 xmlto, 此开关将禁用 html 文档的构建和安装。如果安装了 xmlto, 并且您希望构建它们, 请删除此参数。
        # ..........................................
        # *  Option: --disable-static: This switch prevents installation of static versions of the libraries.
        #                              此选项可防止安装库的静态版本。
        # ..........................................
        # *  Option: --with-systemd{user,system}unitdir=no: These switches disable installation of systemd units on elogind based systems.
        #                                                   这些开关禁止在基于 elogind 的系统上安装 systemd 单元。
        # ..........................................
        # *  Option: --with-system-socket=/run/dbus/system_bus_socket: This parameter specifies the location of the system bus socket.
        #                                                              此参数指定 system bus socket(套接字) 的位置。
        # ..........................................
        # *  Option: --enable-tests: Builds extra parts of the code to support all tests. Do not use on a production build.
        #                            构建代码的额外部分以支持所有测试。不要在生产版本中使用。
        # ..........................................
        # *  Option: --enable-embedded-tests: Builds extra parts of the code to support only unit tests. Do not use on a production build.
        #                                     构建代码的额外部分以仅支持单元测试。不要在生产版本中使用。
        # ..........................................
        # *  Option: --enable-asserts: Enables debugging code to run assertions for statements normally assumed to be true.
        #                              This prevents a warning that '--enable-tests' on its own is only useful for profiling and might not give true results for all tests, but adds its own NOTE that this should not be used in a production build.
        #                              使调试代码能够为通常假定为 true 的语句运行断言。
        #                              这防止了 "--enable-tests" 本身仅用于分析, 可能不会为所有测试提供真实结果的警告, 但添加了自己的注意事项, 即不应在生产构建中使用此功能。
        cd $STORAGE/dbus-1.14.10 && ./configure --prefix=/opt/dbus-1.14.10 \
                                                --disable-doxygen-docs \
                                                --disable-xml-docs \
                                                --disable-static \
                                                --with-systemduserunitdir=no \
                                                --with-systemdsystemunitdir=no && \
                                                STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # If you are using a DESTDIR install, dbus-daemon-launch-helper needs to be fixed afterwards. Issue, as root user:
        # 如果您使用的是 DESTDIR 安装, 则需要在安装之后修复 dbus 守护进程启动帮助程序。作为 root 用户使用指令:
        #     chown -v root:messagebus /usr/libexec/dbus-daemon-launch-helper &&
        #     chmod -v      4750       /usr/libexec/dbus-daemon-launch-helper
        # ..........................................
        # If you are still building your system in chroot or you did not start the daemon yet, but you want to compile some packages that require D-Bus, generate the D-Bus UUID to avoid warnings when compiling some packages with the following command as the root user:
        # 如果您仍在 chroot 中构建系统, 或者尚未启动守护进程, 但您想编译一些需要 D-Bus 的包, 请生成 D-Bus UUID, 以避免在以 root 用户身份使用以下命令编译某些包时出现警告:
        # dbus-uuidgen --ensure
        # ..........................................
        # If using elogind-252.9, create a symlink to the /var/lib/dbus/machine-id file:
        # 如果使用 elogind-252.9, 请创建一个指向 /var/lib/dbus/machine-id 文件的符号链接:
        #     ln -sfv /var/lib/dbus/machine-id /etc
        # ..........................................
        # Many tests are disabled unless both D-Bus Python-1.3.2 and PyGObject-3.46.0 have been installed.
        # They must be run as an unprivileged user from a local session with bus address. To run the standard tests issue make check.
        # 除非同时安装了D-Bus Python-1.3.2 和 PyGObject-3.46.0, 否则许多测试都会被禁用。
        # 它们必须以无特权用户的身份从具有总线地址的本地会话中运行。要运行标准测试问题, 请进行检查。
        # ..........................................
        # If you want to run the unit regression tests, configure requires additional parameters which expose additional functionality in the binaries that are not intended to be used in a production build of D-Bus.
        # If you would like to run the tests, issue the following commands (for the tests, you don't need to build the docs):
        # 如果您想运行单元回归测试, configure 需要额外的参数, 这些参数会在二进制文件中暴露出不打算在 D-Bus 的生产构建中使用的额外功能。
        # 如果您想运行测试, 请使用以下命令 (对于测试, 您不需要构建文档):
        #     make distclean                                    &&
        #     PYTHON=python3 ./configure --enable-tests         \
        #                                --enable-asserts       \
        #                                --disable-doxygen-docs \
        #                                --disable-xml-docs     &&
        #     make                                              &&
        #     make check
        # One test, test-autolaunch, is known to fail.
        # There have also been reports that the tests may fail if running inside a Midnight Commander shell.
        # You may get out-of-memory error messages when running the tests. These are normal and can be safely ignored.
        # 一个测试, 测试自动启动, 已知失败。
        # 也有报告，如果在午夜指挥官的外壳内运行, 测试可能会失败。
        # 运行测试时, 您可能会收到内存不足的错误消息。这些都是正常的, 可以安全地忽略。
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/dbus-1.14.10/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/dbus-1.14.10/include/ /usr/local/include/
            # Skip # rsync -av /opt/dbus-1.14.10/lib/     /usr/local/lib/
            # Skip # rsync -av /opt/dbus-1.14.10/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/dbus-1.14.10/lib/pkgconfig/dbus-1.pc /opt/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        # Configuring D-Bus
        #
        # Config Files
        #     /etc/dbus-1/session.conf, /etc/dbus-1/system.conf and /etc/dbus-1/system.d/*
        # 
        # Configuration Information
        #     The configuration files listed above should probably not be modified.
        #     If changes are required, you should create /etc/dbus-1/session-local.conf and/or /etc/dbus-1/system-local.conf and make any desired changes to these files.
        # 
        #     If any packages install a D-Bus .service file outside of the standard /usr/share/dbus-1/services directory, that directory should be added to the local session configuration.
        #     For instance, /usr/local/share/dbus-1/services can be added by performing the following commands as the root user:
        # 
        #         cat > /etc/dbus-1/session-local.conf << "EOF"
        #         <!DOCTYPE busconfig PUBLIC
        #          "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"
        #          "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
        #         <busconfig>
        #         
        #           <!-- Search for .service files in /usr/local -->
        #           <servicedir>/usr/local/share/dbus-1/services</servicedir>
        #         
        #         </busconfig>
        #         EOF
        #
        # D-Bus Session Daemon
        #     To automatically start dbus-daemon when the system is rebooted, install the /etc/rc.d/init.d/dbus bootscript from the blfs-bootscripts-20240209 package.
        # 
        #         make install-dbus
        #     If this is the first time to install D-Bus on the system and you are not operating in a chroot environment, you can immediately start dbus-daemon without rebooting the system:
        # 
        #         /etc/init.d/dbus start
        #     Note that this boot script only starts the system-wide D-Bus daemon.
        #     Each user requiring access to D-Bus services will also need to run a session daemon as well.
        #     There are many methods you can use to start a session daemon using the dbus-launch command.
        #     Review the dbus-launch man page for details about the available parameters and options. Here are some suggestions and examples:
        # 
        #         * Add dbus-launch to the line in the ~/.xinitrc file that starts your graphical desktop environment.
        # 
        #         * If you use gdm or some other display manager that calls the ~/.xsession file, you can add dbus-launch to the line in your ~/.xsession file that starts your graphical desktop environment.
        #           The syntax would be similar to the example in the ~/.xinitrc file.
        # 
        #         * The examples shown previously use dbus-launch to specify a program to be run.
        #           This has the benefit (when also using the --exit-with-x11 parameter) of stopping the session daemon when the specified program is stopped.
        #           You can also start the session daemon in your system or personal startup scripts by adding the following lines:
        # 
        #             # Start the D-Bus session daemon
        #             eval `dbus-launch`
        #             export DBUS_SESSION_BUS_ADDRESS
        #           This method will not stop the session daemon when you exit your shell, therefore you should add the following line to your ~/.bash_logout file:
        # 
        #             # Kill the D-Bus session daemon
        #             kill $DBUS_SESSION_BUS_PID

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/dbus-1.14.10 && return 0
    else
    
        echo "[Caution] Path: ( /opt/dbus-1.14.10 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) recordproto-1.14.2
# ##################################################
function Compile_Install_recordproto_1_14_2() {

    if [[ ! -d "/opt/recordproto-1.14.2" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( recordproto-1.14.2 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/recordproto-1.14.2.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/recordproto-1.14.2 && ./configure --prefix=/opt/recordproto-1.14.2 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/recordproto-1.14.2/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/recordproto-1.14.2/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/recordproto-1.14.2/lib/pkgconfig/recordproto.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/recordproto-1.14.2/ /opt/sandbox-X11/
            # ......................................
            # recordproto 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/recordproto-1.14.2 && return 0
    else
    
        echo "[Caution] Path: ( /opt/recordproto-1.14.2 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libXtst-1.2.3
# ##################################################
function Compile_Install_libXtst_1_2_3() {

    if [[ ! -d "/opt/libXtst-1.2.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libXtst-1.2.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/libXtst-1.2.3.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libXtst-1.2.3 && ./configure --prefix=/opt/libXtst-1.2.3 \
                                                 PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                 STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/libXtst-1.2.3/include/ /usr/local/include/
            # ......................................
            # Skip # rsync -av /opt/libXtst-1.2.3/lib/ /usr/local/lib/
            # ......................................
            cp -f /opt/libXtst-1.2.3/lib/pkgconfig/xtst.pc /opt/lib/pkgconfig/
            # ......................................
            # Synchronize to sandbox.
            rsync -av /opt/libXtst-1.2.3/ /opt/sandbox-X11/
            # ......................................
            # libXtst 属于 X11 开发套件, 其默认 CMake 可查找路径为:
            #    /opt/X11/include 或 /usr/include/X11/include
            #    /opt/X11/lib 或 /usr/pkg/xorg/lib
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libXtst-1.2.3 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libXtst-1.2.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) at-spi2-core-2.38.0
# ##################################################
function Build_Install_at_spi2_core_2_38_0() {

    # at-spi2-core-2.38.0 Provide: libatspi.so (contains the At-Spi2 API functions)

    if [[ ! -d "/opt/at-spi2-core-2.38.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( at-spi2-core-2.38.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/at-spi2-core-2.38.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: -Dsystemd_user_dir=/tmp: This flag puts the systemd unit file in /tmp where it will be removed. SysV, is unable to use this file.
        #                                     此选项将 systemd 单元文件放在 /tmp 中, 它将被移除。SysV, 无法使用此文件。
        cd $STORAGE/at-spi2-core-2.38.0 && meson build/ --prefix=/opt/at-spi2-core-2.38.0 \
                                                        --buildtype=release \
                                                        --pkg-config-path=/opt/lib/pkgconfig && \
                                                        STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/at-spi2-core-2.38.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # Now, as the root user:
        # 现在, 以 root 用户使用指令:
        # rm /tmp/at-spi-dbus-bus.service
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/at-spi2-core-2.38.0/include/ /usr/local/include/
            # Skip # rsync -av /opt/at-spi2-core-2.38.0/lib/     /usr/local/lib/
            # Skip # rsync -av /opt/at-spi2-core-2.38.0/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/at-spi2-core-2.38.0/lib/pkgconfig/atspi-2.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/at-spi2-core-2.38.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/at-spi2-core-2.38.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) at-spi2-atk-2.20.1
# ##################################################
function Compile_Install_at_spi2_atk_2_20_1() {

    # at-spi2-atk-2.20.1 Provide: libatk-bridge.so
    # at-spi2-atk-2.20.1 Provide: libatk-bridge-2.0.so

    if [[ ! -d "/opt/at-spi2-atk-2.20.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( at-spi2-atk-2.20.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/at-spi2-atk-2.20.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Explain: sed -i ... ltmain.sh: This sed silences several useless and obsolete warnings generated from libtool.
        #                                  这个 sed 使 libtool 生成的几个无用和过时的警告静音。
        # sed -i "/seems to be moved/s/^/#/" config/ltmain.sh
        
        # ------------------------------------------
        cd $STORAGE/at-spi2-atk-2.20.1 && ./configure --prefix=/opt/at-spi2-atk-2.20.1 \
                                                      PKG_CONFIG_PATH="/opt/lib/pkgconfig" && \
                                                      STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        # If you installed the package to your system using a “DESTDIR” method, /usr/share/glib-2.0/schemas/gschemas.compiled was not updated/created.
        # Create (or update) the file using the following command as the root user:
        # 如果使用 "DESTDIR" 方法将软件包安装到系统中, 则 /usr/share/glib-2.0/schemas/gschemas.compied 不会 更新/创建。
        # 使用以下命令作为根用户创建 (或更新) 文件:
        # glib-compile-schemas /usr/share/glib-2.0/schemas
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # rsync -av /opt/at-spi2-atk-2.20.1/include/ /usr/local/include/
            # Skip # rsync -av /opt/at-spi2-atk-2.20.1/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/at-spi2-atk-2.20.1/lib/pkgconfig/atk-bridge-2.0.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/at-spi2-atk-2.20.1 && return 0
    else
    
        echo "[Caution] Path: ( /opt/at-spi2-atk-2.20.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 构建安装(Build Install) libxkbcommon-1.6.0
# ##################################################
function Build_Install_libxkbcommon_1_6_0() {

    # xkbcommon is a library for handling of keyboard descriptions, including loading them from disk, parsing them and handling their state.
    # xkbcommon 是一个用于处理键盘描述的库, 包括从磁盘加载、解析和处理它们的状态。
    # It's mainly meant for client toolkits, window systems, and other system applications.
    # 它主要用于客户端工具包、窗口系统和其他系统应用程序。

    if [[ ! -d "/opt/libxkbcommon-1.6.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( libxkbcommon-1.6.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/libxkbcommon-1.6.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libxkbcommon-1.6.0 && meson build/ --prefix=/opt/libxkbcommon-1.6.0 \
                                                       --pkg-config-path=/opt/lib/pkgconfig && \
                                                       STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/libxkbcommon-1.6.0 && ninja -C build/ install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # Skip # if [[ ! -d "/usr/local/libexec" ]]; then mkdir /usr/local/libexec; fi
            # ......................................
            # Skip # ln -sf /opt/libxkbcommon-1.6.0/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/include/ /usr/local/include/
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/lib/     /usr/local/lib/
            # Skip # rsync -av /opt/libxkbcommon-1.6.0/libexec/ /usr/local/libexec/
            # ......................................
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbcommon.pc     /opt/lib/pkgconfig/
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbcommon-x11.pc /opt/lib/pkgconfig/
            cp -f /opt/libxkbcommon-1.6.0/lib/pkgconfig/xkbregistry.pc   /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libxkbcommon-1.6.0 && return 0
    else
    
        echo "[Caution] Path: ( /opt/libxkbcommon-1.6.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ######################################## gir-file-for-gtk+ #########################################

# Function: 编译安装(Deploy Install) gir-File-for-GTK+-20190203
# ##################################################
function Deploy_Install_gir_File_for_GTK_Plus_20190203() {
    
    local VERIFY
    local STEP_UNZIPPED=0
    local STEP_DEPLOYED=0
    
    # ----------------------------------------------
    read -p "[Confirm] Deploy and Install ( gir-file-for-gtk+-20190203 )? (y/n)>" VERIFY
    if [[ "$VERIFY" != "y" ]]; then exit 1; fi

    # ----------------------------------------------
    tar -zxvf $STORAGE/gir-file-for-gtk+-20190203.tar.gz && STEP_UNZIPPED=1
    
    # ----------------------------------------------
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/Atk-1.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/Atk-1.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/Gdk-3.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/Gdk-3.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/GdkPixbuf-2.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/GdkPixbuf-2.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/GdkPixdata-2.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/GdkPixdata-2.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/GdkX11-3.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/GdkX11-3.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/Pango-1.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/Pango-1.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/PangoCairo-1.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/PangoCairo-1.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/PangoFT2-1.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/PangoFT2-1.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    if [[ ! -f "/opt/gobject-introspection-1.78.1/share/gir-1.0/PangoXft-1.0.gir" ]]; then
        cp -v $STORAGE/gir-file-for-gtk+-20190203/PangoXft-1.0.gir /opt/gobject-introspection-1.78.1/share/gir-1.0/
    fi
    # ..............................................
    STEP_DEPLOYED=1

    # ----------------------------------------------
    cd $STORAGE && rm -rf $STORAGE/gir-file-for-gtk+-20190203 && return 0
}

# ############################################### GTK+ ###############################################

# Function: 构建安装(Build Install) GTK+-3.24.41
# ##################################################
function Build_Install_GTK_Plus_3_24_41() {

    if [[ ! -d "/opt/gtk+-3.24.41" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_BUILDED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Build and Install ( gtk+-3.24.41 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -xvJf $STORAGE/gtk+-3.24.41.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # *  Option: -Dman=true: This switch allows generating manual pages.
        #                        此选项允许生成手册页面。
        # ..........................................
        # *  Option: -Dbroadway_backend=true: This switch enables the HTML5 GTK backend.
        #                                     此选项启用 HTML5 GTK 后端。
        # ..........................................
        # * Problem: Run-time dependency cairo-xlib found: NO (tried pkgconfig and cmake)
        #            meson.build:506:97: ERROR: Dependency "cairo-xlib" not found, tried pkgconfig and cmake
        #   - Solve: Open Option "-Dxlib=enabled" when Building and Installing "Cairo"。
        # ..........................................
        # * Problem: [155/1665] Generating gdk/Gdk-3.0.gir with a custom command (wrapped by meson to set env)
        #            FAILED: gdk/Gdk-3.0.gir
        #            env PKG_CONFIG_PATH=/opt/lib/pkgconfig:/home/goufeng/gtk+-3.24.41/build/meson-uninstalled ...... --sources-top-dirs /home/goufeng/gtk+-3.24.41/build/
        #            Couldn't find include 'GdkPixbuf-2.0.gir' (search path: '['/opt/gobject-introspection-1.78.1/share/gir-1.0', ...... , '/usr/share/gir-1.0']')
        #            [157/1665] Generating gtk/gtkresources_c with a custom command
        #            ninja: build stopped: subcommand failed.
        #   - Solve: 具体原因就是在安装 gobject-introspection 的时候, 没有生成 .gir 文件。
        #            ...............................
        #            方法一 (Meson 构建添加选项): enable-introspection=no 或者 introspection=false (依版本而定)。
        #            ...............................
        #            方法二 (下载 .gir 文件): Gdk-3.0.gir, GdkPixbuf-2.0.gir, GdkPixdata-2.0.gir, GdkX11-3.0.gir, 然后复制到 /opt/gobject-introspection-1.78.1/share/gir-1.0/ 目录下。
        #                                     类似的情况还缺少 Atk-1.0.gir, Pango-1.0.gir, PangoCairo-1.0.gir, PangoFT2-1.0.gir, PangoXft-1.0.gir, 可以一并下载。
        cd $STORAGE/gtk+-3.24.41 && meson build/ --prefix=/opt/gtk+-3.24.41 \
                                                 --buildtype=release \
                                                 -Dman=true \
                                                 -Dbroadway_backend=true \
                                                 --pkg-config-path=/opt/lib/pkgconfig && \
                                                 STEP_BUILDED=1
        
        # ------------------------------------------
        cd $STORAGE/gtk+-3.24.41 && ninja -C build/ install && STEP_INSTALLED=1
        
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/opt/lib" ]]; then mkdir /opt/lib; fi
            if [[ ! -d "/opt/lib/pkgconfig" ]]; then mkdir /opt/lib/pkgconfig; fi
            # ......................................
            # Skip # ln -sf /opt/gtk+-3.24.41/bin/* /usr/local/bin/
            # ......................................
            # Skip # rsync -av /opt/gtk+-3.24.41/include/ /usr/local/include/
            # Skip # rsync -av /opt/gtk+-3.24.41/lib/     /usr/local/lib/
            # ......................................
            cp -f /opt/gtk+-3.24.41/lib/pkgconfig/*.pc /opt/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gtk+-3.24.41 && return 0
    else
    
        echo "[Caution] Path: ( /opt/gtk+-3.24.41 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    # ----------- Compilation Environment ----------
    # 编译 GTK+ 时时需要引入 Cairo 的 cairo-xlib.h 头文件
    export C_INCLUDE_PATH=/opt/cairo-1.18.0/include
    export CPLUS_INCLUDE_PATH=/opt/cairo-1.18.0/include
    # ..............................................
    export LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib
    export LD_LIBRARY_PATH=/opt/sandbox-glib/lib:/opt/libjpeg-turbo-3.0.0/lib
    # ..............................................
    export PATH=$PATH:/opt/sandbox-glib/bin:/opt/gdk-pixbuf-2.42.10/bin
    # ..............................................
    export PKG_CONFIG_PATH=/opt/lib/pkgconfig

    # ----------------- Dependency -----------------
    Build_Install_Shared_Mime_Info_2_2
    Build_Install_libjpeg_turbo_3_0_0
    Build_Install_docutils_0_20_1_by_Python3
    Build_Install_GDK-Pixbuf_2_42_10
    Build_Install_libepoxy_1_5_10
    Build_Install_GObject_Introspection_1_78_1
    Build_Install_ATK_2_35_1
    Compile_Install_dbus_1_14_10
    Compile_Install_recordproto_1_14_2
    Compile_Install_libXtst_1_2_3
    Build_Install_at_spi2_core_2_38_0
    Compile_Install_at_spi2_atk_2_20_1
    Build_Install_libxkbcommon_1_6_0
    # ------------- gir-file-for-gtk+ --------------
    Deploy_Install_gir_File_for_GTK_Plus_20190203
    # -------------------- GTK+ --------------------
    Build_Install_GTK_Plus_3_24_41
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装GTK+-3.24.41 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
