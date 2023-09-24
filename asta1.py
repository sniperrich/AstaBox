import tkinter as tk
from tkinter import messagebox
import requests
import parsel
import uuid
import time
import random
import os
import webbrowser
import base64
import json
import binascii
import random
import string
from urllib import parse
from Crypto.Cipher import AES

def getsong(songname):
    def get_random():
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        return random_str

    # AES加密要求加密的文本长度必须是16的倍数，密钥的长度固定只能为16,24或32位，因此我们采取统一转换为16位的方法
    def len_change(text):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        text = text.encode("utf-8")
        return text

    # AES加密方法
    def aes(text, key):
        # 首先对加密的内容进行位数补全，然后使用 CBC 模式进行加密
        iv = b'0102030405060708'
        text = len_change(text)
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(text)
        encrypt = base64.b64encode(encrypted).decode()
        return encrypt

    # js中的 b 函数，调用两次 AES 加密
    # text 为需要加密的文本， str 为生成的16位随机数
    def b(text, str):
        first_data = aes(text, '0CoJUm6Qyw8W8jud')
        second_data = aes(first_data, str)
        return second_data

    # 这就是那个巨坑的 c 函数
    def c(text):
        e = '010001'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        text = text[::-1]
        result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
        return format(result, 'x').zfill(131)

    # 获取最终的参数 params 和 encSecKey 的方法
    def get_final_param(text, str):
        params = b(text, str)
        encSecKey = c(str)
        return {'params': params, 'encSecKey': encSecKey}

    # 通过参数获取搜索歌曲的列表
    def get_music_list(params, encSecKey):
        url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

        payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
        headers = {
            'authority': 'music.163.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/search/',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    # 通过歌曲的id获取播放链接
    def get_reply(params, encSecKey):
        url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
        payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
        headers = {
            'authority': 'music.163.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    if __name__ == '__main__':
        song_name = songname
        d = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song_name, "type": "1", "offset": "0",
             "total": "true", "limit": "30", "csrf_token": ""}
        information=list()
        d = json.dumps(d)
        random_param = get_random()
        param = get_final_param(d, random_param)
        song_list = get_music_list(param['params'], param['encSecKey'])
        print('搜索结果如下：')
        if len(song_list) > 0:
            song_list = json.loads(song_list)['result']['songs']
            for i, item in enumerate(song_list):
                item = json.dumps(item)
                print(str(i) + "：" + json.loads(str(item))['name'])
                d = {"ids": "[" + str(json.loads(str(item))['id']) + "]", "level": "standard", "encodeType": "",
                     "csrf_token": ""}
                d = json.dumps(d)
                param = get_final_param(d, random_param)
                song_info = get_reply(param['params'], param['encSecKey'])
                if len(song_info) > 0:
                    song_info = json.loads(song_info)
                    song_url = json.dumps(song_info['data'][0]['url'], ensure_ascii=False)
                    print(song_url)
                else:
                    print("该首歌曲解析失败，可能是因为歌曲格式问题")
        else:
            print("很抱歉，未能搜索到相关歌曲信息")
def genshinstart():
    webbrowser.open("https://www.qijieya.cn/game/linux/")
def novel(id):
    id = id
    baseUrl = "http://www.zongheng.com/"

    bookId = "https://book.zongheng.com/book/" + id + ".html"

    bookIdDir = bookId.replace("book/", "showchapter/")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    listChild = []
    listDate = []
    mTitle = []
    # 文章链接与标题独立列表
    a_href_list = ["", ""]
    # 存放文章链接与标题数组列表
    a_href_arr = []

    def GetUrl(url):
        html = requests.get(url, headers=headers)
        sel = parsel.Selector(html.text)
        # 获取主Title
        mTitle.append(sel.css(".book-meta h1::text").getall()[0])
        os.mkdir("./" + mTitle[0] + "/", mode=0o777)
        print(mTitle)
        # 获取文章url列表
        href = sel.css(".volume-list ul a::attr(href)").getall()
        # 获取标题
        text = sel.css(".volume-list ul a::text").getall()
        for item1, item2 in zip(href, text):
            a_href_list = ["", ""]
            a_href_list[0] = item1
            a_href_list[1] = item2
            a_href_arr.append(a_href_list)

    def GetTxt(url, title):
        print(url)
        print(mTitle)
        print(title)
        html = requests.get(url, headers=headers)
        sel = parsel.Selector(html.text)
        # 文章
        infoDate = []
        info = sel.css(".content p::text").getall()
        for item in info:
            infoDate.append(item + "\r\n")
        title = str(title).replace(" ", "_")
        title = str.format("{0}/{1}.txt", mTitle[0], title)
        with open(title, "w+", encoding="utf-8") as f:
            f.write("".join(infoDate))
            f.close()
        print(title, "保存完毕")

    GetUrl(bookIdDir)

    for item in a_href_arr:
        GetTxt(item[0], item[1])
        time.sleep(random.uniform(0.5, 1.5))
def getsongname():
    win=tk.Tk()
    win.geometry("330x100")
    win.resizable(0, 0)
    win.title("音乐")
    e2 = tk.Entry(win)
    e2.pack()
    def gete2():
        sn=e2.get()
        getsong(sn)
    b5=tk.Button(win,text="confirm",command=gete2)
    b5.pack()
    win.mainloop()
def getId():
    messagebox.showinfo(message="请在纵横网上寻找心仪的小说哦",title="666")
    webbrowser.open("https://www.zongheng.com/")
    root = tk.Tk()

    root.geometry("330x100")
    root.resizable(0,0)
    root.title("小说")
    e1=tk.Entry(root)
    e1.pack()
    def gete1():
        num=e1.get()
        try:
            novel(num)

        except:
            messagebox.showerror(title="失败，请重试",message="失败，请重试")
        else:
            messagebox.showinfo(title="下载开始", message="下载开始")
    l3=tk.Label(root,text="请输入纵横小说网id 就是书的介绍界面detail后面的那串数字")
    l3.pack()
    l4=tk.Label(root,text="未响应就是开始下载 下载的text在程序同目录")
    l4.pack()
    b4=tk.Button(root,text="确定",command=gete1)
    b4.pack()

    root.mainloop()
window=tk.Tk()
window.geometry("450x300")
window.title("Asta")
window.resizable(0,0)
l1=tk.Label(window,text="Welcome to",font=("Consolas",30))
l1.place(x=20,y=60)
l2=tk.Label(window,text="Asta",font=("Freestyle Script",60))
l2.place(x=20,y=100)
lf1 = tk.LabelFrame(window,text="Function")
lf1.place(x=290,y=18)
b1=tk.Button(lf1,text="Novel",font=("Impact",15),command=getId)
b1.pack(padx=20,pady=15)
b2=tk.Button(lf1,text="Music",font=("Impact",15),command=getsongname)
b2.pack(padx=20,pady=15)
b3=tk.Button(lf1,text="Genshin",font=("Impact",15),command=genshinstart)
b3.pack(padx=20,pady=15)




window.mainloop()