# -*- coding:utf-8-*-
import json
import datetime
import uuid
from cmdbServer import models
from cmdbServer.core.logger import logger
from django.utils import timezone
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class SaveLog(object):

    def default(self,log):
        if isinstance(log,bytes):
            return str(log,encoding='utf-8')
        return json.JSONEncoder.default(self,log)

    def saveFunc(self,log):
        self.save_log_to_db(log)
        self.save_log_to_file(log)
        return True

    def save_log_to_db(self,log):
        '''save logs to db'''

        try:
            return models.Logs.objects.create(user=log.get('user'),
                                          action=log.get('action'),
                                          content=log.get('content'),
                                          date=log.get('date'),
                                          )
        except TypeError:
            log = self.default(log)
            return models.Logs.objects.create(user=log.get('user'),
                                              action=log.get('action'),
                                              content=log.get('content'),
                                              date=log.get('date'),
                                              )

    def save_log_to_file(self,log):
        if log['action'] == 'Info':
            logger.logger_info(log,)
        elif log['action'] == 'Error':
            logger.logger_error(log)

    def log_info(self,user,action,content):
        now_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        log = {"date":now_date,"user":user,"action":action,'content':content}
        self.saveFunc(log)
        return True

class ReadLog(object):
    def read_log(self,admin_class,date,user,action):
        now_time = datetime.datetime.now()
        if date:
            end_time = now_time - datetime.timedelta(days=int(date))
        if not date:
            end_time = now_time - datetime.timedelta(days=2000)
        if user == 'null' and action == 'null':
            obj = admin_class.model.objects.filter(date__gt=end_time).values()
        elif user and action == 'null':
            obj = admin_class.model.objects.filter(date__gt=end_time,user=user).values()
        elif action and user == 'null':
            obj = admin_class.model.objects.filter(date__gt=end_time,action=action).values()
        else:
            obj = admin_class.model.objects.filter(date__gt=end_time,user=user,action=action).values()
        _list = []
        for objs in obj:
            if type(objs['date']) is datetime.datetime:
                objs['date'] = objs['date'].strftime("%Y-%m-%d %H:%M:%S")
            _list.append(objs)

        return json.dumps({"data":_list})

class HashPass:
    def __init__(self):
        key = 'o9eowjflkwjo2oOoiw'
        self.aes = AES.new(self.pad(key).encode(),AES.MODE_ECB)

    def pad(self,password):
        while len(password) % 32 != 0:
            password += " "
        return password

    def encrypt(self,password):
        pad_password = self.pad(password)
        return b2a_hex(self.aes.encrypt(pad_password.encode("utf-8")))

    def decrypt(self,password):
        return self.aes.decrypt(a2b_hex(password)).decode()

class DBFunc:

    def hostInfo(self,admin_class,hostList=None,id=None):
        '''

        :param admin_class: 传入admin_class类
        :param hostList: 前端传入的主机列表
        :return: 返回主机所有字段
        '''

        # if id:
        #     info = [admin_class.model.objects.filter(id=int(host)).values()[0] for host in hostList if len(host) > 0]
        # elif hostList:
        info = [admin_class.model.objects.filter(id=int(host)).values()[0]  for host in hostList if len(host) > 0]
        return info

    def hostinfo(self,admin_class,groupID):
        info = [admin_class.model.objects.filter(group_id=int(ids)).values() for ids in groupID if len(ids) > 0]
        return info

    def changePasswd(self,admin_class,hostname,password):
        '''
        :param admin_class: DB queryset
        :param hostID: hostID must is a list
        :return:
        '''
        info = admin_class.model.objects.filter(hostname=hostname).update(password=password)
        return info

    def saveTask(self,model_class,users=None,result=None,jobid=None):
        model_class.model.objects.create(users=users,result=result,script_id=jobid)
        taskid = model_class.model.objects.order_by("-id").values("id")[0]['id']
        return taskid

    def updateTask(self,model_class,taskID=None,**kwargs):
        if taskID:
            obj = model_class.model.objects.filter(id=taskID)
            obj.update(**dict(kwargs))
            return True
        model_class.model.objects.create(**dict(kwargs))
        return True

    def saveJob(self,path):
        '''
        :param path: playbook file path
        :return: return a uuid
        '''
        uid = uuid.uuid4().hex
        models.Job.objects.create(id=uid,path=path)
        return uid

    def getPath(self,uid,admin_class=None):
        if admin_class:
            return admin_class.model.objects.filter(id=uid).values("script__path")[0].get("script__path")
        return models.Job.objects.filter(id=uid).values('path')[0].get('path')

    def getResult(self,taskid,admin_class):
        return admin_class.model.objects.filter(id=taskid).values("result")[0]

    def filterd(self,admin_class,users,start_date=None,end_date=None):
        if type(users) is list:
            users = users[0]
        if start_date is None or not start_date:
            start_date = '1900-01-01 00:00:00'
        if end_date is None or not end_date:
            end_date = '2099-12-31 00:00:00'
        date = admin_class.model.objects.filter(users=users).filter(date__gte=start_date).filter(date__lte=end_date).values()
        info = []
        for i in date:
            if i.get('script_id') is not None :
                i['script_id'] = i.get('script_id').hex
            if i.get("date"):
                i['date'] = i.get('date').strftime("%Y-%m-%d %H:%M:%S")
            info.append(i)
        return info


savelog = SaveLog()
readlog = ReadLog()
hashpwd = HashPass()
dbFunc = DBFunc()
