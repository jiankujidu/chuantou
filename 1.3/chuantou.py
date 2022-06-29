# -*- coding: UTF-8 -*-
# Version: v1.3
# Created by lstcml on 2022/04/01
# 建议定时10分钟：*/10 * * * *
#个人QQ交流群：641307462

import os
import re
import requests
from time import sleep

'''
cron: */10 * * * *
new Env('钉钉内网穿透');
'''
def update():
    print("当前运行的脚本版本：" + str(version ))
    try:
        r1 = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/1.3/chuantou.py").text
        r2 = re.findall(re.compile("version = \d.\d"),r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            os.system("ql raw https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/1.3/chuantou.py &")
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
        res = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/1.3/ngrok.py")
        with open("ngrok.py", "wb") as f:
            f.write(res.content)
    start_nwct()

# 进程守护
def process_daemon(qlurl):
    try:
        res = requests.get(qlurl + "/login").text
        if "/images/g5.ico" in res:
            return "success"
        elif "Unable to initiate connection to" in res:
            return "regustered"
        else:
            return "fail"
    except:
        return "fail"

# 执行程序
def start_nwct():
    qlurl = "http://" + subdomain + ".vaiwan.com"
    if process_daemon(qlurl) != "success":
        os.system("kill -9 `ps -ef | grep 'ngrok.py' | grep -v 'grep' | awk '{print $1}'`")
        os.system("python3 ngrok.py " + subdomain + "&")
        print("启动中...")
        sleep(5)
        r = process_daemon(qlurl)
        if r == "success":
            print("启动成功！\n青龙面板：" + qlurl)
        elif r == "regustered":
            print(subdomain + "已被注册，请重新设置！")
        else:
             print("启动失败！请重试！")
    else:
        print("程序运行中...\n青龙面板：" + qlurl)

if __name__ == '__main__':
    version = 1.3
    update()
    try:
        subdomain = os.environ['qlsubdomain']
    except:
        subdomain = ""
    if len(subdomain) < 1:
        print("请新增变量qlsubdomain指定域名前缀！")
    else:
        if other_character(subdomain):
            download_ngrok()
        else:
            print("变量qlsubdomain仅支持英文数字组合！")
