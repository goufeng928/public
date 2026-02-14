# 文章_PHP教程_PHP5函数preg_match正则表达式匹配_GF_2022-10-09

PHP (PHP: Hypertext Preprocessor) 即 "超文本预处理器", 是在服务器端执行的脚本语言, 尤其适用于Web开发并可嵌入HTML中。

PHP 语法学习了 C语言, 吸纳 Java 和 Perl 多个语言的特色发展出自己的特色语法, 并根据它们的长项持续改进提升自己, 例如 Java 的面向对象编程, 该语言当初创建的主要目标是让开发人员快速编写出优质的 Web 网站。

PHP 同时支持面向对象和面向过程的开发, 使用上非常灵活。

## 函数 preg_match() 介绍

**定义和用法**:

preg_match 函数用于执行一个正则表达式匹配。

**语法**:

int preg_match ( string $pattern , string $subject [, array &$matches [, int $flags = 0 [, int $offset = 0 ]]] )

搜索 subject 与 pattern 给定的正则表达式的一个匹配。

**参数说明**：

```txt
* $pattern: 要搜索的模式, 字符串形式。

* $subject: 输入字符串。

* $matches: 如果提供了参数 matches, 它将被填充为搜索结果。$matches[0] 将包含完整模式匹配到的文本,  $matches[1] 将包含第一个捕获子组匹配到的文本, 以此类推。

* $flags：flags 可以被设置为以下标记值：

  PREG_OFFSET_CAPTURE: 如果传递了这个标记, 对于每一个出现的匹配返回时会附加字符串偏移量 (相对于目标字符串的)。

  注意：这会改变填充到 matches 参数的数组, 使其每个元素成为一个由 "第 0 个元素是匹配到的字符串", "第 1 个元素是该匹配字符串" 在目标字符串 subject 中的偏移量。

* offset: 通常, 搜索从目标字符串的开始位置开始。可选参数 offset 用于 "指定从目标字符串的某个未知开始搜索 (单位是字节)"。
```

**返回值**:

返回 pattern 的匹配次数。它的值将是 0 次 (不匹配) 或 1 次, 因为 preg_match() 在第一次匹配后 将会停止搜索。preg_match_all() 不同于此, 它会一直搜索subject 直到到达结尾。如果发生错误 preg_match() 返回 FALSE。

## 函数 preg_match() 示例

* 查找文本字符串 "php"。

**示例代码**:

```php
<?php

// 模式分隔符后的 "i" 标记这是一个大小写不敏感的搜索。

if (preg_match("/php/i", "PHP is the web scripting language of choice.")) {
    echo "查找到匹配的字符串 php。";
} else {
    echo "未发现匹配的字符串 php。";
}

?>
```

**输出**:

```txt
查找到匹配的字符串 php。
```

* 查找单词 "web"。

**示例代码**:

```php
<?php

/*
 * 模式中的 \b 标记一个单词边界, 所以只有独立的单词"web"会被匹配, 而不会匹配。
 * 单词的部分内容比如"webbing" 或 "cobweb"。
 */

if (preg_match("/\bweb\b/i", "PHP is the web scripting language of choice.")) {
    echo "查找到匹配的字符串。\n";
} else {
    echo "未发现匹配的字符串。\n";
}
 
if (preg_match("/\bweb\b/i", "PHP is the website scripting language of choice.")) {
    echo "查找到匹配的字符串。\n";
} else {
    echo "未发现匹配的字符串。\n";
}

?>
```

**输出**:

```txt
查找到匹配的字符串。
未发现匹配的字符串。
```

* 获取 URL 中的域名。

**示例代码**:

```php
<?php

// 从 URL 中获取主机名称。
preg_match('@^(?:http://)?([^/]+)@i', "http://www.php.net/index.php", $matches);

$host = $matches[1];
 
// 获取主机名称的后面两部分。
preg_match('/[^.]+\.[^.]+$/', $host, $matches);

echo "domain name is: {$matches[0]}\n";

?>
```

**输出**:

```txt
domain name is: php.net
```

* 使用命名子组。

**示例代码**:

```php
<?php
 
$str = 'foobar: 2008';
 
preg_match('/(?P<name>\w+): (?P<digit>\d+)/', $str, $matches);
 
// 下面例子在 PHP 5.2.2 (PCRE 7.0) 或更新版本下工作, 然而, 为了后向兼容, 上面的方式是推荐写法。
// preg_match('/(?<name>\w+): (?<digit>\d+)/', $str, $matches);
 
print_r($matches);
 
?>
```

**输出**:

```txt
Array
(
    [0] => foobar: 2008
    [name] => foobar
    [1] => foobar
    [digit] => 2008
    [2] => 2008
)
```

## 总结

以上就是关于 PHP教程 PHP5函数preg_match正则表达式匹配 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
