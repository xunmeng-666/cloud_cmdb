from django.db import models

# Create your models here.

device_status = (
    (0,'未启用'),
    (1,'已启用'),
    (2,'故障'),
    (3,'下线'),
)

approver_status = (
    (0,'待审批'),
    (1,'已审批'),
    (2,'待协商'),
)

class IDC(models.Model):
    name = models.CharField(verbose_name='机房名称',max_length=200,unique=True)
    address = models.CharField(verbose_name='机房地址',max_length=200)
    contacts = models.CharField(verbose_name='机房联系组',max_length=32,blank=True,null=True)
    phone = models.CharField(verbose_name='联系电话',max_length=12,blank=True,null=True)
    remarks = models.CharField(verbose_name='备注',max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = '机房信息'
        verbose_name_plural = '机房信息'

    def __str__(self):
        return self.name

class Cabint(models.Model):
    number = models.CharField(verbose_name='编号',max_length=32,blank=True,null=True,unique=True)
    size = models.CharField(verbose_name='容量',max_length=128,blank=True,null=True)
    room_number = models.CharField(verbose_name='机房编号',max_length=32,blank=True,null=True)
    idc = models.ForeignKey(IDC,on_delete=models.CASCADE,related_name='cabintd')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = '机柜'

    def __str__(self):
        return "%s" %self.number


# class Application(models.Model):
#     name = models.CharField(verbose_name='应用',max_length=64)
#     version = models.CharField(verbose_name='版本号',max_length=32)
#
#     class Meta:
#         verbose_name = "应用"
#         verbose_name_plural = '应用'
#
#     def __str__(self):
#         return self.name

class Company(models.Model):
    device_types = (
        (0,'服务器'),
        (1,'CPU'),
        (2,'硬盘'),
        (3,'内存'),
        (4,'网络设备'),
    )
    name = models.CharField(verbose_name='厂商', max_length=64, blank=True, null=True,)
    model = models.CharField(verbose_name='型号', max_length=64, blank=True, null=True,unique=True)
    types = models.SmallIntegerField(verbose_name="设备类型",choices=device_types,default=0)
    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'

    def __str__(self):
        return "%s,%s" %(self.name,self.model)

class Devices(models.Model):
    device_types = (
        (0,'交换机'),
        (1,'路由器'),
        (2,'防火墙'),
        (3,'IDS/IPS'),
        (4,'WAF'),
        (5,'DDOS防火墙'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    name = models.SmallIntegerField(verbose_name='设备类型',choices=device_types,default=0)
    company = models.ForeignKey(Company,)
    ipaddress = models.GenericIPAddressField(unique=True)
    height = models.CharField(verbose_name='高度',max_length=4,blank=True,null=True)
    position = models.CharField(verbose_name='机柜位置',max_length=12,blank=True,null=True,unique=True)
    cabint = models.ForeignKey(Cabint,related_name='devices',on_delete=models.CASCADE)
    device_statuses = models.SmallIntegerField(choices=device_status,default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = '网络设备'

    def __str__(self):
        return "%s,%s" %(self.get_name_display(),self.ipaddress)

class Protocol(models.Model):
    protocols = (
        (0,'VLAN'),
        (1,'TRUNK'),
        (2,'RIP'),
        (3,'OSPF'),
        (4,'IBGP'),
        (5,'EBGP'),
    )
    name = models.SmallIntegerField(verbose_name='协议类型',choices=protocols,default=0,)
    number = models.CharField(verbose_name='协议号',max_length=8,default='VLAN1')
    ipaddress = models.GenericIPAddressField(verbose_name='协议IP',blank=True,null=True)
    port_range = models.CharField(verbose_name='端口范围',max_length=8,default='1-4',)
    device = models.ForeignKey(Devices,related_name='protocols',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = '协议'
        verbose_name_plural = '协议'

    def __str__(self):
        return "%s,%s" %(self.device,self.number)


class Servers(models.Model):
    device_status = (
        (0, '未启用'),
        (1, '已启用'),
        (2, '故障'),
        (3, '下线'),
    )
    servers_type = (
        (0,'机架'),
        (1,'塔式'),
        (2,'小型机'),
        (3,'刀片'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    model = models.ForeignKey(Company,related_name='servers',on_delete=models.CASCADE)
    cabint = models.ForeignKey(Cabint, on_delete=models.CASCADE, related_name='servers')
    types = models.SmallIntegerField(verbose_name='服务器类型',choices=servers_type,null=True,blank=True)
    hostname = models.CharField(verbose_name='主机名', max_length=64, unique=True)
    ipmi_ipaddress = models.GenericIPAddressField(verbose_name='管理IP',unique=True)
    system = models.CharField(verbose_name='操作系统',max_length=32,blank=True,null=True)
    version = models.CharField(verbose_name='系统版本号',max_length=32,blank=True,null=True)
    height = models.CharField(verbose_name='高度',max_length=4,blank=True,null=True)
    position = models.CharField(verbose_name='机柜位置', max_length=12, blank=True, null=True, unique=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    device_statuses = models.SmallIntegerField(choices=device_status, default=0)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        return "%s,%s" %(self.hostname,self.ipmi_ipaddress)

class Nic(models.Model):
    choice_speed = (
        (0, '万兆'),
        (1, '千兆'),
        (2, '百兆'),
    )
    choice_type = (
        (0,'服务器'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    name = models.ForeignKey(Company,verbose_name='厂商', max_length=200, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(verbose_name='IP地址', blank=True, null=True, unique=True)
    speed = models.SmallIntegerField(verbose_name='速率', choices=choice_speed, default=2)
    types = models.SmallIntegerField(choices=choice_type, default=0, verbose_name='类型')
    protocol = models.ForeignKey(Protocol, verbose_name='交换机', related_name='nics',
                                 on_delete=models.CASCADE, blank=True, null=True)
    server = models.ForeignKey(Servers,related_name='nics',on_delete=models.CASCADE,blank=True,null=True)
    remarks = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = '网卡'

    def __str__(self):
        return "%s,%s" % (self.ipaddress,self.get_speed_display())


class Ram(models.Model):

    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    name = models.ForeignKey(Company,verbose_name='厂商', max_length=200, blank=True, null=True)
    size = models.CharField(verbose_name='运行内存',max_length=32,default='32G')
    count = models.IntegerField(verbose_name='数量',default='1')
    server = models.ForeignKey(Servers,related_name='rams',on_delete=models.CASCADE,blank=True,null=True)


    class Meta:
        verbose_name = '内存'
        verbose_name_plural = '内存'

    def __str__(self):
        return "%s,%s" %(self.name,self.size)

class Disk(models.Model):
    disk_types = (
        (0,'SATA硬盘'),
        (1,'SCSI硬盘'),
        (2,'SAS硬盘'),
        (3,'SSD硬盘'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    name = models.ForeignKey(Company,verbose_name='厂商', max_length=200, blank=True, null=True)
    types = models.SmallIntegerField(choices=disk_types,verbose_name='磁盘类型',default=0,blank=True,null=True)
    size = models.CharField(verbose_name='磁盘容量',max_length=32)
    server = models.ForeignKey(Servers,related_name='disks',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = '磁盘'
        verbose_name_plural = '磁盘'

    def __str__(self):
        return "%s,%s" %(self.types,self.size)

class CPU(models.Model):
    name = models.ForeignKey(Company,verbose_name='厂商', max_length=200, blank=True, null=True)
    kernel = models.IntegerField(verbose_name='核数',)
    frequency = models.CharField(verbose_name='主频',max_length=12,blank=True,null=True)
    counts = models.IntegerField(verbose_name='数量',blank=True,null=True)
    server = models.ForeignKey(Servers, related_name='cpus', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'

    def __str__(self):
        return "%s,%s" %(self.name,self.kernel)




# class Router(models.Model):
#     sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
#     name = models.CharField(max_length=32, unique=True)
#     company = models.ForeignKey(Company)
#     ipaddress = models.GenericIPAddressField(unique=True)
#     protocol = models.ForeignKey(Protocol, blank=True,null=True)
#     cabint = models.ForeignKey(Cabint,related_name='routerd',on_delete=models.CASCADE )
#     device_statuses = models.SmallIntegerField(choices=device_status,default=0)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(blank=True,null=True)
#
#     class Meta:
#         verbose_name = '路由器'
#         verbose_name_plural = '路由器'
#
#     def __str__(self):
#         return "%s,%s" %(self.ipaddress,self.device_statuses)
#
# class GFW(models.Model):
#     sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
#     name = models.CharField(max_length=32,unique=True)
#     company = models.ForeignKey(Company, )
#     nic = models.ForeignKey(Nic, )
#     ram = models.ForeignKey(Ram, )
#     ipaddress = models.GenericIPAddressField(unique=True)
#     protocol = models.ForeignKey(Protocol, )
#     cabint = models.ForeignKey(Cabint, related_name='gfwd',on_delete=models.CASCADE)
#     device_statuses = models.SmallIntegerField(choices=device_status,default=0)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(blank=True,null=True)
#
#     class Meta:
#         verbose_name = '防火墙'
#         verbose_name_plural = '防火墙'
#
#     def __str__(self):
#         return self.name
#
#
#
# class Taskflow(models.Model):
#     titel = models.CharField(verbose_name='标题',max_length=128)
#     device = models.CharField(verbose_name='设备名称',max_length=64)
#     ipaddress = models.GenericIPAddressField()
#     content = models.CharField(verbose_name='内容',max_length=200,)
#     proposer = models.CharField(verbose_name='申请人',max_length=64)
#     approver = models.CharField(verbose_name='审批者',max_length=64)
#     approver_statuses = models.SmallIntegerField(choices=approver_status,default=0)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(blank=True,null=True)
#
#     class Meta:
#         verbose_name = '任务'
#         verbose_name_plural = '任务'
#
# class Logs(models.Model):
#     types = models.CharField(verbose_name='行为',max_length=32)
#     content = models.CharField(verbose_name='内容',max_length=200)
#     date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = '日志'
#         verbose_name_plural = '日志'

