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
                                           "nics__protocol__device__id")
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
