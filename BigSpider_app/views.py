#! /usr/bin/env python
# coding=utf-8
import os
import uuid
import time

from BigSpider import spiderserver
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from BigSpider_app.DataBase import mysql_options, redis_options, mongodb_options

db = mongodb_options.mongodb_init_spider_ms()
uestc = mongodb_options.mongodb_init_uestc()
uestc_redis = redis_options.redis_init()
# mysql_conn = mysql_options.mysql_init()


# 在url.py中，网页中名称 view中名称 html网页中名称
def pre_index(request):
    return render(request, 'pre_index.html')


# 用户页面
def index(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        # 从redis中读取当前爬虫队列长度（爬取的url）
        crawling_queue = redis_options.crawling_queue(uestc_redis)

        # 从mongo中的读取爬取成功的数据数量（文章等）
        crawling_succeed_num = mongodb_options.crawling_succeed_num(uestc)

        return render(request, 'index.html', {'login_user': username, 'flag': flag, 'crawling_queue': crawling_queue,
                                              'crawling_succeed_num': crawling_succeed_num})
    else:
        return render(request, 'index.html', {'flag': flag})

# 站点管理部分 by Prince_CHEN
def site_management(request):
    mysql_conn = mysql_options.mysql_init()
    flag = False
    myid=[]
    if "username" in request.session:
        username = request.session['username']
        flag = True

    if flag:
        site_list = mysql_options.get_site_info(mysql_conn)
        for list in site_list:
            myid.append(list[0])
        return render(request, 'site_management.html', {'login_user': username, 'flag': flag, 'site_list': site_list, 'myid': myid})
        # return render(request, 'site_management.html', {'login_user': username, 'flag': flag})
    else:
        return render(request, 'site_management.html', {'flag': flag})

#运行爬虫
def do_run(request):
    mysql_conn = mysql_options.mysql_init()
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        id = request.GET['run_id']
        sit_data = mysql_options.get_site_info_by_id(mysql_conn,id)
        try:
            spiderserver.spider_server(sit_data,id)
        except expression as e:
            print "SpiderERROR:"+e
        finally:
            if sit_data[3] == "jingdongpinglun":
                crawling_number = mongodb_options.crawling_jingdong_comments_succeed_num_by_id(uestc,id)
            else:
                crawling_number = mongodb_options.crawling_succeed_num_by_id(uestc,id)
            print sit_data
            name = sit_data[0]
            keyword = sit_data[2]
            overtime = time.time()
            site_id = id
            mysql_options.add_spiderinfo(mysql_conn,name,keyword,overtime,crawling_number,site_id)
            return render(request, 'index.html', {'flag': flag})
    else:
        return render(request, 'index.html', {'flag': flag})

#获取单次爬虫的详细数据
def do_detail(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        id = request.GET['detail_id']
        sit_data = mysql_options.get_site_info_by_id(mysql_conn,id)
        if sit_data[3] == "jingdongpinglun":
            crawling_info = mongodb_options.crawling_jingdong_comments_web_info_by_id(uestc,id)
        else:
            crawling_info = mongodb_options.crawling_web_info_by_id(uestc,id) 
        return render(request, 'crawling_detail.html', {'flag': flag,'crawlingInfo':crawling_info})
    else:
        return render(request, 'index.html', {'flag': flag})

# 删除选中的站点 by Prince_CHEN 2016.10.09
def delete_siteall(request):
    mysql_conn = mysql_options.mysql_init()
    ids=request.GET['del_ids']
    # print ids
    myid = []
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True

    if flag:
        if ids:
            ids = ids.split(',')
            # print ids
            result = mysql_options.delete_site_by_id(mysql_conn, ids)
            site_list = mysql_options.get_site_info(mysql_conn)
            for list in site_list:
                myid.append(list[0])
            if result:
                mymessage = "<script>alert('删除成功!')</script>"
                return render(request, 'site_management.html', {'message': mymessage, 'flag': flag,'site_list':site_list,'myid': myid})
            else:
                mymessage = "<script>alert('删除失败!')</script>"
                return render(request, 'site_management.html', {'message': mymessage, 'flag': flag,'site_list':site_list,'myid': myid})
        else:
            site_list = mysql_options.get_site_info(mysql_conn)
            for list in site_list:
                myid.append(list[0])
            mymessage = "<script>alert('请选择一个站点删除!')</script>"
            return render(request, 'site_management.html', {'message': mymessage, 'flag': flag,'site_list':site_list,'myid': myid})
    else:
        return render(request, 'spiders_management.html', {'flag': flag})


# 修改站点信息 by Prince_CHEN
def do_update(request):
    mysql_conn = mysql_options.mysql_init()
    myid = request.GET['site_id']
    name = request.GET['name']
    url = request.GET['start_urls']
    rule = request.GET['extract_from']
    # print myid,name,url,rule
    result = mysql_options.update_site_info(mysql_conn, myid, name, url, rule)
    print result
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        myid = []
        site_list = mysql_options.get_site_info(mysql_conn)
        for list in site_list:
            myid.append(list[0])
        if result:
            updatemessage = "<script>alert('修改成功!')</script>"
            return render(request, 'site_management.html',
                          {'message': updatemessage, 'flag': flag, 'site_list': site_list, 'myid': myid})
        else:
            updatemessage = "<script>alert('修改失败!')</script>"
            return render(request, 'site_management.html',
                          {'message': updatemessage, 'flag': flag, 'site_list': site_list, 'myid': myid})
    else:
        return render(request, 'spiders_management.html', {'flag': flag})

# 添加站点 by Prince_CHEN
def do_add_site(request):
    name = request.GET['name']
    url = request.GET['start_urls']
    rule = request.GET['extract_from']
    firstsit = request.GET['firstsit']
    mysql_conn = mysql_options.mysql_init()
    result = mysql_options.add_site(mysql_conn, name, url, rule,firstsit)
    if "username" in request.session:
        username = request.session['username']
        flag = True

    if flag:
        myid = []
        site_list = mysql_options.get_site_info(mysql_conn)
        for list in site_list:
            myid.append(list[0])
        if result:
            addMessage = "<script>alert('添加成功!')</script>"
            return render(request, 'site_management.html',
                          {'message': addMessage, 'flag': flag, 'site_list': site_list, 'myid': myid})
        else:
            addMessage = "<script>alert('添加失败!')</script>"
            return render(request, 'site_management.html',
                          {'message': addMessage, 'flag': flag, 'site_list': site_list, 'myid': myid})
    else:
        return render(request, 'spiders_management.html', {'flag': flag})


def spiders_management(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True

        # 启动爬虫
        # os.chdir('/home/double/project/generic-master/generic')  # 切换到安装路径
        # os.system('python run.py')  # 执行run.py 文件
        # print "启动爬虫成功"
    if flag:
        return render(request, 'spiders_management.html', {'login_user': username, 'flag': flag})
    else:
        return render(request, 'spiders_management.html', {'flag': flag})


def timing_monitoring(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def log_management(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        return render(request, 'log_management.html', {'login_user': username, 'flag': flag})
    else:
        return render(request, 'log_management.html', {'flag': flag})


def crawling_info(request):
    crawling_list = []
    mysql_conn = mysql_options.mysql_init()
    flag = False
    # web_info = []
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        crawling_web_info = mysql_options.get_spiderinfo_info(mysql_conn)
        for crawling_info in crawling_web_info:
            over_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(crawling_info[3]))
            crawling_info = (crawling_info[1],crawling_info[2],crawling_info[4],crawling_info[5],over_time)
            crawling_list.append(crawling_info)
        # for info in crawling_web_info:
        # url = info['url'].replace("?touping=", "")
        # info['url'] = url
        # web_info.append(info)
        # return render(request, 'crawling_info.html', {'login_user': username, 'crawling_web_info': web_info, 'crawling_succeed_num':crawling_succeed_num, 'flag': flag})
        return render(request, 'crawling_info.html', {'login_user': username, 'crawling_web_info': crawling_list,'flag': flag})
    else:
        return render(request, 'crawling_info.html', {'flag': flag})


def about(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        return render(request, 'about.html', {'login_user': username, 'flag': flag})
    else:
        return render(request, 'about.html', {'flag': flag})


def contact(request):
    flag = False
    if "username" in request.session:
        username = request.session['username']
        flag = True
    if flag:
        return render(request, 'contact.html', {'login_user': username, 'flag': flag})
    else:
        return render(request, 'contact.html', {'flag': flag})


def req_register(request):
    return render(request, 'register.html')


def register(request):
    userid = str(uuid.uuid1())
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    phone_num = request.POST['phone_num']
    user = mongodb_options.find_user_by_username(db, username)
    if not user:
        mongodb_options.insert_user(db, userid, username, password, email, phone_num)
        return render(request, 'index.html',
                      {'message': '<script type="text/javascript">alert("恭喜您,注册成功了！");</script>'})
    else:
        return render(request, 'register.html', {'message': '用户名已被注册了'})


def req_login(request):
    return render(request, 'login.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print "------>"+username
    user = mongodb_options.find_user_by_username_password(db, username, password)
    print "################"+str(user)
    if user:
        request.session['username'] = username
        return HttpResponseRedirect('/index')
    else:
        return render(request, 'login.html', {'login_message': '用户名和密码不一致'})


def logout(request):
    username = ''
    if "username" in request.session:
        username = request.session['username']
    if not username == '':
        del request.session['username']
        return HttpResponseRedirect('/index')
    else:
        return render(request, 'index.html',
                      {'message': '<script type="text/javascript">alert("您还没登录，无法注销！");</script>'})


# 管理员页面
def req_admin_login(request):
    return render(request, 'admin_login.html')


def admin_login(request):
    admin_name = request.POST['admin_name']
    admin_psd = request.POST['admin_psd']
    admin = mongodb_options.find_admin_by_name_psd(db, admin_name, admin_psd)
    if admin:
        request.session['admin_name'] = admin_name
        users_list = mongodb_options.admin_find_all_users(db)
        return render(request, 'admin_index.html', {'admin_name': admin_name, 'users_list': users_list, 'flag': True})
    else:
        return render(request, 'admin_login.html', {'login_message': '用户名和密码不一致'})


def admin_logout(request):
    admin_name = ''
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
    if not admin_name == '':
        del request.session['admin_name']
        return HttpResponseRedirect('/index')
    else:
        return render(request, 'index.html',
                      {'message': '<script type="text/javascript">alert("您还没登录，无法注销！");</script>'})


def admin_index(request):
    flag = False
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
        flag = True

    if flag:
        return render(request, 'admin_index.html', {'admin_name': admin_name, 'flag': flag})
    else:
        return render(request, 'admin_login.html', {'flag': flag})


def admin_manage_users(request):
    flag = False
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
        flag = True
    users_list = mongodb_options.admin_find_all_users(db)
    admin_list = mongodb_options.admin_find_all(db)
    if flag:
        return render(request, 'admin_manage_users.html',
                      {'admin_name': admin_name, 'users_list': users_list, 'admin_list': admin_list, 'flag': flag})
    else:
        return render(request, 'admin_login.html', {'flag': flag})


def admin_delete_user(request):
    flag = False
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
        flag = True
    if flag:
        userid = request.GET['userid']
        mongodb_options.admin_delete_user(db, userid)
        users_list = mongodb_options.admin_find_all_users(db)
        return render(request, 'admin_index.html', {'admin_name': admin_name, 'users_list': users_list, 'flag': flag})
    else:
        return render(request, 'admin_login.html', {'flag': flag})


def admin_req_modify_user(request):
    flag = False
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
        flag = True
    if flag:
        userid = request.GET['userid']
        user = mongodb_options.admin_find_one_user_byuserid(db, userid)

        return render(request, 'admin_modify_user.html', {'admin_name': admin_name, 'user': user, 'flag': flag})
    else:
        return render(request, 'admin_login.html', {'flag': flag})


def admin_modify_user(request):
    flag = False
    if "admin_name" in request.session:
        admin_name = request.session['admin_name']
        flag = True
    if flag:
        userid = request.POST['userid']
        username = request.POST['username']
        email = request.POST['email']
        phone_num = request.POST['phone_num']
        remark = request.POST['remark']
        mongodb_options.admin_update_user(db, userid, username, email, phone_num, remark)
        users_list = mongodb_options.admin_find_all_users(db)
        admin_list = mongodb_options.admin_find_all(db)
        return render(request, 'admin_manage_users.html', {'admin_name': admin_name, 'users_list': users_list, 'admin_list': admin_list, 'flag': flag})
    else:
        return render(request, 'admin_login.html', {'flag': flag})
