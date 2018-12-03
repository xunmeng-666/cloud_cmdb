# -*- coding:utf-8-*-

from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from cmdbApi import views

urlpatterns = format_suffix_patterns([
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^idc/$',views.IdcList.as_view(),name='idc-list'),
    url(r'^idc/(?P<pk>[0-9]+)/$',views.IdcDetail.as_view(),name='idc-detail'),
    url(r'^cabint/$',views.CabintList.as_view(),name='cabint-list'),
    url(r'^cabint/(?P<pk>[0-9]+)/$',views.CabintDetail.as_view(),name='cabint-detail'),
    url(r'^server/$',views.ServerList.as_view(),name='server-list'),
    url(r'^server/(?P<pk>[0-9]+)/$', views.ServerDetail.as_view(), name='servers-detail'),
    url(r'^group/$',views.GroupList.as_view(),name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$',views.GroupDetail.as_view(),name='group-detail'),
    url(r'^company/$',views.CompanyList.as_view(),name='company-list'),
    url(r'^company/(?P<pk>[0-9]+)/$',views.CompanyDetail.as_view(),name='company-detail'),
    url(r'^warranty/$',views.warrantyList.as_view(),name='warranty-list'),
    url(r'^warranty/(?P<pk>[0-9]+)/$',views.warrantyDetail.as_view(),name='warranty-detail'),
    url(r'^nic/$',views.NicList.as_view(),name='nic-list'),
    url(r'^nic/(?P<pk>[0-9]+)/$',views.NicDetail.as_view(),name='nic-detail'),
    url(r'^bonding/$',views.BondingList.as_view(),name='bonding-list'),
    url(r'^bonding/(?P<pk>[0-9]+)/$',views.BondingDetail.as_view(),name='bonding-detail'),
    url(r'^ram/$',views.RamList.as_view(),name='ram-list'),
    url(r'^ram/(?P<pk>[0-9]+)/$',views.RamDetail.as_view(),name='ram-detail'),
    url(r'^disk/$',views.DiskList.as_view(),name='disk-list'),
    url(r'^disk/(?P<pk>[0-9]+)/$',views.DiskDetail.as_view(),name='disk-detail'),
    url(r'^cpu/$',views.CpuList.as_view(),name='cpu-list'),
    url(r'^cpu/(?P<pk>[0-9]+)/$',views.CpuDetail.as_view(),name='cpu-detail'),
    url(r'^device/$',views.DeviceList.as_view(),name='device-list'),
    url(r'^device/(?P<pk>[0-9]+)/$',views.DeviceDetail.as_view(),name='device-detail'),
    url(r'^protocol/$',views.ProtocolList.as_view(),name='protocol-list'),
    url(r'^protocol/(?P<pk>[0-9]+)/$',views.ProtocolDetail.as_view(),name='protocol-detail'),
    # url(r'^bonding/$', views.BondingList.as_view(), name='router-list'),
    # url(r'^router/(?P<pk>[0-9]+)/$',views.RouterDetail.as_view(), name='router-detail'),

    # url(r'^gfw/$',views.GFWList.as_view(),name='gfw-list'),
    # url(r'^gfw/(?P<pk>[0-9]+)/$',views.GFWDetail.as_view(),name='gfw-detail'),

    # url(r'^task/$',views.TaskList.as_view(),name='task-list'),
    # url(r'^task/(?P<pk>[0-9]+)/$',views.TaskDetail.as_view(),name='task-detail'),

])