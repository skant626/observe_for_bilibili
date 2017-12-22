import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
import os
import json
import _thread as thread,queue,time

#连接本地数据库
client = MongoClient()
db = client.bilibili_danmu2
collection = db.items

#获取一个session对象
session = requests.session()

#线程数目

#获得队列对象
cidpagesQueue = queue.Queue()
messagePagesQueue= queue.Queue()
cidQueue = queue.Queue()
messageQueue = queue.Queue()

def CidAidPages(session,aid):
    url = "https://www.bilibili.com/video/av"+str(aid)
    headers = {
                "Host":"www.bilibili.com",
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding":"gzip, deflate, br",
                "Referer":"https://www.bilibili.com/",
                "Cookie":"LIVE_BUVID=AUTO2515129070719029; buvid3=F8AF3CC5-52FD-400B-B720-7152331133A732272infoc; finger=fab92007; sid=c647y304; fts=1513490621; purl_token=bilibili_1513491107; UM_distinctid=1606319a27014f-0a3e7138cbb666-71206751-100200-1606319a271540; CNZZDATA2724999=cnzz_eid%3D758342305-1513487992-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1513493384; pgv_pvi=3759538176; rpdid=olxqqommqmdosokplowxw; pgv_si=s2417956864",
                "Connection":"keep-alive",
                "Upgrade-Insecure-Requests":"1",
                "Cache-Control":"max-age=0",

    }

    r = session.get(url,headers=headers)
    #print(r.text)
    return r
def getCidAidPages(session,aid,count):
    for i in range(count):
        r = CidAidPages(session,aid+i)
        #print(r)
        cidpagesQueue.put(r)
def getCidAid():
    while True:
        try:
            r = cidpagesQueue.get(block=False)
            bsObj = BeautifulSoup(r.text,"html.parser",from_encoding="utf-8")
            cid_aid = bsObj.findAll("div",id="player_placeholder",attrs={"class":"player"})
            cid_aid = [item.split("&")[0] for item in cid_aid[0].next.text.split("=")[1:3]]
            #print(cid_aid)
            cidQueue.put(cid_aid)
        except queue.Empty:
            time.sleep(2)
            #print("cidpagesQueue为空!")
            pass
        except IndexError as e:
            #print("e:",e)
            continue

def getCommentsPages(session):
    while True:
        try:
            cid_aid = cidQueue.get(block=False)
            #print(cid_aid)
            comment_url = "https://comment.bilibili.com/"+str(cid_aid[0])+".xml"
            comment_text = session.get(comment_url)
            #print(comment_text.text)
            commentTextandAid = [comment_text,cid_aid[1]] 
            messagePagesQueue.put(commentTextandAid)
        except queue.Empty:
            #print("cidQueue为空!")
            time.sleep(2)
            pass
def getComments():
    i = 1
    while True:
        try:
            comment_text,aid = messagePagesQueue.get(block=False)
            #print(aid)
            bsObj = BeautifulSoup(comment_text.text,"html.parser",from_encoding="utf-8")
            comments = bsObj.findAll("d")
            for item in comments:
                p = item["p"].split(",")
                #print(item.text)
                messageQueue.put([p,aid,item.text])
            print(i)
            i += 1
        except queue.Empty:
            #print("messagePagesQueue为空!")
            time.sleep(2)
            pass

def saveData(collection):
    while True:
        try:
            p,aid,text = messageQueue.get(block=False)
            #print(p,aid,text)
            collection.insert_one({"aid":aid,
                                   "dtTime":p[0],
                                   "danmu_type":p[1],
                                   "font":p[2],
                                   "color":p[3],
                                   "unix_time":p[4],
                                   "danmuchi":p[5],
                                   "userID":p[6],
                                   "rowID":p[7],
                                   "text":text,
                                   })
            
        except queue.Empty:
            #print("messageQueue为空!")
            time.sleep(2)
            pass
#cid_aid = get_cid_aid(session,item['aid'])
#get_comments(session,cid_aid,collection)
thread.start_new_thread(saveData,(collection,))
thread.start_new_thread(getCidAid,())
thread.start_new_thread(getCommentsPages,(session,))
thread.start_new_thread(getComments,())
thread.start_new_thread(getCidAidPages,(session,17240508,1000,))
time.sleep(3600)


