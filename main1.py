#coding:utf-8

import os
import requests
import json
import time

if os.path.exists('add_ip_port.txt') or os.path.exists('del_ip_port.txt'):
    os.system('rm -rf add_ip_port.txt')
    os.system('rm -rf del_ip_port.txt')

def masscan():
    os.system('masscan -iL ip.txt -p1-65535 -oL masscannewtmp.txt --rate=2000')

def newresult():
    masscanfile = open("masscannewtmp.txt", "r")
    masscanfile.seek(0)
    for line in masscanfile:
        if line.startswith("#"):
            continue
        if line.startswith("open"):
            line = line.split(" ")
            with open("newResult.txt", "a") as f:
                f.write(line[3]+":"+line[2]+"\n")
                f.close()
                os.system('rm -rf masscannewtmp.txt')
    masscanfile.close()

def compare():
    if os.path.exists('oldResult.txt'):
        oldfile = open("oldResult.txt", "r")
        oldfile.seek(0)
        oldlist = []
        for line in oldfile:
            oldlist.append(line.strip())
        oldfile.close()
        newfile = open("newResult.txt", "r")
        newfile.seek(0)
        newlist = []
        for line in newfile:
            newlist.append(line.strip())
        newfile.close()
        addlist = []
        for i in newlist:
            if i not in oldlist:
                addlist.append(i)
        delfile = open("del_ip_port.txt", "a")
        for i in oldlist:
            if i not in newlist:
                delfile.write(i+"\n")
        delfile.close()
        addfile = open("add_ip_port.txt", "a")
        for i in addlist:
            addfile.write(i+"\n")
        addfile.close()
    else:
        newfile = open("newResult.txt", "r")
        newfile.seek(0)
        newlist = []
        for line in newfile:
            newlist.append(line.strip())
        newfile.close()
        addfile = open("add_ip_port.txt", "a")
        for i in newlist:
            addfile.write(i+"\n")
        addfile.close()
def send_msg():
    if os.path.exists('add_ip_port.txt'):
        addfile = open("add_ip_port.txt", "r")
        addfile.seek(0)
        addlist = []
        for line in addfile:
            addlist.append(line.strip())
        addfile.close()
        for i in addlist:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9xxxxx'
            data = {
                "msgtype": "text",
                "text": {
                    "content": "(部分系统全端口)新开放的IP和端口："+i
                }
            }
            data = json.dumps(data)
            r = requests.post(url, data=data)
            print(r.text)
    if os.path.exists('del_ip_port.txt'):
        delfile = open("del_ip_port.txt", "r")
        delfile.seek(0)
        dellist = []
        for line in delfile:
            dellist.append(line.strip())
        delfile.close()
        for i in dellist:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx'
            data = {
                "msgtype": "text",
                "text": {
                    "content": "(部分系统全端口)关闭的IP和端口："+i
                }
            }
            data = json.dumps(data)
            r = requests.post(url, data=data)
            print(r.text)

def dismap():
    addfile = open("add_ip_port.txt", "r")
    addfile.seek(0)
    addlist = []
    for line in addfile:
        addlist.append(line.strip())
    addfile.close()
    for i in addlist:
        i = i.split(":")
        os.system('./dismap -i '+i[0]+' -p '+i[1]+' --np')

def send_msg_dismap():
    if os.path.exists('output.txt'):
        with open("output.txt", "r") as f:
            for line in f:
                url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx'
                data = {
                    "msgtype": "text",
                    "text": {
                        "content": line
                    }
                }
                data = json.dumps(data)
                r = requests.post(url, data=data)
                print(r.text)

def dismap_old():
    if os.path.exists('oldResult.txt'):
        oldfile = open("oldResult.txt", "r")
        oldfile.seek(0)
        oldlist = []
        for line in oldfile:
            oldlist.append(line.strip())
        oldfile.close()
        for i in oldlist:
            i = i.split(":")
            os.system('./dismap -i '+i[0]+' -p '+i[1]+' --np -o allportresult.csv')




def wx_post(file):
    id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=xxxxx&type=file'  # 上传文件接口地址
    data = {'file': open(file, 'rb')}  # post jason
    response = requests.post(url=id_url, files=data)  # post 请求上传文件
    json_res = response.json()  # 返回转为json
    media_id = json_res['media_id']  # 提取返回ID
    wx_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx'  # 发送消息接口地址
    data = {"msgtype": "file", "file": {"media_id": media_id}}  # post json
    r = requests.post(url=wx_url, json=data)  # post请求消息
    return r  # 返回请求状态
    print(r.text)


def main():
    masscan()
    newresult()
    compare()
    send_msg()
    dismap()
    send_msg_dismap()
    dismap_old()
    wx_post('allportresult.csv')


if __name__ == '__main__':
    main()
    os.system('mv newResult.txt oldResult.txt')
    os.system('rm -rf add_ip_port.txt')
    os.system('rm -rf del_ip_port.txt')
    os.system('rm -rf masscannewtmp.txt')
    os.system('rm -rf output.txt')
    os.system('rm -rf allportresult.csv')

