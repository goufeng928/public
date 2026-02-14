# 文章_PHP实例_PHP5使用mysql_connect函数的增删改查操作_GF_2022-10-09

有时候会下载到非常老版本的 PHP 源码，在新版 PHP 中，连接数据库就会出错。因此不得不记录不同版本 PHP 连接数据库的方式，用以熟悉老版本 PHP 连接数据库的操作步骤，便于替换相应代码来使较老的 PHP 源码能够正常连接数据库，并进行一些数据库操作。PHP5.6.40 及以前版本用 mysql_connect() 函数，这个函数在 PHP5.6.40 会发出警告信息，告知即将弃用。

## 实例介绍

* 这个 mysql_connect() 函数内包含了 "增、删、查、改、创建数据库、创建数据表" 几类操作。

* 函数 mysql_connect() 用于 PHP 3, PHP 4 兼容 PHP 5+ 并且在 PHP 7.0.0 中完全被移除, 因为它可能会导致性能问题和死锁。

* PHP 5.6.40 及以上版本应使用 mysqli 或者 pdo 扩展, 用这两个扩展连接数据库比之前的 mysql_connect() 更安全。

## 实例代码

```php
<?php

/*
 * Create By GF 2022-10-09
 *
 * 在 PHP 环境下以 mysql_connect 方式连接数据库。
 * mysql_connect() 用于 PHP 3, PHP 4 兼容 PHP 5+。
 */

header("Content-Type: text/html;charset=utf-8");

//禁止以下错误输出 : 
//Deprecated: mysql_connect(): The mysql extension is deprecated and will be removed in the future.
error_reporting(0);

class database {
    
    public $host = '127.0.0.1';
    public $database = 'xxxxxx';
    public $username = 'xxxxxx';
    public $password = 'xxxxxx';

    public function connect() {
        
        $host = $this->host;
        $username = $this->username;
        $password = $this->password;

        //创建mysql_connect数据库连接。
        $conn = mysql_connect($host.":3306", $username, $password);

        if (!$conn) {
            
            //显示出错误信息。
            die("Database Connect Failed : ".mysql_error()."<br />");
            
        }else {
            
            echo "Database Connect Successful<br />";
            
            return $conn;
            
        }
        
    }
    
    public function create_database() {
        
        $conn = $this->connect();
        
        $sql = "CREATE DATABASE mydbdemo";
        
        //执行创建数据库语句并判断创建数据库是否成功。
        if (mysql_query($sql, $conn)) {
            
            //成功后的提示。
	        echo "Create Database Successful<br />";
	        
        }else {
            
            //失败后的出错提示。
            echo "Create Database Failed : ".mysql_error()."<br />";
            
        }
        
        mysql_close($conn);

    }
    
    public function create_table() {
        
        $conn = $this->connect();
        
        $database = $this->database;
        
        //选择需要使用的数据库。
        mysql_select_db($database, $conn);
        
        $sql = "create table fruit (name  varchar(15), 
                                     color varchar(15),
                                     price float)";
        
        //执行创建数据表语句并判断创建数据表是否成功。
        //前面已经选择过数据库，可以直接使用mysql_query($sql)执行语句。
        if (mysql_query($sql)) {
            
            //成功后的提示。
	        echo "Create Table Successful<br />";
	        
        }else {
            
            //失败后的出错提示。
            echo "Create Table Failed : ".mysql_error()."<br />";
            
        }
        
        mysql_close($conn);

    }
    
    public function insert() {
        
        $conn = $this->connect();
        
        $database = $this->database;
        
        //选择需要使用的数据库。
        mysql_select_db($database, $conn);
        
        $sql = "INSERT INTO 测试_工商银行_20101231_20201231 (日期, 名称, 代码, 开盘价) 
                                                     values ('2022-10-07', '中国银行', '601399', 30)";
        
        //执行插入语句并判断插入是否成功。
        if (mysql_query($sql, $conn)) {
            
            //成功后的提示。
	        echo "Database Insert Successful<br />";
	        
        }else {
            
            //失败后的出错提示。
            echo "Database Insert Failed : ".mysql_error()."<br />";
            
        }
        
        mysql_close($conn);

    }
    
    public function delete() {
        
        $conn = $this->connect();
        
        $database = $this->database;
        
        //选择需要使用的数据库。
        mysql_select_db($database, $conn);
        
        $sql = "DELETE FROM 测试_工商银行_20101231_20201231 WHERE 开盘价='12';";
        
        //执行删除语句并判断删除是否成功。
        if (mysql_query($sql, $conn)) {
            
            //成功后的提示。
	        echo "Database Delete Successful<br />";
	        
        }else {
            
            //失败后的出错提示。
            echo "Database Delete Failed : ".mysql_error()."<br />";
            
        }
        
        mysql_close($conn);

    }
    
    public function select() {
        
        $conn = $this->connect();
        
        $database = $this->database;

        //选择需要使用的数据库。
        mysql_select_db($database, $conn);

        $sql = "SELECT * FROM 测试_工商银行_20101231_20201231 LIMIT 0,10";

        $result = mysql_query($sql);
        
        //构造表头
        echo "<table border='1'>
                  <tr>
                      <th>日期</th>
                      <th>名称</th>
                      <th>代码</th>
                      <th>开盘价</th>
                  </tr>";

        while ($row = mysql_fetch_array($result)) {

            echo "<tr>";
            echo     "<td>".$row['日期']."</td>";
            echo     "<td>".$row['名称']."</td>";
            echo     "<td>".$row['代码']."</td>";
            echo     "<td>".$row['开盘价']."</td>";
            echo "</tr>";
        
        }
        
        mysql_close($conn);
        
    }

    public function update(){

        $conn = $this->connect();
        
        $database = $this->database;
        
        //选择需要使用的数据库。
        mysql_select_db($database, $conn);
        
        $sql = "UPDATE 测试_工商银行_20101231_20201231 SET 名称='建设银行' WHERE 开盘价='30';";
        
        //执行更新语句并判断更新是否成功。
        //前面已经选择过数据库，可以直接使用mysql_query($sql)执行语句。
        if (mysql_query($sql)) {
            
            //成功后的提示。
	        echo "Database Update Successful<br />";
	        
        }else {
            
            //失败后的出错提示。
            echo "Database Update Failed : ".mysql_error()."<br />";
            
        }
        
        mysql_close($conn);

    }
}

$classtest = new database();
//$classtest->connect();
//$classtest->create_database();
//$classtest->create_table();
//$classtest->insert();
//$classtest->delete();
//$classtest->update();
$classtest->select();

?>
```

## 使用说明

**代码末尾的实例化调用**：

$classtest->connect(); // 连接数据库。

$classtest->create_database(); // 创建数据库。

$classtest->create_table(); // 创建数据表。

$classtest->insert(); // 插入操作。

$classtest->delete(); // 删除操作。

$classtest->update(); // 更新操作。

$classtest->select(); // 查询操作。

取消相应的注释可以逐一测试其功能，并了解函数操作过程。

## 总结

以上就是关于 PHP实例 PHP5使用mysql_connect函数的增删改查操作 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
