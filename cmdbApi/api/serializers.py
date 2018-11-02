# -*- coding:utf-8-*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from cmdbServer.models import *


class IdcSerializer(serializers.HyperlinkedModelSerializer):
    cabintd = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='cabint-detail')
    class Meta:
        model = IDC
        # 显示所有字段
        fields = ("url","name","address","contacts","phone","remarks","cabintd")
        depth = 3

class CabintSerializer(serializers.HyperlinkedModelSerializer):
    servers = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='servers-detail')
    devices = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='devices-detail')

    class Meta:
        model = Cabint
        fields = ("number","size","room_number","idc","servers","devices","start_date","end_date")
        # fields = "__all__"
        # depth = 3

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    nics = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='nic-detail')
    cpus = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='cpu-detail')
    disks = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='disk-detail')
    rams = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='ram-detail')

    class Meta:
       model = Servers
       fields = ("url", "model", "sn", "hostname", "ipmi_ipaddress", "cpus", "rams", "nics",
                 "disks", "system", "version", "types", "height", "cabint", "position",
                 "start_date", "end_date", "device_statuses")
        # depth = 3

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    servers = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='servers-detail')
    class Meta:
        model = Company
        fields = ("url","name","model","types","servers")
        depth = 3

#
# class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Application
#         fields = "__all__"
#
class NicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nic
        fields = ("url","sn","name","ipaddress","speed","types","server","remarks")
        depth = 3

class RamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ram
        fields = ("url","sn","name","size","count","server")
        depth = 3

class DiskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Disk
        fields = ("url","sn","name","types","size","server")
        depth = 3

class CpuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CPU
        fields = ("url","name","kernel","frequency","counts","server")
        depth = 3

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    protocols = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='protocol-detail')
    class Meta:
        model = Devices
        fields = ("url","name","sn","company","ipaddress","protocols","height","cabint","position",
                  "device_statuses","start_date","end_date")
        depth = 3

class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    servers = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='servers-detail')

    class Meta:
        model = Protocol
        fields = ("url","name","number","ipaddress","port_range","servers","device")
        depth = 3


# class RouterSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Router
#         fields = "__all__"
#
# class GFWSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = GFW
#         fields = "__all__"
#

#
# class TaskflowSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Taskflow
#         fields = "__all__"





