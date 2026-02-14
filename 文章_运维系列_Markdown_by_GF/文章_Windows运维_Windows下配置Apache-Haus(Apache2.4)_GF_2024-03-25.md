# 文章_Windows运维_Windows下配置Apache-Haus(Apache2.4)_GF_2024-03-25

Apache Haus 是一个由网站管理员, 开发人员和爱好者组成的社区, 他们更喜欢使用 Apache Web 服务器而不是 IIS。

无论是出于商业还是娱乐目的, Apache 在 Windows 上的使用正在稳步增加, 我们希望通过为人们提供一个可以获得帮助并分享他们在 Windows 上使用 Apache 的经验的地方, 看到这一趋势继续下去。

我们的论坛为人们提供了一个会面, 提问或分享有关 Apache 安装和操作知识的场所, 并帮助他们了解最新技术。

请注意, Apache Haus 不隶属于 Apache 软件基金会, 不受其认可。Apache HTTP Server, Apache 和 Apache 羽毛徽标是 Apache 软件基金会的商标。

The Apache Haus is a community of webmasters, developers and hobbyists who prefer using the Apache Web Server over IIS.

Whether for business or pleasure, the use of Apache on Windows is steadily gaining and we hope to see the trend continue by offering people a place to come where they can get help and share their experiences using Apache on Windows.

Our forums provide the place for people to meet and ask questions or share their knowledge concerning the installation and operation of Apache, as well as helping them keep up to date with the latest technologies.

Please note that the Apache Haus is not affiliated with, or endorsed by, the Apache Software Foundation. The Apache HTTP Server, Apache, and the Apache feather logo are trademarks of The Apache Software Foundation.

Server powered by: Finetworks Ay

* 由以上  Apache Haus 的申明可知, Apache HTTP Server 官方不提供二进制  (可执行) 的发行版, 所以我们只能选择一些贡献者编译完成的版本, 这里我们当然选择了 Apache Haus。

