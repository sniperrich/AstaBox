import requests
import parsel
import uuid
import time
import random
import os
id = input("请输入纵横小说网id 就是书的介绍界面detail后面的那串数字:")
baseUrl = "http://www.zongheng.com/"

bookId = "https://book.zongheng.com/book/"+id+".html"

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
        infoDate.append(item+"\r\n")
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