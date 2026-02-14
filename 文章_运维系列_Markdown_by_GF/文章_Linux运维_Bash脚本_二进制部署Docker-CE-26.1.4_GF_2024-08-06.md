# 文章_Linux运维_Bash脚本_二进制文件部署Docker-CE-26.1.4_GF_2024-08-06

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载源码包:

docker-26.1.4.tgz (Binary)

shadow-4.2.1.tar.xz (Source)

docker-rootless-extras-26.1.4.tgz (Binary)

buildx-v0.16.2.linux-amd64 (Binary)
  
* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。
  
* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-08-06 01:34

# --------------------------------------------------
# Install First:
# * None

# --------------------------------------------------
# Download Site:
# Docker-CE 二进制(Binary)可执行文件: https://mirrors.aliyun.com/docker-ce/linux/static/
# buildx 二进制(Binary)可执行文件: https://github.com/docker/buildx/releases

# --------------- Docker-CE - 26.1.4 ---------------
# Need File: docker-26.1.4.tgz (Binary)
# ------- Docker-CE - 26.1.4 Rootless Extras -------
# Need File: shadow-4.2.1.tar.xz (Source)
# Need File: docker-rootless-extras-26.1.4.tgz (Binary)
# --------------- Docker-CE - Plugins --------------
# Need File: buildx-v0.16.2.linux-amd64 (Binary)

# ##################################################
STORAGE=/home/goufeng

# ######################################## Docker-CE - 26.1.4 ########################################

# 二进制文件部署(Binary File Deploy) Docker-CE - 26.1.4
# --------------------------------------------------

DOCKER_CE_VERIFY='n'
DOCKER_CE_CREATE_GROUP=0
DOCKER_CE_UNZIPPED=0
DOCKER_CE_DEPLOYED=0

read -p "[Confirm] Binary File Deploy ( docker-ce-26.1.4 )? (y/n)>" DOCKER_CE_VERIFY

test "$DOCKER_CE_VERIFY" != "y" && exit 1

test ! -f "/usr/sbin/groupadd" && (echo "[Stopped] Command ( groupadd ) Cannot be Found." && exit 1)

GROUP_NAME=$(cat /etc/group | grep -o docker)

test -z "$GROUP_NAME" && (/usr/sbin/groupadd docker && /usr/sbin/usermod -aG docker $USER && DOCKER_CE_CREATE_GROUP=1)

test ! -f "/opt/sandbox-docker-ce/bin/docker" && (

    (tar -zxvf $STORAGE/docker-26.1.4.tgz -C $STORAGE && DOCKER_CE_UNZIPPED=1) &&

    (test ! -d "/opt/sandbox-docker-ce/bin" && mkdir -p /opt/sandbox-docker-ce/bin || echo "Continue......") &&

    (cp -v $STORAGE/docker/ctr                     /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/containerd              /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/containerd-shim-runc-v2 /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/docker                  /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/docker-init             /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/docker-proxy            /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/dockerd                 /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker/runc                    /opt/sandbox-docker-ce/bin/) &&
    
    (chmod +x /opt/sandbox-docker-ce/bin/ctr                    ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/containerd             ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/containerd-shim-runc-v2) &&
    (chmod +x /opt/sandbox-docker-ce/bin/docker                 ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/docker-init            ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/docker-proxy           ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/dockerd                ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/runc                   ) &&

    (cp -v /opt/sandbox-docker-ce/bin/ctr                     /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/containerd              /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/containerd-shim-runc-v2 /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/docker                  /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/docker-init             /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/docker-proxy            /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/dockerd                 /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/runc                    /usr/local/bin/) &&
    (DOCKER_CE_DEPLOYED=1) &&

    (cd $STORAGE && rm -rf $STORAGE/docker)
) || (

    echo "[Caution] Binary: ( /opt/sandbox-docker-ce/bin/docker ) Already Exists."
)

# ################################ Docker-CE - 26.1.4 Rootless Extras ################################

# 编译安装(Compile Install) Shadow - 4.2.1
# --------------------------------------------------

