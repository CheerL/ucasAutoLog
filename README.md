# UCAS--国科大校园网自动登录程序

由于早已经毕业无法接触校园网环境，本软件很早以前就**停止维护**，仅供参考

## 说明

本软件用于中国科学院大学校园网自动登录，若非我校校园网用户请勿下载使用（反正也用不了）

软件原理是寻找未修改默认密码的校园网账号，使用其流量

因手段不太光彩，且流量有限，**请勿大规模推广**

## 功能

软件主要功能为

1. 自动登录（包括断线重连，一定时间切换账号）
2. 寻找可用账号（建议每隔5天运行一次，可以在`src`文件夹下的`success.txt`中看到结果）

## 下载使用

你可以直接运行脚本，或下载对应你系统的客户端

### Windows客户端

[点击下载](https://github.com/CheerL/ucasAutoLog/releases/download/1.2.0/ucas_auto_login_win_release.exe)

### Mac客户端

[点击下载](https://github.com/CheerL/ucasAutoLog/releases/download/1.2.0/ucas_auto_login_mac_release.dmg)

### Ubuntu客户端

[点击下载](https://github.com/CheerL/ucasAutoLog/releases/download/1.2.0/ucas_auto_login_ubuntu_release.deb)

### 其他系统客户端

开发中

### 运行脚本

若有一定的开发能力，可以自行安装`python3`并安装相关依赖库，脚本在`script`文件夹下，`run.py`对应自动登录功能，`list_update.py`对应寻找可用账号功能
