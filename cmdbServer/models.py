from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,MaxLengthValidator
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from cmdbServer.core.model_func import savelog

# Create your models here.


device_status = (
    (0,'已启用'),
    (1,'未启用'),
    (2,'故障'),
    (3,'下线'),
)

approver_status = (
    (0,'待审批'),
    (1,'已审批'),
    (2,'待协商'),
)

location= ((x,x) for x in range(1,43))

class IDC(models.Model):
    name = models.CharField(verbose_name='机房名称', max_length=200, unique=True)
    address = models.CharField(verbose_name='机房地址', max_length=200)
    contacts = models.CharField(verbose_name='机房联系组', max_length=32, blank=True, null=True)
    phone = models.CharField(verbose_name='联系电话', max_length=12, blank=True, null=True)
    remarks = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '机房信息'
        verbose_name_plural = '机房信息'

    def __str__(self):
        return self.name

class Cabint(models.Model):
    number = models.CharField(verbose_name='编号',max_length=32,blank=True,null=True)
    size = models.IntegerField(verbose_name='容量')
    useposition = models.SlugField(verbose_name='已用高度',default=0,blank=True)
    room_number = models.CharField(verbose_name='机房编号',max_length=32,blank=True,null=True)
    idc = models.ForeignKey(IDC,on_delete=models.CASCADE,related_name='cabintd')

    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = '机柜'
        unique_together = ("number",'room_number','idc')

    def __str__(self):
        return "%s,%s" %(self.idc,self.number)

    @property
    def idc_name(self):
        return "%s" % (self.idc.name)

class Warranty(models.Model):
    company = models.CharField(verbose_name='质保商',max_length=200,unique=True)
    start_date = models.DateTimeField(verbose_name='质保起始时间')
    end_date = models.DateTimeField(verbose_name='质保结束时间')

    class Meta:
        verbose_name = '质保信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" %(self.end_date)


