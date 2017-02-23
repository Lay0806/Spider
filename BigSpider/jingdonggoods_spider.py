#! /usr/bin/env python
# coding=utf-8
import requests
import sqlite3
import datetime
import re
from bs4 import BeautifulSoup
from BigSpider_app.DataBase import mysql_options,mongodb_options
from throttle import Throttle
import proxyutil

# 保存到数据库
def saveToSqlite(spider_info,id):
    # 获取spider_info字典中的信息
    jingdong_good_id = spider_info['goods_id']
    site_id = id
    # 连接数据库并插入相应数据
    mongodb_conn = mongodb_options.mongodb_init_uestc()
    print "-------------->"
    print id
    mongodb_options.insert_goods_id(mongodb_conn,jingdong_good_id,site_id)

# 抓取京东商品主函数
def startGrab(keyword,id):
    #判断是否末页
    flag = True
    # 所有页面的BaseURL
    base_url = "http://search.jd.com/search?keyword="+keyword+"&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&cid2=653&cid3=655&page="
    # 当前页码
    page_number = 1
    headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"
                        , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}


    while flag:
        url = base_url + str(page_number)
        proxy = proxyutil.getProxy()
        # 可能因为超时等网络问题造成异常，需要捕获并重新抓取
        try:
            #throttle = Throttle(delay=1000)
            #throttle.wait(url)
            page = requests.get(url,headers=headers,proxies={'http': 'http://%s' % proxy})
        except:
            continue

        # 使用BeautifulSoup规范化网页并生成对象
        print "============start=========="
        soup = BeautifulSoup(page.content)
        print "============end=========="
        spider_result = soup.find_all("li",class_ = "gl-item")
        for item in spider_result:  
            try:
                goods_id = item.get("data-pid")
                spiderinfo = {"goods_id":goods_id}
                saveToSqlite(spiderinfo,id)
            except:
                pass
        if spider_result:
            flag = True
        else:
            flag = False
        page_number = page_number + 1
        print page_number




