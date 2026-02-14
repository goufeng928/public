# 文章_PHP教程_PHP5函数mysql_connect协同的mysql_fetch_row函数_GF_2024-02-06

PHP (PHP: Hypertext Preprocessor) 即 "超文本预处理器", 是在服务器端执行的脚本语言, 尤其适用于Web开发并可嵌入HTML中。

PHP 语法学习了 C语言, 吸纳 Java 和 Perl 多个语言的特色发展出自己的特色语法, 并根据它们的长项持续改进提升自己, 例如 Java 的面向对象编程, 该语言当初创建的主要目标是让开发人员快速编写出优质的 Web 网站。

PHP 同时支持面向对象和面向过程的开发, 使用上非常灵活。

## 函数 mysql_connect() 介绍

* 函数 mysql_connect() 用于 PHP 3, PHP 4 兼容 PHP 5+ 并且在 PHP 7.0.0 中完全被移除, 因为它可能会导致性能问题和死锁。

* PHP 5.6.40 及以上版本应使用 mysqli 或者 pdo 扩展, 用这两个扩展连接数据库比之前的 mysql_connect() 更安全。

## 函数 mysql_fetch_row() 介绍

* 函数 mysql_fetch_row() 是 mysql_connect() 的协同函数。

**定义和用法**:

mysql_fetch_row() 函数从结果集中取得一行作为数字数组。

**语法**:

mysql_fetch_row(data)

```txt
+-----+------------------------------------------------------------------+
|参数 |描述                                                              |
+-----+------------------------------------------------------------------+
|data |必需。要使用的数据指针。该数据指针是从 mysql_query() 返回的结果。 |
+-----+------------------------------------------------------------------+
```

**说明**:

mysql_fetch_row() 从和结果标识 data 关联的结果集中取得一行数据并作为数组返回。每个结果的列储存在一个数组的单元中, 偏移量从 0 开始。

依次调用 mysql_fetch_row() 将返回结果集中的下一行, 如果没有更多行则返回 FALSE。

**返回值**:

返回根据所取得的行生成的数组, 如果没有更多行则返回 false。

## 函数 mysql_fetch_row() 示例

**示例代码**:

```php
<?php

/* 创建数据库连接 */
$con = mysql_connect("localhost", "hello", "321");

/* 判断数据库连接是否成功 */
if (!$con) {
  die('Could not connect: ' . mysql_error());
}

/* 通过创建的数据库连接选择数据库 "test_db" */
$db_selected = mysql_select_db("test_db", $con);

/* 组织 SQL 语句 */
$sql = "SELECT * from Person WHERE Lastname='Adams'";

/* 通过创建的数据库连接执行 SQL 语句 */
$result = mysql_query($sql, $con);

/* 使用 mysql_fetch_row() 函数从 SQL 查询结果中取得一行数据并作为数组返回, 并将返回的数组输出 */
print_r(mysql_fetch_row($result));

/* 关闭数据库连接 */
mysql_close($con);

?>
```

**输出**:

```txt
Array
(
[0] => Adams
[1] => John
[2] => London
)
```

## 总结

以上就是关于 PHP教程 PHP5函数mysql_connect协同的mysql_fetch_row函数 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
