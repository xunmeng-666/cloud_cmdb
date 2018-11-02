# -*- coding:utf-8-*-

from django.conf.urls import url
from cmdbServer import views

urlpatterns = [
    url(r'^/',views.index),
    url(r'^idc/$',views.idc),
    url(r'^cabint/$',views.cabint),
    url(r'^(\w+)/(\w+)/add/$',views.add_idc),
    url(r'^(\w+)/(\w+)/del/$',views.del_idc),
    url(r'^(\w+)/(\w+)/del/$',views.edit_idc),
    url(r'^(\w+)/(\w+)/upload/$',views.uploadfile,name='uploadfile'),
    url(r'^(\w+)/(\w+)/download/$',views.downloadfile,name='downloadfile'),
]
