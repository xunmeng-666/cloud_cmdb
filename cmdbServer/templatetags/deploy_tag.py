# -*- coding:utf-8-*-
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_project_name(admin_class):
    return admin_class.model._meta.model_name

@register.simple_tag
def build_idc_info(admin_class,obj_id):
    obj = admin_class.model.objects.get(id=obj_id)
    ele_span = "<span class='percent' style='color: #0e0e0e;font-weight:bold'>机柜数量:%s</span>" %obj.cabintd.count()
    return mark_safe(ele_span)


@register.simple_tag
def build_project_verbose_name(admin_class):
    print('admin_class',admin_class)
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_readonly_field_val(field_name,obj_instance):
    """
    1.根据obj_instance反射出field_name 的值
    :param field_name:
    :param obj_instance:
    :return:
    """
    field_type =  obj_instance._meta.get_field(field_name).get_internal_type()
    if field_type == "ManyToManyField":
        m2m_obj = getattr(obj_instance,field_name)
        return ",".join([ i.__str__() for i in m2m_obj.all()])
    return getattr(obj_instance,field_name)

@register.simple_tag
def get_selected_m2m_objects(form_obj,field_name):
    """
    1.根据field_name反射出form_obj.instance里的字段对象
    2. 拿到字段对象关联的所有数据
    :param form_obj:
    :param field:
    :return:
    """

    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field_name)
        return field_obj.all()
    else:
        return []

@register.simple_tag
def get_m2m_objects(admin_class,field_name,selected_objs):
    """
    1.根据field_name从admin_class.model反射出字段对象
    2.拿到关联表的所有数据
    3.返回数据
    :param admin_class:
    :param field_name:
    :return:
    """

    field_obj = getattr(admin_class.model,field_name)
    all_objects = field_obj.rel.to.objects.all()
    return set(all_objects) - set(selected_objs)

@register.simple_tag
def get_filter_condtions_string(filter_conditions,q_val):
    condtion_str = ""
    if q_val:#拼接search 字段
        condtion_str += "&_q=%s" % q_val
    return condtion_str

@register.simple_tag
def generate_orderby_icon(new_order_key):
    if new_order_key.startswith('-'):
        icon_ele = """<i class="fa fa-angle-down" aria-hidden="true"></i>"""
    else:
        icon_ele = """<i class="fa fa-angle-up" aria-hidden="true"></i>"""
    return mark_safe(icon_ele)

