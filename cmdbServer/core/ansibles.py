# -*- coding:utf-8-*-
#!/usr/local/bin/python


import os
import json
import logging
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleParserError
from ansible import constants as C



class AnsibleTaskResultCallback(CallbackBase):
    def __init__(self,websocket,*args):
        super(AnsibleTaskResultCallback,self).__init__(*args)
        self.logs = []
        self.result = {}
        self.faield = {}
        self.hosts = None
        self.websocket = websocket

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        failed = "failed:[%s]>>:%s" %(host,result._result.get("stdout"))
        self.websocket.send(failed)



    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.websocket.send("ok:[%s]" %host)
        if result._result.get("stdout"):
            for info in result._result.get('stdout_lines'):
                self.websocket.send("%s\n" %info)

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        fatal = "fatal:[%s]: UNREACHABLE! => %s" %(host,result._result.get("msg"))
        self.websocket.send(fatal)
        self.faield[host] = result._result.get("msg")

    def v2_playbook_on_play_start(self, play):
        plays = "PLAY:[%s]" %play.name
        self.hosts = play.hosts
        self.websocket.send(plays)

    def v2_playbook_on_task_start(self, task, is_conditional):
        tasks = "TASK:[%s]" %task
        self.websocket.send(tasks)

    def v2_playbook_on_no_hosts_matched(self):
        '''打印警告信息'''
        warning = "Could not match supplied host pattern, ignoring: %s" %self.hosts
        self.websocket.send(warning)
        self.logs.append(warning)

    def v2_playbook_on_stats(self, stats):
        _list = []
        recap = "\nPLAY RECAP *********************************************************************"
        self.websocket.send(recap)
        _list.append(recap)
        for host in stats.processed:
            info = stats.summarize(host)
            _dict = "%s\t\tok=%s,changed=%s,unreachable=%s,failed=%s,skipped=%s" %(host,
                                                                                 info.get("ok"),
                                                                                 info.get("changed"),
                                                                                 info.get("unreachable"),
                                                                                 info.get("failures"),
                                                                                 info.get("skipped"),
                                                                                 )
            self.websocket.send(_dict)
            self.result[host] = info
            _list.append(_dict)
        self.logs.append(self.result)
        if self.faield:
            self.logs.append(self.faield)


class AnsibleTask:
    def __init__(self, hosts_list, extra_vars=None):
        self.hosts_file = hosts_list
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff', 'host_key_checking', 'listhosts', 'listtasks', 'listtags', 'syntax'])
        self.options = Options(connection='ssh', module_path=None, forks=10,
                               become=None, become_method=None, become_user=None, check=False, diff=False,
                               host_key_checking=False, listhosts=None, listtasks=None, listtags=None, syntax=None)
        self.loader = DataLoader()
        self.passwords = dict(vault_pass='secret')

        self.inventory = InventoryManager(loader=self.loader, sources=[self.hosts_file])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if extra_vars:
            self.variable_manager.extra_vars = extra_vars
            logging.info('variable111',self.variable_manager.extra_vars)

    def exec_playbook(self,websocket, playbooks):
        if not os.path.exists(playbooks[0]):
            websocket.send("Error: playbook does not exist or not fund run.yaml")
            logging.error('not fund playbook')
            code = 1000
            complex = {"playbook":playbooks,'msg':playbooks +"playbook does not exist",'flag':False}
            simple = 'playbook does not exist about' + playbooks
            return code,complex,simple
        results_callback = AnsibleTaskResultCallback(websocket)
        playbook = PlaybookExecutor(playbooks=playbooks, inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.options, passwords=self.passwords)
        setattr(getattr(playbook, '_tqm'), '_stdout_callback', results_callback)
        try:
            playbook.run()
        except AnsibleParserError as e:
            print('RunError: %s' %e)
        return results_callback.logs


def run_ansi(playbook,inventory,websocket):
    task = AnsibleTask(hosts_list=inventory)
    result = task.exec_playbook(websocket=websocket,playbooks=[playbook])
    return result

# if __name__ == '__main__':
#     inventory = '/Users/lixichang/Documents/项目/个人/monitor/Open_CMDB/cmdbServer/ansible/inventory'
#     playbook = '/Users/lixichang/Documents/项目/个人/monitor/Open_CMDB/cmdbServer/ansible/playbook.yaml'
#     run_ansi(playbook,inventory)
