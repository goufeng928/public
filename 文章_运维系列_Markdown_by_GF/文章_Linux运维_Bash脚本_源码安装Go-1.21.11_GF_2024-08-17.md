# 文章_Linux运维_Bash脚本_源码安装Go-1.21.11_GF_2024-08-17

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

go1.4-bootstrap-20171003.tar.gz

go1.16.src.tar.gz

go1.17.3.src.tar.gz

go1.21.11.src.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-08-03 01:34

# --------------------------------------------------
# Install First: 
# * GCC

# ----------------- Dep for Go 1.16 ----------------
# Need File: go1.4-bootstrap-20171003.tar.gz
# -------------------- Go - 1.16 -------------------
# Need File: go1.16.src.tar.gz
# ------------------- Go - 1.17.3 ------------------
# Need File: go1.17.3.src.tar.gz
# ------------------- Go - 1.21.11 -----------------
# Need File: go1.21.11.src.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ########################################## Dep for Go 1.16 #########################################

# Function: 制作安装(Make Install) Go-1.4-Bootstrap-20171003
# ##################################################
function Make_Install_Go_1_4_Bootstrap_20171003() {

    # Compile Error Handle:
    # ----------------------------------------------
    # /home/liu/go1.4/src/lib9/fmt/fltfmt.c: In function '__efgfmt':
    # /home/liu/go1.4/src/lib9/fmt/fltfmt.c:437:5: error: this statement may fall through [-Werror=implicit-fallthrough=]
    #    if(ndigits > prec) {
    #      ^
    # /home/liu/go1.4/src/lib9/fmt/fltfmt.c:451:2: note: here
    #   default:
    #   ^~~~~~~
    # cc1: all warnings being treated as errors
    # ..............................................
    # 1. 确认 switch 语句: 找到包含 default: 的 switch 语句。
    # 2. 检查 case 分支: 查看在 default: 之前的所有 case 分支, 确保每个分支在结束时都有适当的 break (或 return、continue 等, 取决于上下文)。
    # 3. 理解逻辑: 确保 switch 语句的逻辑是你所期望的。如果某个 case 分支确实应该允许控制流落入下一个 case 或 default, 那么确保这是有意的, 并且代码的可读性和可维护性不会因此受损。
    # 4. 修改代码: 如果发现有不必要的 fall through, 添加缺失的 break 语句。如果 fall through 是有意的, 但编译器警告你, 你可以考虑使用编译器特定的注释来指示这是预期的行为 (例如, 对于 GCC 和 Clang, 你可以在两个 case 之间添加 // fall through 注释)。
    # ----------------------------------------------
    # /home/goufeng/go/src/cmd/6c/txt.c: In function 'gmove':
    # /home/goufeng/go/src/cmd/6c/txt.c:995:28: error: left shift of negative value [-Werror=shift-negative-value]
    #      f->vconst |= (vlong)~0 << 32;
    #                             ^~
    # /home/goufeng/go/src/cmd/6c/txt.c:1045:28: error: left shift of negative value [-Werror=shift-negative-value]
    #      f->vconst |= (vlong)~0 << 32;
    #                             ^~
    # cc1: all warnings being treated as errors
    # ..............................................
    # 这个错误是由于在 C 语言中, 对负数进行左移操作是不被允许的, 尤其是在严格的编译环境下 (如你的编译器将所有警告视为错误)。
    # 在代码中, (vlong)~0 << 32 试图将一个全为 1 的负数 (通过 ~0 得到) 左移 32 位。这通常用于设置一个特定大小的数据类型的所有位为 1, 但在 C 语言中, 直接对负数进行位移操作可能会导致未定义行为。
    # 可以通过确保参与位移操作的值是正数或无符号数来避免这个错误。可以显式地将 ~0 转换为无符号类型来解决这个问题, 例如:
    # 将 "f->vconst |= (vlong)~0 << 32;" 改为 "f->vconst |= (vlong)((unsigned long long)~0ULL << 32);"。

    if [[ ! -d "/opt/go-1.4-bootstrap-20171003" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_MOVED=0
        local STEP_CHANGE_DIRECTORY=0
        local STEP_MADE=0
    
        # ------------------------------------------
        read -p "[Confirm] Make and Install ( go-1.4-bootstrap-20171003 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/go1.4-bootstrap-20171003.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # The compilation directory of "Go" needs to be stored properly. After compilation, "GOROOT" defaults to the compilation directory.
        # Go 的编译目录需要妥善存放, 编译完成后, GOROOT 默认在编译目录下。
        cp -r $STORAGE/go /opt/go-1.4-bootstrap-20171003 && STEP_MOVED=1
        
        # ------------------------------------------
        cd /opt/go-1.4-bootstrap-20171003/src && STEP_CHANGE_DIRECTORY=1
        
        # ------------------------------------------
        sed -i "1045s%(vlong)~0 << 32%(vlong)((unsigned long long)~0ULL << 32)%" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/txt.c
        sed -i  "995s%(vlong)~0 << 32%(vlong)((unsigned long long)~0ULL << 32)%" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/txt.c
        
        # ------------------------------------------
        sed -i "451i // fall through" /opt/go-1.4-bootstrap-20171003/src/lib9/fmt/fltfmt.c
        # ..........................................
        sed -i "204i // fall through" /opt/go-1.4-bootstrap-20171003/src/lib9/fmt/strtod.c
        sed -i "198i // fall through" /opt/go-1.4-bootstrap-20171003/src/lib9/fmt/strtod.c
        sed -i "187i // fall through" /opt/go-1.4-bootstrap-20171003/src/lib9/fmt/strtod.c
        sed -i "145i // fall through" /opt/go-1.4-bootstrap-20171003/src/lib9/fmt/strtod.c
        # ..........................................
        sed -i "53i // fall through" /opt/go-1.4-bootstrap-20171003/src/libbio/bflush.c
        # ..........................................
        sed -i "53i // fall through" /opt/go-1.4-bootstrap-20171003/src/libbio/bseek.c
        # ..........................................
        sed -i "2618i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm5.c
        sed -i "1353i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm5.c
        # ..........................................
        sed -i "3380i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "2702i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "2200i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "2158i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "2013i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "1985i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        sed -i "1910i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm6.c
        # ..........................................
        sed -i "2696i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm8.c
        sed -i "2138i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm8.c
        sed -i "1467i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/asm8.c
        # ..........................................
        sed -i "385i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/obj5.c
        # ..........................................
        sed -i "171i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/sym.c
        sed -i "151i // fall through" /opt/go-1.4-bootstrap-20171003/src/liblink/sym.c
        # ..........................................
        sed -i "177i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/acid.c
        # ..........................................
        sed -i "303i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/com64.c
        sed -i "301i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/com64.c
        sed -i "265i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/com64.c
        # ..........................................
        sed -i "297i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/dcl.c
        # ..........................................
        sed -i "122i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/dpchk.c
        # ..........................................
        sed -i "339i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/lex.c
        sed -i "309i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/lex.c
        # ..........................................
        sed -i "1131i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        sed -i  "956i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        sed -i  "902i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        sed -i  "882i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        sed -i  "865i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        sed -i  "530i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/cc/sub.c
        # ..........................................
        sed -i "1428i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/const.c
        sed -i "1051i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/const.c
        sed -i  "472i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/const.c
        sed -i  "240i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/const.c
        sed -i  "226i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/const.c
        # ..........................................
        sed -i "900i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/esc.c
        # ..........................................
        sed -i "628i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/fmt.c
        # ..........................................
        sed -i "552i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/gen.c
        # ..........................................
        sed -i "1689i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/lex.c
        sed -i "1683i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/lex.c
        # ..........................................
        sed -i "470i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/mparith1.c
        sed -i "385i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/mparith1.c
        sed -i "354i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/mparith1.c
        # ..........................................
        sed -i "733i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/order.c
        sed -i "513i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/order.c
        sed -i "455i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/order.c
        sed -i "143i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/order.c
        # ..........................................
        sed -i "158i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/racewalk.c
        # ..........................................
        sed -i "146i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/range.c
        # ..........................................
        sed -i "291i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/select.c
        sed -i "225i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/select.c
        sed -i "130i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/select.c
        # ..........................................
        sed -i "1453i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/sinit.c
        sed -i "1376i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/sinit.c
        sed -i "1042i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/sinit.c
        # ..........................................
        sed -i "2986i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/subr.c
        sed -i "2746i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/subr.c
        sed -i "1293i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/subr.c
        # ..........................................
        sed -i "341i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/typecheck.c
        # ..........................................
        sed -i "1130i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/walk.c
        sed -i  "221i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/walk.c
        # ..........................................
        sed -i "1142i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/elf.c
        # ..........................................
        sed -i "316i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/data.c
        # ..........................................
        sed -i "876i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/ldelf.c
        # ..........................................
        sed -i "299i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/ldpe.c
        # ..........................................
        sed -i "418i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/macho.c
        sed -i "359i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/macho.c
        # ..........................................
        sed -i "618i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/pe.c
        # ..........................................
        sed -i "248i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/ld/symtab.c
        # ..........................................
        sed -i "87i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6l/obj.c
        # ..........................................
        sed -i "753i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/peep.c
        sed -i "577i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/peep.c
        sed -i "113i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/peep.c
        # ..........................................
        sed -i "343i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/reg.c
        # ..........................................
        sed -i "773i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6c/txt.c
        # ..........................................
        sed -i "201i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/cplx.c
        sed -i  "57i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/gc/cplx.c
        # ..........................................
        sed -i "1130i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/cgen.c
        # ..........................................
        sed -i "1283i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/gsubr.c
        sed -i "1216i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/gsubr.c
        sed -i  "689i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/gsubr.c
        sed -i  "387i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/gsubr.c
        sed -i  "375i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/gsubr.c
        # ..........................................
        sed -i "526i // fall through" /opt/go-1.4-bootstrap-20171003/src/cmd/6g/reg.c
        
        
        # ------------------------------------------
        if [[ $STEP_CHANGE_DIRECTORY == 1 ]]; then
            # make.bash / all.bash must be run from $GOROOT/src
            ./make.bash && STEP_MADE=1
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/go && return 0
    else
    
        echo "[Caution] Path: ( /opt/go-1.4-bootstrap-20171003 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################# Go - 1.16 ############################################

# Function: 制作安装(Make Install) Go-1.16
# ##################################################
function Make_Install_Go_1_16() {

    # 源码安装 Go 1.5 版本以上时会报 ERROR: Cannot find /root/go1.4/bin/go 这个错误。
    # 因为 Go 1.5 开始编译器和运行时用 Go 自身编写, 要编译它们, 首先要安装 Go 编译器。所以如果想要通过源码方式安装高版本 Go, 必须先安装好 Go 1.4 版本。
    
    if [[ ! -d "/opt/go-1.16" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_MOVED=0
        local STEP_CHANGE_DIRECTORY=0
        local STEP_MADE=0
    
        # ------------------------------------------
        read -p "[Confirm] Make and Install ( go-1.16 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/go1.16.src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # The compilation directory of "Go" needs to be stored properly. After compilation, "GOROOT" defaults to the compilation directory.
        # Go 的编译目录需要妥善存放, 编译完成后, GOROOT 默认在编译目录下。
        cp -r $STORAGE/go /opt/go-1.16 && STEP_MOVED=1
        
        # ------------------------------------------
        cd /opt/go-1.16/src && STEP_CHANGE_DIRECTORY=1
        
        # ------------------------------------------
        if [[ $STEP_CHANGE_DIRECTORY == 1 ]]; then
            # make.bash / all.bash must be run from $GOROOT/src
            ./make.bash && STEP_MADE=1
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/go && return 0
    else
    
        echo "[Caution] Path: ( /opt/go-1.16 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################ Go - 1.17.3 ###########################################

# Function: 制作安装(Make Install) Go-1.17.3
# ##################################################
function Make_Install_Go_1_17_3() {
    
    if [[ ! -d "/opt/go-1.17.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_MOVED=0
        local STEP_CHANGE_DIRECTORY=0
        local STEP_MADE=0
    
        # ------------------------------------------
        read -p "[Confirm] Make and Install ( go-1.17.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/go1.17.3.src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # The compilation directory of "Go" needs to be stored properly. After compilation, "GOROOT" defaults to the compilation directory.
        # Go 的编译目录需要妥善存放, 编译完成后, GOROOT 默认在编译目录下。
        cp -r $STORAGE/go /opt/go-1.17.3 && STEP_MOVED=1
        
        # ------------------------------------------
        cd /opt/go-1.17.3/src && STEP_CHANGE_DIRECTORY=1
        
        # ------------------------------------------
        if [[ $STEP_CHANGE_DIRECTORY == 1 ]]; then
            # make.bash / all.bash must be run from $GOROOT/src
            ./make.bash && STEP_MADE=1
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/go && return 0
    else
    
        echo "[Caution] Path: ( /opt/go-1.17.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# ############################################ Go - 1.21.11 ##########################################

# Function: 制作安装(Make Install) Go-1.21.11
# ##################################################
function Make_Install_Go_1_21_11() {

    # Compilation Time Error of "Go":
    # ----------------------------------------------
    # found packages main (build.go) and building_Go_requires_Go_1_17_13_or_later (notgo117.go) in /opt/Go-1.21.0/src/cmd/dist
    # ..............................................
    # Go 1.21.0 依赖的某个包需要 Go 语言的版本至少是 Go 1.17.13 或更高版本。
    # ..............................................
    # Building Go cmd/dist using /opt/go-1.4-bootstrap-20171003. (go1.4-bootstrap-20170531 linux/amd64)
    # cmd/dist/build.go:13:2: cannot find package "io/fs" in any of:
    #         /opt/go-1.4-bootstrap-20171003/src/io/fs (from $GOROOT)
    #         ($GOPATH not set)
    # ..............................................
    # 无法在指定的目录中找到 io/fs 包。这通常是因为 io/fs 包是在 Go 1.16 版本引入的, 而报错中提到的 Go 版本是 1.4。需要先安装 Go 1.16。
    
    if [[ ! -d "/opt/go-1.21.11" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_MOVED=0
        local STEP_CHANGE_DIRECTORY=0
        local STEP_MADE=0
    
        # ------------------------------------------
        read -p "[Confirm] Make and Install ( go-1.21.11 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar -zxvf $STORAGE/go1.21.11.src.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # The compilation directory of "Go" needs to be stored properly. After compilation, "GOROOT" defaults to the compilation directory.
        # Go 的编译目录需要妥善存放, 编译完成后, GOROOT 默认在编译目录下。
        cp -r $STORAGE/go /opt/go-1.21.11 && STEP_MOVED=1
        
        # ------------------------------------------
        cd /opt/go-1.21.11/src && STEP_CHANGE_DIRECTORY=1
        
        # ------------------------------------------
        if [[ $STEP_CHANGE_DIRECTORY == 1 ]]; then
            # all.bash / make.bash must be run from $GOROOT/src
            ./all.bash && STEP_MADE=1
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/go && return 0
    else
    
        echo "[Caution] Path: ( /opt/go-1.21.11 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {
    
    # ----------- Compilation Environment ----------
    ORIGINAL_PATH=$PATH

    # --------------- Dep for Go 1.16 --------------
    Make_Install_Go_1_4_Bootstrap_20171003
    # ------------------ Go - 1.16 -----------------
    export PATH=/opt/go-1.4-bootstrap-20171003/bin:$ORIGINAL_PATH
    Make_Install_Go_1_16
    # ----------------- Go - 1.17.3 ----------------
    export PATH=/opt/go-1.16/bin:$ORIGINAL_PATH
    Make_Install_Go_1_17_3
    # ----------------- Go - 1.21.11 ---------------
    export PATH=/opt/go-1.17.3/bin:$ORIGINAL_PATH
    Make_Install_Go_1_21_11
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 源码安装Go-1.21.11 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
