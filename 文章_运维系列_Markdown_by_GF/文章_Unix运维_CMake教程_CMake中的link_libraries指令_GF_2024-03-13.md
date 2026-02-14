# 文章_Unix运维_CMake教程_CMake中的link_libraries指令_GF_2024-03-13

CMake 的构建系统是通过一个高度抽象的目标集合进行组织的。集合中的每个目标要么对应一个可执行文件或库, 要么包含了自定义的命令行。构建系统根据目标之间的依赖关系确定目标的构建顺序和生成规则。

## link_libraries 和 target_link_libraries 的区别

* **link_libraries**: 向总工程添加库目录的搜索路径

语法:

```txt
link_libraries([item1 [item2 [...]]]
               [[debug|optimized|general] <item>] ...)
```

* **target_link_libraries**: 子工程需要用到哪个 lib 库文件, 需要使用 target_link_libraries 指定。 (该 lib 库文件必须能在搜索路径中找到)

语法:

```txt
target_link_libraries(<target> 
                      <PRIVATE|PUBLIC|INTERFACE> <item>... 
                      [<PRIVATE|PUBLIC|INTERFACE> <item>...]...)
```

## link_libraries (引入库文件目录)

**link_libraries** 表示添加第三方 lib 库文件的搜索路径。若工程在编译的时候会需要用到某个第三方库的 lib 文件，此时就可以使用 **link_libraries** 来添加搜索路径。

(**link_libraries** 类似于 Linux 中配置完成后 make 时用到的 **LD_LIBRARY_PATH=/usr/local/lib** 环境变量)

## target_link_libraries (引入库文件到子工程)

**target_link_libraries** 表示添加第三方 lib 库文件到目标工程, 该 lib 库文件必须能在搜索路径中找到。

(**target_link_libraries** 类似于 Linux 中配置完成后 make 时用到的 **LIBS=-lfuse3** 环境变量)

## 以 FreeRDP 3.3.0 的 CMakeLists.txt 文件为例

```txt
cmake_minimum_required(VERSION 3.13)

if(POLICY CMP0091)
	cmake_policy(SET CMP0091 NEW)
endif()
project(FreeRDP
	LANGUAGES C
)

SET(CMAKE_INCLUDE_PATH /opt/icu-74.2/include /opt/sandbox-X11/include /opt/cups-2.4.7/include /opt/libusb-1.0.27/include)
SET(CMAKE_LIBRARY_PATH /opt/icu-74.2/lib /opt/sandbox-X11/lib /opt/cups-2.4.7/lib /opt/libusb-1.0.27/lib)
LINK_DIRECTORIES(/opt/icu-74.2/lib /opt/fuse-3.16.2/lib)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

add_custom_target(fuzzers
	COMMENT "Build fuzzers"
)

if(NOT DEFINED VENDOR)
	set(VENDOR "FreeRDP" CACHE STRING "FreeRDP package vendor")
endif()
```

在配置 FreeRDP 3.3.0 时, 需要用到 ICU, X11, Cups, libusb 的头文件, 故向 CMakeLists.txt 中添加了 **SET(CMAKE_INCLUDE_PATH /opt/icu-74.2/include /opt/sandbox-X11/include /opt/cups-2.4.7/include /opt/libusb-1.0.27/include)**

在配置 FreeRDP 3.3.0 时, 需要用到 ICU, X11, Cups, libusb 的库文件, 故向 CMakeLists.txt 中添加了 **SET(CMAKE_LIBRARY_PATH /opt/icu-74.2/lib /opt/sandbox-X11/lib /opt/cups-2.4.7/lib /opt/libusb-1.0.27/lib)**

在编译 FreeRDP 3.3.0 时, 需要用到 ICU, Fuse3 的库文件, 故向 CMakeLists.txt 中添加了 **LINK_DIRECTORIES(/opt/icu-74.2/lib /opt/fuse-3.16.2/lib)**

## 指令解释: SET(CMAKE_INCLUDE_PATH /opt/icu-74.2/include)

其中的 **SET(CMAKE_INCLUDE_PATH /opt/icu-74.2/include)** 意为设置 CMAKE_INCLUDE_PATH 变量的值为 /opt/icu-74.2/include, 使得配置 FreeRDP 3.3.0 时能够找到 ICU 的 include 头文件。

## 指令解释: SET(CMAKE_LIBRARY_PATH /opt/icu-74.2/lib)

其中的 **SET(CMAKE_LIBRARY_PATH /opt/icu-74.2/lib)** 意为设置 CMAKE_LIBRARY_PATH 变量的值为 /opt/icu-74.2/lib, 使得配置 FreeRDP 3.3.0 时能够找到 ICU 的 lib 库文件。

## 指令解释: LINK_DIRECTORIES(/opt/icu-74.2/lib)

其中的 **LINK_DIRECTORIES(/opt/icu-74.2/lib)** 意为将 /opt/icu-74.2/lib 目录包含进 FreeRDP 工程, 使得编译 FreeRDP 3.3.0 时能够找到 ICU 的 lib 库文件。

## 总结

以上就是关于 Unix运维 CMake教程 CMake中的link_libraries指令 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