# Suggested Operation:
# ..................................................
# sed -i 's/groups$(EXEEXT) //' src/Makefile.in &&
# find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \; &&
#
# sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
#        -e 's@/var/spool/mail@/var/mail@' etc/login.defs &&
#
# sed -i 's/1000/999/' etc/useradd
# ..................................................
# * sed -i 's/groups$(EXEEXT) //' src/Makefile.in:
#   This sed is used to suppress the installation of the groups program as the version from the Coreutils package installed during LFS is preferred.
#   此 sed 用于抑制组程序的安装, 因为首选 LFS 期间安装的 Coreutils 包中的版本。
# ..................................................
# * find man -name Makefile.in -exec ... {} \;:
#   This command is used to suppress the installation of the groups man pages so the existing ones installed from the Coreutils package are not replaced.
#   此命令用于禁止安装组手册页, 这样就不会替换从 Coreutils 软件包安装的现有手册页。
# ..................................................
# * sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' -e 's@/var/spool/mail@/var/mail@' etc/login.defs:
#   Instead of using the default 'DES' method, this command modifies the installation to use the more secure 'SHA512' method of hashing passwords, which also allows passwords longer than eight characters.
#   It also changes the obsolete /var/spool/mail location for user mailboxes that Shadow uses by default to the /var/mail location.
#   此命令修改安装以使用更安全的哈希密码 "SHA512" 方法, 而不是使用默认的 "DES" 方法, 该方法还允许使用长度超过八个字符的密码。
#   它还将 Shadow 默认使用的用户邮箱的过时 /var/spool/mail 位置更改为 /var/mail 位置。
# ..................................................
# * sed -i 's/1000/999/' etc/useradd:
#   Make a minor change to make the default useradd consistent with the LFS groups file.
#   稍作更改, 使默认 useradd 与 LFS 组文件一致。

# Configure Explain:
# ..................................................
# * --with-group-name-max-length=32:
#   The maximum user name is 32 characters. Make the maximum group name the same.
#   用户名的最大长度为 32 个字符。使最大组名相同。

# Optional Operation:
# ..................................................
# * mv -v /usr/bin/passwd /bin:
#   The passwd program may be needed during times when the /usr filesystem is not mounted so it is moved into the root partition.
#   当 /usr 文件系统未被挂载时, 可能需要使用 passwd 程序, 以便将其移动到根分区。

SHADOW_VERIFY='n'   
SHADOW_UNZIPPED=0   
SHADOW_CONFIGURED=0 
SHADOW_INSTALLED=0  

read -p "[Confirm] Compile and Install ( shadow-4.2.1 )? (y/n)>" SHADOW_VERIFY

test "$SHADOW_VERIFY" != "y" && exit 1

if ! command -v newuidmap > /dev/null 2>&1; then

    (tar -Jxvf $STORAGE/shadow-4.2.1.tar.xz -C $STORAGE && SHADOW_UNZIPPED=1) &&

    (cd $STORAGE/shadow-4.2.1 && ./configure --prefix=/opt/shadow-4.2.1 --with-group-name-max-length=32 && SHADOW_CONFIGURED=1) &&
    
    (cd $STORAGE/shadow-4.2.1 && make && make install && SHADOW_INSTALLED=1) &&

    (echo "# Binary File from Shadow-4.2.1                             ") &&
    (echo "# --------------------------------------------------        ") &&
    (echo "# /opt/shadow-4.2.1/bin/chage                               ") &&
    (echo "# /opt/shadow-4.2.1/bin/chfn                                ") &&
    (echo "# /opt/shadow-4.2.1/bin/chsh                                ") &&
    (echo "# /opt/shadow-4.2.1/bin/expiry                              ") &&
    (echo "# /opt/shadow-4.2.1/bin/faillog                             ") &&
    (echo "# /opt/shadow-4.2.1/bin/gpasswd                             ") &&
    (echo "# /opt/shadow-4.2.1/bin/lastlog                             ") &&
    (echo "# /opt/shadow-4.2.1/bin/login                               ") &&
    (echo "# /opt/shadow-4.2.1/bin/newgidmap                           ") &&
    (echo "# /opt/shadow-4.2.1/bin/newgrp                              ") &&
    (echo "# /opt/shadow-4.2.1/bin/sg         ---> ( Link from newgrp )") &&
    (echo "# /opt/shadow-4.2.1/bin/newuidmap                           ") &&
    (echo "# /opt/shadow-4.2.1/bin/passwd                              ") &&
    (echo "# /opt/shadow-4.2.1/bin/su                                  ") &&

    (ln -svf /opt/shadow-4.2.1/bin/newgidmap /usr/local/bin/) &&
    (ln -svf /opt/shadow-4.2.1/bin/newuidmap /usr/local/bin/) &&

    (cd $STORAGE && rm -rf $STORAGE/shadow-4.2.1)
