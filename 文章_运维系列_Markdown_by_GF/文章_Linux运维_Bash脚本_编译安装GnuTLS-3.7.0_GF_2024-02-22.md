# 文章_Linux运维_Bash脚本_编译安装GnuTLS-3.7.0_GF_2024-02-22

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

nettle-3.6.tar.gz

gmp-6.3.0.tar.xz

libtasn1-4.19.0.tar.gz

libunistring-1.1.tar.gz

libffi-3.4.4.tar.gz

p11-kit-0.25.3.tar.xz

texinfo-7.1.tar.xz

gnutls-3.7.0.tar.xz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-22 20:21

# Need File: nettle-3.6.tar.gz
# Need File: gmp-6.3.0.tar.xz
# Need File: libtasn1-4.19.0.tar.gz
# Need File: libunistring-1.1.tar.gz
# Need File: libffi-3.4.4.tar.gz
# Need File: p11-kit-0.25.3.tar.xz
# Need File: texinfo-7.1.tar.xz
# Need File: gnutls-3.7.0.tar.xz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) nettle-3.6 (for Linux)
# ##################################################
function compile_install_nettle_3_6_for_linux() {

    if [[ ! -d "/usr/local/nettle-3.6" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( nettle-3.6 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/nettle-3.6.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        # * Problem: Libhogweed (nettle's companion library) was not found. Note that you must compile nettle with gmp support.
        #   - Solve: ./configure --enable-mini-gmp
        cd $STORAGE/nettle-3.6 && ./configure --prefix=/usr/local/nettle-3.6 \
                                              --enable-shared \
                                              --enable-mini-gmp && ldconfig && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/include/nettle" ]]; then mkdir /usr/local/include/nettle; fi
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/nettle-3.6/bin/nettle-hash        /usr/local/bin/
            ln -sf /usr/local/nettle-3.6/bin/nettle-lfib-stream /usr/local/bin/
            ln -sf /usr/local/nettle-3.6/bin/nettle-pbkdf2      /usr/local/bin/
            ln -sf /usr/local/nettle-3.6/bin/pkcs1-conv         /usr/local/bin/
            ln -sf /usr/local/nettle-3.6/bin/sexp-conv          /usr/local/bin/
            # ......................................
            ln -sf /usr/local/nettle-3.6/include/nettle/aes.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/arcfour.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/arctwo.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/asn1.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/base16.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/base64.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/bignum.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/blowfish.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/buffer.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/camellia.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/cast128.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/cbc.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ccm.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/cfb.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/chacha.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/chacha-poly1305.h /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/cmac.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ctr.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/curve25519.h      /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/curve448.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/des.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/dsa-compat.h      /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/dsa.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/eax.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ecc-curve.h       /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ecc.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ecdsa.h           /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/eddsa.h           /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/gcm.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/gostdsa.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/gosthash94.h      /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/hkdf.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/hmac.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/knuth-lfib.h      /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/macros.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/md2.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/md4.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/md5-compat.h      /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/md5.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/memops.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/memxor.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/mini-gmp.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/nettle-meta.h     /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/nettle-types.h    /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/pbkdf2.h          /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/pgp.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/pkcs1.h           /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/poly1305.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/pss.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/pss-mgf1.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/realloc.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/ripemd160.h       /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/rsa.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/salsa20.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/serpent.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/sexp.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/sha1.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/sha2.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/sha3.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/sha.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/siv-cmac.h        /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/twofish.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/umac.h            /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/version.h         /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/xts.h             /usr/local/include/nettle/
            ln -sf /usr/local/nettle-3.6/include/nettle/yarrow.h          /usr/local/include/nettle/
            # ......................................
            ln -sf /usr/local/nettle-3.6/lib/libhogweed.a      /usr/local/lib/
            ln -sf /usr/local/nettle-3.6/lib/libhogweed.so.6.0 /usr/local/lib/libhogweed.so
            ln -sf /usr/local/nettle-3.6/lib/libhogweed.so.6.0 /usr/local/lib/libhogweed.so.6
            ln -sf /usr/local/nettle-3.6/lib/libhogweed.so.6.0 /usr/local/lib/
            ln -sf /usr/local/nettle-3.6/lib/libnettle.a       /usr/local/lib/
            ln -sf /usr/local/nettle-3.6/lib/libnettle.so.8.0  /usr/local/lib/libnettle.so
            ln -sf /usr/local/nettle-3.6/lib/libnettle.so.8.0  /usr/local/lib/libnettle.so.8
            ln -sf /usr/local/nettle-3.6/lib/libnettle.so.8.0  /usr/local/lib/
            # ......................................
            ln -sf /usr/local/nettle-3.6/lib/pkgconfig/hogweed.pc /usr/local/lib/pkgconfig/
            ln -sf /usr/local/nettle-3.6/lib/pkgconfig/nettle.pc  /usr/local/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/nettle-3.6 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/nettle-3.6 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) gmp-6.3.0
# ##################################################
function compile_install_gmp_6_3_0() {

    if [[ ! -d "/usr/local/gmp-6.3.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gmp-6.3.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/gmp-6.3.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gmp-6.3.0 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make check && make install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gmp-6.3.0 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/gmp-6.3.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libtasn1-4.19.0
# ##################################################
function compile_install_libtasn1_4_19_0() {

    if [[ ! -d "/usr/local/libtasn1-4.19.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libtasn1-4.19.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libtasn1-4.19.0.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libtasn1-4.19.0 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libtasn1-4.19.0 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/libtasn1-4.19.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libunistring-1.1
# ##################################################
function compile_install_llibunistring_1_1() {

    if [[ ! -d "/usr/local/libunistring-1.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libunistring-1.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libunistring-1.1.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libunistring-1.1 && ./configure && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/libunistring-1.1 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/libunistring-1.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) libffi-3.4.4
# ##################################################
function compile_install_libffi_3_4_4() {

    if [[ ! -d "/usr/local/libffi-3.4.4" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( libffi-3.4.4 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/libffi-3.4.4.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/libffi-3.4.4 && ./configure --prefix=/usr/local/libffi-3.4.4 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/libffi-3.4.4/include/ffi.h       /usr/local/include/
            ln -sf /usr/local/libffi-3.4.4/include/ffitarget.h /usr/local/include/
            # ......................................
            ln -sf /usr/local/libffi-3.4.4/lib/libffi.a        /usr/local/lib/
            ln -sf /usr/local/libffi-3.4.4/lib/libffi.la       /usr/local/lib/
            ln -sf /usr/local/libffi-3.4.4/lib/libffi.so.8.1.2 /usr/local/lib/libffi.so
            ln -sf /usr/local/libffi-3.4.4/lib/libffi.so.8.1.2 /usr/local/lib/libffi.so.8
            ln -sf /usr/local/libffi-3.4.4/lib/libffi.so.8.1.2 /usr/local/lib/
            # ......................................
            ln -sf /usr/local/libffi-3.4.4/lib/pkgconfig/libffi.pc /usr/local/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/llibffi-3.4.4 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/libffi-3.4.4 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) p11-kit-0.25.3
# ##################################################
function compile_install_p11_kit_0_25_3() {

    if [[ ! -d "/usr/local/p11-kit-0.25.3" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( p11-kit-0.25.3 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/p11-kit-0.25.3.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/p11-kit-0.25.3 && ./configure --prefix=/usr/local/p11-kit-0.25.3 \
                                                  PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/include/p11-kit-1" ]]; then mkdir /usr/local/include/p11-kit-1; fi
            if [[ ! -d "/usr/local/include/p11-kit-1/p11-kit" ]]; then mkdir /usr/local/include/p11-kit-1/p11-kit; fi
            if [[ ! -d "/usr/local/lib/pkcs11" ]]; then mkdir /usr/local/lib/pkcs11; fi
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/p11-kit-0.25.3/bin/p11-kit /usr/local/bin/
            ln -sf /usr/local/p11-kit-0.25.3/bin/trust   /usr/local/bin/
            # ......................................
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/deprecated.h /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/iter.h       /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/p11-kit.h    /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/pin.h        /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/pkcs11.h     /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/pkcs11x.h    /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/remote.h     /usr/local/include/p11-kit-1/p11-kit/
            ln -sf /usr/local/p11-kit-0.25.3/include/p11-kit-1/p11-kit/uri.h        /usr/local/include/p11-kit-1/p11-kit/
            # ......................................
            ln -sf /usr/local/p11-kit-0.25.3/lib/libp11-kit.la       /usr/local/lib/
            ln -sf /usr/local/p11-kit-0.25.3/lib/libp11-kit.so.0.3.1 /usr/local/lib/libp11-kit.so
            ln -sf /usr/local/p11-kit-0.25.3/lib/libp11-kit.so.0.3.1 /usr/local/lib/libp11-kit.so.0
            ln -sf /usr/local/p11-kit-0.25.3/lib/libp11-kit.so.0.3.1 /usr/local/lib/
            ln -sf /usr/local/p11-kit-0.25.3/lib/libp11-kit.so.0.3.1 /usr/local/lib/p11-kit-proxy.so
            # ......................................
            ln -sf /usr/local/p11-kit-0.25.3/lib/pkcs11/p11-kit-client.la /usr/local/lib/pkcs11/
            ln -sf /usr/local/p11-kit-0.25.3/lib/pkcs11/p11-kit-client.so /usr/local/lib/pkcs11/
            ln -sf /usr/local/p11-kit-0.25.3/lib/pkcs11/p11-kit-trust.la  /usr/local/lib/pkcs11/
            ln -sf /usr/local/p11-kit-0.25.3/lib/pkcs11/p11-kit-trust.so  /usr/local/lib/pkcs11/
            # ......................................
            ln -sf /usr/local/p11-kit-0.25.3/lib/pkgconfig/p11-kit-1.pc /usr/local/lib/pkgconfig/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/p11-kit-0.25.3 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/p11-kit-0.25.3 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) texinfo-7.1
# ##################################################
function compile_install_texinfo_7_1() {

    if [[ ! -d "/usr/local/texinfo-7.1" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( texinfo-7.1 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/texinfo-7.1.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/texinfo-7.1 && ./configure --prefix=/usr/local/texinfo-7.1 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/texinfo" ]]; then mkdir /usr/local/lib/texinfo; fi
            # ......................................
            ln -sf /usr/local/texinfo-7.1/bin/install-info /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/texi2any     /usr/local/bin/makeinfo
            ln -sf /usr/local/texinfo-7.1/bin/pdftexi2dvi  /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/pod2texi     /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/texi2any     /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/texi2dvi     /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/texi2pdf     /usr/local/bin/
            ln -sf /usr/local/texinfo-7.1/bin/texindex     /usr/local/bin/
            # ......................................
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/MiscXS.la      /usr/local/lib/texinfo/
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/MiscXS.so      /usr/local/lib/texinfo/
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/Parsetexi.la   /usr/local/lib/texinfo/
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/Parsetexi.so   /usr/local/lib/texinfo/
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/XSParagraph.la /usr/local/lib/texinfo/
            ln -sf /usr/local/texinfo-7.1/lib/texinfo/XSParagraph.so /usr/local/lib/texinfo/
        fi

        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/texinfo-7.1 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/texinfo-7.1 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) gnutls-3.7.0
# ##################################################
function compile_install_gnutls_3_7_0() {

    if [[ ! -d "/usr/local/gnutls-3.7.0" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( gnutls-3.7.0 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar xvJf $STORAGE/gnutls-3.7.0.tar.xz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/gnutls-3.7.0 && ./configure --prefix=/usr/local/gnutls-3.7.0 \
                                                PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" && STEP_CONFIGURED=1
        
        # ------------------------------------------
        # * Problem: /home/goufeng/gnutls-3.7.0/build-aux/missing: line 81: makeinfo: command not found.
        #   - Solve: Install "textinfo".
        make && make install && STEP_INSTALLED=1

        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/include/gnutls" ]]; then mkdir /usr/local/include/gnutls; fi
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/gnutls-3.7.0/bin/certtool         /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/gnutls-cli       /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/gnutls-cli-debug /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/gnutls-serv      /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/ocsptool         /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/p11tool          /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/psktool          /usr/local/bin/
            ln -sf /usr/local/gnutls-3.7.0/bin/srptool          /usr/local/bin/
            # ......................................
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/abstract.h    /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/compat.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/crypto.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/dtls.h        /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/gnutls.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/gnutlsxx.h    /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/ocsp.h        /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/openpgp.h     /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/pkcs11.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/pkcs12.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/pkcs7.h       /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/self-test.h   /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/socket.h      /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/system-keys.h /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/tpm.h         /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/urls.h        /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/x509-ext.h    /usr/local/include/gnutls/
            ln -sf /usr/local/gnutls-3.7.0/include/gnutls/x509.h        /usr/local/include/gnutls/
            # ......................................
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutls.la          /usr/local/lib/
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutls.so.30.29.0  /usr/local/lib/libgnutls.so
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutls.so.30.29.0  /usr/local/lib/libgnutls.so.30
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutls.so.30.29.0  /usr/local/lib/
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutlsxx.la        /usr/local/lib/
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutlsxx.so.28.1.0 /usr/local/lib/libgnutlsxx.so
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutlsxx.so.28.1.0 /usr/local/lib/libgnutlsxx.so.28
            ln -sf /usr/local/gnutls-3.7.0/lib/libgnutlsxx.so.28.1.0 /usr/local/lib/
            # ......................................
            ln -sf /usr/local/gnutls-3.7.0/lib/pkgconfig/gnutls.pc   /usr/local/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/gnutls-3.7.0 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/gnutls-3.7.0 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    compile_install_nettle_3_6_for_linux
    compile_install_gmp_6_3_0
    compile_install_libtasn1_4_19_0
    compile_install_llibunistring_1_1
    compile_install_libffi_3_4_4
    compile_install_p11_kit_0_25_3
    compile_install_texinfo_7_1
    compile_install_gnutls_3_7_0
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装GnuTLS-3.7.0 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
