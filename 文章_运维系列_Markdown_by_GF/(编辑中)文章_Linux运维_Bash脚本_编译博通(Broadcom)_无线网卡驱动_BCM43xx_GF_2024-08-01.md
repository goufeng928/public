# 文章_Linux运维_Bash脚本_编译博通(Broadcom)_无线网卡驱动_BCM43xx_GF_2024-08-01

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

hybrid-v35-nodebug-pcoem-6_30_223_271.tar.gz 或者 hybrid-v35_64-nodebug-pcoem-6_30_223_271.tar.gz

wl-kmod-01_kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch

wl-kmod-02_kernel_4.8_add_cfg80211_scan_info_struct.patch

wl-kmod-03_fix_kernel_warnings.patch

wl-kmod-04_kernel_4.11_remove_last_rx_in_net_device_struct.patch

wl-kmod-05_kernel_4.12_add_cfg80211_roam_info_struct.patch
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell

# 第 1 步: 在 /usr/local/src 下创建 hybrid-wl 目录。

mkdir -p /usr/local/src/hybrid-wl

cd /usr/local/src/hybrid-wl

tar -zxvf /path/to/the/tarball/hybrid-v35_64-nodebug-pcoem-6_30_223_271.tar.gz

chown -R nobody.nobody /usr/local/src/hybrid-wl

# 第 2 步: 使用 patch 命令对源码文件打补丁 (也可对照 xxx.patch 文件中内容手动修改源码)。

patch -p1 < ../wl-kmod-01_kernel_4.7_IEEE80211_BAND_to_NL80211_BAND.patch

patch -p1 < ../wl-kmod-02_kernel_4.8_add_cfg80211_scan_info_struct.patch

patch -p1 < ../wl-kmod-03_fix_kernel_warnings.patch

patch -p1 < ../wl-kmod-04_kernel_4.11_remove_last_rx_in_net_device_struct.patch

patch -p1 < ../wl-kmod-05_kernel_4.12_add_cfg80211_roam_info_struct.patch

# 第 3 步: 使用 sed 命令对源码文件进行修改。

sed -i "s/>= KERNEL_VERSION(3, 11, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(3, 15, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/< KERNEL_VERSION(3, 18, 0)/< KERNEL_VERSION(3, 9, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(4, 0, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/< KERNEL_VERSION(4,2,0)/< KERNEL_VERSION(3, 9, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(4, 7, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(4, 8, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(4, 11, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/< KERNEL_VERSION(4, 12, 0)/< KERNEL_VERSION(3, 9, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/>= KERNEL_VERSION(4, 12, 0)/>= KERNEL_VERSION(3, 10, 0)/" src/wl/sys/wl_cfg80211_hybrid.c

sed -i "s/<= KERNEL_VERSION(4, 10, 0)/< KERNEL_VERSION(3, 9, 0)/" src/wl/sys/wl_linux.c

# 第 4 步: 使用 make 命令对源码文件进行编译制作。
# ..................................................
# make 选项格式: make -C /lib/modules/[内核版本]/build/ M=[当前目录]

make -C /lib/modules/`uname -r`/build/ M=`pwd`
```

## 总结

以上就是关于 Linux运维 Bash脚本 编译安装Flex-2.6.4 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
