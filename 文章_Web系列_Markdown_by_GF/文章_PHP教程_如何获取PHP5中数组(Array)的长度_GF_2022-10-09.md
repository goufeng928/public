# 文章_PHP教程_如何获取PHP5中数组(Array)的长度_GF_2022-10-09

PHP (PHP: Hypertext Preprocessor) 即 "超文本预处理器", 是在服务器端执行的脚本语言, 尤其适用于Web开发并可嵌入HTML中。

PHP 语法学习了 C语言, 吸纳 Java 和 Perl 多个语言的特色发展出自己的特色语法, 并根据它们的长项持续改进提升自己, 例如 Java 的面向对象编程, 该语言当初创建的主要目标是让开发人员快速编写出优质的 Web 网站。

PHP 同时支持面向对象和面向过程的开发, 使用上非常灵活。

## 使用 PHP5 内置函数 count() 获取数组长度

**示例代码**:

```php
<?php

$array = array(1, 2, 3, 4, 5);

echo count($array);

?>
```

**输出**:

```txt
5
```

## 使用 PHP5 内置函数 count() 并传入第 2 参数 COUNT_NORMAL 获取多维数组长度

**示例代码**:

```php
<?php

$multiArray = array(
    array(1, 2, 3),
    array(4, 5, 6),
    array(7, 8, 9)
);

echo count($multiArray, COUNT_NORMAL);

?>
```

**输出**:

```txt
3
```

## 使用 PHP5 内置函数 count() 并传入第 2 参数 COUNT_RECURSIVE 获取多维数组中所有元素的总数

请注意, 对于大型数组, COUNT_RECURSIVE 可能会消耗较多资源并导致性能问题。

**示例代码**:

```php
<?php

$multiArray = array(
    array(1, 2, 3),
    array(4, 5, 6),
    array(7, 8, 9)
);

echo count($multiArray, COUNT_RECURSIVE);

?>
```

**输出**:

```txt
9
```

## 总结

以上就是关于 PHP教程 如何获取PHP5中数组(Array)的长度 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
