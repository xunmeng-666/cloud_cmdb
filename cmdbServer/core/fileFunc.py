# -*- coding:utf-8-*-
from config.config import *
import xlrd
import xlwt
import os
import datetime

class FileFunc(object):
    def _device_id(self,admin_class,field):
        if type(field) is int:
            return field
        return admin_class.model.device.get_queryset().filter(name=field).values('id')[0]['id']

    def _company_id(self,admin_class,field):
        if type(field) is int:
            return field
        return admin_class.model.company.get_queryset().filter(name=field).values('id')[0]['id']

    def _group_id(self,admin_class,field):
        if type(field) is int:
            return field
        return admin_class.model.group.get_queryset().filter(name=field).values('id')[0]['id']


    def _cabint_id(self,admin_class,field):
        if type(field) is int:
            return field
        print('c_id',admin_class.model.cabint.get_queryset().filter(number=field).values('id')[0]['id'])
        return admin_class.model.cabint.get_queryset().filter(number=field).values('id')[0]['id']

    def _warranty_id(self,admin_class,field):
        if type(field) is datetime.datetime:
            return  str(field)
        elif not field:
            return None
        fields = xlrd.xldate_as_datetime(field,0)
        return admin_class.model.warranty.get_queryset().filter(end_date=fields).values('id')[0]['id']

    def _server_id(self,admin_class,field):
        if type(field) is int:
            return field
        return admin_class.model.server.get_queryset().filter(hostname=field).values('id')[0]['id']

    def _protocol_id(self,admin_class,field):
        if type(field) is int:
            return field
        return admin_class.model.protocol.get_queryset().filter(number=field).values('id')[0]['id']

    def export_file(self,model_name,admin_class):
        '''
        导出数据到Excel
        :ws:创建新的文件
        :w:向新文件写入sheet，cell_overwrite_ok:单元格允许多次重写
        '''


        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(model_name,cell_overwrite_ok=True)
        objects = admin_class.model.objects.values()
        for index in range(0,len(admin_class.export_fields)):

            w.write(0, index,admin_class.export_fields[index])

        excel_row = 1
        for contents in objects:
            for index,content in enumerate(contents):
                if type(contents[content]) is datetime.datetime:
                    contents[content] = str(contents[content].strftime('%Y-%m-%d %H:%M:%S'))
                w.write(excel_row,index,contents[content])
            excel_row += 1

        if os.path.exists(export_file):
            os.remove(export_file)
        ws.save(export_file)
        return export_file

    def import_idc_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(name=row[1]).exists():
                    x = x + 1

                else:
                    WorkList.append(
                        admin_class.model(id=row[0], name=row[1], address=row[2], contacts=row[3], phone=row[4],
                                          remarks=row[5]))
                    y += 1
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        try:
            admin_class.model.objects.bulk_create(WorkList)
        except AttributeError as e:
            pass
        return import_status

    def import_cabint_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(number=row[1]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], number=row[1], size=row[2], room_number=row[3],
                                          idc_id=row[4]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        try:
            admin_class.model.objects.bulk_create(WorkList)
        except AttributeError as e:
            pass
        return import_status

    def import_company_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(name=row[1],model=row[2]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], name=row[1], model=row[2], types=row[3], height=row[4]))
            else:
                z += 1
        import_status = {'seccuss': y, 'skip': x, 'error': z}
        print('work',WorkList)
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_protocol_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                device_id = self._device_id(admin_class,row[5])
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], name=row[1],number=row[2],ipaddress=row[3],port_range=row[4],device_id=device_id))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_nic_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                company_id = self._company_id(admin_class, row[2])
                server_id = self._server_id(admin_class,row[9])
                protocol_id = self._protocol_id(admin_class,row[7])
                if admin_class.model.objects.filter(ipaddress=row[3]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], sn=row[1],company_id=company_id,ipaddress=row[3],model=row[4],mac_address=row[5],
                                          types=row[6],protocol_id=protocol_id,speed=row[8],server_id=server_id,remarks=row[10]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_ram_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                company_id = self._company_id(admin_class,row[1])
                server_id = self._server_id(admin_class, row[4])
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company_id=company_id,size=row[2],count=row[3],server_id=server_id))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_disk_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                company_id = self._company_id(admin_class, row[2])
                server_id = self._server_id(admin_class, row[5])
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1

                    WorkList.append(
                        admin_class.model(id=row[0], sn=row[1],company_id=company_id,types=row[3],size=row[4],server_id=server_id,
                                          status=row[6],remarks=row[7]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_cpu_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                company_id = self._company_id(admin_class, row[1])
                server_id = self._server_id(admin_class,row[5])
                if admin_class.model.objects.filter(id=row[0], company_id=company_id,kernel=row[2],frequency=row[3],counts=row[4],server_id=server_id).exists():
                    x = x + 1
                else:
                    y += 1

                    WorkList.append(
                        admin_class.model(id=row[0], company_id=company_id,kernel=row[2],frequency=row[3],counts=row[4],server_id=server_id))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_group_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(name=row[1]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], name=row[1]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_device_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        PositionList = []
        company_height = 0
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(sn=row[1],ipaddress=row[5]).exists():
                    x += 1
                else:
                    y += 1
                    company_id = self._company_id(admin_class, row[4])
                    cabint_id = self._cabint_id(admin_class, row[6])
                    group_id = self._group_id(admin_class, row[9])
                    warranty_id = self._warranty_id(admin_class, row[11])
                    cabint_useposition = int(
                        admin_class.model.cabint.get_queryset().filter(id=cabint_id).values('useposition')[0]['useposition'])
                    company_height += int(
                        admin_class.model.company.get_queryset().filter(id=company_id).values('height')[0]['height'])
                    cabint_useposition += company_height
                    WorkList.append(
                        admin_class.model(id=row[0], sn=row[1],name=row[2],types=row[3],company_id=company_id,ipaddress=row[5],
                                          cabint_id=cabint_id,position=row[7],device_statuses=row[8],
                                          group_id=group_id,warranty_id=warranty_id,contacts=row[11],))
                    PositionList.append({'id': cabint_id, 'useposition': cabint_useposition})
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        for position in PositionList:
            admin_class.model.cabint.get_queryset().filter(id=position['id']).update(useposition=position['useposition'])
        return import_status

    def import_servers_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        PositionList = []
        x = y = z = 0
        company_height = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:

                if admin_class.model.objects.filter(sn=row[1], ipaddress=row[7]).exists():
                    x = x + 1
                else:
                    y += 1
                    company_id = self._company_id(admin_class,row[2])
                    cabint_id = self._cabint_id(admin_class,row[4])
                    group_id = self._group_id(admin_class,row[12])
                    warranty_id = self._warranty_id(admin_class,row[13])
                    cabint_useposition = int(
                        admin_class.model.cabint.get_queryset().filter(id=cabint_id).values('useposition')[0]['useposition'])
                    company_height += int(admin_class.model.company.get_queryset().filter(id=company_id).values('height')[0]['height'])
                    cabint_useposition += company_height
                    WorkList.append(
                        admin_class.model(id=row[0], sn=row[1],company_id=company_id,types=row[3],cabint_id=cabint_id,position=row[5],
                                          hostname=row[6],ipaddress=row[7],vlan_id=row[8],system=str(row[9]),version=row[10],status=row[11],
                                          group_id=group_id,warranty_id=warranty_id,userinfo=row[14],contacts=row[15]))
                    PositionList.append({'id': cabint_id, 'useposition': cabint_useposition})

            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        for position in PositionList:
            admin_class.model.cabint.get_queryset().filter(id=position['id']).update(useposition=position['useposition'])
        return import_status


    def import_warranty_file(self,filename,model_name,admin_class):
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_name(model_name)
        nrows = table.nrows
        ncols = table.ncols
        WorkList = []
        x = y = z = 0
        for i in range(1, nrows):
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = int(row[j])
            if row:
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],start_date=row[2],end_date=row[3]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_funct(self,filename,model_name,admin_class):
        model_dict = {
            'idc':self.import_idc_file,
            'cabint':self.import_cabint_file,
            'company':self.import_company_file,
            'protocol':self.import_protocol_file,
            'nic':self.import_nic_file,
            'ram':self.import_ram_file,
            'disk':self.import_disk_file,
            'cpu':self.import_cpu_file,
            'group':self.import_group_file,
            'device':self.import_device_file,
            'servers':self.import_servers_file,
            'warranty':self.import_warranty_file,
        }
        if model_name not in model_dict:return False
        res = model_dict[model_name](filename=filename,model_name=model_name,admin_class=admin_class)
        return res

    def writefile(self,filename,model_name):
        filepath = os.path.join(import_file_dir,"%s.xls" %model_name)
        if os.path.exists(filepath):
            os.remove(filepath)
        f = open(filepath,'wb')
        for chunk in filename.readlines():
            if type(chunk) is float:
                chunk = int(chunk)
            f.write(chunk)
        f.close()
        return filepath
fileFunc = FileFunc()


