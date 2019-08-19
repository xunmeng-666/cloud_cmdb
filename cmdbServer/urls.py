# -*- coding:utf-8-*-

from django.conf.urls import url
from cmdbServer import views

urlpatterns = [
    url(r'^/',views.index),
    url(r'^idc/$',views.idc),
    url(r'^cabint/$',views.cabint),
    url(r'^company/$',views.company),
    url(r'^device/$',views.device),
    url(r'^servers/$',views.server),
    url(r'^protocol/$',views.protocol),
    url(r'^group/$',views.device_group),
    url(r'^warranty/$',views.warranty),
    url(r'^cpu/$',views.cpu),
    url(r'^disk/$',views.disk),
    url(r'^ram/$',views.ram),
    url(r'^nic/$',views.nic),
    url(r'^bonding/$',views.bonding),
    url(r'^application/$',views.apps),
    url(r'^tasks/$',views.tasks),
    url(r'^tasks/history/$',views.taskHistory),
    url(r'^tasks/result/$',views.result),
    url(r'^(\w+)/download/$',views.downPlaybook),
    url(r'^task_websocket/$',views.tasks_websocket),
    url(r'^logs/$',views.logs),
    url(r'^(\w+)/(\w+)/add/$',views.table_obj_add),
    url(r'^(\w+)/(\w+)/del/$',views.table_obj_del),
    url(r'^(\w+)/(\w+)/change/$',views.table_obj_change,name='editobject'),
    url(r'^(\w+)/(\w+)/upload/$',views.uploadfile,name='uploadfile'),
    url(r'^(\w+)/(\w+)/download/$',views.downloadfile,name='downloadfile'),
    url(r'^(\w+)/(\w+)/detail/$',views.table_obj_detail,name='detail'),
]
