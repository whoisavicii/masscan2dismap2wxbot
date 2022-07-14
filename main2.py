#coding:utf-8

import os
import requests



def masscan():
    os.system('masscan -iL ip.txt -p1-65535 -oL masscannewtmp.txt --rate=20000')

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

def dismap():
    addfile = open("newResult.txt", "r")
    addfile.seek(0)
    addlist = []
    for line in addfile:
        addlist.append(line.strip())
    addfile.close()
    for i in addlist:
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
    dismap()
    wx_post('allportresult.csv')


if __name__ == '__main__':
    main()
    os.system('rm -rf masscannewtmp.txt')
    os.system('rm -rf allportresult.csv')

