from django.shortcuts import render,redirect,HttpResponse
from django.http import FileResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from cmdbServer.admin_base import site
from cmdbServer import forms
from cmdbServer.core.fileFunc import fileFunc
import json
# Create your views here.

def account_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            # save_db.save_logs_to_db("User:%s Login system" % request.user)
            return  redirect(request.GET.get('next') or '/')

    return render(request, 'login.html', locals())

def account_logout(request,**kwargs):
    request.session.clear()
    logout(request)

    return redirect('/accounts/login/')

@login_required
def index(request):
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name]['idc']
        objects = admin_class.model.objects.values('id','name')
    return render(request,'index.html',locals())


def adminfunc():
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name]
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
    """
    q_val = request.GET.get('_q')  # None
    if q_val:
        q_obj = Q()
        q_obj.connector = "OR"
        for search_field in admin_class.search_fields:  # 2
            q_obj.children.append(("%s__contains" % search_field, q_val))
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

# @login_required
def idc(request,no_render=False):
    model_name = 'idc'
    # admin_class = adminfunc()[model_name]
    for app_name in site.registered_admins:
        # for model_name in site.registered_admins[app_name]:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data = request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/idc/")
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
        return render(request,'idc/idc.html',locals())


def add_idc(request,app_name,model_name):

    admin_class = site.registered_admins[app_name][model_name]
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == 'POST':
        form_obj = form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/asset/%s/"%model_name)
    elif request.method == 'GET':
        form_obj = form()
    return render(request,'gloab-form/add_form.html',locals())

def table_obj_detail(request,app_name,model_name):

    admin_class = site.registered_admins[app_name][model_name]
    obj = admin_class.model.objects.all()
    obj_id = request.GET.get('id')
    if model_name == 'idc':
        '''显示机柜数量，机柜使用百分比'''
        objects = obj.filter(id=obj_id).values('cabintd__number','cabintd__size','cabintd__useposition')
    elif model_name == 'cabint':
        '''显示单个几个使用详情，机柜编号，位置、设备IP、服务器IP'''
        objects = obj.filter(id=obj_id).values('number','useposition','devices__company__name',"devices__position",
                                               "servers__hostname","servers__position")
    elif model_name == 'devices':
        pass
    elif model_name == "servers":
        pass



    return render(request,'gloab-form/detail_form.html',locals())


@csrf_exempt
def table_obj_del(request,app_name,model_name):
    obj_id = request.GET.get('idAll')
    admin_class = site.registered_admins[app_name][model_name]
    if ',' in obj_id:
        status = {'success':[],'error':[]}
        for id in obj_id.split(','):
            if id:
                obj = admin_class.model.objects.get(id=id.strip())
                obj.delete()
                status['success'].append(id)
        return HttpResponse(json.dumps(status))
    else:
        obj = admin_class.model.objects.get(id=obj_id)
        obj.delete()
        return redirect("/asset/{model_name}".format(model_name=model_name))

@csrf_exempt
def table_obj_change(request,app_name,model_name,no_render=False):
    admin_class = site.registered_admins[app_name][model_name]
    object_id = request.GET.get('project_id')
    obj = admin_class.model.objects.get(id=object_id)
    form = forms.create_dynamic_modelform(admin_class.model)
    if request.method == 'GET':
        form_obj = form(instance=obj)

    elif request.method == 'POST':
        form_obj = form(instance=obj,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/asset/%s"%model_name)
    if no_render:
        return locals()
    else:
        return render(request,'gloab-form/change_form.html',locals())

def cabint(request, no_render=False):
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

def company(request,no_render=False):
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


def device(request,no_render=False):
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
            for row in querysets:
                print("row", row)
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
        return render(request, 'device/device_list.html', locals())

def device_group(request,no_render=False):
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
        return render(request, 'device/device_group.html', locals())

def server(request,no_render=False):
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
                querysets = paginator.page(1)
            except EmptyPage:
                querysets = paginator.page(paginator.num_pages)

        if no_render:
            return locals()
        return render(request, 'gloab-form/list_form.html', locals())

def warranty(request,no_render=False):
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

def protocol(request,no_render=False):
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


def cpu(request,no_render=False):
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

def disk(request,no_render=False):
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

def ram(request,no_render=False):
    model_name = 'ram'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/ram/")
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

def nic(request,no_render=False):
    model_name = 'nic'
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name][model_name]
        form = forms.create_dynamic_modelform(admin_class.model)
        if request.method == 'POST':
            form_obj = form(data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect("/asset/nic/")
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

@csrf_exempt
def uploadfile(request,app_name,model_name):

    if request.method == 'POST':
        admin_class = site.registered_admins[app_name][model_name]
        filename = request.FILES.get('upfile')
        filepath = fileFunc.writefile(filename,model_name)
        try:
            fileFunc.import_funct(filepath, model_name, admin_class)
            return redirect('/asset/%s/'%model_name)
        except AttributeError as e:
            print('err',e)
            return False

@csrf_exempt
def downloadfile(request,app_name,model_name):
    admin_class = site.registered_admins[app_name][model_name]
    downfile = fileFunc.export_file(model_name=model_name,admin_class=admin_class)
    response = FileResponse(open(downfile,'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content=Disposition'] = 'application;filename="%s.xls"' %model_name
    return response


