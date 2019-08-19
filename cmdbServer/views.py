# -*- coding:utf-8-*-

from django.shortcuts import render,redirect,HttpResponse
from django.http import FileResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.http import urlquote
from cmdbServer.admin_base import site
from cmdbServer import forms
from cmdbServer.core.fileFunc import fileFunc
from cmdbServer.core.model_func import savelog,readlog,hashpwd,dbFunc
import json
import os
# Create your views here.


def account_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        savelog.log_info(username, "Info","尝试登录系统")
        if user:
            login(request,user)
            savelog.log_info(username,"Success","成功登录系统")
            return  redirect(request.GET.get('next') or '/')
        savelog.log_info(username,"Error","登录系统失败")
    return render(request, 'login.html', locals())

def account_logout(request,**kwargs):
    savelog.log_info(request.user,"Info","登出服务器")
    request.session.clear()
    logout(request)
    return redirect('/accounts/login/')

@login_required
def index(request):
    savelog.log_info("%s"%request.user,"Info",'AccessUrl:%s'%request.get_raw_uri())
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name]['idc']
        objects = admin_class.model.objects.values('id','name')
    return render(request,'index.html',locals())


def adminfunc(model_name):
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        return admin_class



def get_filter_objs(request, admin_class):
    """返回filter的结果queryset"""

    filter_condtions = {}
    for k, v in request.GET.items():
        if k in ['_page', '_q', '_o']:
            continue
        if v:  # valid condtion
            filter_condtions[k] = v

    queryset = admin_class.model.objects.filter(**filter_condtions)

    return queryset, filter_condtions

def get_search_objs(request, querysets, admin_class):
    """
    1.拿到_q的值
    2.拼接Q查询条件
    3.调用filter(Q条件)查询
    4. 返回查询结果
    :param request:
    :param querysets:
    :param admin_class:
    :return:
    contains： 区分大小写
    icontains: 不区分大小写
    """
    q_val = request.GET.get("_q")  # None
    if q_val:
        q_obj = Q()
        q_obj.connector = 'OR'
        for search_field in admin_class.search_fields:  # 2
            q_obj.children.append(('%s__icontains' % search_field, q_val))

        search_results = querysets.filter(q_obj)  # 3
    else:
        search_results = querysets
    return search_results, q_val

def get_orderby_objs(request, querysets):
    """
    排序
    1.获取_o的值
    2.调用order_by(_o的值)
    3.处理正负号，来确定下次的排序的顺序
    4.返回
    :param request:
    :param querysets:
    :return:
    """
    orderby_key = request.GET.get('_o')  # -id
    last_orderby_key = orderby_key or ''
    if orderby_key:
        order_column = orderby_key.strip('-')
        order_results = querysets.order_by(orderby_key)
        if orderby_key.startswith('-'):
            new_order_key = orderby_key.strip('-')
        else:
            new_order_key = "-%s" % orderby_key
        return order_results, new_order_key, order_column, last_orderby_key
    else:
        return querysets, None, None, last_orderby_key

@login_required
def idc(request,no_render=False):
    model_name = 'idc'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'GET':
            savelog.log_info("%s" % request.user, "Info",'AccessURL:%s' % request.get_raw_uri())
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)

            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request,'idc/idc.html',locals())

@login_required
def table_obj_add(request,app_name,model_name):

    admin_class = site.registered_admins[app_name][model_name]
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == 'POST':
        if request.POST.get("password"):
            request.POST._mutable = True
            request.POST.update({'password': hashpwd.encrypt(request.POST.get("password"))})
            savelog.log_info("%s" % request.user,"Create",request.POST.get("ipaddress"))
        form_obj = form(data=request.POST)

        if form_obj.is_valid():
            form_obj.save()
            return redirect("/asset/%s/"%model_name)
    elif request.method == 'GET':
        form_obj = form()
    return render(request,'gloab-form/add_form.html',locals())

@login_required
def table_obj_detail(request,app_name,model_name):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    admin_class = site.registered_admins[app_name][model_name]
    obj = admin_class.model.objects.all()
    if model_name == 'bonding':
        obj_id = request.GET.get('device')
    else:
        obj_id = request.GET.get('id')


    return render(request,'gloab-form/detail_form.html',locals())

