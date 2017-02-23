#! /usr/bin/env python
# coding=utf-8
import requests
import sqlite3
import datetime
import re
import json
from bs4 import BeautifulSoup
from BigSpider_app.DataBase import mysql_options,mongodb_options
from throttle import Throttle
import proxyutil

# 保存到数据库
def saveToSqlite(spider_info,id):
    # 获取spider_info字典中的信息
    usr_id = spider_info["usr_id"]
    goods_id = spider_info["goods_id"]
    referenceName = spider_info["referenceName"]
    content = spider_info["content"]
    score = spider_info["score"]
    creationTime = spider_info["creationTime"]
    site_id = id
    # 连接数据库并插入相应数据
    mongodb_conn = mongodb_options.mongodb_init_uestc()
    print "-------------->"
    print id
    mongodb_options.insert_goods_comments(mongodb_conn,usr_id,goods_id,referenceName,content,score,creationTime,site_id)

# 抓取京东商品主函数
def startGrab(goods_id,id):
    #判断是否末页
    flag = True
    # 所有页面的BaseURL
    base_url = "http://s.club.jd.com/productpage/p-"+goods_id+"-s-0-t-0-p-"
    # 当前页码
    page_number = 0
    headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"
                        , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}


    while flag:
        url = base_url + str(page_number)+".html"
        proxy = proxyutil.getProxy()
        print proxy
        # 可能因为超时等网络问题造成异常，需要捕获并重新抓取
        try:
            print url
            #throttle = Throttle(delay=1000)
            #throttle.wait(url)
            page = requests.get(url,headers=headers,proxies={'http': 'http://%s' % proxy})
        except:
            continue
        if page.text:
            print len(page.text)
            print "============start=========="
            goods_infos = json.loads(page.text)
            comment_list = goods_infos["comments"]
            for comment_info in comment_list:
                usr_id = comment_info["id"]
                goods_id = comment_info["referenceId"]
                referenceName = comment_info["referenceName"]
                content = comment_info["content"]
                score = comment_info["score"]
                creationTime = comment_info["creationTime"]
                spiderinfo = {"usr_id":usr_id,"goods_id":goods_id,"referenceName":referenceName,"content":content,"score":score,"creationTime":creationTime}
                saveToSqlite(spiderinfo,id)
                print usr_id
            #comments_info = json.decode(soup)
            if comment_list:
                flag = True
            else:
                flag = False
            page_number = page_number + 1
            print page_number
            
            print "============end=========="
        else:
            break





