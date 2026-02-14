# 文章_Linux运维_Bash脚本_编译安装OpenSSL-1.1.1g_GF_2024-02-20

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

zlib-1.2.13.tar.gz

openssl-1.1.1g.tar.gz
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-02-20 21:42

# Need File: zlib-1.2.13.tar.gz
# Need File: openssl-1.1.1g.tar.gz

# ##################################################
STORAGE=/home/goufeng

# Function: 编译安装(Compile Install) zlib-1.2.13
# ##################################################
function compile_install_zlib_1_2_13() {

    if [[ ! -d "/usr/local/zlib-1.2.13" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( zlib-1.2.13 )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/zlib-1.2.13.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/zlib-1.2.13 && ./configure --prefix=/usr/local/zlib-1.2.13 && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/zlib-1.2.13/include/zconf.h /usr/local/include/
            ln -sf /usr/local/zlib-1.2.13/include/zlib.h  /usr/local/include/
            # ......................................
            ln -sf /usr/local/zlib-1.2.13/lib/libz.a         /usr/local/lib/
            ln -sf /usr/local/zlib-1.2.13/lib/libz.so        /usr/local/lib/
            ln -sf /usr/local/zlib-1.2.13/lib/libz.so.1      /usr/local/lib/
            ln -sf /usr/local/zlib-1.2.13/lib/libz.so.1.2.13 /usr/local/lib/
            # ......................................
            ln -sf /usr/local/zlib-1.2.13/lib/pkgconfig/zlib.pc /usr/local/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/zlib-1.2.13 && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/zlib-1.2.13 ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

# Function: 编译安装(Compile Install) openssl-1.1.1g (for Linux)
# ##################################################
function compile_install_openssl_1_1_1g_for_linux() {

    if [[ ! -d "/usr/local/openssl-1.1.1g" ]]; then
    
        local VERIFY
        local STEP_UNZIPPED=0
        local STEP_CONFIGURED=0
        local STEP_INSTALLED=0
    
        # ------------------------------------------
        read -p "[Confirm] Compile and Install ( openssl-1.1.1g )? (y/n)>" VERIFY
        if [[ "$VERIFY" != "y" ]]; then exit 1; fi

        # ------------------------------------------
        tar zxvf $STORAGE/openssl-1.1.1g.tar.gz && STEP_UNZIPPED=1
        
        # ------------------------------------------
        cd $STORAGE/openssl-1.1.1g && ./config --prefix=/usr/local/openssl-1.1.1g \
                                               --openssldir=/usr/local/openssl-1.1.1g/ssl \
                                               --shared \
                                               zlib && STEP_CONFIGURED=1
        
        # ------------------------------------------
        make && make install && STEP_INSTALLED=1
        
        # ------------------------------------------
        if [[ $STEP_INSTALLED == 1 ]]; then
            if [[ -f "/usr/bin/openssl" && ! -f "/usr/bin/openssl.bak" ]]; then mv /usr/bin/openssl /usr/bin/openssl.bak; fi
            # ......................................
            if [[ ! -d "/usr/local/include/openssl" ]]; then mkdir /usr/local/include/openssl; fi
            if [[ ! -d "/usr/local/lib/engines-1.1" ]]; then mkdir /usr/local/lib/engines-1.1; fi
            if [[ ! -d "/usr/local/lib/pkgconfig" ]]; then mkdir /usr/local/lib/pkgconfig; fi
            # ......................................
            ln -sf /usr/local/openssl-1.1.1g/bin/openssl /usr/local/bin/
            # ......................................
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/aes.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/asn1err.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/asn1.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/asn1_mac.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/asn1t.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/asyncerr.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/async.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/bioerr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/bio.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/blowfish.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/bnerr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/bn.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/buffererr.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/buffer.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/camellia.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cast.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cmac.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cmserr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cms.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/comperr.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/comp.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/conf_api.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/conferr.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/conf.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cryptoerr.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/crypto.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/cterr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ct.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/des.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/dherr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/dh.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/dsaerr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/dsa.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/dtls1.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ebcdic.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ecdh.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ecdsa.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ecerr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ec.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/engineerr.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/engine.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/e_os2.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/err.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/evperr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/evp.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/hmac.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/idea.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/kdferr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/kdf.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/lhash.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/md2.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/md4.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/md5.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/mdc2.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/modes.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/objectserr.h  /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/objects.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/obj_mac.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ocsperr.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ocsp.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/opensslconf.h /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/opensslv.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ossl_typ.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pem2.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pemerr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pem.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pkcs12err.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pkcs12.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pkcs7err.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/pkcs7.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rand_drbg.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/randerr.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rand.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rc2.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rc4.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rc5.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ripemd.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rsaerr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/rsa.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/safestack.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/seed.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/sha.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/srp.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/srtp.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ssl2.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ssl3.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/sslerr.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ssl.h         /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/stack.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/storeerr.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/store.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/symhacks.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/tls1.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/tserr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ts.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/txt_db.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/uierr.h       /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/ui.h          /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/whrlpool.h    /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/x509err.h     /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/x509.h        /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/x509v3err.h   /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/x509v3.h      /usr/local/include/openssl/
            ln -sf /usr/local/openssl-1.1.1g/include/openssl/x509_vfy.h    /usr/local/include/openssl/
            # ......................................
            ln -sf /usr/local/openssl-1.1.1g/lib/libcrypto.a      /usr/local/lib/
            ln -sf /usr/local/openssl-1.1.1g/lib/libcrypto.so     /usr/local/lib/
            ln -sf /usr/local/openssl-1.1.1g/lib/libcrypto.so.1.1 /usr/local/lib/
            ln -sf /usr/local/openssl-1.1.1g/lib/libssl.a         /usr/local/lib/
            ln -sf /usr/local/openssl-1.1.1g/lib/libssl.so        /usr/local/lib/
            ln -sf /usr/local/openssl-1.1.1g/lib/libssl.so.1.1    /usr/local/lib/
            # ......................................
            ln -sf /usr/local/openssl-1.1.1g/lib/engines-1.1/afalg.so   /usr/local/lib/engines-1.1/
            ln -sf /usr/local/openssl-1.1.1g/lib/engines-1.1/capi.so    /usr/local/lib/engines-1.1/
            ln -sf /usr/local/openssl-1.1.1g/lib/engines-1.1/padlock.so /usr/local/lib/engines-1.1/
            # ......................................
            ln -sf /usr/local/openssl-1.1.1g/lib/pkgconfig/libcrypto.pc /usr/local/lib/pkgconfig/
            ln -sf /usr/local/openssl-1.1.1g/lib/pkgconfig/libssl.pc    /usr/local/lib/pkgconfig/
            ln -sf /usr/local/openssl-1.1.1g/lib/pkgconfig/openssl.pc   /usr/local/lib/pkgconfig/
        fi
        
        # ------------------------------------------
        cd $STORAGE && rm -rf $STORAGE/openssl-1.1.1g && return 0
    else
    
        echo "[Caution] Path: ( /usr/local/openssl-1.1.1g ) Already Exists."
        # ------------------------------------------
        return 0
    fi
}

function main() {

    cocompile_install_zlib_1_2_13
    compile_install_openssl_1_1_1g_for_linux
}

main
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装OpenSSL-1.1.1g 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
