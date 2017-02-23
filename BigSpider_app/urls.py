# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.pre_index, name='pre_index'),
    # url(r'^index$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^req_register/$', views.req_register, name='req_register'),
    url(r'^register/$', views.register, name='register'),
    url(r'^req_login/$', views.req_login, name='req_login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^site_management/$', views.site_management, name='site_management'),
    url(r'^do_run/$',views.do_run, name='do_run'),
    url(r'^do_detail/$',views.do_detail, name='do_detail'),
    url(r'^spiders_management/$', views.spiders_management, name='spiders_management'),
    url(r'^timing_monitoring/$', views.timing_monitoring, name='timing_monitoring'),
    url(r'^log_management/$', views.log_management, name='log_management'),
    url(r'^crawling_info/$', views.crawling_info, name='crawling_info'),
    url(r'^req_admin_login/$', views.req_admin_login, name='req_admin_login'),
    url(r'^admin_login/$', views.admin_login, name='admin_login'),
    url(r'^admin_logout/$', views.admin_logout, name='admin_logout'),
    url(r'^admin_index/$', views.admin_index, name='admin_index'),
    url(r'^admin_manage_users/$', views.admin_manage_users, name='admin_manage_users'),
    url(r'^admin_delete_user/$', views.admin_delete_user, name='admin_delete_user'),
    url(r'^admin_req_modify_user/$', views.admin_req_modify_user, name='admin_req_modify_user'),
    url(r'^admin_modify_user/$', views.admin_modify_user, name='admin_modify_user'),

    # 站点管理部分 by Prince_CHEN 2016.10.09
    url(r'^delete_siteall/$', views.delete_siteall, name='delete_siteall'),
    url(r'^do_update$', views.do_update, name='do_update'),
    url(r'^do_add_site$', views.do_add_site, name='do_add_site'),
]