# -*- coding: UTF-8 -*-
# Version: v1.1
# Created by lstcml on 2022/08/08
# 建议定时60分钟：*/60 * * * *

'''
更新记录：
v1.1
1、自动安装必要模块；
2、支持自定义域名前缀；
'''
'''
cron: */60 * * * *
new Env('localtunnel内网穿透');
'''
import os
import re
import sys
import requests
from time import sleep

def update():
    print("当前运行的脚本版本：" + str(version))
    sys.stdout.flush()
    try:
        r1 = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/chuantou.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            sys.stdout.flush()
            os.system("ql raw https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/main/chuantou.py &")
            os._exit()
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
            
# 进程守护
def process_daemon():
    global qlurl
    qlurl = get_url()
    try:
        res = requests.get(qlurl + "/login").text
        if "/images/g5.ico" in res:
            return True
        else:
            return False
    except:
        return False

# 获取穿透url
def get_url():
    try:
        with open('localtunnel.lstcml', encoding='utf-8') as f:
            _content = f.read()
            if 'your url is' in _content:
                print("获取穿透链接成功...")
                sys.stdout.flush()
                return _content.split(': ')[1].replace('\n','')
            else:
                return 'https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/'
    except:
        return 'https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/'

# 执行程序
def start_nwct(parameter):
    if not process_daemon():
        if parameter == 1:
            os.system('lt --port 5700 > localtunnel.lstcml &')
        else:
            os.system('lt --port 5700 -s ' + subdomain + ' > localtunnel.lstcml &')
        print("正在启动内网穿透...")
        sleep(10)
        print("正在检测穿透状态...")
        sys.stdout.flush()
        if process_daemon():
            if load_send():
                print("启动内网穿透成功！\n公众号：一起瞎折腾\n青龙面板：%s" % qlurl)
                print("若访问穿透地址出现安全检测界面，点击蓝色'Click to Continue'按钮可跳过！")
                sys.stdout.flush()
                send("内网穿透通知", "青龙面板访问地址：" + qlurl)
        else:
            print("启动内网穿透失败...")
            sys.stdout.flush()
    else:
        print("穿透程序已在运行...\n公众号：一起瞎折腾\n青龙面板：%s" % qlurl)
        sys.stdout.flush()
        
# 推送
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/jiankujidu/chuantou/raw/master/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)
        
    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False

if __name__ == '__main__':
    version = 1.1
    try:
        subdomain = os.environ['qlsubdomain']
    except:
        subdomain = ""
    try:
        check_update = os.environ['qlnwctupdate']
    except:
        check_update = "true"
    try:
        import requests
    except:
        os.system('pip3 install requests >/dev/null 2>&1')
 
    if check_update != "false":
        update()
    else:
        print("变量qlnwctupdate未设置，脚本自动更新未开启！")
        sys.stdout.flush()
    if os.system('lt --help >/dev/null 2>&1') !=0:
        os.system('npm install -g localtunnel >/dev/null 2>&1')
    if len(subdomain) < 1:
        print("变量qlsubdomain未设置，将随机分配域名前缀！")
        sys.stdout.flush()
        start_nwct(1)
    else:
        if other_character(subdomain):
            start_nwct(2)
        else:
            print("变量qlsubdomain仅支持英文数字组合！")
    