else

    echo "[Caution] Command: ( newuidmap ) Already Exists."
fi

# 二进制文件部署(Binary File Deploy) Docker-CE - 26.1.4 Rootless Extras # ---> Optional (Non root User Running "dockerd-rootless-setuptool.sh").
# --------------------------------------------------

# Require: newuidmap # ---> from shadow-4.2.1.tar.xz.

# Install: After Deployment is Completed, Non root User Running "dockerd-rootless-setuptool.sh".

DOCKER_CE_ROOTLESS_VERIFY='n'
DOCKER_CE_ROOTLESS_UNZIPPED=0
DOCKER_CE_ROOTLESS_DEPLOYED=0

read -p "[Confirm] Binary File Deploy ( docker-ce-26.1.4-rootless-extras )? (y/n)>" DOCKER_CE_ROOTLESS_VERIFY

test "$DOCKER_CE_ROOTLESS_VERIFY" != "y" && exit 1

test ! -f "/opt/sandbox-docker-ce/bin/dockerd-rootless-setuptool.sh" && (

    (tar -zxvf $STORAGE/docker-rootless-extras-26.1.4.tgz -C $STORAGE && DOCKER_CE_ROOTLESS_UNZIPPED=1) &&
    
    (test ! -d "/opt/sandbox-docker-ce/bin" && mkdir -p /opt/sandbox-docker-ce/bin || echo "Continue......") &&

    (cp -v $STORAGE/docker-rootless-extras/dockerd-rootless.sh           /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker-rootless-extras/dockerd-rootless-setuptool.sh /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker-rootless-extras/rootlesskit                   /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker-rootless-extras/rootlesskit-docker-proxy      /opt/sandbox-docker-ce/bin/) &&
    (cp -v $STORAGE/docker-rootless-extras/vpnkit                        /opt/sandbox-docker-ce/bin/) &&

    (chmod +x /opt/sandbox-docker-ce/bin/dockerd-rootless.sh          ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/dockerd-rootless-setuptool.sh) &&
    (chmod +x /opt/sandbox-docker-ce/bin/rootlesskit                  ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/rootlesskit-docker-proxy     ) &&
    (chmod +x /opt/sandbox-docker-ce/bin/vpnkit                       ) &&

    (cp -v /opt/sandbox-docker-ce/bin/dockerd-rootless.sh           /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/dockerd-rootless-setuptool.sh /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/rootlesskit                   /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/rootlesskit-docker-proxy      /usr/local/bin/) &&
    (cp -v /opt/sandbox-docker-ce/bin/vpnkit                        /usr/local/bin/) &&
    (DOCKER_CE_ROOTLESS_DEPLOYED=1) &&
    
    (cd $STORAGE && rm -rf $STORAGE/docker-rootless-extras)
) || (

    echo "[Caution] Script: ( /opt/sandbox-docker-ce/bin/dockerd-rootless-setuptool.sh ) Already Exists."
)

# ####################################### Docker-CE - Plugins ########################################

# 二进制文件部署(Binary File Deploy) Docker-CE - Plugins: buildx-0.16.2-Linux-Amd64
# --------------------------------------------------

BUILDX_VERIFY='n'
BUILDX_DEPLOYED=0

read -p "[Confirm] Binary File Deploy ( docker-ce-plugins: buildx-0.16.2-linux-amd64 )? (y/n)>" BUILDX_VERIFY

test "$BUILDX_VERIFY" != "y" && exit 1