@register.simple_tag
def build_cabint_listinfo(obj,obj_id):
    objects = obj.filter(id=obj_id).values('cabintd__id','cabintd__number','cabintd__size','cabintd__useposition')
    ele = ""
    for info in objects:
        ele_tr = "<tr>"
        ele_td = "<td style='text-align: center'><a href='/asset/cmdbServer/cabint/detail/?id=%s'>%s</a></td>" %(info['cabintd__id'],info['cabintd__number'])
        ele_td += "<td style='text-align: center'>%s</td>" %round(int(info['cabintd__useposition']) / int(info['cabintd__size']) * 100,2)
        ele_tr += ele_td
        ele_tr += "</tr>"
        ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_cabint_useinfo(obj,obj_id):
    devices = obj.filter(id=obj_id).values("number","devices__position","devices__name","devices__ipaddress",
                                           "devices__company__height","devices__id")
    servers = obj.filter(id=obj_id).values("number","servers__position","servers__hostname","servers__ipaddress",
                                           "servers__company__height","servers__id")
    ele = ""
    if devices[0]['devices__position']:
        for info in devices:
            ele_tr = "<tr>"
            ele_td = "<td style='text-align: center'>%s</td>" %info['number']
            ele_td += "<td style='text-align: center'>%sU</td>" %info['devices__position']
            ele_td += "<td style='text-align: center'><a href='/asset/cmdbServer/device/detail/?id=%s'>%s</a></td>" %(info['devices__id'],info['devices__name'])
            ele_td += "<td style='text-align: center'>%s</td>" %info['devices__ipaddress']
            ele_td += "<td style='text-align: center'>%s</td>" %info['devices__company__height']
            ele_tr += ele_td +"</tr>"
            ele += ele_tr
    if servers[0]['servers__position']:
        for info in servers:
            ele_tr = "<tr>"
            ele_td = "<td style='text-align: center'>%s</td>" %info['number']
            ele_td += "<td style='text-align: center'>%sU</td>" %info['servers__position']
            ele_td += "<td style='text-align: center'><a href='/asset/cmdbServer/device/detail/?id=%s'>%s</a></td>" %(info['servers__id'],info['servers__hostname'])
            ele_td += "<td style='text-align: center'>%s</td>" %info['servers__ipaddress']
            ele_td += "<td style='text-align: center'>%s</td>" %info['servers__company__height']
            ele_tr += ele_td +"</tr>"
            ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_device_info(obj,obj_id):
    objects = obj.filter(id=obj_id).values("name","ipaddress","protocols__number","protocols__port_range",
                                           "protocols__nics__server__hostname","protocols__nics__server__id")
    ele = ""
    for info in objects:
        ele_tr = "<tr>"
        ele_td = "<td style='text-align: center'>%s</td>" % info['name']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress']
        ele_td += "<td style='text-align: center'>%s</td>" % info['protocols__number']
        ele_td += "<td style='text-align: center'>%s</td>" % info['protocols__port_range']
        ele_td += "<td style='text-align: center'><a href='/asset/cmdbServer/servers/detail/?id=%s'>%s</a></td>" %(info['protocols__nics__server__id'],info['protocols__nics__server__hostname'])
        ele_tr += ele_td + "</tr>"
        ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_servers_info(obj,obj_id):
    objects = obj.filter(id=obj_id).values("hostname", "ipaddress", "cpus__kernel", "cpus__counts","rams__size","disks__size",
                                           "nics__ipaddress", "nics__protocol__number","nics__protocol__device__name",
                                           "nics__bonding__ipaddress1","nics__bonding__ipaddress2","nics__bonding__ipaddress3",
                                           "nics__bonding__ipaddress4","nics__protocol__device__id")
    size = 0
    for disk in objects:
        if disk['disks__size']:
            if disk['disks__size'][-1] is 'T':
                size += int(disk['disks__size'][0]) * 1000
            elif disk['disks__size'][-1] is 'G':
                size += int(disk['disks__size'].split('G')[0])

    ele = ""
    for info in objects:
        ele_tr = "<tr>"
        ele_td = "<td style='text-align: center'>%s</td>" % info['hostname']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress']
        ele_td += "<td style='text-align: center'>%s</td>" % info['cpus__kernel']
        ele_td += "<td style='text-align: center'>%s</td>" % info['cpus__counts']
        ele_td += "<td style='text-align: center'>%sG</td>" % info['rams__size']
        ele_td += "<td style='text-align: center'>%sG</td>" % size
        if info["nics__ipaddress"]:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__ipaddress']
        elif info['nics__bonding__ipaddress1']:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__bonding__ipaddress1']
        elif info['nics__bonding__ipaddress2']:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__bonding__ipaddress2']
        elif info['nics__bonding__ipaddress3']:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__bonding__ipaddress3']
        elif info['nics__bonding__ipaddress4']:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__bonding__ipaddress4']
        else:
            ele_td += "<td style='text-align: center'>%s</td>" % info['nics__ipaddress']
        ele_td += "<td style='text-align: center'>%s</td>" % info['nics__protocol__number']
        ele_td += "<td style='text-align: center'><a href='/asset/cmdbServer/device/detail/?id=%s'>%s</a></td>" %(info['nics__protocol__device__id'],info['nics__protocol__device__name'])

        ele_tr += ele_td + "</tr>"
        ele += ele_tr
        return mark_safe(ele)

