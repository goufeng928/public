# 文章_Unix运维_Unix下配置PHP-7.x.x和Apache-2.x.x_GF_2023-03-20

Apache HTTP Server (简称 Apache, 音译为: 阿帕奇) 是 Apache 软件基金会的一个开放源码的网页服务器。

Apache 源于 NCSAhttpd 服务器, 经过多次修改, 成为世界上最流行的 Web 服务器软件之一。

Apache 可以运行在几乎所有广泛使用的计算机平台上, 由于其跨平台和安全性被广泛使用。它快速, 可靠并且可通过简单的 API 扩充, 将 Perl / Python 等解释器编译到服务器中。

PHP (PHP: Hypertext Preprocessor) 即 "超文本预处理器", 是在服务器端执行的脚本语言, 尤其适用于 Web 开发并可嵌入 HTML 中。

PHP 语法学习了 C 语言, 吸纳 Java 和 Perl 多个语言的特色发展出自己的特色语法, 并根据它们的长项持续改进提升自己, 例如 Java 的面向对象编程, 该语言当初创建的主要目标是让开发人员快速编写出优质的 Web 网站。

PHP 同时支持面向对象和面向过程的开发, 使用上非常灵活。

## Unix 下配置 Apache2 对 PHP7 的解析

1。编辑 /etc/httpd/conf/httpd.conf, 寻找以下代码, 若没有则加入到 LoadModule 处。

```txt
LoadModule php7_module modules/libphp7.so
```

2。在 httpd.conf 中的末尾加入如下代码以支持 Apache2 对 PHP7 的解析。

```txt
<IfModule mod_php7.c>
    AddType application/x-httpd-php .php
</IfModule>
```

3。在 httpd.conf 中找到如下代码, 在 index.html 末尾加上 index.php。

* 编辑前:

```txt
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>
```

* 编辑后:

```txt
<IfModule dir_module>
    DirectoryIndex index.html index.php
</IfModule>
```

4。重启 Apache2 服务。

```shell
/usr/local/bin/apachectl restart
```

在 /var/www 下放入 .php 文件, 写入:

```php
<meta charset=utf8>
<?php phpinfo(); ?>
```

通过 Web 页面访问, 若能执行 PHP 代码而不是直接输出 PHP 代码, 说明配置成功。

## Unix 下 PHP-7.x.x 的 php-fpm 配置详解

本例中, PHP 配置文件 php-fpm.conf 的路径为 "/opt/php-7.4.28/etc/php-fpm.conf"。

```txt
# pid 设置, 默认在安装目录中的 var/run/php-fpm.pid, 建议开启。
pid = run/php-fpm.pid

# 错误日志, 默认在安装目录中的 var/log/php-fpm.log
error_log = log/php-fpm.log

# 错误级别, 可用级别有: alert(必须立即处理), error(错误情况), warning(警告情况), notice(一般重要信息), debug(调试信息)。默认为: notice。
log_level = notice

# 表示在 emergency_restart_interval 所设值内出现 SIGSEGV 或者 SIGBUS 错误的 php-cgi 进程数如果超过 emergency_restart_threshold 个, php-fpm 就会优雅重启。这两个选项一般保持其默认值。
emergency_restart_threshold = 60
emergency_restart_interval = 60s

# 设置子进程接受主进程复用信号的超时时间, 可用单位: s(秒), m(分), h(小时), d(天)。默认单位: s(秒)。默认值: 0。
process_control_timeout = 0

# 后台执行 fpm, 默认值为 yes, 如果为了调试可以改为 no。在 FPM 中, 可以使用不同的设置来运行多个进程池。这些设置可以针对每个进程池单独设置。
daemonize = yes

# fpm 监听端口, 即 Nginx 中 PHP 处理的地址, 一般默认值即可。可用格式为: "ip:port", "port", "/path/to/unix/socket"。每个进程池都需要设置。
listen = 127.0.0.1:9000

# backlog 数, -1 表示无限制, 由操作系统决定, 此行注释掉就行。
listen.backlog = -1

# 允许访问 FastCGI 进程的 IP, 设置 any 为不限制 IP, 如果要设置其他主机的 Nginx 也能访问这台 FPM 进程, listen 处要设置成本地可被访问的 IP。默认值是 any。每个地址是用逗号分隔。如果没有设置或者为空, 则允许任何服务器请求连接。
listen.allowed_clients = 127.0.0.1

# Unix Socket 设置选项, 如果使用 TCP 方式访问, 这里注释即可。
listen.owner = www
listen.group = www
listen.mode = 0666

# 启动进程的用户和用户组。
user = www
group = www

# pm 选项决定如何控制子进程, 选项有 static 和 dynamic。如果选择 static, 则由 pm.max_children 指定固定的子进程数。如果选择 dynamic, 则由下面参数决定:
pm = dynamic         # -> 对于专用服务器, pm 可以设置为 static。
pm.max_children      # -> 子进程最大数。
pm.start_servers     # -> 启动时的进程数。
pm.min_spare_servers # -> 保证空闲进程数最小值, 如果空闲进程小于此值, 则创建新的子进程。
pm.max_spare_servers # -> 保证空闲进程数最大值, 如果空闲进程大于此值, 此进行清理。

# 设置每个子进程重生之前服务的请求数, 对于可能存在内存泄漏的第三方模块来说是非常有用的。如果设置为 "0" 则一直接受请求, 等同于 PHP_FCGI_MAX_REQUESTS 环境变量。默认值: "0"。
pm.max_requests = 1000

# FPM 状态页面的网址, 如果没有设置, 则无法访问状态页面。默认值: none。munin 监控会使用到。
pm.status_path = /status

# FPM 监控页面的 ping 网址。如果没有设置, 则无法访问 ping 页面。该页面用于外部检测 FPM 是否存活并且可以响应请求。请注意必须以斜线开头 "/"。
ping.path = /ping

# 用于定义 ping 请求的返回相应。返回为 HTTP 200 的 text/plain 格式文本。默认值: "pong"。
ping.response = pong

# 设置单个请求的超时中止时间。该选项可能会对 php.ini 设置中的 "max_execution_time" 因为某些特殊原因没有中止运行的脚本有用。设置为 "0" 表示 "Off"。当经常出现 502 错误时可以尝试更改此选项。
request_terminate_timeout = 0

# 当一个请求该设置的超时时间后, 就会将对应的 PHP 调用堆栈信息完整写入到慢日志中。设置为 "0" 表示 "Off"。
request_slowlog_timeout = 10s

# 慢请求的记录日志, 配合 request_slowlog_timeout 使用。
slowlog = log/$pool.log.slow

# 设置文件打开描述符的 rlimit 限制。默认值: 系统定义值默认可打开句柄是 1024, 可使用 ulimit -n 查看, ulimit -n 2048 修改。
rlimit_files = 1024

# 设置核心 rlimit 最大限制值。可用值: "unlimited", 0 或者正整数。默认值: 系统定义值。
rlimit_core = 0

# 启动时的 chroot 目录。所定义的目录需要是绝对路径。如果没有设置, 则 chroot 不被使用。
chroot =

# 设置启动目录, 启动时会自动 chdir 到该目录。所定义的目录需要是绝对路径。默认值: 当前目录, 或者 / 目录 (chroot 时)。
chdir =

# 重定向运行过程中的 stdout 和 stderr 到主要的错误日志文件中。如果没有设置, stdout 和 stderr 将会根据 FastCGI 的规则被重定向到 /dev/null。默认值: 空。
catch_workers_output = yes
```

