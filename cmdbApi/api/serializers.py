# -*- coding:utf-8-*-

from rest_framework import serializers
from cmdbServer.models import *
import time




class WarrantySerializer(serializers.HyperlinkedModelSerializer):
    devices = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='device-detail',)
    class Meta:
        model = Cabint
        fields = ("url","company","start_date","end_date","devices")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url',"name")


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    devices = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='device-detail')
    servers = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='servers-detail')
    class Meta:
        model = Company
        fields = ("url","name","model","types","height","devices","servers")
        # depth = 3

class DeviceSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField()
    group_name = serializers.ReadOnlyField()
    class Meta:
        model = Device
        fields = ("url","sn","types","company_name","ipaddress","position",
                  "device_statuses",'group_name',"start_date","end_date","cabint","contacts")

class NicSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField()
    class Meta:
        model = Nic
        fields = ("url","sn","company_name","ipaddress","model","mac_address","speed","types","protocol","server","remarks")

class RamSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField()
    class Meta:
        model = Ram
        fields = ("url","company_name","size","count","server")

class DiskSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField()
    class Meta:
        model = Disk
        fields = ("url","sn","company_name","types","size","server","status","remarks")

class CpuSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField()
    class Meta:
        model = CPU
        fields = ("url","company_name","kernel","frequency","counts","server")

class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    servers = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='servers-detail')

    class Meta:
        model = Protocol
        fields = ("url","name","number","ipaddress","port_range","servers","device")
        depth = 3

class ServerSerializer(serializers.ModelSerializer):
    nics = NicSerializer(many=True,read_only=True,)
    cpus = CpuSerializer(many=True,read_only=True,)
    disks = DiskSerializer(many=True,read_only=True)
    rams = RamSerializer(many=True,read_only=True,)
    group_name = serializers.ReadOnlyField()
    company_name = serializers.ReadOnlyField()

    class Meta:
        model = Servers
        fields = ("url","sn","company","company_name","types","position", "hostname","ipaddress",'vlan',"system","version","nics",
                  "cpus","disks","rams","status",'group',"group_name","start_date","end_date","warranty","contacts")


class CabintSerializer(serializers.HyperlinkedModelSerializer):
    devices = DeviceSerializer(many=True,read_only=True,)
    servers = ServerSerializer(many=True,read_only=True,)
    idc_name = serializers.ReadOnlyField()
    class Meta:
        model = Cabint
        fields = ("url","number","size","useposition","room_number","idc","idc_name","devices","servers")

class IdcSerializer(serializers.ModelSerializer):
    cabintd = CabintSerializer(many=True,read_only=True,)
    class Meta:
        model = IDC
        # 显示所有字段
        fields = ("url","name","address","contacts","phone","cabintd","remarks")
        depth = 10

