# 文章_Unix运维_CMake教程_CMake中的include指令和.cmake文件_GF_2024-03-13

CMake 的构建系统是通过一个高度抽象的目标集合进行组织的。集合中的每个目标要么对应一个可执行文件或库, 要么包含了自定义的命令行。构建系统根据目标之间的依赖关系确定目标的构建顺序和生成规则。

## CMakeLists.txt 文件

而 CMakeLists.txt 是 CMake 配置项目的构建系统, 配合使用 cmake 命令行工具生成构建系统并执行编译、测试, 相比于手动编写构建系统 (如 Makefile) 要高效许多。

## .cmake 文件

在 /usr/local/share/cmake-3.xx/Modules 中会看到 大量 .cmake 文件。特别是 find_package 指令会用到的 FindX11.camke 等文件, 其实 .cmake 文件是一个模块文件, 可以被 include 到 CMakeLists.txt 中。

## 以 freeGLUT 3.4.0 的 CMakeLists.txt 文件为例

```txt
INCLUDE(CheckIncludeFiles)
IF(UNIX AND NOT(ANDROID OR BLACKBERRY OR FREEGLUT_WAYLAND))
    FIND_PACKAGE(X11 REQUIRED)
    INCLUDE_DIRECTORIES(${X11_X11_INCLUDE_PATH})
    LIST(APPEND LIBS ${X11_X11_LIB})
    IF(X11_Xrandr_FOUND)
        SET(HAVE_X11_EXTENSIONS_XRANDR_H TRUE)
        LIST(APPEND LIBS ${X11_Xrandr_LIB})
    ENDIF()
    IF(X11_xf86vmode_FOUND)
        SET(HAVE_X11_EXTENSIONS_XF86VMODE_H TRUE)
        LIST(APPEND LIBS ${X11_Xxf86vm_LIB})
    ENDIF()
    IF(X11_Xinput_FOUND)
        # Needed for multi-touch:
        CHECK_INCLUDE_FILES("${X11_Xinput_INCLUDE_PATH}/X11/extensions/XInput2.h" HAVE_X11_EXTENSIONS_XINPUT2_H)
        LIST(APPEND LIBS ${X11_Xinput_LIB})
    ELSE()
        MESSAGE(FATAL_ERROR "Missing X11's XInput2.h (X11/extensions/XInput2.h)")
    ENDIF()
ENDIF()

# FreeBSD and NetBSD joystick code uses libusbhid
IF(CMAKE_SYSTEM_NAME STREQUAL FreeBSD OR CMAKE_SYSTEM_NAME STREQUAL NetBSD)
    IF(HAVE_USBHID_H)
        LIST(APPEND LIBS "-lusbhid")
    ENDIF()
ENDIF()
```

## 指令解释: INCLUDE(CheckIncludeFiles)

其中的 **INCLUDE(CheckIncludeFiles)** 意为引入一个模块, 这个模块名为 **CheckIncludeFiles**, 包含了用于==检查引入文件==的一些函数。

## 指令解释: FIND_PACKAGE(X11 REQUIRED)

其中的 **FIND_PACKAGE(X11 REQUIRED)** 意为查找软件包, 而 **X11 REQUIRED** 代表查找 X11 的相关信息被请求了, 将会调用 /usr/local/share/cmake-3.xx/Modules 目录下的 **FindX11.camke** 模块, 这样就能够使用 **FindX11.camke** 模块中定义的查找路径 (包括可能存在的安装目录 .h 头文件路径和 .so 库文件路径)。

## 总结

以上就是关于 Unix运维 CMake教程 CMake中的include指令和.cmake文件 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
