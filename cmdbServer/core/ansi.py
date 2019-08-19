# _*_ coding:utf-8 _*_
import os
import datetime
import subprocess
from config.config import ansible_path
from cmdbServer.core.model_func import hashpwd

class Ansible:

    def __init__(self):
        self.inventorys = os.path.join(ansible_path, 'inventory')
        self.inven_cache = os.path.join(ansible_path, 'inventory_cache')
        self.playbooks = os.path.join(ansible_path, 'playbook.yaml')
        taskPath = os.path.join(ansible_path,'tasks')
        self.now_date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.logsFile = os.path.join(taskPath, 'ansible_%s.log' %self.now_date)

        if not os.path.exists(taskPath):
            os.mkdir(taskPath)


    def inventory(self,hostinfo):
        if type(hostinfo) is list:
            for auth in hostinfo:
                password = hashpwd.decrypt(auth.get('password')).strip()
                text = '''%s ansible_host=%s ansible_user=%s ansible_password=%s ansible_port=%s'''\
                       %(auth['hostname'],auth['ipaddress'],auth['user'],password,auth['port'])
                self.write_to_file(text,'inventory')
        else:
            auth = hostinfo
            text = '''%s ansible_host=%s ansible_user=%s ansible_password=%s ansible_port=%s'''% \
                   (auth['hostname'], auth['ipaddress'], auth['user'], hashpwd.decrypt(auth['password']), auth['port'])
            self.write_to_file(text, 'inventory')

        return self.inventory

    def changeFile(self):
        with open(self.inventorys,'w+') as f:
            f.write("[all]\n")
            with open(self.inven_cache,'r') as cache:
                for content in cache.readlines():
                    f.write(content)
            cache.close()
        f.close()
        os.remove(self.inven_cache)
        return self.inventorys
    def write_to_file(self,text,type):
        '''
        :param text: is inventory or playbook content
        :param type: must 'inventory' or 'playbook' , catnot other
        :return:
        '''

        if type == 'inventory':
            with open(self.inven_cache, 'a+') as file:
                file.write(text +"\n")
            file.close()

        elif type == 'playbook':
            with open(self.playbooks, 'w+') as file:
                file.write(text +"\n")
            file.close()
            return self.playbooks

        elif type == 'logs':
            with open(self.logsFile,'a+') as file:
                file.write("%s %s\n" %(self.now_date,text))
            file.close()

    def playbook(self,bash):
        text = '''
- name: Run shell command
  hosts: all
  tasks:
    - name: Use shell model
      command: %s
      register: result
    
    - name: Display Result
      debug: msg="{{result}}"
        ''' %bash
        playbook = self.write_to_file(text,'playbook')
        return playbook

    def expect_playbook(self,bash):
        text = '''
- name: Run shell command
  hosts: all
  tasks:
    - name: Use shell model
      shell: echo '%s' | passwd root --stdin > /dev/null 2>&1
        ''' %hashpwd.decrypt(bash).strip()
        playbook = self.write_to_file(text,'playbook')
        return playbook

    def run_ansi(self,inventory=None,playbook=None,request=None):
        if inventory is None:
            inventory = self.inventorys
        if playbook is None:
            playbook = self.playbooks
        stdout = subprocess.Popen("ansible-playbook -i %s %s" %(inventory,playbook),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        try:
            for out in stdout.stdout:
                if len(out) > 1:
                    request.websocket.send(out)
                    self.write_to_file(out.decode('utf-8'), 'logs')
        except:
            print('error')
        if stdout.stderr:
            print('stderr',stdout.stderr.read())
        return self.logsFile


    def check_file(self):
        if os.path.exists(self.inventorys) or os.path.exists(self.playbooks):
            os.remove(self.inventorys)
            os.remove(self.playbooks)

        with open(self.inventorys,'w+') as f:
            f.write("[all]\n")
        f.close()

    def run(self,auht,bash):
        self.check_file()
        for auths in auht:
            self.inventory(auths)
        self.playbook(bash)
        self.run_ansi()


ansible = Ansible()