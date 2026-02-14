# 文章_Linux运维_Bash脚本_部署安装DocBook-XML-4.5(XML-DTD)_GF_2024-03-01

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

docbook-xml-4.5.zip
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-03-01 12:55

# Need File: docbook-xml-4.5.zip

# ##################################################
STORAGE=/home/goufeng

# Function: 部署安装(Deploy Install) XML-DTD: DocBook-XML-4.5
# ##################################################
function Deploy_Install_XML_DTD_DocBook_XML_4_5() {

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
        #
        # 以根用户身份运行以下命令, 安装 DocBook XSL 样式表: 
        # Install DocBook XML DTD by running the following commands as the root user:
        install -v -d -m755 /usr/share/xml/docbook/xml-dtd-4.5 &&
        install -v -d -m755 /etc/xml &&
        cp -v -af --no-preserve=ownership docbook.cat *.dtd ent/ *.mod \
            /usr/share/xml/docbook/xml-dtd-4.5
        
        # ------------------------------------------
        # 配置 DocBook XML DTD
        # Configuring DocBook XML DTD
        #
        # Config Files: /etc/xml/catalog
        #               /etc/xml/docbook
        #
        # /etc/xml/docbook 文件示例:
        # /etc/XML/docbook Example of File:
        #
        # <?xml version="1.0"?>
        # <!DOCTYPE catalog PUBLIC "-//OASIS//DTD Entity Resolution XML Catalog V1.0//EN" "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd">
        # <catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
        #   <public publicId="-//OASIS//DTD DocBook XML V4.5//EN" uri="http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd"/>
        #   <public publicId="-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/calstblx.dtd"/>
        #   <public publicId="-//OASIS//DTD XML Exchange Table Model 19990315//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/soextblx.dtd"/>
        #   <public publicId="-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/dbpoolx.mod"/>
        #   <public publicId="-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/dbhierx.mod"/>
        #   <public publicId="-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/htmltblx.mod"/>
        #   <public publicId="-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/dbnotnx.mod"/>
        #   <public publicId="-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/dbcentx.mod"/>
        #   <public publicId="-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" uri="file:///usr/share/xml/docbook/xml-dtd-4.5/dbgenent.mod"/>
        #   <rewriteSystem systemIdStartString="http://www.oasis-open.org/docbook/xml/4.5" rewritePrefix="file:///usr/share/xml/docbook/xml-dtd-4.5"/>
        #   <rewriteURI uriStartString="http://www.oasis-open.org/docbook/xml/4.5" rewritePrefix="file:///usr/share/xml/docbook/xml-dtd-4.5"/>
        # </catalog>
        #
        # /etc/xml/catalog 文件示例:
        # /etc/XML/catalog Example of File:
        #
        # <?xml version="1.0"?>
        # <!DOCTYPE catalog PUBLIC "-//OASIS//DTD Entity Resolution XML Catalog V1.0//EN" "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd">
        # <catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
        #   <rewriteSystem systemIdStartString="http://docbook.sourceforge.net/release/xsl/1.79.1" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteURI uriStartString="http://docbook.sourceforge.net/release/xsl/1.79.1" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteSystem systemIdStartString="http://docbook.sourceforge.net/release/xsl/current" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <rewriteURI uriStartString="http://docbook.sourceforge.net/release/xsl/current" rewritePrefix="/usr/share/xml/docbook/xsl-stylesheets-1.79.1"/>
        #   <delegatePublic publicIdStartString="-//OASIS//ENTITIES DocBook XML" catalog="file:///etc/xml/docbook"/>
        #   <delegatePublic publicIdStartString="-//OASIS//DTD DocBook XML" catalog="file:///etc/xml/docbook"/>
        #   <delegateSystem systemIdStartString="http://www.oasis-open.org/docbook/" catalog="file:///etc/xml/docbook"/>
        #   <delegateURI uriStartString="http://www.oasis-open.org/docbook/" catalog="file:///etc/xml/docbook"/>
        # </catalog>
        #
        # ..........................................
        # 以 root 用户身份运行以下命令, 创建 (或更新) 并填充 /etc/xml/docbook 目录文件:
        # Create (or update) and populate the /etc/xml/docbook catalog file by running the following commands as the root user:
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
        # 以 root 用户身份运行以下命令, 创建 (或更新) 并填充 /etc/xml/catalog 目录文件:
        # Create (or update) and populate the /etc/xml/catalog catalog file by running the following commands as the root user:
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
        # 注意:
        # Caution:
        #
        # 各种 BLFS 包在 V4.5 之前都要求 DocBook XML DTD 4.x 版本, 因此必须完成以下步骤才能成功构建这些包。
        # Various BLFS packages request DocBook XML DTD version 4.x before V4.5, so the following step must be done for those packages to be built successfully.
        #
        # 上述安装将创建文件并更新目录。为了在系统标识符中请求任何 4.x 版本时使用 DocBook XML DTD V4.5, 您需要向目录文件中添加其他语句。
        # 如果您的系统上已经安装了下面引用的任何 DocBook XML DTD, 请从下面的 for 命令中删除这些条目 (以 root 用户身份执行命令):
        # The above installation creates the files and updates the catalogs. In order to utilize DocBook XML DTD V4.5 when any version 4.x is requested in the System Identifier, you need to add additional statements to the catalog files. 
        # If you have any of the DocBook XML DTD's referenced below already installed on your system, remove those entries from the for command below (issue the commands as the root user):
        #
        # for DTDVERSION in 4.1.2 4.2 4.3 4.4
        # do
        #   xmlcatalog --noout --add "public" \
        #     "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
        #     "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
        #     /etc/xml/docbook
        #   xmlcatalog --noout --add "rewriteSystem" \
        #     "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
        #     "file:///usr/share/xml/docbook/xml-dtd-4.5" \
        #     /etc/xml/docbook
        #   xmlcatalog --noout --add "rewriteURI" \
        #     "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
        #     "file:///usr/share/xml/docbook/xml-dtd-4.5" \
        #     /etc/xml/docbook
        #   xmlcatalog --noout --add "delegateSystem" \
        #     "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
        #     "file:///etc/xml/docbook" \
        #     /etc/xml/catalog
        #   xmlcatalog --noout --add "delegateURI" \
        #     "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
        #     "file:///etc/xml/docbook" \
        #     /etc/xml/catalog
        # done

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/docbook-xml-4.5 && return 0
    else
    
        echo "[Caution] Path: ( /usr/share/xml/docbook/xml-dtd-4.5 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    Deploy_Install_XML_DTD_DocBook_XML_4_5
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 部署安装DocBook-XML-4.5(XML-DTD) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