test ! -f "/opt/sandbox-docker-ce/cli-plugins/buildx" && (
    
    (test ! -d "/opt/sandbox-docker-ce/cli-plugins" && mkdir -p /opt/sandbox-docker-ce/cli-plugins || echo "Continue......") &&
    
    (cp -v $STORAGE/buildx-v0.16.2.linux-amd64 /opt/sandbox-docker-ce/cli-plugins/buildx) &&
    
    (chmod 755 /opt/sandbox-docker-ce/cli-plugins/buildx) &&
    
    (test ! -d "$HOME/.docker/cli-plugins" && mkdir -p $HOME/.docker/cli-plugins || echo "Continue......") &&
    
    (cp -v /opt/sandbox-docker-ce/cli-plugins/buildx $HOME/.docker/cli-plugins) &&
    (BUILDX_DEPLOYED=1)
) || (

    echo "[Caution] Binary: ( /opt/sandbox-docker-ce/cli-plugins/buildx ) Already Exists."
)

# docker-ce-26.1.4.installed.path
# --------------------------------------------------
#     # docker-ce-26.1.4
#     f: /usr/local/bin/ctr                    
#     f: /usr/local/bin/containerd             
#     f: /usr/local/bin/containerd-shim-runc-v2
#     f: /usr/local/bin/docker                 
#     f: /usr/local/bin/docker-init            
#     f: /usr/local/bin/docker-proxy           
#     f: /usr/local/bin/dockerd                
#     f: /usr/local/bin/runc                   
#     
#     # docker-rootless-extras-26.1.4
#     f: /usr/local/bin/dockerd-rootless.sh          
#     f: /usr/local/bin/dockerd-rootless-setuptool.sh
#     f: /usr/local/bin/rootlesskit                  
#     f: /usr/local/bin/rootlesskit-docker-proxy     
#     f: /usr/local/bin/vpnkit                       
#     
#     # buildx-0.16.2
#     f: /root/.docker/cli-plugins
#     
#     # configure file
#     d: /etc/docker
#     f: /etc/docker/daemon.json
#
#     # service file
#     f: /lib/systemd/system/docker.service
#     f: /lib/systemd/system/docker.socket

# Docker-CE Configure File 1: docker.service
# --------------------------------------------------
#     # "docker.service" is Located by Default in "/etc/systemd/system" or "/lib/systemd/system".

#     [Unit]
#     Description=Docker Application Container Engine
#     Documentation=https://docs.docker.com
#     After=network-online.target docker.socket firewalld.service
#     Wants=network-online.target
#     Requires=docker.socket
#
#     [Service]
#     Type=notify
#     ExecStart=/usr/local/bin/dockerd
#     ExecReload=/bin/kill -s HUP $MAINPID
#     LimitNOFILE=1048576
#     LimitNPROC=infinity
#     LimitCORE=infinity
#     TasksMax=infinity
#     TimeoutStartSec=0
#     Delegate=yes
#     KillMode=process
#     Restart=on-failure
#     StartLimitBurst=3
#     StartLimitInterval=60s
#
#     [Install]
#     WantedBy=multi-user.target

# Docker-CE Configure File 2: docker.socket
# --------------------------------------------------
#     # "docker.socket" is Located by Default in "/etc/systemd/system" or "/lib/systemd/system".
#
#     [Unit]
#     Description=Docker Socket for the API
#     PartOf=docker.service
#
#     [Socket]
#     ListenStream=/run/docker.sock
#     SocketMode=0660
#     SocketUser=root
#     SocketGroup=root
#
#     [Install]
#     WantedBy=sockets.target

# Docker-CE Configure File 3: daemon.json (Path: /etc/docker/daemon.json)
# --------------------------------------------------
#     {
#         "data-root": "/data/docker",
#         "exec-root": "/var/run/docker",
#         "iptables": true,
#         "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:4243"],
#         "exec-opts": ["native.cgroupdriver=systemd"],
#         "log-driver": "json-file",
#         "log-level": "warn",
#         "log-opts": {
#             "max-size": "500m",
#             "max-file": "3"
#         },
#         "insecure-registries" : ["demo.local.hub:5000"],
#         "bip": "192.168.100.1/24",
#         "default-address-pools": [
#             {
#                 "scope": "local",
#                 "base": "172.17.0.0/16",
#                 "size": 24
#             }
#         ],
#         "registry-mirrors": ["https://registry.docker-cn.com"],
#         "storage-driver": "overlay2",
#         "live-restore": true,
#         "max-concurrent-downloads": 5
#     }

```

## 总结

以上就是关于 Linux运维 Bash脚本 二进制文件部署Docker-CE-26.1.4 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
