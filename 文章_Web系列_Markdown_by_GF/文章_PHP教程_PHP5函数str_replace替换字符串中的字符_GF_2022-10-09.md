# 文章_PHP教程_PHP5函数str_replace替换字符串中的字符_GF_2022-10-09

PHP (PHP: Hypertext Preprocessor) 即 "超文本预处理器", 是在服务器端执行的脚本语言, 尤其适用于Web开发并可嵌入HTML中。

PHP 语法学习了 C语言, 吸纳 Java 和 Perl 多个语言的特色发展出自己的特色语法, 并根据它们的长项持续改进提升自己, 例如 Java 的面向对象编程, 该语言当初创建的主要目标是让开发人员快速编写出优质的 Web 网站。

PHP 同时支持面向对象和面向过程的开发, 使用上非常灵活。

## 函数 str_replace() 试用

把字符串 "Hello world!" 中的字符 "world" 替换成 "Peter"。

**试用代码**:

```php
<!DOCTYPE html>
<html>
<body>

<?php
echo str_replace("world","Peter","Hello world!");
?>

<p>In this example, we search for the string "Hello World!", find the value "world" and then replace the value with "Peter".</p>

</body>
</html>
```

**输出**:

```txt
Hello Peter!
In this example, we search for the string "Hello World!", find the value "world" and then replace the value with "Peter".
```

## 函数 str_replace() 介绍

**定义和用法**:

str_replace() 函数替换字符串中的一些字符 (区分大小写)。

该函数必须遵循下列规则: 

    * 如果搜索的字符串是一个数组, 那么它将返回一个数组。

    * 如果搜索的字符串是一个数组, 那么它将对数组中的每个元素进行查找和替换。

    * 如果同时需要对某个数组进行查找和替换, 并且需要执行替换的元素少于查找到的元素的数量, 那么多余的元素将用空字符串进行替换。

    * 如果是对一个数组进行查找, 但只对一个字符串进行替换, 那么替代字符串将对所有查找到的值起作用。

注释: 该函数是区分大小写的。请使用 str_ireplace() 函数执行不区分大小写的搜索。

注释: 该函数是二进制安全的。

**语法**:

str_replace(find, replace, string, count)

```txt
+--------+-----------------------------------+
|参数    |描述                               |
+--------+-----------------------------------+
|find    |必需。规定要查找的值。             |
+--------+-----------------------------------+
|replace |必需。规定替换 find 中的值的值。   |
+--------+-----------------------------------+
|string  |必需。规定被搜索的字符串。         |
+--------+-----------------------------------+
|count   |可选。一个变量, 对替换数进行计数。 |
+--------+-----------------------------------+
```

**技术细节**:

```txt
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|返回值:   |返回带有替换值的字符串或数组。                                                                                                                                    |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|PHP 版本: |4+                                                                                                                                                                |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|更新日志: |在 PHP 5.0 中, 新增了 count 参数。                                                                                                                                |
|          |在 PHP 4.3.3 之前, 该函数的 find 和 replace 参数都为数组时将会遇到麻烦, 会引起空的 find 索引在内部指针没有更换到 replace 数组上时被忽略。新的版本不会有这个问题。 |
|          |自 PHP 4.0.5 起, 大多数参数可以是一个数组。                                                                                                                       |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

**返回值**:

返回根据所取得的行生成的数组, 如果没有更多行则返回 false。

## 函数 str_replace() 示例

* 使用带有数组和 count 变量的 str_replace() 函数。

**示例代码**:

```php
<!DOCTYPE html>
<html>
<body>

<?php
$arr = array("blue","red","green","yellow");
print_r(str_replace("red","pink",$arr,$i));
echo "<br>" . "Replacements: $i";
?>

<p>In this example, we search an array to find the value "red", and then we replace the value "red" with "pink".</p>

</body>
</html>
```

**输出**:

```txt
Array ( [0] => blue [1] => pink [2] => green [3] => yellow )
Replacements: 1
In this example, we search an array to find the value "red", and then we replace the value "red" with "pink".
```

* 使用带有需要替换的元素少于查找到的元素的 str_replace() 函数。

**示例代码**:

```php
<!DOCTYPE html>
<html>
<body>

<?php
$find = array("Hello","world");
$replace = array("B");
$arr = array("Hello","world","!");
print_r(str_replace($find,$replace,$arr));
?>

</body>
</html>
```

**输出**:

```txt
Array ( [0] => B [1] => [2] => ! )
```

## 总结

以上就是关于 PHP教程 PHP5函数str_replace替换字符串中的字符 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