@register.simple_tag
def build_protocol_info(obj,obj_id):
    objects = obj.filter(id=obj_id).values("name","number","ipaddress","port_range","device__ipaddress","device__id")
    ele = ""
    name = {0:'VLAN',1:'TRUNK',2:'RIP',3:'OSPF',4:'IBGP',5:'EBGP'}
    for info in objects:
        ele_tr = "<tr>"
        ele_td = "<td style='text-align: center'>%s</td>" %name[info['name']]
        ele_td += "<td style='text-align: center'>%s</td>" % info['number']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress']
        ele_td += "<td style='text-align: center'>%s</td>" % info['port_range']
        ele_td += "<td style='text-align: center'><a href='/asset/cmdbServer/device/detail/?id=%s'>%s</a></td>" %(info['device__id'],info['device__ipaddress'])
        ele_tr += ele_td + "</tr>"
        ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_bonding_info(obj,obj_id):
    objects = obj.filter(device=obj_id).values("nic__sn","model","ipaddress1","ipaddress2","ipaddress3","ipaddress4",)
    ele = ""
    model = {0: 'Round-robin policy(平衡抡循环策略', 1: 'Active-backup policy(主-备份策略)', 2: 'XOR policy(平衡策略)',
            3: 'broadcast(广播策略)', 4: 'Dynamic link aggregation(IEEE802.3ad 动态链接聚合)', 5: 'Adaptive transmit load balancing(适配器传输负载均衡)',
            6: 'Adaptive load balancing(适配器适应性负载均衡)'}

    for info in objects:
        ele_tr = "<tr>"
        ele_td = "<td style='text-align: center'>%s</td>" % info['nic__sn']
        ele_td += "<td style='text-align: center'>%s</td>" %obj_id
        ele_td += "<td style='text-align: center'>%s</td>" % model[info['model']]
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress1']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress2']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress3']
        ele_td += "<td style='text-align: center'>%s</td>" % info['ipaddress4']
        ele_tr += ele_td + "</tr>"
        ele += ele_tr
    return mark_safe(ele)



import json
@register.simple_tag
def build_logs_info(obj):
    ele = ""
    for content in obj.values():
        ele_tr = "<tr>"
        ele_td = "<td>%s</td>" %content["date"].strftime("%Y-%m-%d %H:%M:%S")
        ele_td += "<td>%s</td>" %content["user"]
        ele_td += "<td>%s</td>" %content["action"]
        ele_td += "<td>%s</td>" %content["content"]
        ele_tr += ele_td
        ele_tr += "</tr>"
        ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_option_user(obj):
    ele = ""
    for user in obj.values('user').distinct():
        ele_option = "<option label='%s' value='%s'></option>" %(user['user'],user['user'])
        ele += ele_option
    return mark_safe(ele)

@register.simple_tag
def build_option_action(obj):
    ele = ""
    for user in obj.values('action').distinct():
        ele_option = "<option label='%s' value='%s'></option>" %(user['action'],user['action'])
        ele += ele_option
    return mark_safe(ele)

@register.simple_tag
def build_nic_bonding(row,admin_class):
    ele = ""
    obj = admin_class.model.objects.filter(sn=row.sn).values('bonding__device',"bonding__device")
    for i in obj:
        ele += "<a href='/asset/cmdbServer/bonding/detail/?device=%s'>%s</a>" %(i['bonding__device'],i['bonding__device'])
    return mark_safe(ele)


@register.simple_tag
def build_bonding_nic(admin_class):
    obj = admin_class.model.objects.values("nic__sn")
    ele = ""
    for sn in obj:
        if sn['nic__sn']:
            ele += sn['nic__sn']
    return  mark_safe(ele)

@register.simple_tag
def get_abs_value(loop_num , curent_page_number):
    """返回当前页与循环loopnum的差的绝对值"""
    return abs(loop_num - curent_page_number)