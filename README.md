# qinglong_chuantou

# 原作者:[四天](https://gitee.com/lstcml)

## 个人QQ交流群：[641307462](https://qm.qq.com/cgi-bin/qm/qr?k=B5meSMnKmXOIACK9VyWTYjIxdLWpSbRm&authKey=EMQROjU6NjgLUwmHnYJF052JFdpfBq7mB+nNuC5JRxk5JZyFbbFzgT1fSzAq4vHB&noverify=0)

## 说明

基于钉钉开发平台，有人说新版有问题我就备份了个旧版本

* 使用方法
## 第一步拉库：
* 青龙面版5700端口
```sh
ql raw https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/1.3/chuantou.py
```
* elecV2P8000端口
```sh
ql raw https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/1.3/chuantou8000.py
```

## 第二步填前缀变量（英文数据都可以）:
* 青龙5700端口
```sh
export qlsubdomain='xxxx'
```
* elecV2P8000端口
```sh
export qlsubdomain8000='xxxx'
```
## 第三步定时10分钟一次:
```sh
*/10 * * * *
```
## 这第四步那就是访问咯:
```sh
xxxx.vaiwan.com
```

* 建议首次手动运行一次任务，访问URL查看任务日志


## 链接
[python-ngrok](https://github.com/hauntek/python-ngrok)
[open-dingtalk](https://github.com/open-dingtalk/pierced)