class Company(models.Model):
    device_types = (
        (0,'服务器'),
        (1,'网络设备'),
        (2,'CPU'),
        (3,'内存'),
        (4,'硬盘'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='厂商', max_length=64, blank=True, null=True,)
    model = models.CharField(verbose_name='型号', max_length=64, blank=True, null=True,unique=True)
    types = models.SmallIntegerField(verbose_name="设备类型",choices=device_types,default=0)
    height = models.IntegerField(verbose_name='设备高度',blank=True,null=True,validators=[MaxValueValidator(42),
                                                                             MinValueValidator(1)])
    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'

    def __str__(self):
        return "%s,%s,%s" %(self.name,self.model,self.get_types_display())

class Group(models.Model):
    name = models.CharField(verbose_name='组',max_length=32,unique=True)

    class Meta:
        verbose_name = "设备组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" %self.name

class Device(models.Model):
    device_types = (
        (0,'交换机'),
        (1,'路由器'),
        (2,'防火墙'),
        (3,'IDS/IPS'),
        (4,'WAF'),
        (5,'DDOS防火墙'),
    )
    id = models.AutoField(primary_key=True)
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    name = models.CharField(max_length=32,unique=True)
    types = models.SmallIntegerField(verbose_name='设备类型', choices=device_types, default=0)
    company = models.ForeignKey(Company,verbose_name='型号',related_name='devices', on_delete=models.CASCADE,)
    ipaddress = models.GenericIPAddressField(unique=True,verbose_name='IP地址')
    cabint = models.ForeignKey(Cabint, verbose_name='机柜', related_name='devices', on_delete=models.CASCADE,blank=True,null=True)
    position = models.IntegerField(verbose_name='机柜位置', default=1, blank=True, null=True,unique=True,
                                   validators=[MaxValueValidator(42),
                                               MinValueValidator(1)])
    device_statuses = models.SmallIntegerField(choices=device_status, default=0,verbose_name='设备状态')
    group = models.ForeignKey(Group,related_name='device', on_delete=models.CASCADE, verbose_name='设备组', blank=True,
                              null=True)
    start_date = models.DateTimeField(verbose_name='上线时间',auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='下线时间',blank=True, null=True)
    warranty = models.ForeignKey(Warranty,verbose_name='质保时间', related_name='device', on_delete=models.CASCADE, blank=True, null=True)
    contacts = models.CharField(verbose_name='负责人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = '网络设备'

    def create(self,*args,**kwargs):
        self.save(args,kwargs)
    def save(self, *args, **kwargs):
        objects = Cabint.objects.filter(id=self.cabint_id).values('useposition', 'size')[0]
        useposition = objects['useposition']
        cabint_size = objects['size']
        if not useposition:
            useposition = 0
        useposition = int(useposition)
        if self.company.height is None:
            self.company.height = 0
        height = int(self.company.height)
        if height + useposition < cabint_size:
            useposition += height
            if not self.id:
                super(self.__class__, self).save(*args, **kwargs)
                Cabint.objects.filter(id=self.cabint_id).update(useposition=useposition)
            super(self.__class__, self).save(*args, **kwargs)

        return MaxLengthValidator(cabint_size)

    def delete(self, using=None, keep_parents=False):
        objects = Cabint.objects.filter(id=self.cabint_id).values('useposition')[0]
        useposition = int(objects['useposition']) - int(self.company.height)
        if useposition < 0: useposition = 0
        Cabint.objects.filter(id=self.cabint_id).update(useposition=useposition)

        super(self.__class__, self).delete()

    def __str__(self):
        return "%s,%s" %(self.get_types_display(),self.ipaddress,)

    @property
    def group_name(self):
        return self.group.name

    @property
    def company_name(self):
        return "%s,%s" % (self.company.name, self.company.model)

class Protocol(models.Model):
    protocols = (
        (0,'VLAN'),
        (1,'TRUNK'),
        (2,'RIP'),
        (3,'OSPF'),
        (4,'IBGP'),
        (5,'EBGP'),
        (6,'BIND'),
    )
    name = models.SmallIntegerField(verbose_name='协议类型',choices=protocols,default=0,)
    number = models.CharField(verbose_name='协议号',max_length=8,default='VLAN1')
    ipaddress = models.GenericIPAddressField(verbose_name='协议IP',blank=True,null=True)
    port_range = models.CharField(verbose_name='端口范围',max_length=8,default='1-4',)
    device = models.ForeignKey(Device,related_name='protocols',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = '协议'
        verbose_name_plural = '协议'

    def __str__(self):
        return "%s,%s" %(self.device,self.number,)

class Servers(models.Model):
    servers_type = (
        (0, '机架'),
        (1, '塔式'),
        (2, '小型机'),
        (3, '刀片'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    company = models.ForeignKey(Company,verbose_name='型号',related_name='servers', on_delete=models.CASCADE,blank=True,null=True,)
    types = models.SmallIntegerField(verbose_name='服务器类型', choices=servers_type,default=0,)
    cabint = models.ForeignKey(Cabint,verbose_name='机柜',related_name='servers',on_delete=models.CASCADE,blank=True,null=True)
    position = models.IntegerField(verbose_name='机柜位置',blank=True,null=True,validators=[MaxValueValidator(42),
                                               MinValueValidator(1)])
    hostname = models.CharField(verbose_name='主机名', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(verbose_name='管理地址',unique=True)
    vlan = models.ForeignKey(Protocol,verbose_name='管理VLAN',blank=True,related_name='servers', on_delete=models.CASCADE)
    system = models.CharField(verbose_name='操作系统', max_length=32, blank=True, null=True)
    version = models.CharField(verbose_name='系统版本号', max_length=32, blank=True, null=True)
    status = models.SmallIntegerField(verbose_name='主机状态',choices=device_status,default=0)
    group = models.ForeignKey(Group,verbose_name='服务器组',blank=True,null=True,related_name='servers', on_delete=models.CASCADE,)
    start_date = models.DateTimeField(verbose_name='上线时间', auto_now_add=True)
    end_date = models.DateTimeField(verbose_name='下线时间', blank=True, null=True)
    warranty = models.ForeignKey(Warranty, verbose_name='质保时间', related_name='servers', on_delete=models.CASCADE,
                                 blank=True, null=True)
    userinfo = models.CharField(verbose_name='IPMI用户信息',max_length=32,blank=True,null=True)
    contacts = models.CharField(verbose_name='负责人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'
        unique_together = "cabint","position"

    def save(self, *args, **kwargs):
        objects = Cabint.objects.filter(id=self.cabint_id).values('useposition','size')[0]
        useposition = objects['useposition']
        cabint_size = objects['size']
        if not useposition:
            useposition = 0
        useposition = int(useposition)
        if self.company.height is None:
            self.company.height = 0
        height = int(self.company.height)
        if height + useposition < cabint_size:
            useposition += height
            if not self.id:
                super(self.__class__, self).save(*args, **kwargs)
                Cabint.objects.filter(id=self.cabint_id).update(useposition=useposition)
            super(self.__class__, self).save(*args, **kwargs)

        return MaxLengthValidator(cabint_size)

    def delete(self, using=None, keep_parents=False):
        objects = Cabint.objects.filter(id=self.cabint_id).values('useposition')[0]
        useposition = int(objects['useposition']) - int(self.company.height)
        if useposition < 0: useposition = 0
        Cabint.objects.filter(id=self.cabint_id).update(useposition=useposition)
        super(self.__class__,self).delete()


    def __str__(self):
        return "%s,%s" % (self.hostname,self.ipaddress)

    @property
    def group_name(self):
        return  self.group.name

    @property
    def company_name(self):
        return "%s,%s"%(self.company.name,self.company.model)


class Nic(models.Model):
    choice_speed = (
        (0, '万兆'),
        (1, '千兆'),
        (2, '百兆'),
    )
    choice_type = (
        (0,'服务器'),
        (1,'网络设备'),
    )
    ip_model = (
        (0,'DHCP'),
        (1,'STATIC'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    company = models.ForeignKey(Company,verbose_name='型号',related_name='nics',on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField(verbose_name='IP地址', blank=True, null=True, unique=True)
    model = models.SmallIntegerField(verbose_name='IP获取方式',choices=ip_model,default=0,blank=True,null=True)
    mac_address = models.CharField(verbose_name='MAC地址',max_length=32,blank=True,null=True)
    speed = models.SmallIntegerField(verbose_name='速率', choices=choice_speed, default=0)
    types = models.SmallIntegerField(choices=choice_type, default=0, verbose_name='类型')
    protocol = models.ForeignKey(Protocol, verbose_name='VLAN', related_name='nics',
                                 on_delete=models.CASCADE, blank=True, null=True)
    server = models.ForeignKey(Servers,related_name='nics',on_delete=models.CASCADE,blank=True,null=True)
    remarks = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = '网卡'

    def __str__(self):
        return "%s,%s,%s,%s" % (self.sn,self.ipaddress,self.server.hostname,self.get_speed_display(),)

    @property
    def company_name(self):
        return "%s,%s" % (self.company.name, self.company.model)


class Ram(models.Model):
    company = models.ForeignKey(Company,verbose_name='型号',related_name='rams',on_delete=models.CASCADE)
    size = models.IntegerField(verbose_name='运行内存',default='32')
    count = models.IntegerField(verbose_name='数量',default=1,)
    server = models.ForeignKey(Servers,related_name='rams',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = '内存'

    def __str__(self):
        return "%s,%s" %(self.company,self.size)

    @property
    def company_name(self):
        return "%s,%s" % (self.company.name, self.company.model)

class Disk(models.Model):
    disk_types = (
        (0,'SATA硬盘'),
        (1,'SCSI硬盘'),
        (2,'SAS硬盘'),
        (3,'SSD硬盘'),
    )
    disk_status = (
        (0,'已启用'),
        (1,'故障'),
        (2,'已下线'),
        (3,'未使用'),
        (4,'已更换'),
        (5,'READ'),
    )
    sn = models.CharField(max_length=32, blank=True, null=True, unique=True)
    company = models.ForeignKey(Company,verbose_name='型号',related_name='disks',on_delete=models.CASCADE)
    types = models.SmallIntegerField(choices=disk_types,verbose_name='磁盘类型',default=0,blank=True,null=True)
    size = models.CharField(verbose_name='磁盘容量',max_length=32)
    count = models.IntegerField(verbose_name='磁盘数量',blank=True,null=True)
    server = models.ForeignKey(Servers,related_name='disks',on_delete=models.CASCADE,blank=True,null=True)
    status = models.SmallIntegerField(verbose_name='状态',choices=disk_status,default=0,)
    remarks = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = '磁盘'
        verbose_name_plural = '磁盘'

    def __str__(self):
        return "%s,%s,%s" %(self.get_types_display(),self.size,self.get_status_display())

    @property
    def company_name(self):
        return "%s,%s" % (self.company.name, self.company.model)

class CPU(models.Model):
    company = models.ForeignKey(Company, verbose_name='型号', related_name='cpus', on_delete=models.CASCADE)
    kernel = models.IntegerField(verbose_name='核数',)
    frequency = models.CharField(verbose_name='主频',max_length=12,blank=True,null=True)
    counts = models.IntegerField(verbose_name='数量',blank=True,null=True)
    server = models.ForeignKey(Servers, related_name='cpus', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'

    def __str__(self):
        return "%s,%s" %(self.kernel,self.counts)

    @property
    def company_name(self):
        return "%s,%s" % (self.company.name, self.company.model)

class Bonding(models.Model):
    bonding_model= (
        (0,"Round-robin policy(平衡抡循环策略"),
        (1,"Active-backup policy(主-备份策略)"),
        (2,"XOR policy(平衡策略)"),
        (3,"broadcast(广播策略)"),
        (4,"Dynamic link aggregation(IEEE802.3ad 动态链接聚合)"),
        (5,"Adaptive transmit load balancing(适配器传输负载均衡)"),
        (6,"Adaptive load balancing(适配器适应性负载均衡)"),
    )
    nic = models.ManyToManyField(Nic,verbose_name='网卡',related_name='bonding',)
    device = models.CharField(verbose_name='设备',max_length=16,blank=True,null=True)
    model = models.SmallIntegerField(choices=bonding_model,verbose_name='Bonding模式',default=0)
    ipaddress1 = models.GenericIPAddressField(verbose_name='IP地址1',blank=True,null=True)
    ipaddress2 = models.GenericIPAddressField(verbose_name='IP地址2',blank=True,null=True)
    ipaddress3 = models.GenericIPAddressField(verbose_name='IP地址3',blank=True,null=True)
    ipaddress4 = models.GenericIPAddressField(verbose_name='IP地址4',blank=True,null=True)

    class Meta:
        verbose_name = 'Bonding'
        verbose_name_plural = verbose_name
        unique_together = ('ipaddress1','ipaddress2','ipaddress3','ipaddress4')

    def __str__(self):
        return "%s,%s" %(self.device,self.get_model_display())

class Logs(models.Model):
    user = models.CharField(max_length=32)
    action = models.CharField(max_length=32,)
    content = JSONField()
    date = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = '日志'
        verbose_name_plural = verbose_name

