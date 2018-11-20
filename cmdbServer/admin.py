from django.contrib import admin

# Register your models here.
from cmdbServer.admin_base import site,BaseAdmin
from cmdbServer import models

class IdcInfoAdmin(BaseAdmin):
    list_display = ("id","name","address","contacts","phone",'remarks')
    list_filter = ["ID","机房名称","机房地址","机房联系人","联系电话","备注"]
    export_fields = list_display
    list_per_page = 10
    search_fields = ['name','address']

class CabintAdmin(BaseAdmin):
    list_display = ("id","number",'size','useposition','room_number','idc')
    list_filter = ["ID","机柜编号","机柜大小","已用大小","机房编号","机房"]
    export_fields = ("id","number",'size','room_number','idc')
    list_per_page = 10
    search_fields = ['number','size','room_number','idc__name']

class GroupAdmin(BaseAdmin):
    list_display = ("id","name")
    list_filter = ["ID","组名",]
    list_per_page = 10
    search_fields = ['name']


class CompanyAdmin(BaseAdmin):
    list_display = ("id",'name','model',"types",'height')
    list_filter = ["ID","厂商","型号","设备类型",'设备高度']
    export_fields = list_display
    list_per_page = 10
    search_fields = ['name','model',"types"]

class ProtocolAdmin(BaseAdmin):
    list_display = ("name","number","ipaddress","port_range","device")
    list_filter = ["协议名称","协议号","IP地址","端口范围","设备"]
    export_fields = ["id","name","number","ipaddress","port_range","device"]
    list_per_page = 10
    search_fields = ["name","number","ipaddress","device"]

class NicAdmin(BaseAdmin):
    list_display = ("id",'sn','company','ipaddress','model','mac_address','types','protocol','speed','server','remarks')
    list_filter = ["ID",'SN',"型号",'IP地址','IP地址获取方式','MAC地址','所属设备','VLAN','速率','服务器','备注']
    export_fields = list_display
    list_per_page = 10
    search_fields = ['sn','company__name','ipaddress','speed','server__hostname']

class RamAdmin(BaseAdmin):
    list_display = ("id",'company','size','server')
    list_filter = ["ID","型号",'运行内存','服务器']
    export_fields = ("id",'company','size','count','server')
    list_per_page = 10
    search_fields = ['company__name', 'size','server__hostname']

class DiskAdmin(BaseAdmin):
    list_display = ("id","sn",'company', 'types', 'size', 'server','status','remarks')
    list_filter = ["ID","SN","型号", '磁盘类型', '磁盘容量','服务器','状态','备注']
    export_fields = list_display
    list_per_page = 10
    search_fields = ['sn','company__name', 'types', 'size', 'server__hostname','status']

class CPUAdmin(BaseAdmin):
    list_display = ("id",'company', 'kernel', 'frequency','counts','server')
    list_filter = ["ID","型号", '核数', '主频','数量','服务器']
    export_fields = ("id",'company', 'kernel', 'frequency','counts','server')
    list_per_page = 10
    search_fields = ['company__name', 'kernel', 'frequency','counts','server__hostname']

class DevicesAdmin(BaseAdmin):
    list_display = ("id",'sn','company','ipaddress','height','cabint',"position",'device_statuses','group',"warranty",'start_date','end_date','contacts')
    list_filter = ["ID","SN","型号",'IP地址','高度','机柜',"机柜位置",'设备状态','设备组','质保结束时间','上线时间','下线时间','负责人']
    export_fields = ["id",'sn','name','types','company','ipaddress','cabint',"position",'device_statuses','group',"warranty",'contacts']
    list_per_page = 10
    search_fields = ['sn','company__name','model','ipaddress','cabint','device_statuses','contacts']


class ServersAdmin(BaseAdmin):
    list_display = ("id","sn","cabint",'hostname','ipaddress','vlan',"group",'status','warranty','userinfo','contacts')
    list_filter = ["ID","SN","机柜","主机名",'管理地址','管理VLAN','主机组','状态','质保截止时间','IPMI用户信息','负责人']
    export_fields = ["id","sn","company_id","types",'cabint_id',"position",'hostname','ipaddress','vlan_id',"system","version","status",
                     "group_id","warranty",'userinfo','contacts']
    list_per_page = 10
    search_fields = ["sn","cabint__number",'hostname','ipaddress',"group__name","status"]

class WarrantyAdmin(BaseAdmin):
    list_display = ('company',"start_date",'end_date')
    list_filter = ['质保商','质保开始时间','质保结束时间']
    export_fields = ('id','company',"start_date",'end_date')
    list_per_page = 10
    search_fields = list_display


site.register(models.IDC,IdcInfoAdmin)
site.register(models.Cabint,CabintAdmin)
site.register(models.Group,GroupAdmin)
site.register(models.Company,CompanyAdmin)
site.register(models.Protocol,ProtocolAdmin)
site.register(models.Nic,NicAdmin)
site.register(models.Ram,RamAdmin)
site.register(models.Disk,DiskAdmin)
site.register(models.CPU,CPUAdmin)
site.register(models.Device,DevicesAdmin)
site.register(models.Servers,ServersAdmin)
site.register(models.Warranty,WarrantyAdmin)
