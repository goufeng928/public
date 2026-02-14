# 文章_Linux运维_Bash脚本_编译安装FreeType-2.12.0_GF_2024-02-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

freetype-2.12.0.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-20 21:42

# Need File: freetype-2.12.0.tar.gz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) freetype-2.12.0
# ##################################################
function compile_install_freetype_2_12_0() {

    if [[ ! -d "/usr/local/freetype-2.12.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( freetype-2.12.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/freetype-2.12.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/freetype-2.12.0 && ./configure --prefix=/usr/local/freetype-2.12.0 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/include/freetype2" ]]; then mkdir /usr/local/include/freetype2; fi
            if [[ ! -d "/usr/local/include/freetype2/freetype" ]]; then mkdir /usr/local/include/freetype2/freetype; fi
            if [[ ! -d "/usr/local/include/freetype2/freetype/config" ]]; then mkdir /usr/local/include/freetype2/freetype/config; fi
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/ft2build.h /usr/local/include/freetype2/
            # ......................................
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/freetype.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftadvanc.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftbbox.h     /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftbdf.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftbitmap.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftbzip2.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftcache.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftchapters.h /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftcid.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftcolor.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftdriver.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/fterrdef.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/fterrors.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftfntfmt.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftgasp.h     /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftglyph.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftgxval.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftgzip.h     /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftimage.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftincrem.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftlcdfil.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftlist.h     /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftlogging.h  /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftlzw.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftmac.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftmm.h       /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftmodapi.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftmoderr.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftotval.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftoutln.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftparams.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftpfr.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftrender.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftsizes.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftsnames.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftstroke.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftsynth.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftsystem.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/fttrigon.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/fttypes.h    /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ftwinfnt.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/otsvg.h      /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/t1tables.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/ttnameid.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/tttables.h   /usr/local/include/freetype2/freetype/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/tttags.h     /usr/local/include/freetype2/freetype/
            # ......................................
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/ftconfig.h      /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/ftheader.h      /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/ftmodule.h      /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/ftoption.h      /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/ftstdlib.h      /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/integer-types.h /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/mac-support.h   /usr/local/include/freetype2/freetype/config/
            ln -sf /usr/local/freetype-2.12.0/include/freetype2/freetype/config/public-macros.h /usr/local/include/freetype2/freetype/config/
            # ......................................
            ln -sf /usr/local/freetype-2.12.0/lib/libfreetype.a         /usr/local/lib/
            ln -sf /usr/local/freetype-2.12.0/lib/libfreetype.la        /usr/local/lib/
            ln -sf /usr/local/freetype-2.12.0/lib/libfreetype.so.6.18.2 /usr/local/lib/libfreetype.so
            ln -sf /usr/local/freetype-2.12.0/lib/libfreetype.so.6.18.2 /usr/local/lib/libfreetype.so.6
            ln -sf /usr/local/freetype-2.12.0/lib/libfreetype.so.6.18.2 /usr/local/lib/
            # ......................................
            ln -sf /usr/local/freetype-2.12.0/lib/pkgconfig/freetype2.pc /usr/local/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/freetype-2.12.0 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/freetype-2.12.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    compile_install_freetype_2_12_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装FreeType-2.12.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
