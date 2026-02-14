# 文章_Linux运维_Bash脚本_部署安装DocBook-XSL-1.79.1(XSL-Stylesheets)_GF_2024-03-01

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

docbook-xsl-1.79.1.tar.bz2

docbook-xsl-doc-1.79.1.tar.bz2
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-01 12:19

# Need File: docbook-xsl-1.79.1.tar.bz2
# Need File: docbook-xsl-doc-1.79.1.tar.bz2

# ##################################################
STORAGE=/home/goufeng

# Function: 部署安装(Deploy Install) XSL-Stylesheets: DocBook-XSL-1.79.1
# ##################################################
function Deploy_Install_XSL_Stylesheets_DocBook_XSL_1_79_1() {

    # Linux 的 install 命令用于安装或升级软件、备份数据。
    #
    # 其常用的格式有: 
    # 
    #     1. install [OPTION]... SOURCE DEST: 将源文件复制到目标目录。
    #     
    #     2. install [OPTION]... SOURCE... DIRECTORY: 将多个源文件复制到已存在的目录。
    #     
    #     3. install -d [OPTION]... DIRECTORY...: 在指定目录下创建新目录。
    # 
    # 常用的参数包括: 
    # 
    #     1. -c: 如果目标文件已经存在, 不覆盖, 保留原有的文件。
    #     
    #     2. -D: 如果目标文件是一个目录, 则在该目录下创建源文件的一个快捷方式。
    #     
    #     3. -b: 如果目标文件已经存在, 则将目标文件备份, 并将源文件复制到目标文件路径。
    #     
    #     4. -m: 设置目标文件的权限。
    #     
    #     5. -o: 设置目标文件的拥有者。
    #     
    #     6. -p: 以源文件 访问/修改 的时间作为目标文件的时间属性, 即不改变文件的时间属性。
    #     
    #     7. -s: 对待拷贝的可执行文件进行 strip 操作, 取出文件中的符号表。

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
        #
        # 以根用户身份运行以下命令, 安装 DocBook XSL 样式表: 
        # Install DocBook XSL Stylesheets by running the following commands as the root user:
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
        #
        # Config Files: /etc/xml/catalog
        #
        # /etc/xml/catlog 文件示例:
        # /etc/XML/catlog Example of File:
        #
        # <?xml version="1.0"?>
        # <!DOCTYPE catalog PUBLIC "-//OASIS//DTD Entity Resolution XML Catalog V1.0//EN" "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd">
        # <catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
        #   <rewriteSystem systemIdStartString="http://docbook.sourceforge.net/release/xsl/1.79.1" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteURI uriStartString="http://docbook.sourceforge.net/release/xsl/1.79.1" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteSystem systemIdStartString="http://docbook.sourceforge.net/release/xsl/current" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteURI uriStartString="http://docbook.sourceforge.net/release/xsl/current" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        # </catalog>
        #
        # 作为 root 用户, 使用以下命令创建 (或附加) 并填充 XML catalog 文件:
        # Create (or append) and populate the XML catalog file using the following commands as the root user:
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
        # 有时, 您可能会发现需要安装其他版本的 XSL 样式表, 因为某些项目引用了特定的版本。
        # 一个例子是 BLFS-6.0, 它需要 1.67.2 版本。
        # 在这些情况下, 您应该在其自己的版本目录中安装任何其他所需版本, 并按如下方式创建目录条目 (用所需的版本号代替 <version>): 
        # Occasionally, you may find the need to install other versions of the XSL stylesheets as some projects reference a specific version. 
        # One example is BLFS-6.0, which required the 1.67.2 version. 
        # In these instances you should install any other required version in its own versioned directory and create catalog entries as follows (substitute the desired version number for <version>):
        #
        # xmlcatalog --noout --add "rewriteSystem" \
        #            "http://docbook.sourceforge.net/release/xsl/<version>" \
        #            "/usr/share/xml/docbook/xsl-stylesheets-<version>" \
        #     /etc/xml/catalog &&
        # 
        # xmlcatalog --noout --add "rewriteURI" \
        #            "http://docbook.sourceforge.net/release/xsl/<version>" \
        #            "/usr/share/xml/docbook/xsl-stylesheets-<version>" \
        #     /etc/xml/catalog

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/docbook-xsl-1.79.1 && \
        cd $STORAGE && rm -rf $STORAGE/docbook-xsl-doc-1.79.1 && return 0
    else
    
        echo "[Caution] Path: ( /usr/share/xml/docbook/xsl-stylesheets-1.79.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    Deploy_Install_XSL_Stylesheets_DocBook_XSL_1_79_1
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 部署安装DocBook-XSL-1.79.1(XSL-Stylesheets) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