* 在 Apache Haus 下载页面 (https://www.apachehaus.com/) 下载 Apache 2.4 Server Binaries (Windows 需要安装对应的 VC 环境)。

## Apache Haus 配置 1 - httpd.conf

**设置 Apache 目录, 即 ServerRoot 选项, 将其改成你的 Apache 程序的文件夹**。

如果存在 Define SRVROOT "[ApachePath]", 则修改此处的 [ApachePath]。

如果只有 ServerRoot "[ApachePath]", 则修改此处的 [ApachePath]。

如果既存在 Define SRVROOT, 也存在 ServerRoot "${SRVROOT}", 则只需要修改 Define SRVROOT "[ApachePath]" 中的 [ApachePath]。

当然也可以直接修改 ServerRoot "[ApachePath]" 中的 [ApachePath], 只不过灵活性要差一些。

修改示例:

```txt
Define SRVROOT "D:\Program\Apache24"
ServerRoot "${SRVROOT}"
```

**设置 Apache 服务监听的端口, 即 Listen 选项, 一般不修改, 使用默认 80, 在开启服务器前请保证 80 端口未被占用**。

修改示例:

```txt
Listen 80
```

**设置 Apache 服务根目录, 即 DocumentRoot 选项, 是存放 .html 文件的目录, 用户输入 IP地址 + 端口号 (如: 12.34.56.78:80) 能够访问到的目录**。

请保证 DocumentRoot 所设置的目录存在, 否则服务器无法正常启动。

同时也需要修改随后的 <Directory>...<Directory/> XML标签中的路径属性, 保证其与服务器根目录相同。

修改示例:

```txt
DocumentRoot "D:\Program\Apache24\htdocs"
<Directory "D:\Program\Apache24\htdocs">
    #
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"
    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks

    #
    # AllowOverride controls what directives may be placed in .htaccess files.
    # It can be "All", "None", or any combination of the keywords:
    #   Options FileInfo AuthConfig Limit
    #
    AllowOverride None

    #
    # Controls who can get stuff from this server.
    #
    Require all granted
</Directory>
```

**设置 Apache 的 cgi-bin 路径, 即 ScriptAlias /cgi-bin/ 选项, 通常将其设置为 Apache 目录下的 cgi-bin 文件夹**。

需同时要找到随后的 <Directory>...<Directory/> XML标签, 设置脚本目录, 需要将其设置为和前面的 ScriptAlias /cgi-bin/ 所指定的目录相同。

修改示例:

```txt
<IfModule alias_module>
    #
    # Redirect: Allows you to tell clients about documents that used to 
    # exist in your server's namespace, but do not anymore. The client 
    # will make a new request for the document at its new location.
    # Example:
    # Redirect permanent /foo http://www.example.com/bar

    #
    # Alias: Maps web paths into filesystem paths and is used to
    # access content that does not live under the DocumentRoot.
    # Example:
    # Alias /webpath /full/filesystem/path
    #
    # If you include a trailing / on /webpath then the server will
    # require it to be present in the URL.  You will also likely
    # need to provide a <Directory> section to allow access to
    # the filesystem path.

    #
    # ScriptAlias: This controls which directories contain server scripts. 
    # ScriptAliases are essentially the same as Aliases, except that
    # documents in the target directory are treated as applications and
    # run by the server when requested rather than as documents sent to the
    # client.  The same rules about trailing "/" apply to ScriptAlias
    # directives as to Alias.
    #
    ScriptAlias /cgi-bin/ "D:\Program\Apache24\cgi-bin\"

</IfModule>

<IfModule cgid_module>
    #
    # ScriptSock: On threaded servers, designate the path to the UNIX
    # socket used to communicate with the CGI daemon of mod_cgid.
    #
    #Scriptsock logs/cgisock
</IfModule>

#
# "${SRVROOT}/cgi-bin" should be changed to whatever your ScriptAliased
# CGI directory exists, if you have that configured.
#
<Directory "D:\Program\Apache24\cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
```

## Apache Haus 配置 2 - 尝试启动 Apache 服务

**配置环境变量**: 右键点击 "计算机" -> 属性 -> 高级系统设置 -> 环境变量 -> 编辑 Path -> 新建 -> 添加 "D:\Program\Apache24\bin" 路径

**测试环境变量**: Win 键 + r 打开 "运行" -> 输入 cmd 打开 Windows 终端 -> 输入 httpd -v 显示 Apache 版本号

(如果之前安装并使用过 Nginx, 需要先清除浏览器缓存)

**安装 Apache 服务**: 以管理员的身份再次打开 Windows 终端, 输入 httpd -k install 安装 Apache 服务 (未安装 Apache 服务可能无法启动 Apache 服务)。

**启动 Apache 服务 (方式 1)**: 打开 Windows 终端, 输入 httpd -k start 启动 Apache 服务。

**启动 Apache 服务 (方式 2)**: 打开 D:\Program\Apache24\bin 目录下的 ApacheMonitor.exe, 点击右边的 start 启动 Apache 服务。

Windows 系统下 Apache 24.x 常见命令:

```cmd
httpd -k install      安装 Apache 服务
httpd -k uninstall    移除 Apache 服务

httpd -k start        启动 Apache 服务
httpd -k restart      重启 Apache 服务
httpd -k stop         关闭已安装的 Apache 服务

httpd -v              查看 Apache 版本
httpd -t              查看 Apache 配置文件状态
```

**错误处理**: (OS 10048)通常每个套接字地址(协议/网络地址/端口)只允许使用一次。 : AH00072: make_sock: could not bind to address [::]:443

意思就是 443 端口号被占用了

修改 1: 将 D:\Program\Apache24\conf\extra 中 httpd-ahssl.conf 的 Listen 443 https 修改为 Listen 442 https 或 Listen 444 https

修改 2: 将 D:\Program\Apache24\conf\extra 中 httpd-ssl.conf 的 Listen 443 修改为 Listen 442 或 Listen 444

**错误处理**: Windows不能在本地计算机启动Apache2.2。有关更多信息，查阅系统日志文件。如果这是非Microsoft服务，请与厂商联系，并参考特定服务器错误代码1。

右键点击 "计算机" -> 事件查看器 -> Windows 日志 -> 应用程序 -> 查看对应时间出错的应用其 "常规" 或 "详细信息" 中的信息

```txt
错误日志 1:

The Apache service nnamed reported the following error:
>>> Syntax error on line 133 of C:/Users/xyb-C308/Downloads/httpd-2.2.31-x86-r3/Apache22/conf/extra/httpd-ahssl.conf:.

错误日志 2:

The Apache service nnamed reported the following error:
>>> SSLCertificateFile 'C:/Apache22/conf/ssl/server.crt' dose not exist or is empty.
```

这是由于 SSL 配置不正确所产生的, 以下是解决办法。

打开 D:\Program\Apache22\conf\extra\httpd-ahssl.conf 文件, 配置 VirtualHost 选项。

注意: 可能不止一处名为 VirtualHost 的选项, 均需修改。

将其中的 SSLCertificateFile 改为 D:/Program/Apache22/conf/ssl/server.crt

将其中的 SSLCertificateKeyFile 改为 D:/Program/Apache22/conf/ssl/server.key

将其中的 DocumentRoot 改为你的服务器根目录。

```txt
##
## SSL Virtual Host Context
##

<VirtualHost _default_:443>
  SSLEngine on
  ServerName localhost:443
  SSLCertificateFile "D:/Program/Apache22/conf/ssl/server.crt"
  SSLCertificateKeyFile "D:/Program/Apache22/conf/ssl/server.key"
  DocumentRoot "D:/Program/Apache22/htdocs"
# DocumentRoot access handled globally in httpd.conf
	CustomLog "${SRVROOT}/logs/ssl_request.log" \
          "%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x \"%r\" %b"
	<Directory "${SRVROOT}/htdocs">
		Options Indexes Includes FollowSymLinks
		AllowOverride AuthConfig Limit FileInfo
    Require all granted
	</Directory>
</virtualhost>
```

将其中的 CustomLog 改为 D:/Program/Apache22/logs/ssl_request.log, 这个不改的话也会错, 通常会出现如下错误:

```txt
错误日志:
Apache2.2 服务由于下列服务特定错误而终止:
函数不正确。
```

这样, 错误就算处理完了, 如果还有问题, 可能还需配置 D:\Program\Apache22\conf\extra\httpd-ssl.conf, 配置方法和配置 httpd-ahssl.conf 的 VirtualHost 的相似。

## Apache Haus 配置 3 - 启动 Apache 服务

**配置 Apache 服务 -> 安装 Apache 服务 -> 启动 Apache 服务**

**整个流程下来没有错误, 或处理完所有错误后, 以后都按以下方式启动 Apache 服务即可**。

启动 Apache 服务 (方式 1): 打开 Windows 终端, 输入 httpd -k start 启动 Apache 服务。

启动 Apache 服务 (方式 2): 打开 D:\Program\Apache24\bin 目录下的 ApacheMonitor.exe, 点击右边的 start 启动 Apache 服务。

**也可以显示启动过程中的日志, 便于分析错误**。

使用 httpd -w -n "Apache2" -k start 命令启动服务器

## Apache Haus 配置 4 - 开机启动 Apache 服务

**右键点击 "计算机" -> 管理 -> 服务和应用程序 -> 服务 -> 找到 Apache2.4 -> 右键点击 "Apache2.4" -> 属性 -> 修改启动类型**

**启动类型**说明:

自动: 开机自动启动

手动: 每次手动启动

## Apache Haus 可选配置 - 配置 PHP-7.x.x 支持

**下载 PHP-7.x.x。注意: 需要下载 "线程安全(THREAD SAFE)版", 如果是 "非线程安全(NOT THREAD SAFE)版", 则不包含 "php7apache2_4.dll" 库文件**。

**修改 Apache Haus 的 httpd.conf 文件, 加载 PHP-7.x.x 的支持, 在 httpd.conf 文件末尾添加如下内容**:

```txt
# Load PHP7 Module for PHP7 Support.
LoadModule php7_module D:\Program\PHP-7.4.28-TS-Win32-VC15-X64\php7apache2_4.dll

# 将 PHP 配置文件加载到 Apache 配置文件中, 使其共同生效。
PHPIniDir "D:\Program\PHP-7.4.28-TS-Win32-VC15-X64"
```

**修改 Apache Haus 的 httpd.conf 文件, 让 Apache 分配模块工作, 将含有 PHP 代码的 .php 文件分配给 PHP 模块处理, 在 httpd.conf 文件末尾添加如下内容**:

```txt
# 让 Apache 分配模块工作, 将含有 PHP 代码的 .php 文件分配给 PHP 模块处理。
AddType application/x-httpd-php .php
```

或者:

```txt
# 让 Apache 分配模块工作, 将含有 PHP 代码的 .php 文件分配给 PHP 模块处理。
<IfModule mod_php7.c>
    AddType application/x-httpd-php .php
</IfModule>
```

**修改 Apache Haus 的 httpd.conf 文件, 让 Apache 解析 index.php 主页索引文件**。

找到以下内容:

```txt
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>
```

将找到的 DirectoryIndex 参数末尾添加上 index.php 项目:

```txt
<IfModule dir_module>
    DirectoryIndex index.html index.php
</IfModule>
```

**重启 Apache 服务, 使 httpd.conf 配置生效**。

```cmd
httpd -k restart
```

## 总结

以上就是关于 Windows运维 Windows下配置Apache-Haus(Apache2.4) 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
