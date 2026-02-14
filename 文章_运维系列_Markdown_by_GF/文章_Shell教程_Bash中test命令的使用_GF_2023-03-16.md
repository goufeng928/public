# 文章_Shell教程_Bash中test命令的使用_GF_2023-03-16

test 命令在 if 条件句中用得很多。test 命令后都会跟一个表达式, 作为它的参数。它有两种写法:

```shell
test EXPRESSION
[ EXPRESSION ]
```

## test 命令的使用

test 的执行过程就是拿一个元素与另一个元素进行比较。在网络上找了一个很有意思的例子, 用它来说明一下 test 命令的使用:

```shell
test 1 -eq 2 && echo "true" || echo "false"
```

参数说明:

```txt
*   1: 是用来作比较的第一个参数。
* -eq: 这是具体的比较方法。
*   2: 这是用来比较的第二个参数。
```

如果比较的结果是 true, 打印 true, 否则打印 false。

我们可以通过 $? 拿到 test 的结果。如果表达式的值是 false, 则$?的值是 1, 否则就是 0。

上面的语句与下同的表达是一样的:

```shell
[ 1 -eq 2 ] && echo "true" || echo "false"
```

## 整型相关的比较表达式 (两个数据的比较)

```txt
* -eq: 等于 (equal to)。
* -ne: 等于 (not equal to)。
* -gt: 大于 (greater than)。
* -ge: 大于或等于 (greater than or equal to)。
* -lt: 小于 (less than)。
* -le: 小于或等于 (less than or equal to)。
```

```shell
#!/usr/bin/env bash
 
test 1 -eq 2 && echo "true" || echo "false"
test 1 -ne 2 && echo "true" || echo "false"
test 1 -gt 2 && echo "true" || echo "false"
test 1 -ge 2 && echo "true" || echo "false"
test 1 -lt 2 && echo "true" || echo "false"
test 1 -le 2 && echo "true" || echo "false"
 
[ 1 -eq 2 ] && echo "true" || echo "false"
[ 1 -ne 2 ] && echo "true" || echo "false"
[ 1 -gt 2 ] && echo "true" || echo "false"
[ 1 -ge 2 ] && echo "true" || echo "false"
[ 1 -lt 2 ] && echo "true" || echo "false"
[ 1 -le 2 ] && echo "true" || echo "false"
```

## 字符串相关的比较表达式

```txt
*            -n <string>: 字符串长度不为零。
*            -z <string>: 字符串长度为零。
*               <string>: 字符串值非零, 与 -n <string> 等价。
*  <string1> = <string2>: 两个字符串是否相等。
* <string1> != <string2>: 两个字符串是否不相等。
```

针对字符串, Shell 提供了这些方便使用的表达式。比如说: -n <string> 这个表达式就是将字符串长度与 0 作比较。其他依次类推。

```shell
test -n string1 && echo "true" || echo "false"
test -z string1 && echo "true" || echo "false"
test string1 && echo "true" || echo "false"
test string1=string2 && echo "true" || echo "false"
test string1!=string2 && echo "true" || echo "false"
 
[ -n string1 ] && echo "true" || echo "false"
[ -z string1 ] && echo "true" || echo "false"
[ string1 ] && echo "true" || echo "false"
[ string1=string2 ] && echo "true" || echo "false"
[ string1!=string2 ] && echo "true" || echo "false"
```

## 文件相关的比较表达式

```txt
* <file1> -ef <file2>: 两个文件是否有相似的 device 和 inode 编号 (这些概念在 Linux 相关的知识可以了解到)。
* <file1> -nt <file2>: 通过比较文件的修改日期, 判断 file1 是否比 file2 要新。(nt : newer than)。
* <file1> -ot <file2>: 通过比较文件的修改日期, 判断 file1 是否比 file2 要旧。(ot : older than)。
*           -e <file>: 文件是否存在 (exists)。
*           -f <file>: 文件存在且是一个常规文件 (file)。
*           -d <file>: 文件存在且是一个目录 (directory)。
*           -r <file>: 文件存在且有读权限 (read)。
*           -w <file>: 文件存在且有写权限 (write)。
*           -x <file>: 文件存在且有执行权限  (execute)。
*           -s <file>: 文件存在且文件大小大于 0 (size)。
*           -S <file>: 文件存在且文件是一个 socket。
*           -O <file>: 文件存在且文件所有者是有效的用户 ID (owner)。
*           -G <file>: 文件存在且文件所有者是有效的用户组 ID (group)。
*           -h <file>: 文件存在且是一个符号连接文件 (hard)。
*           -L <file>: 文件存在且是一个符号连接文件 (link)。
*           -b <file>: 文件存在且是一个特殊块文件 (block)。
*           -c <file>: 文件存在且是一个特殊字符文件 (character)。
```

```shell
#!/usr/bin/env bash
 
test -e /bin/bash && echo $? || echo $?
test -f /bin/bash && echo $? || echo $?
test -d /bin/bash && echo $? || echo $?
test -r /bin/bash && echo $? || echo $?
test -w /bin/bash && echo $? || echo $?
test -x /bin/bash && echo $? || echo $?
test -s /bin/bash && echo $? || echo $?
test -S /bin/bash && echo $? || echo $?
test -O /bin/bash && echo $? || echo $?
test -G /bin/bash && echo $? || echo $?
test -h /bin/bash && echo $? || echo $?
test -L /bin/bash && echo $? || echo $?
test -b /bin/bash && echo $? || echo $?
test -c /bin/bash && echo $? || echo $?
 
#!/usr/bin/env bash
 
[ -e /bin/bash ] && echo $? || echo $?
[ -f /bin/bash ] && echo $? || echo $?
[ -d /bin/bash ] && echo $? || echo $?
[ -r /bin/bash ] && echo $? || echo $?
[ -w /bin/bash ] && echo $? || echo $?
[ -x /bin/bash ] && echo $? || echo $?
[ -s /bin/bash ] && echo $? || echo $?
[ -S /bin/bash ] && echo $? || echo $?
[ -O /bin/bash ] && echo $? || echo $?
[ -G /bin/bash ] && echo $? || echo $?
[ -h /bin/bash ] && echo $? || echo $?
[ -L /bin/bash ] && echo $? || echo $?
[ -b /bin/bash ] && echo $? || echo $?
[ -c /bin/bash ] && echo $? || echo $?
```

Shell 提供了上面这些方便的表达式, 我们就少做了很多功夫。

所以, 现在看来 test 很简单, 但是很有用。因为 Shell 脚本里会出现很多条件语句, test 会用到很多。

## 总结

以上就是关于 Shell教程 Bash中test命令的使用 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