@login_required
@csrf_exempt
def table_obj_del(request,app_name,model_name):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    obj_id = request.GET.get('idAll')
    admin_class = site.registered_admins[app_name][model_name]
    if ',' in obj_id:
        status = {'success':[],'error':[]}
        for id in obj_id.split(','):
            if id:
                obj = admin_class.model.objects.get(id=id.strip())
                obj.delete()
                savelog.log_info("%s" % request.user,"Delete", {'id': id.strip(), "名称": obj._meta.fields[1].name})
                status['success'].append(id)
        return HttpResponse(json.dumps(status))
    else:
        obj = admin_class.model.objects.get(id=obj_id)
        obj.delete()
        savelog.log_info("%s" % request.user, "Delete",{'Status':'Seccuss',"data":{'id': obj_id, "主机": obj.hostname}})
        return redirect("/asset/{model_name}".format(model_name=model_name))

@login_required
@csrf_exempt
def table_obj_change(request,app_name,model_name,no_render=False):
    admin_class = site.registered_admins[app_name][model_name]
    object_id = request.GET.get('project_id')
    obj = admin_class.model.objects.get(id=object_id)
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == 'GET':
        form_obj = form(instance=obj)

    elif request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({'password':hashpwd.encrypt(request.POST.get("password"))})
        form_obj = form(instance=obj,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            savelog.log_info("%s" % request.user,"Updata",request.POST.get("ipaddress"))
            return redirect("/asset/%s"%model_name)
    if no_render:
        return locals()
    else:
        return render(request,'gloab-form/change_form.html',locals())

@login_required
def cabint(request, no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'cabint'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/cabint/")
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)

            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'idc/cabint.html', locals())

@login_required
def company(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'company'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/company/")
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)

            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'company/company_list.html', locals())

@login_required
def device(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'device'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/device/")
        elif request.method == 'GET':
            form_obj = form()

            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets.order_by('sn'), admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'device/device_list.html', locals())

@login_required
def device_group(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'group'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/device_group/")
        elif request.method == 'GET':
            form_obj = form()

            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'device/device_group.html', locals())


@login_required
def server(request,no_render=False):
    pal = request.GET.get('_q')
    # savelog.log_info("%s" % request.user, "Info",'访问URL:http://%s%s' %(request.get_host(),os.path.join(request.path,"_q=%s"%pal)))
    savelog.log_info("%s" % request.user, "Info",'访问URL:http://%s' %(request.get_raw_uri()))

    model_name = 'servers'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/servers/")
        elif request.method == 'GET':
            form_obj = form()

            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                querysets = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

@login_required
def warranty(request,no_render=False):
    savelog.log_info("%s" % request.user,"Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'warranty'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/warranty/")
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'warranty/warranty.html', locals())

