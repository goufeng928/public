# 文章_sed教程_使用sed命令向行尾添加字符(附sed元字符集)_GF_2024-03-23

sed 是一项 Linux 指令, 功能同 awk 类似, 差别在于, sed 简单, 对列处理的功能要差一些, awk 的功能复杂, 对列处理的功能比较强大。

* sed 元字符集:

```txt
^ 锚定行的开始, 如: /^sed/ 匹配所有以 sed 开头的行。

$ 锚定行的结束, 如: /sed$/ 匹配所有以 sed 结尾的行。

. 匹配一个非换行符的字符, 如: /s.d/ 匹配 s 后接一个任意字符, 然后是 d。

* 匹配零或多个字符, 如: /*sed/ 匹配所有模板是一个或多个空格后紧跟 sed 的行。

[] 匹配一个指定范围内的字符, 如: /[Ss]ed/ 匹配 sed 和 Sed。

[^] 匹配一个不在指定范围内的字符, 如: /[^A-RT-Z]ed/ 匹配不包含 A-R 和 T-Z 的一个字母开头, 紧跟 ed 的行。

\(..\) 保存匹配的字符, 如: s/\(love\)able/\1rs, loveable 被替换成 lovers。

& 保存搜索字符用来替换其他字符, 如 s/love/**&**/, love 这成 **love**。

\< 锚定单词的开始, 如: /\<love/ 匹配包含以 love 开头的单词的行。

> 锚定单词的结束, 如: /love\>/ 匹配包含以 love 结尾的单词的行。

x\{m\} 重复字符 x, m 次, 如: /0\{5\}/ 匹配包含 5 个 o 的行。

x\{m,\} 重复字符 x, 至少 m 次, 如: /o\{5,\}/ 匹配至少有 5 个 o 的行。

x\{m,n\} 重复字符 x, 至少 m 次, 不多于 n 次, 如: /o\{5,10\}/ 匹配 5-10 个 o 的行。
```

## 使用 sed 命令向行尾添加字符 (方法 1: 使用 $ 元字符定位行尾)

* 示例文件 /var/File.txt

获取文件内容:

```shell
cat /var/File.txt
```

输出:

```txt
Line 1
Line 2
```

* 使用 sed 命令向第 2 行的行尾添加 "Have a Apple" 字符串:

命令:

```shell
sed "2 s/$/ Have a Apple/" File.txt
```

输出:

```txt
Line 1
Line 2 Have a Apple
```

* 释义: "/" 表示分隔符, "2 s" 表示修改第 2 行, "$" 表示行尾, " Have a Apple" 表示需要添加的字符串。

## 使用 sed 命令向行尾添加字符 (方法 2: 使用 & 元字符引用匹配结果)

命令:

```shell
echo "Hello World" | sed "s/World/& World/"
```

输出:

```txt
Hello World World
```

* 释义: "&" 符号代表的是前面的匹配的模式, 相当于把匹配到的 "World" 引用过来。

## 总结

以上就是关于 sed教程 使用sed命令向行尾添加字符(附sed元字符集) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
