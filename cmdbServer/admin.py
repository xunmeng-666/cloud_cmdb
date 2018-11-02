from django.contrib import admin

# Register your models here.
from cmdbServer.admin_base import site,BaseAdmin
from cmdbServer import models

class IdcInfoAdmin(BaseAdmin):
    list_display = ("id","name","address","contacts","phone",'remarks')
    list_filter = ["ID","机房名称","机房地址","机房联系人","联系电话","备注"]
    search_fields = ['name','address']

class CabintAdmin(BaseAdmin):
    list_display = ("id","number",'size','room_number','idc')
    list_filter = ["ID","机柜编号","机柜大小","机房编号"]
    search_fields = ['number','size','room','IDC']

class CompanyAdmin(BaseAdmin):
    list_display = ("id",'name','model',"types")
    list_filter = ["ID","厂商","型号","设备类型"]
    search_fields = ['name','model',"types"]


class ProtocolAdmin(BaseAdmin):
    list_display = ("id",'name')
    list_filter = ["ID","协议"]
    search_fields = ['name']

class ApplicationAdmin(BaseAdmin):
    list_display = ("id",'name','version')
    list_filter = ["ID","名称",'版本']
    search_fields = ['name']

class NicAdmin(BaseAdmin):
    list_display = ("id",'sn','name','ipaddress','speed','remarks')
    list_filter = ["ID",'SN',"名称",'IP地址','速率','备注']
    search_fields = ['sn','name','ipaddress','speed','remarks']

class RamAdmin(BaseAdmin):
    list_display = ("id","sn",'company', 'model','size','device_statuses')
    list_filter = ["ID","SN","厂商", '型号','大小','状态']
    search_fields = ['sn','company', 'model', 'device_statuses']

class DiskAdmin(BaseAdmin):
    list_display = ("id","sn",'company', 'model', 'size', 'device_statuses')
    list_filter = ["ID","SN","厂商", '型号', '大小', '状态']
    search_fields = ['sn','company', 'model', 'device_statuses']

class SwitchAdmin(BaseAdmin):
    list_display = ("id",'sn','company','model','nic','ram','ipaddress','cabint','device_statuses','start_date','end_date')
    list_filter = ["ID","SN","厂商",'型号','网卡','内存','IP地址','机柜','状态','开始时间','接收时间']
    search_fields = ["sn",'company','model','ipaddress','cabint','device_statuses']

class RouterAdmin(BaseAdmin):
    list_display = ("id","sn",'company', 'model', 'nic', 'ram', 'ipaddress', 'cabint', 'device_statuses','start_date','end_date')
    list_filter = ["ID","SN","厂商", '型号', '网卡', '内存', 'IP地址', '机柜', '状态','开始时间','接收时间']
    search_fields = ['sn','company', 'model', 'ipaddress', 'cabint', 'device_statuses']

class GfwAdmin(BaseAdmin):
    list_display = ("id","sn",'company', 'model', 'nic', 'ram', 'ipaddress', 'cabint', 'device_statuses','start_date','end_date')
    list_filter = ["ID","SN","厂商", '型号', '网卡', '内存', 'IP地址', '机柜', '状态','开始时间','接收时间']
    search_fields = ['sn','company', 'model', 'ipaddress', 'cabint', 'device_statuses']

class ServersAdmin(BaseAdmin):
    list_display = ("id","sn",'hostname','ipmi_ipaddress','company','model','nic','ram','disk','device_statuses','start_date','end_date')
    list_filter = ["ID","SN","主机名",'IP地址','厂商','型号','网卡','内存','硬盘','状态','开始时间','结束时间']
    search_fields = ["sn",'hostname','ipaddress','device_statuses']

class TaskflowAdmin(BaseAdmin):
    list_display = ('titel','content','proposer','approver','approver_statuses','start_date','end_date')
    list_filter = ['标题','内容','申请人','审批者','审批状态','开始时间','结束时间']
    search_fields = ['titel','proposer','approver','approver_statuses']

site.register(models.IDC,IdcInfoAdmin)
site.register(models.Cabint,CabintAdmin)
# site.register(models.Company,CompanyAdmin)
# site.register(models.Protocol,ProtocolAdmin)
# site.register(models.Application,ApplicationAdmin)
# site.register(models.Nic,NicAdmin)
# site.register(models.Ram,RamAdmin)
# site.register(models.Router,RouterAdmin)
# site.register(models.GFW,GfwAdmin)
# site.register(models.Switch,SwitchAdmin)
# site.register(models.Servers,ServersAdmin)
# site.register(models.Taskflow,TaskflowAdmin)