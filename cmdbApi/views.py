from cmdbApi.api.serializers import *
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IdcList(generics.ListCreateAPIView):
    '''
    list all code IDC, and create a new idc list
    '''
    queryset = IDC.objects.all()
    serializer_class = IdcSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
class IdcDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    list all code IDC ,supper 'PUT','DELETE','GET'
    '''
    queryset = IDC.objects.all()
    serializer_class = IdcSerializer

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CabintList(generics.ListCreateAPIView):
    queryset = Cabint.objects.all()
    serializer_class = CabintSerializer

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CabintDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabint.objects.all()
    serializer_class = CabintSerializer

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class ServerList(generics.ListCreateAPIView):
    queryset = Servers.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class ServerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servers.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )



class warrantyList(generics.ListCreateAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class warrantyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class NicList(generics.ListCreateAPIView):
    queryset = Nic.objects.all()
    serializer_class = NicSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class NicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nic.objects.all()
    serializer_class = NicSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class RamList(generics.ListCreateAPIView):
    queryset = Ram.objects.all()
    serializer_class = RamSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class RamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ram.objects.all()
    serializer_class = RamSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class DiskList(generics.ListCreateAPIView):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class DiskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CpuList(generics.ListCreateAPIView):
    queryset = CPU.objects.all()
    serializer_class = CpuSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class CpuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CPU.objects.all()
    serializer_class = CpuSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class ProtocolList(generics.ListCreateAPIView):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class ProtocolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class BondingList(generics.ListCreateAPIView):
    queryset = Bonding.objects.all()
    serializer_class = BondingSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class BondingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bonding.objects.all()
    serializer_class = BondingSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
