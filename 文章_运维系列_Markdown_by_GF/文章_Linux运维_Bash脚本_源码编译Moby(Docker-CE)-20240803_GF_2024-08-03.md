# 文章_Linux运维_Bash脚本_源码编译Moby(Docker-CE)-20240803_GF_2024-08-03

Bash (Bourne Again Shell) 是一个解释器，负责处理 Unix 系统命令行上的命令。它是由 Brian Fox 编写的免费软件，并于 1989 年发布的免费软件，作为 Sh (Bourne Shell) 的替代品。

您可以在 Linux 和 MacOS 机器上使用 Bash，甚至可以通过适用于 Linux 的 Windows 子系统在 Windows 10 机器上使用。

## 使用方法

* 下载 docker 镜像及源码包:

offline.for.cli.26/amd64/alpine/3.20:golang-1.21.12

(以上 offline.for.cli.26/amd64/alpine/3.20:golang-1.21.12 docker 镜像链接: https://download.csdn.net/download/goufeng93/90611287)

offline.for.cli.26/arm64/alpine/3.20:golang-1.21.12

(以上 offline.for.cli.26/arm64/alpine/3.20:golang-1.21.12 docker 镜像链接: https://download.csdn.net/download/goufeng93/90611290)

offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12

(以上 offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12 docker 镜像链接: https://download.csdn.net/download/goufeng93/90612327)

offline.for.moby.26/arm64/debian/bookworm:golang-1.21.12

(以上 offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12 docker 镜像链接: https://download.csdn.net/download/goufeng93/90613419)

buildx-0.16.2.tar.gz

runc-master-20240804.tar.gz

cli-master-20240805.tar.gz

(以上 cli-master-20240805.tar.gz 源码包链接: https://download.csdn.net/download/goufeng93/89711126)

moby-matser-20240803.tar.gz

(以上 moby-matser-20240803.tar.gz 源码包链接: https://download.csdn.net/download/goufeng93/89714646)

* 放于指定路径:

这里 Bash Shell 脚本的全局变量 STORAGE 指定的存放源码包的路径 ==/home/goufeng== 可进行修改。

* 执行 Bash Shell 脚本:

输入 ==/[路径名]/[脚本名].sh== 即可进行自动编译部署，过程中提示输入 **(y/n)** 输入 **y** 则进行下一步，这样分阶段确认的原因是为了确保能够看到上一个源码编译结果中可能的错误和提示。

## 完整脚本

```shell
#! /bin/bash
# Create By GF 2024-08-03 01:34

# --------------------------------------------------
# Install First:
# * Go >= 1.21.x
# * Git
# * Docker-CE >= 20.10 (Binary Deploy)

# -------------- Docker Image for Cli --------------
# Need File: offline.for.cli.26/amd64/alpine/3.20:golang-1.21.12
# Need File: offline.for.cli.26/arm64/alpine/3.20:golang-1.21.12

# -------------- Docker Image for Moby -------------
# Need File: offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12
# Need File: offline.for.moby.26/arm64/debian/bookworm:golang-1.21.12

# ------------------- Dependency -------------------
# Need File: buildx-0.16.2.tar.gz
# Need File: runc-master-20240804.tar.gz
# ------------ Docker-CE-Cli - 20240805 ------------
# Need File: cli-master-20240805.tar.gz
# ----------- Moby(Docker-CE) - 20240803 -----------
# Need File: moby-matser-20240803.tar.gz

# ##################################################
STORAGE=/home/goufeng

# ############# Compilation Environment ############
ORIGINAL_PATH=$PATH

# ######################## offline.for.cli.26/amd64/alpine/3.20:golang-1.21.12 #######################

Installed APK:
  + bash  + build-base  +          clang  +    curl
  + file  +        gcc  +            git  +     lld
  + llvm  +   musl-dev  + openssh-client  + openssl

/go/bin/
  + gotestsum
  + goversioninfo

/go/pkg/mod/
  + github.com/josephspurrier/goversioninfo@v1.3.0
  + github.com/akavel/rsrc@v0.10.2
  + github.com/fsnotify/fsnotify@v1.5.4
  + github.com/mattn/go-isatty@v0.0.14
  + github.com/mattn/go-colorable@v0.1.12
  + github.com/google/shlex@v0.0.0-20191202100458-e7afc7fbc510
  + github.com/fatih/color@v1.13.0
  + github.com/dnephin/pflag@v1.0.7
  + gotest.tools/gotestsum@v1.10.0
  + golang.org/x/sync@v0.0.0-20220601150217-0de741cfad7f
  + golang.org/x/mod@v0.6.0-dev.0.20220419223038-86c51ed26bb4
  + golang.org/x/tools@v0.1.11
  + golang.org/x/term@v0.0.0-20220526004731-065cf7ba2467
  + golang.org/x/sys@v0.0.0-20220715151400-c0bba94af5f8

/usr/local/bin/
  + notary  (Only Platform AMD64 Exists)

# ##################### offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12 #####################

Installed DEB:
  +                apparmor  +        autoconf  +               automake  + bash-completion
  +         build-essential  +           bzip2  +        ca-certificates  +           clang
  +                   cmake  +            criu  +                   curl  +            dbus
  +       dbus-user-session  +        dpkg-dev  +                   file  +             g++
  +                     gcc  +  inetutils-ping  +               iproute2  +        iptables
  +                      jq  + libapparmor-dev  +           libbtrfs-dev  +       libc6-dev
  +             libcap2-bin  +      libcap-dev  +          libgcc-12-dev  +         libnet1
  +             libnl-3-200  +  libprotobuf-c1  +      libprotobuf-c-dev  +  libseccomp-dev
  +         libsecret-1-dev  +  libsystemd-dev  +                libtool  +     libudev-dev
  +                libyajl2  +     libyajl-dev  +                    lld  +            llvm
  +               net-tools  +  openssh-client  +                openssl  +           patch
  +                    pigz  +         pkgconf  +             pkg-config  +         python3
  +                    sudo  +         systemd  + systemd-journal-remote  +    systemd-sysv
  + thin-provisioning-tools  +          uidmap  +                    vim  +      vim-common
  +                xfsprogs  +        xz-utils  +               yamllint  +             zip
  +                    zstd

/go/bin/
  + golangci-lint
  + gopls

/go/pkg/mod/
  + gitlab.com/bosi/decorder@v0.4.1
  + google.golang.org/protobuf@v1.28.0
  + go.uber.org/atomic@v1.7.0
  + go.uber.org/multierr@v1.6.0
  + go.uber.org/zap@v1.24.0
  + honnef.co/go/tools@v0.4.6
  + honnef.co/go/tools@v0.4.7
  + 4d63.com/gocheckcompilerdirectives@v1.2.1
  + 4d63.com/gochecknoglobals@v0.2.1
  + github.com/go-xmlfmt/xmlfmt@v1.1.2
  + github.com/securego/gosec/v2@v2.18.2
  + github.com/gordonklaus/ineffassign@v0.0.0-20230610083614-0e73809eb601
  + github.com/sivchari/tenv@v1.7.1
  + github.com/sivchari/nosnakecase@v1.7.0
  + github.com/sivchari/containedctx@v1.0.3
  + github.com/stbenjam/no-sprintf-host-port@v0.1.1
  + github.com/nakabonne/nestif@v0.3.1
  + github.com/butuzov/ireturn@v0.2.2
  + github.com/butuzov/mirror@v1.1.0
  + github.com/cespare/xxhash/v2@v2.1.2
  + github.com/gofrs/flock@v0.8.1
  + github.com/hashicorp/errwrap@v1.0.0
  + github.com/hashicorp/go-multierror@v1.1.1
  + github.com/hashicorp/go-version@v1.6.0
  + github.com/hashicorp/hcl@v1.0.0
  + github.com/alecthomas/go-check-sumtype@v0.1.3
  + github.com/gobwas/glob@v0.2.3
  + github.com/ettle/strcase@v0.1.1
  + github.com/sanposhiho/wastedassign/v2@v2.0.7
  + github.com/kk!h!a!i!k!e/contextcheck@v1.1.4
  + github.com/prometheus/client_model@v0.2.0
  + github.com/prometheus/client_golang@v1.12.1
  + github.com/prometheus/common@v0.32.1
  + github.com/prometheus/procfs@v0.7.3
  + github.com/blizzy78/varnamelen@v0.8.0
  + github.com/macabu/inamedparam@v0.1.2
  + github.com/chavacava/garif@v0.1.0
  + github.com/sirupsen/logrus@v1.9.3
  + github.com/matoous/godox@v0.0.0-20230222163458-006bad1f9d26
  + github.com/alingse/asasalint@v0.0.11
  + github.com/polyfloyd/go-errorlint@v1.4.5
  + github.com/fsnotify/fsnotify@v1.5.4
  + github.com/ldez/tagliatelle@v0.5.0
  + github.com/ldez/gomoddirectives@v0.2.3
  + github.com/uudashr/gocognit@v1.1.2
  + github.com/tetafro/godot@v1.4.15
  + github.com/sonatard/noctx@v0.0.2
  + github.com/4meepo/tagalign@v1.3.3
  + github.com/ryancurrah/gomodguard@v1.3.0
  + github.com/alexkohler/nakedret/v2@v2.0.2
  + github.com/alexkohler/prealloc@v1.0.0
  + github.com/!djarvur/go-err113@v0.0.0-20210108212216-aea10b59be24
  + github.com/jingyugao/rowserrcheck@v1.1.1
  + github.com/hexops/gotextdiff@v1.0.3
  + github.com/fzipp/gocyclo@v0.6.0
  + github.com/beorn7/perks@v1.0.1
  + github.com/shazow/go-diff@v0.0.0-20160112020656-b6b7b6733b8c
  + github.com/davecgh/go-spew@v1.1.1
  + github.com/!gaijin!entertainment/go-exhaustruct/v3@v3.1.0
  + github.com/olekukonko/tablewriter@v0.0.5
  + github.com/maratori/testableexamples@v1.0.0
  + github.com/maratori/testpackage@v1.1.1
  + github.com/golang/protobuf@v1.5.2
  + github.com/mattn/go-isatty@v0.0.17
  + github.com/mattn/go-runewidth@v0.0.9
  + github.com/mattn/go-colorable@v0.1.13
  + github.com/kyoh86/exportloopref@v0.1.11
  + github.com/go-toolsmith/typep@v1.1.0
  + github.com/go-toolsmith/astequal@v1.1.0
  + github.com/go-toolsmith/astcast@v1.1.0
  + github.com/go-toolsmith/astcopy@v1.1.0
  + github.com/go-toolsmith/astfmt@v1.1.0
  + github.com/go-toolsmith/strparse@v1.1.0
  + github.com/go-toolsmith/astp@v1.1.0
  + github.com/!burnt!sushi/toml@v1.3.2
  + github.com/!burnt!sushi/toml@v1.2.1
  + github.com/tdakkota/asciicheck@v0.2.0
  + github.com/bombsimon/wsl/v3@v3.4.0
  + github.com/golangci/go-misc@v0.0.0-20220329215616-d24fe342adfe
  + github.com/golangci/gofmt@v0.0.0-20231018234816-f50ced29576e
  + github.com/golangci/misspell@v0.4.1
  + github.com/golangci/lint-1@v0.0.0-20191013205115-297bf364a8e0
  + github.com/golangci/check@v0.0.0-20180506172741-cfe4005ccda2
  + github.com/golangci/revgrep@v0.5.2
  + github.com/golangci/golangci-lint@v1.55.2
  + github.com/golangci/maligned@v0.0.0-20180506175553-b1d89398deca
  + github.com/golangci/unconvert@v0.0.0-20180507085042-28b1c447d1f4
  + github.com/golangci/dupl@v0.0.0-20180902072040-3e9179ac440a
  + github.com/jgautheron/goconst@v1.6.0
  + github.com/pelletier/go-toml/v2@v2.0.5
  + github.com/pelletier/go-toml@v1.9.5
  + github.com/google/go-cmp@v0.6.0
  + github.com/timonwong/loggercheck@v0.9.4
  + github.com/!masterminds/semver@v1.5.0
  + github.com/curioswitch/go-reassign@v0.2.0
  + github.com/kisielk/gotool@v1.0.0
  + github.com/kisielk/errcheck@v1.6.3
  + github.com/ykadowak/zerologlint@v0.1.3
  + github.com/jirfag/go-printf-func-name@v0.0.0-20200119135958-7558a9eaa5af
  + github.com/mbilski/exhaustivestruct@v1.2.0
  + github.com/ultraware/whitespace@v0.0.5
  + github.com/ultraware/funlen@v0.1.0
  + github.com/ssgreg/nlreturn/v2@v2.2.1
  + github.com/kunwardeep/paralleltest@v1.0.8
  + github.com/charithe/durationcheck@v0.0.10
  + github.com/nishanths/predeclared@v0.2.2
  + github.com/nishanths/exhaustive@v0.11.0
  + github.com/mitchellh/go-homedir@v1.1.0
  + github.com/mitchellh/mapstructure@v1.5.0
  + github.com/ryanrolds/sqlclosecheck@v0.5.1
  + github.com/matttproud/golang_protobuf_extensions@v1.0.1
  + github.com/fatih/structtag@v1.2.0
  + github.com/fatih/color@v1.15.0
  + github.com/esimonov/ifshort@v1.0.4
  + github.com/tommy-muehle/go-mnd/v2@v2.5.1
  + github.com/subosito/gotenv@v1.4.1
  + github.com/leonklingele/grouper@v1.1.1
  + github.com/kulti/thelper@v0.6.3
  + github.com/!abirdcfly/dupword@v0.0.13
  + github.com/gostaticanalysis/comment@v1.4.2
  + github.com/gostaticanalysis/forcetypeassert@v0.1.0
  + github.com/gostaticanalysis/nilerr@v0.1.1
  + github.com/gostaticanalysis/analysisutil@v0.7.1
  + github.com/denis-tingaikin/go-header@v0.4.3
  + github.com/xen0n/gosmopolitan@v1.2.2
  + github.com/nunnatsa/ginkgolinter@v0.14.1
  + github.com/spf13/jwalterweatherman@v1.1.0
  + github.com/spf13/cast@v1.5.0
  + github.com/spf13/pflag@v1.0.5
  + github.com/spf13/cobra@v1.7.0
  + github.com/spf13/viper@v1.12.0
  + github.com/spf13/afero@v1.8.2
  + github.com/mgechev/revive@v1.3.4
  + github.com/firefart/nonamedreturns@v1.0.4
  + github.com/yagipy/maintidx@v1.0.0
  + github.com/lufeee/execinquery@v1.2.1
  + github.com/sashamelentyev/usestdlibvars@v1.24.0
  + github.com/sashamelentyev/interfacebloat@v1.1.0
  + github.com/catenacyber/perfsprint@v0.2.0
  + github.com/ccojocar/zxcvbn-go@v1.0.1
  + github.com/yeya24/promlinter@v0.2.0
  + github.com/ghostiam/protogetter@v0.2.3
  + github.com/!antonboom/testifylint@v0.2.3
  + github.com/!antonboom/errname@v0.1.12
  + github.com/!antonboom/nilnil@v0.1.7
  + github.com/daixiang0/gci@v0.11.2
  + github.com/timakin/bodyclose@v0.0.0-20230421092635-574207250966
  + github.com/tomarrell/wrapcheck/v2@v2.8.1
  + github.com/moricho/tparallel@v0.3.1
  + github.com/bkielbasa/cyclop@v1.2.1
  + github.com/sourcegraph/go-diff@v0.7.0
  + github.com/julz/importas@v0.1.0
  + github.com/pmezard/go-difflib@v1.0.0
  + github.com/magiconair/properties@v1.8.6
  + github.com/ashanbrown/forbidigo@v1.6.0
  + github.com/ashanbrown/makezero@v1.1.1
  + github.com/stretchr/testify@v1.8.4
  + github.com/stretchr/objx@v0.5.0
  + github.com/breml/bidichk@v0.2.7
  + github.com/breml/errchkjson@v0.3.6
  + github.com/!open!pee!dee!p/depguard/v2@v2.1.0
  + github.com/quasilyte/stdinfo@v0.0.0-20220114132959-f7386bf02567
  + github.com/quasilyte/regex/syntax@v0.0.0-20210819130434-b3f0c404a727
  + github.com/quasilyte/gogrep@v0.5.0
  + github.com/quasilyte/go-ruleguard@v0.4.0
  + github.com/go-critic/go-critic@v0.9.0
  + gopkg.in/ini.v1@v1.67.0
  + gopkg.in/yaml.v2@v2.4.0
  + gopkg.in/yaml.v3@v3.0.1
  + mvdan.cc/lint@v0.0.0-20170908181259-adc824a0674b
  + mvdan.cc/interfacer@v0.0.0-20180901003855-c20040233aed
  + mvdan.cc/unparam@v0.0.0-20221223090309-7455f1af531d
  + mvdan.cc/gofumpt@v0.5.0
  + mvdan.cc/xurls/v2@v2.5.0
  + mvdan.cc/gofumpt@v0.6.0
  + go.tmz.dev/musttag@v0.7.2
  + golang.org/x/text@v0.13.0
  + golang.org/x/sync@v0.4.0
  + golang.org/x/mod@v0.13.0
  + golang.org/x/sys@v0.13.0
  + golang.org/x/tools@v0.14.0
  + golang.org/x/exp/typeparams@v0.0.0-20230307190834-24139beb5833
  + golang.org/x/exp/typeparams@v0.0.0-20221212164502-fae10dda9338
  + golang.org/x/exp@v0.0.0-20230510235704-dd950f8aeaea
  + golang.org/x/mod@v0.18.0
  + golang.org/x/tools@v0.22.1-0.20240628205440-9c895dd76b34
  + golang.org/x/text@v0.16.0
  + golang.org/x/telemetry@v0.0.0-20240607193123-221703e18637
  + golang.org/x/tools@v0.16.1
  + golang.org/x/vuln@v1.0.4
  + golang.org/x/tools/gopls@v0.16.1
  + golang.org/x/sync@v0.7.0
  + go-simpler.org/sloglint@v0.1.2

/usr/local/go/bin/
  + gotestsum
  + go-winres
  + shfmt
  + tomll

/usr/local/go/src/
  + github.com/bitfield/gotestdox
  + github.com/cpuguy83/go-md2man/v2
  + github.com/dnephin/pflag
  + github.com/fatih/color
  + github.com/fsnotify/fsnotify
  + github.com/google/renameio/v2
  + github.com/google/shlex
  + github.com/mattn/go-colorable
  + github.com/mattn/go-isatty
  + github.com/nfnt/resize
  + github.com/pelletier/go-toml
  + github.com/pkg/diff
  + github.com/russross/blackfriday/v2
  + github.com/tc-hib/go-winres
  + github.com/tc-hib/winres
  + github.com/urfave/cli/v2
  + github.com/xrash/smetrics
  + golang.org/x/image
  + golang.org/x/mod
  + golang.org/x/sync
  + golang.org/x/sys
  + golang.org/x/term
  + golang.org/x/text
  + golang.org/x/tools
  + gotest.tools/gotestsum
  + mvdan.cc/editorconfig
  + mvdan.cc/sh/v3

# ############################################ Dependency ############################################

# 构建安装(Build Install) buildx - 0.16.2
# --------------------------------------------------

export PATH=/opt/go-1.21.11/bin:$ORIGINAL_PATH
export GOPATH=/opt/go-1.21.11

BUILDX_VERIFY='n'
BUILDX_UNZIPPED=0
BUILDX_BUILDED=0

read -p "[Confirm] Build and Install ( buildx-0.16.2 )? (y/n)>" BUILDX_VERIFY

test "$BUILDX_VERIFY" != "y" && exit 1

test ! -f "/$USER/.docker/cli-plugins/docker-buildx" && (

    (tar -zxvf $STORAGE/buildx-0.16.2.tar.gz && BUILDX_UNZIPPED=1) &&

    (cd $STORAGE/buildx-0.16.2 && hack/build && BUILDX_BUILDED=1) &&

    (cp -v $STORAGE/buildx-0.16.2/bin/build/docker-buildx /$USER/.docker/cli-plugins/) &&

    (chmod +x /$USER/.docker/cli-plugins/docker-buildx) &&

    (cd $STORAGE && rm -rf $STORAGE/buildx-0.16.2)
) || (

    echo "[Caution] Binary: ( /$USER/.docker/cli-plugins/docker-buildx ) Already Exists."
)

# 编译安装(Build Install) runc - master - 20240804
# --------------------------------------------------

export PATH=/opt/go-1.21.11/bin:$ORIGINAL_PATH
export GOPATH=/opt/go-1.21.11

RUNC_VERIFY='n'
RUNC_UNZIPPED=0
RUNC_BUILDED=0

read -p "[Confirm] Build and Install ( runc-master-20240804 )? (y/n)>" RUNC_VERIFY

test "$RUNC_VERIFY" != "y" && exit 1

test ! -f "/opt/runc-master-20240804/bin/runc" && (

    (tar -zxvf $STORAGE/runc-master-20240804.tar.gz && RUNC_UNZIPPED=1) &&

    (cd $STORAGE/runc-master-20240804 && go build && RUNC_BUILDED=1) &&

    (mkdir -p /opt/runc-master-20240804/bin) &&

    (cp -v $STORAGE/runc-master-20240804/runc /opt/runc-master-20240804/bin/) &&

    (chmod +x /opt/runc-master-20240804/bin/runc) &&

    (cd $STORAGE && rm -rf $STORAGE/runc-master-20240804)
) || (

    echo "[Caution] Binary: ( /opt/runc-master-20240804/bin/runc ) Already Exists."
)

# ################################ Docker-CE: Cli - master - 20240805 ################################

# 编译安装(Make Install) Docker-CE: Cli - master - 20240805
# --------------------------------------------------

DOCKER_CE_CLI_VERIFY='n'
DOCKER_CE_CLI_UNZIPPED=0
DOCKER_CE_CLI_MADE=0

read -p "[Confirm] Make and Install ( docker-ce: cli-master-20240805 )? (y/n)>" DOCKER_CE_CLI_VERIFY

test "$DOCKER_CE_CLI_VERIFY" != "y" && exit 1

test ! -f "/opt/cli-master-20240805/bin/docker" && (

    (tar -zxvf $STORAGE/cli-master-20240805.tar.gz && DOCKER_CE_CLI_UNZIPPED=1) &&

    (echo "--------------------------------------------------") &&

    (echo "Modify Dockerfile (Example of Platform AMD64):"    ) &&
    (echo " - FROM --platform=$BUILDPLATFORM golang:${GO_VERSION}-alpine${ALPINE_VERSION} AS build-base-alpine" ) &&
    (echo " + FROM offline.for.cli.26/amd64/alpine/3.20:golang-1.21.12 AS build-base-alpine" ) &&
    (echo " ... "                                             ) &&
    (echo "Modify Dockerfile (Example of Platform ARM64):"    ) &&
    (echo " - FROM --platform=$BUILDPLATFORM golang:${GO_VERSION}-alpine${ALPINE_VERSION} AS build-base-alpine" ) &&
    (echo " + FROM offline.for.cli.26/arm64/alpine/3.20:golang-1.21.12 AS build-base-alpine" ) &&

    (echo "--------------------------------------------------") &&

    (cd $STORAGE/cli-master-20240805 && make -f docker.Makefile binary && DOCKER_CE_CLI_MADE=1) &&

    (mkdir -p                                      /opt/cli-master-20240805/bin  ) &&
    (cp    -v $STORAGE/cli-master-20240805/build/* /opt/cli-master-20240805/bin/ ) &&
    (chmod +x                                      /opt/cli-master-20240805/bin/*) &&

    (cd $STORAGE && rm -rf $STORAGE/cli-master-20240805)
) || (

    echo "[Caution] Binary: ( /opt/cli-master-20240805/bin/docker ) Already Exists."
)

# ################################ Moby(Docker-CE) - master - 20240803 ###############################

# 编译安装(Make Install) Moby(Docker-CE) - master - 20240803
# --------------------------------------------------

# Git Clone Preparation:
# ----------------------------------------------
# moby-26.1.4/hack/dockerfile/install/containerd.installer:22: git clone https://github.com/containerd/containerd.git "$GOPATH/src/github.com/containerd/containerd"
# moby-26.1.4/hack/dockerfile/install/dockercli.installer:24: git clone https://github.com/docker/docker-ce "$GOPATH/tmp/docker-ce"
# moby-26.1.4/hack/dockerfile/install/runc.installer:18: git clone https://github.com/opencontainers/runc.git "$GOPATH/src/github.com/opencontainers/runc"
# moby-26.1.4/hack/dockerfile/install/tini.installer:10: git clone https://github.com/krallin/tini.git "$GOPATH/tini"

export PATH=/opt/go-1.21.11/bin:$ORIGINAL_PATH
export GOPATH=/opt/go-1.21.11

MOBY_VERIFY='n'
MOBY_UNZIPPED=0
MOBY_MADE=0
MOBY_INSTALLED=0

read -p "[Confirm] Make and Install ( moby(docker-ce)-master-20240803 )? (y/n)>" MOBY_VERIFY

test "$MOBY_VERIFY" != "y" && exit 1

test ! -f "/opt/moby-master-20240803/bin/dockerd" && (

    (tar -zxvf $STORAGE/moby-master-20240803.tar.gz && MOBY_UNZIPPED=1) &&

    (echo "--------------------------------------------------") &&

    (echo "Modify Dockerfile (Example of Platform AMD64):"                           ) &&
    (echo " - FROM --platform=$BUILDPLATFORM ${GOLANG_IMAGE} AS base"                ) &&
    (echo " + FROM offline.for.moby.26/amd64/debian/bookworm:golang-1.21.12 AS base" ) &&
    (echo " ... "                                                                    ) &&
    (echo "Modify Dockerfile (Example of Platform ARM64):"                           ) &&
    (echo " - FROM --platform=$BUILDPLATFORM ${GOLANG_IMAGE} AS base"                ) &&
    (echo " + FROM offline.for.moby.26/arm64/debian/bookworm:golang-1.21.12 AS base" ) &&

    (echo "--------------------------------------------------") &&

    (echo "# Compilation Method for \"moby(docker-ce)\":"                                          ) &&
    (echo "# - Compile in Docker Environment: cd ./moby-master-20240803 && make binary"            ) &&
    (echo "# - Compile in Non Docker Environment: cd ./moby-master-20240803 && hack/make.sh binary") &&

    (echo "--------------------------------------------------") &&

    (cd $STORAGE/moby-master-20240803 && make binary && MOBY_MADE=1) &&

    (mkdir -p                                                /opt/moby-master-20240803/bin  ) &&
    (cp    -v $STORAGE/moby-master-20240803/bundles/binary/* /opt/moby-master-20240803/bin/ ) &&
    (chmod +x                                                /opt/moby-master-20240803/bin/*) &&

    (cd $STORAGE/moby-master-20240803) # && make install MOBY_INSTALLED=1
) || (

    echo "[Caution] Binary: ( /opt/moby-master-20240803/bin/dockerd ) Already Exists."
)

```

## 总结

以上就是关于 Linux运维 Bash脚本 源码编译Moby(Docker-CE)-20240803 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
