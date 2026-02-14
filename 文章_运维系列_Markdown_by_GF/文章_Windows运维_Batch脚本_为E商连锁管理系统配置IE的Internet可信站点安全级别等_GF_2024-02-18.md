# 文章_Windows运维_Batch脚本_为E商连锁管理系统快速配置IE的ActiveX控件和活动脚本以及Internet可信站点安全级别_GF_2024-02-18

E商是一款基于 SAAS 模式开发的连锁行业管理软件。

E商是一项基于互联网应用模式的进销存和连锁店管理服务，它集购、销、存、应收应付款和店铺销售和日常业务管理为一体，帮助企业处理日常的业务经营管理事项及成本、毛利核算，协调购销存业务流转过程，加强店铺的日常销售管理，节省成本，提高效率，进而提升企业的竞争力。

## 适用 IE (Internet Explorer) 版本

* IE 7

* IE 8

* IE 9

* IE 10

* Microsoft Edge 121 (IE模式)

## 完整脚本

```bat
@echo off
echo                       ★ E商连锁管理系统一键启用Internet安全脚本 ★

echo 运行过程中，若遇杀毒软件拦截，请选择允许脚本执行......
ping 127.0.0.1 -n 8 >nul 2>nul

taskkill /f /im iexplore.exe


echo 正在启用IE的 ActiveX控件，请稍候......
ping 127.0.0.1 -n 2 >nul 2>nul 

::set bl=0
:setreg
::if "%bl%"=="5" goto ex

set regpath=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\2

::cls

echo 本脚本可快速启用IE的 ActiveX控件、活动脚本
echo 正在进行Internet可信站点的安全级别设置...
ping 127.0.0.1 -n 2 >nul 2>nul

:启用“activeX控件”“活动脚本”

@reg add "%regpath%" /v "2201" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1405" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1201" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1004" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1001" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1208" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1200" /d "0" /t REG_DWORD /f

@reg add "%regpath%" /v "1609" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1406" /d "0" /t REG_DWORD /f
@reg add "%regpath%" /v "1A00" /d "0" /t REG_DWORD /f

::set /a bl=2
::set /a bl=%bl%+1
::goto setreg
:ex
::cls

echo 正在添加受信任站点与关闭弹窗功能...
ping 127.0.0.1 -n 3 >nul 2>nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges" /v @ /t REG_SZ /d "" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range1" /v "http" /t REG_DWORD  /d 00000002 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range1" /v ":Range" /t REG_SZ /d "125.71.212.39" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range2" /v "http" /t REG_DWORD  /d 00000002 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range2" /v ":Range" /t REG_SZ /d "221.237.155.254" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range3" /v "http" /t REG_DWORD  /d 00000002 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges\Range3" /v ":Range" /t REG_SZ /d "182.148.107.23" /f

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\itsystem.com.cn\eb2006" /v http /t REG_DWORD /d 0x00000002 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\xun-jie.com\oa" /v http /t REG_DWORD /d 0x00000002 /f
reg add "HKCU\Software\Microsoft\Internet Explorer\New Windows" /v "PopupMgr" /t REG_SZ /d "no" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\2" /v "2201" /t REG_DWORD  /d 00000000 /f

echo 正在添加兼容性视图...
ping 127.0.0.1 -n 3 >nul 2>nul

set view=411f00005308adba05000000f400000001000000050000000c000000b42ae9877925d401010000000d003100320035002e00370031002e003200310032002e00330039000c0000005b05388a7925d401010000000f003200320031002e003200330037002e003100350035002e003200350034000c0000009b76858e7925d401010000000e003100380032002e003100340038002e003100300037002e00320033000c000000b8675265cfaed401010000000f0069007400730079007300740065006d002e0063006f006d002e0063006e000c000000fd3f204faecdd401010000000e0078006a00670072006f00750070002e006e00650074002e0063006e00



reg add "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\BrowserEmulation\ClearableListData" /v UserFilter /t REG_BINARY /f /d %view%


echo 设置完毕，请打开IE测试一下是否正常，若不正常，建议关闭所有IE浏览器及杀毒软件再次运行本脚本。
echo 本脚本稍后将自动关闭,感谢使用......
ping 127.0.0.1 -n 8 >nul 2>nul
exit
```

## 总结

以上就是关于 Windows运维 Batch脚本 为E商连锁管理系统快速配置IE的ActiveX控件和活动脚本以及Internet可信站点安全级别 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
