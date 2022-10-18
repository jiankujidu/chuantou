# -*- coding: UTF-8 -*-
# 建议定时60分钟：*/60 * * * *

'''
cron: */10 * * * *
new Env('Cpolar内网穿透');
'''
import os, requests
n = os.popen("ps -ef | grep frpc").read()
command = "/root/frp/frpc -c /root/frp/frpc.ini"
if command not in n:
    print("正在启动FRPC.")
    os.system(command + ">/dev/null 2>&1 &")
    n = os.popen("ps -ef | grep frpc").read()
    if command not in n:
        print("公众号:一起瞎折腾\nQQ群:170095764\n启动FRPC失败...")
    else:
        print("公众号:一起瞎折腾\nQQ群:170095764\n启动FRPC成功...")
else:
    print("公众号:一起瞎折腾\nQQ群:170095764\nFRPC已运行中...")