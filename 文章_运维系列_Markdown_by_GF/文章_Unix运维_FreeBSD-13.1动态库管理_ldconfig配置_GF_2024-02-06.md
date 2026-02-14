# 文章_Unix运维_FreeBSD-13.1动态库管理_ldconfig配置_GF_2024-02-06

大体上库 (Library) 的存在，有两方面的原因，一是代码的复用，二是声明和实现的分离。

将功能相近的使用模块封装成库，使代码的复用、管理和分发变得简单了许多，例如著名的开源图形库 ncurses，你可以自行编译，更可以直接使用已经编译好的现成的库文件。

另外，由于库是二进制文件，某种意义上讲，将功能的实现部分隐藏了起来，这就为商业代码的保护提供了一种方式。

## 配置 ld-elf.so.conf

FreeBSD 和 linux 不是一样的。

在 ==/etc/== 下加入 ld-elf.so.conf 里面写上你的目录，比如 ==/usr/local/samba/lib==，没有的话可以创建。

目录配置完成后，执行以下命令:

```shell
sudo /etc/rc.d/ldconfig restart

# 或者

/etc/rc.d/ldconfig forcerestart
```

## 查看加载的动态库路径

执行以下命令:

```shell
ldconfig -r

ldconfig -r | less
```

## 其它

或者在 ==/etc/rc.conf== 里加上 **ldconfig_path="[Path]"** 来配置动态库路径，这是系统启动起来的时候再设置的。

## 总结

以上就是关于 Unix运维 FreeBSD-13.1动态库管理_ldconfig配置的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