@login_required
def protocol(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'protocol'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/%s/" %model_name)
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

@login_required
def cpu(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'cpu'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/cpu/")
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

@login_required
def disk(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'disk'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/disk/")
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets.order_by('sn'), admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)
        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

@login_required
def ram(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'ram'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(request.path)
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

@login_required
def nic(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    model_name = 'nic'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(request.path)
        elif request.method == 'GET':
            form_obj = form()
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets.order_by('sn'), admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

def bonding(request,no_render=False):
    savelog.log_info("%s" % request.user, "Info", '访问URL:%s' % request.get_raw_uri())
    model_name = 'bonding'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        form_obj = form()


    if no_render:
        return locals()
    return render(request, 'gloab-form/list_form.html', locals())

def queryset(request,admin_class):
    querysets, filter_conditions = get_filter_objs(request, admin_class)
    querysets, q_val = get_search_objs(request, querysets, admin_class)
    querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)

    return locals()

@login_required
@csrf_exempt
def apps(request):
    savelog.log_info("%s" % request.user, "Info", '访问URL:%s' % request.get_raw_uri())
    model_name = 'apps'
    app_name = 'cmdbServer'
    admin_class = adminfunc(model_name)
    form = forms.create_dynamic_modelform(admin_class.model)
    form_obj = form()
    # querysets = queryset(request,admin_class)
    querysets, filter_conditions = get_filter_objs(request, admin_class)
    querysets, q_val = get_search_objs(request, querysets, admin_class)
    querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)
    return render(request,'apps/apps_list.html',locals())

@login_required
@csrf_exempt
def uploadfile(request,app_name,model_name):
    savelog.log_info("%s" % request.user, "Info",'访问URL:%s' % request.get_raw_uri())
    if request.method == 'POST':
        admin_class = site.registered_admins[app_name][model_name]
        filename = request.FILES.get('upfile')
        savelog.log_info("%s" % request.user, 'Info','导入配置文件:%s' %filename)
        filepath = fileFunc.writefile(filename,model_name)
        savelog.log_info("%s" % request.user, 'Info','写入本地文件:%s' %filepath)
        try:
            fileFunc.import_funct(request,filepath, model_name, admin_class)
            savelog.log_info("%s" % request.user, "Success",'成功导入配置文件:%s' %filepath)
            return redirect('/asset/%s/'%model_name)
        except AttributeError as e:
            savelog.log_info("%s" % request.user, "Error",'导入配置文件失败:%s' %e)
            pass
            return redirect('/asset/%s/' % model_name)

@login_required
@csrf_exempt
def downloadfile(request,app_name,model_name):
    admin_class = site.registered_admins[app_name][model_name]
    downfile = fileFunc.export_file(model_name=model_name,admin_class=admin_class)
    response = FileResponse(open(downfile, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(os.path.basename(downfile)))

    savelog.log_info("%s" % request.user, "Success",'下载配置文件模板:%s' %downfile)
    return response

def downPlaybook(request,model_name):
    print('download Playbook')
    taskid = request.GET.get('id')
    admin_class = adminfunc(model_name)
    downfile = dbFunc.getPath(uid=taskid,admin_class=admin_class)
    print('filepath',downfile)
    response = FileResponse(open(downfile, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(os.path.basename(downfile)))

    savelog.log_info("%s" % request.user, "Success", '下载Playbook文件:%s' % downfile)
    return response

@login_required
@csrf_exempt
def logs(request,no_render=False):
    model_name = 'logs'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        obj = admin_class.model.objects.all()
        if request.method == 'POST':
            date = request.GET.get('day')
            user = request.GET.get('user')
            action = request.GET.get('action')
            loginfo = readlog.read_log(admin_class=admin_class,date=date,user=user,action=action)
            return HttpResponse(loginfo)

        elif request.method == 'GET':
            querysets, filter_conditions = get_filter_objs(request, admin_class)
            querysets, q_val = get_search_objs(request, querysets, admin_class)
            querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
            paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
            page = request.GET.get('_page')
            try:
                querysets = paginator.page(page)
            except PageNotAnInteger:
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

            if no_render:
                return locals()
            return render(request, 'systems/logs.html', locals())

from cmdbServer.core.ansi import Ansible
from cmdbServer.core.tasks import task

def _querysets(admin_class,request):
    querysets, filter_conditions = get_filter_objs(request, admin_class)
    querysets, q_val = get_search_objs(request, querysets, admin_class)
    querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)

    return locals()

@login_required
@csrf_exempt
def tasks(request):
    model_name = 'servers'
    modelName = 'tasks'
    admin_class = adminfunc(model_name)
    model_class = adminfunc(modelName)
    if request.method == 'GET':
        querysets = _querysets(admin_class=model_class,request=request)


    elif request.method == 'POST':
        file = request.FILES.get('file')
        path = task.files(file)
        return HttpResponse(json.dumps(path))
    return render(request,'tasks/tasks.html',locals())

@login_required
@csrf_exempt
def taskHistory(request):
    model_name = 'tasks'
    admin_class = adminfunc(model_name)
    if request.method == 'GET':
        querysets = _querysets(admin_class=admin_class, request=request)

    elif request.method == 'POST':
        user = request.POST.get('users')
        startdate = request.POST.get('start')
        enddate = request.POST.get('end')
        data = dbFunc.filterd(admin_class,users=user,start_date=startdate,end_date=enddate)

        return HttpResponse(json.dumps({"data":data}))

    return render(request,'tasks/tasks_history.html',locals())

@login_required
def result(request):
    tasksid = request.GET.get('taskid')
    model_name = 'tasks'
    admin_class = adminfunc(model_name)
    obj = admin_class.model.objects.filter(id=tasksid).values("result")[0]
    return HttpResponse(json.dumps(obj))



from dwebsocket import require_websocket

@login_required
@require_websocket
@csrf_exempt
def tasks_websocket(request):
    model_name = 'servers'
    admin_class = adminfunc(model_name)
    modelName = 'tasks'
    model_class = adminfunc(modelName)
    msg = request.websocket.wait().decode("utf-8")
    data = json.loads(request.GET.get('data'))
    savelog.log_info("%s" % request.user, "Info", 'RunTasks:%s' % (data))
    data = task.encrypt(data)
    run = task.taskFunc(admin_class, data,request,model_class)
    request.websocket.send("success")
    return HttpResponse(json.dumps({"status": run}))


