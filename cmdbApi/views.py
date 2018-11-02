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



# class AppList(generics.ListCreateAPIView):
#     queryset = Application.objects.all()
#     serializer_class = ApplicationSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
# class AppDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Application.objects.all()
#     serializer_class = ApplicationSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
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
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devices.objects.all()
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

# class RouterList(generics.ListCreateAPIView):
#     queryset = Router.objects.all()
#     serializer_class = RouterSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
# class RouterDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Router.objects.all()
#     serializer_class = RouterSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
# class GFWList(generics.ListCreateAPIView):
#     queryset = GFW.objects.all()
#     serializer_class = GFWSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
# class GFWDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = GFW.objects.all()
#     serializer_class = GFWSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#


# class TaskList(generics.ListCreateAPIView):
#     queryset = Taskflow.objects.all()
#     serializer_class = TaskflowSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )
#
# class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Taskflow.objects.all()
#     serializer_class = TaskflowSerializer
#     permission_classes = (
#         IsAuthenticatedOrReadOnly,
#     )