## Unix 下 PHP-7.x.x 的 php-fpm 优化重要配置详解

在 fasgcgi 模式下, php 会启动多个 php-fpm 进程, 来接收 Nginx 发来的请求, 那是不是进程越多, 速度就越快呢? 这可不一定! 得根据我们的机器配置和业务量来决定。

我们先来看下, 设定进程的配置在哪里? 

```txt
# pm 可以设置成这样 3 种, 我们用的最多的是前 2 种。
pm = static | dynamic | ondemand

# pm 的 static 模式表示我们创建的 php-fpm 子进程数量是固定的, 那么就只有 pm.max_children = n 这个参数生效。你启动php-fpm的时候就会一起启动 (1 个主进程 + n 个子进程)。
pm = static

# pm 的 dynamic 模式表示启动进程是动态分配的, 随着请求量动态变化, 由 pm.max_children, pm.start_servers, pm.min_spare_servers, pm.max_spare_servers 这几个参数共同决定。
pm = dynamic
pm.max_children ＝ 50     # -> 最大可创建的子进程的数量。必须设置。这里表示最多只能 50 个子进程。
pm.start_servers = 20     # -> 随着 php-fpm 一起启动时创建的子进程数目。默认值: min_spare_servers + (max_spare_servers - min_spare_servers) / 2。这里表示, 一起启动会有 20 个子进程。
pm.min_spare_servers = 10 # -> 设置服务器空闲时最小 php-fpm 进程数量。必须设置。如果空闲的时候, 会检查如果少于 10 个, 就会启动几个来补上。
pm.max_spare_servers = 30 # -> 设置服务器空闲时最大 php-fpm 进程数量。必须设置。如果空闲时, 会检查进程数, 多于 30 个, 就会关闭几个, 保持 30 个的状态。
```

pm 中 static 和 dynamic 模式的选择:

动态适合小内存机器, 灵活分配进程, 省内存。

静态适用于大内存机器, 动态创建回收进程对服务器资源也是一种消耗。

如果你的内存很大, 有 8G - 20G, 按照一个 php-fpm 进程 20M 算, 100 个就 2G 内存了, 那就可以开启 static 模式。

如果你的内存很小, 比如才 256M, 那就要小心设置了, 因为你的机器里面的其他的进程也算需要占用内存的, 所以设置成 dynamic 是最好的。

比如: pm.max_chindren = 8, 占用内存 160M 左右, 而且可以随时变化, 对于一半访问量的网站足够了。

## Unix 下 PHP-7.x.x 的 php-fpm 慢日志查询

我们有时候会经常饱受 500, 502 问题困扰。当 Nginx 收到如上错误码时, 可以确定后端 php-fpm 解析 php 出了某种问题, 比如, 执行错误, 执行超时。

这个时候, 我们是可以开启慢日志功能的。

```txt
# 以下设置为: 当一个请求该设置的超时时间 10 秒后, 就会将对应的 PHP 调用堆栈信息完整写入到慢日志中。
#             php-fpm 慢日志会记录下进程号, 脚本名称, 具体哪个文件哪行代码的哪个函数执行时间过长。
slowlog = slowlog = log/$pool.log.slow
request_slowlog_timeout = 10s
```

慢日志示例:

```txt
21-Nov-2017 14:30:38] [pool www] pid 11877
script_filename = /u01/www/djwx//fyzb.php
[0xb70fb88c] file_get_contents() /u01/www/djwx//index.php:2
```

通过日志, 我们就可以知道第 2 行的 file_get_contents() 函数有点问题, 这样我们就能追踪问题了。

## 总结

以上就是关于 Unix运维 Unix下配置PHP-7.x.x和Apache-2.x.x 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
