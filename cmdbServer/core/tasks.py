#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from .model_func import dbFunc,hashpwd,savelog
from config.config import script_file
from .ansi import ansible
from .ansibles import run_ansi
import os
import zipfile
import json
import datetime
import shutil


class FileObj:


    def tasksError(self,info):
        return {"Error":"%s" %info}

    def getpath(self,uid,model_class):
        path = dbFunc.getPath(uid)
        playbook = self._zipfile(file=path)
        taskid = dbFunc.saveTask(model_class=model_class,jobid=uid)
        return playbook,taskid,path

    def _zipfile(self,file,path=None):
        if path is None:
            path = os.path.join(script_file,'cache')
        if zipfile.is_zipfile(file):
            zipfile.ZipFile(file).extractall(path=path)
            runYaml = os.path.join(path,'run.yaml')
            return runYaml
        return self.tasksError('Not ZIP File,file is %s' %file)

    def checkFile(self,filePath,filename):
        '''
        检查文件是否存在，如存在择名称+1
        :param filePath:
        :param filename:
        :return:
        '''
        # print('filename',filename)
        nowdate = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        name = "%s.%s" %(filename.split('.')[0]+"_%s" %nowdate,filename.split('.')[1])
        newPath = os.path.join(filePath,name)
        return newPath

    def files(self,files):
        '''
        :param data: 前端传入的文件集合,并执行文件
        :return: playbook path
        '''
        status = {}
        newPath = self.checkFile(script_file,files.name)
        with open(newPath,'wb') as f:
            for chunk in files.chunks():
                f.write(chunk)
            f.close()
        playbook = self._zipfile(file=files.name,path=script_file)
        uid = dbFunc.saveJob(newPath)
        status['uid'] = uid
        status['playbook'] = playbook
        return status

    def removeDir(self,path=None):
        '''删除playbook 缓存目录'''
        try:
            if not path:
                path = os.path.join(script_file, 'cache')
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

class ChangePasswd:
    def encrypt(self,data):
        if data.get("type") == 'changePassword':
            data.update({'data':hashpwd.encrypt(data.get("data"))})
        return data

    def _changePassword(self,admin_class,data,result,request):
        status = {"success":[],'error':[]}
        passwd = data.get('type')
        if passwd == 'changePassword':
            print('result',result)
            for info in result:
                for k,v in info.items():
                    if type(v) is dict:
                        if v.get("unreachable") == 0:
                            c = dbFunc.changePasswd(admin_class, k, password=data.get("data"))
                            status['success'].append(k)
                        else:
                            status['error'].append(k)
                    else:
                        status['error'].append({'info':{k:v}})
            savelog.log_info(request.user, 'Info', "result:%s" % status)
            return status




    def changepassword(self,data,model_class):
        '''
        :param data: 前端传入的字符串，生成playbook
        :return:
        '''
        playbook = ansible.expect_playbook(data)
        return playbook

class Shelled:
    def shellCommand(self,data,model_class):
        '''
        :param data: 前端传入的字符串，生成playbook
        :return:
        '''
        playbook = ansible.playbook(data)
        return playbook

class Task(FileObj,ChangePasswd,Shelled):

    def __init__(self):
        self.result = {'hosts':[],'resutl':[],"command":[]}

    def __del__(self):
        cache = os.path.join(script_file, 'cache')
        if os.path.isdir(cache):
            os.remove(cache)

    def taskFunc(self,admin_class,data,request,model_class):
        '''
        :param data: 前端传入DATA 字典，解析数据并动态生成inventory和playbook
        :return:
        '''
        action = []
        self.model_class = model_class
        self.taskGroup(admin_class,group=data.get('groups'))
        self.taskHost(admin_class,host= data.get("hosts"))
        taskid = None
        if data.get("type") == 'file':
            playbook,taskid,path = self.getpath(data.get("data"),model_class)
            action.append('up file:%s' %path)
        elif data.get("type") == 'changePassword':
            playbook = self.changepassword(data.get("data"),model_class)
            action.append("change password:%s" %data.get("data"))
        else:
            playbook = self.shellCommand(data.get("data"),model_class)
            action.append("%s" %data.get("data"))
        self.result['command'] = action
        inventory = ansible.changeFile()
        result = run_ansi(playbook=playbook,inventory=inventory,websocket=request.websocket)
        status = self._changePassword(admin_class,data,result,request)
        self.result['resutl'] = result
        print('result',result,'status',status,)
        if status:
            self.result['status'] = status
        if not result:result = False
        update = dbFunc.updateTask(model_class=model_class,taskID=taskid,users=str(request.user),result={"taskinfo":self.result})
        self.removeDir()

        return True

    def taskGroup(self,admin_class,group):
        '''
        :param group: group ID in list
        :return:
        '''
        if type(group) is list:
            # 搜索ORM，获取hosts列表 并生成inventory
            hostinfo = dbFunc.hostinfo(admin_class,group)
            print('g_info',hostinfo)
            hosts = [ip.get("ipaddress") for ip in hostinfo]
            inventory = ansible.inventory(hostinfo)
            self.result['hosts'] = list(set(self.result['hosts'] + hosts))
            return inventory
        return False

    def taskHost(self,admin_class,host):
        '''
        :param host: host ID in list
        :return:
        '''
        if type(host) is list:
            # 搜索ORM， 获取hosts 列表并生成inventory
            hostinfo = dbFunc.hostInfo(admin_class,host)
            print('hostinfo',hostinfo)
            hosts = [ ip.get("ipaddress") for ip in hostinfo]
            self.result['hosts'] = list(set(self.result['hosts'] + hosts))
            inventory = ansible.inventory(hostinfo)
            return inventory
        return False

task = Task()
