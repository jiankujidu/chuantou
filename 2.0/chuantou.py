# -*- coding: UTF-8 -*-
# Version: v2.0
# Created by lstcml on 2022/04/01
# 建议定时10分钟：*/10 * * * *
#个人QQ交流群：641307462

'''
v1.9更新记录：
1、新增http_auth认证，使用：新建变量qlhttpauth，值：账号:密码，例：qinglong:123456
2、新增在线获取服务器，便于服务器更新
3、新增服务器自动切换，当穿透失败时自动切换到其他服务器
4、新增pushplus+推送，需提前在配置文件中配置token
'''

'''
cron: */10 * * * *
new Env('钉钉内网穿透');
'''

import os
import re
import json
import requests
from time import sleep
from requests.auth import HTTPBasicAuth

def update():
    print("当前运行的脚本版本：" + str(version))
    try:
        r1 = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/2.0/chuantou.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("kill -9 `ps -ef | grep 'ngrok.py' | grep -v 'grep' | awk '{print $1}'`")
            os.system("rm -f ngrok.py")
            os.system("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/2.0/chuantou.py &")
    except:
        pass

# 判断是否包含中文
def other_character(str):
    match = re.compile(u'[\u4e00-\u9fa5]').search(str)
    if match:
        return False
    else:
        if str.isalnum():
            return True
        else:
            return False

# 下载Ngrok主程序
def download_ngrok():
    if not os.path.exists("ngrok.py"):
        res = requests.get("https://raw.githubusercontent.com/jiankujidu/chuantou/main/2.0/ngrok.py")
        with open("ngrok.py", "wb") as f:
            f.write(res.content)
    start_nwct()

# 进程守护
def process_daemon(qlurl):
    try:
        if qlhttp_auth == "None":
            res = requests.get(qlurl + "/login").text
        else:
            http_auth = qlhttp_auth.split(":")
            res = requests.get(qlurl + "/login", auth=HTTPBasicAuth(http_auth[0], http_auth[1])).text
        if "/images/g5.ico" in res:
            return "success"
        else:
            return "fail"
    except:
        return "fail"

# 执行程序
def start_nwct():
    global qlhttp_auth
    servers = get_server()
    count = len(servers)
    if qlhttp_auth == "":
        qlhttp_auth = "None"
    for i in range(count):
        qlurl = "http://%s.%s" % (subdomain, servers[i]["subdomain"])
        if process_daemon(qlurl) != "success":
            os.system("kill -9 `ps -ef | grep 'ngrok.py' | grep -v 'grep' | awk '{print $1}'`")
            sleep(2)
            os.system("python3 ngrok.py %s %s %s %s &" %(servers[i]["server"], servers[i]["port"], subdomain, qlhttp_auth))
            print("启动中...")
            sleep(5)
            r = process_daemon(qlurl)
            if r == "success":
                url = "http://www.pushplus.plus/send?token=" + token + "&title=内网穿透通知" + "&content=青龙面板访问地址：" + qlurl + "&template=html"
                requests.get(url)
                print("启动成功！\n青龙面板：%s\npush+发送通知消息完成。" % qlurl)
                break
            else:
                if i == count-1:
                    print("启动失败！请重试...")
                else:
                    print("启动失败！正在切换服务器%s..." % str(i+2))
        else:
            print("程序运行中...\n青龙面板：%s" % qlurl)
            break

# 获取服务器地址
def get_server():
    try:
        res = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/2.0/server.fd").text
        # res = '[{"server":"vaiwan.com","port":"443","subdomain":"vaiwan.com"},{"server":"durl.ga","port":"4443","subdomain":"durl.ga"}]'
        return json.loads(res)
    except:
        return json.loads('[{"server":"vaiwan.com","port":"443","subdomain":"vaiwan.com"}]')

if __name__ == '__main__':
    get_server()
    version = 2.0
    update()
    try:
        subdomain = os.environ['qlsubdomain']
    except:
        subdomain = ""
    try:
        qlhttp_auth = os.environ['qlhttpauth']
    except:
        qlhttp_auth = ""
    try:
        token = os.environ['PUSH_PLUS_TOKEN']
    except:
        token = ''

    if len(subdomain) < 1:
        print("请新增变量qlsubdomain指定域名前缀！")
    else:
        if other_character(subdomain):
            if qlhttp_auth == "" or ":" in qlhttp_auth:
                download_ngrok()
            else:
                print("变量qlhttp_auth格式错误！例：qinglong:123456")
        else:
            print("变量qlsubdomain仅支持英文数字组合！")
