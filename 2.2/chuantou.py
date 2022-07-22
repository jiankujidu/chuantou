# -*- coding: UTF-8 -*-
# Version: v2.3
# Created by lstcml on 2022/04/01
# 建议定时10分钟：*/10 * * * *

'''
V2.3
1、移除钉钉服务器

V2.2
1、替换推送逻辑

V2.1
1、新增自定义更新脚本，默认关闭，启用：新建变量qlnwctupdate，值：true
2、替换更新接口和服务端获取接口

V2.0
1、 修复运行中出现切换服务器的问题

v1.9更新记录：
1、新增http_auth认证，使用：新建变量qlhttpauth，值：账号:密码，例：qinglong:123456
2、新增在线获取服务器，便于服务器更新
3、新增服务器自动切换，当穿透失败时自动切换到其他服务器
4、新增pushplus+推送，需提前在配置文件中配置token
'''

import os
import re
import sys
import json
import requests
import random
from time import sleep
from requests.auth import HTTPBasicAuth

def update():
    print("当前运行的脚本版本：" + str(version))
    try:
        r1 = requests.get("https://ghproxy.com/https://github.com/jiankujidu/chuantou/raw/main/2.2/nwct.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("kill -9 `ps -ef | grep 'ngrok.py' | grep -v 'grep' | awk '{print $1}'`")
            os.system("rm -f ngrok.py")
            os.system("ql raw https://ghproxy.com/https://github.com/jiankujidu/chuantou/raw/main/2.2/nwct.py &")
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
        res = requests.get("https://ghproxy.com/https://github.com/jiankujidu/chuantou/raw/main/2.2/ngrok.py")
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
            return True
        else:
            return False
    except:
        return False

# 执行程序
def start_nwct():
    global qlhttp_auth
    servers = get_server()
    count = len(servers)
    if qlhttp_auth == "":
        qlhttp_auth = "None"
    for i in range(count):
        qlurl = "http://%s.%s" % (subdomain, servers[i]["subdomain"])
        if not process_daemon(qlurl):
            os.system("kill -9 `ps -ef | grep 'ngrok.py' | grep -v 'grep' | awk '{print $1}'`")
            sleep(2)
            os.system("python3 ngrok.py %s %s %s %s &" %(servers[i]["server"], servers[i]["port"], subdomain, qlhttp_auth))
            print("启动中...")
            sleep(5)
            if process_daemon(qlurl):
                if load_send():
                     print("启动成功！\n青龙面板：%s" % qlurl)
                     send("内网穿透通知", "青龙面板访问地址：" + qlurl)
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
        res = requests.get("https://ghproxy.com/https://github.com/jiankujidu/chuantou/raw/main/2.2/server.fd").text
        return json.loads(res)
    except:
        return json.loads('[{"server":"durl.ga","port":"4443","subdomain":"durl.ga"}]')

# 推送
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://ghproxy.com/https://github.com/jiankujidu/chuantou/raw/main/2.2/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)
        
    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False

if __name__ == '__main__':
    get_server()
    version = 2.2
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
        token = ""
    try:
        check_update = os.environ['qlnwctupdate']
    except:
        check_update = ""

    if check_update == "true":
        update()
    else:
        print("变量qlnwctupdate未设置，脚本自动更新未开启！")

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