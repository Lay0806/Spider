#! /usr/bin/env python
# coding=utf-8
import requests
import sqlite3
import datetime
import re
from bs4 import BeautifulSoup
from BigSpider_app.DataBase import mysql_options,mongodb_options

# 保存到数据库
def saveToSqlite(spider_info,id):
    # 获取spider_info字典中的信息
    title = spider_info['title']
    context = spider_info['context']
    url = "tieba.baidu.com"+spider_info['url']
    auther = spider_info['auther']
    create_time = spider_info['create_time']
    site_id = id
    # 连接数据库并插入相应数据
    mongodb_conn = mongodb_options.mongodb_init_uestc()
    print "-------------->"
    print id
    result1 = mongodb_options.insert_crawlinginfo(mongodb_conn,title,context,url,auther,create_time,id)

# 抓取主函数
def startGrab(url,id):
    #判断是否末页
    flag = True
    # 所有页面的BaseURL
    base_url = url
    # 当前页码
    page_number = 0
    headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"
                        , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}

    while flag:
        url = base_url + str(page_number)

        # 可能因为超时等网络问题造成异常，需要捕获并重新抓取
        try:
            page = requests.get(url,headers)
        except:
            continue

        # 使用BeautifulSoup规范化网页并生成对象
        print "============start=========="
        soup = BeautifulSoup(page.content)
        print "============end=========="
        spider_result = soup.find_all("div",class_ = "t_con")
        for item in spider_result:  
            try:
                title = item.find("div",{"class":"j_threadlist_li_right"}).find("a",{"class": "j_th_tit"}).get("title")
                context = item.find("div",{"class":"j_threadlist_li_right"}).find("div",{"class": "threadlist_abs"}).text
                url = item.find("div",{"class":"j_threadlist_li_right"}).find("a",{"class": "j_th_tit"}).get("href")
                auther = item.find("div",{"class":"j_threadlist_li_right"}).find("a",{"class": "frs-author-name"}).text
                create_time = item.find("div",{"class":"j_threadlist_li_right"}).find("span",{"class": "is_show_create_time"}).text
                spiderinfo = {"title":title,"context":context,"url":url,"auther":auther,"create_time":create_time}
                saveToSqlite(spiderinfo,id)
            except:
                pass
        pattern = re.compile('next pagination-item', re.S)
        result = re.search(pattern, page.content)
        if result:
            flag = True
        else:
            flag = False
        page_number = page_number + 50
        print page_number
