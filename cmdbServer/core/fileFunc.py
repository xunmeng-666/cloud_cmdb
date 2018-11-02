# -*- coding:utf-8-*-
from config.config import *
import xlrd
import xlwt
import os

class FileFunc(object):

    def export_file(self,model_name,admin_class):
        '''
        导出数据到Excel
        :ws:创建新的文件
        :w:向新文件写入sheet，cell_overwrite_ok:单元格允许多次重写
        '''


        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(model_name,cell_overwrite_ok=True)
        objects = admin_class.model.objects.values()
        # for index,titil in enumerate(admin_class.list_filter):
        #     w.write(0,index,titil)
        w.write(0, 0, 'id')
        for index in range(1,len(admin_class.list_display)):
            w.write(0, index,admin_class.list_display[index])

        excel_row = 1
        for contents in objects:
            for index,content in enumerate(contents):
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    admin_class.model.objects.update(id=row[0], name=row[1], address=row[2], contacts=row[3], phone=row[4],
                                          remarks=row[5])
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], name=row[1], address=row[2], contacts=row[3], phone=row[4],
                                          remarks=row[5]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], number=row[1], size=row[2], room_muber=row[3], start_date=row[4],
                                          end_date=row[5]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
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
                if admin_class.model.objects.filter(id=row[0]).exists():
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

    def import_model_file(self,filename,model_name,admin_class):
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
                        admin_class.model(id=row[0], name=row[1]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
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
                if admin_class.model.objects.filter(id=row[0]).exists():
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

    def import_app_file(self,filename,model_name,admin_class):
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
                        admin_class.model(id=row[0], name=row[1],version=row[2]))
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],model=row[2],device_statuses=row[3]))
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],model=row[2],size=row[3],device_statuses=row[4]))
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],model=row[2],size=row[3],device_statuses=row[4]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status

    def import_switch_file(self,filename,model_name,admin_class):
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
                        admin_class.model(id=row[0], company=row[1],model=row[2],nic=row[3],ram=row[4],
                                          ipaddress=row[5],protocol=row[6]))
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],model=row[2],size=row[3],device_statuses=row[4]))
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
                if admin_class.model.objects.filter(id=row[0]).exists():
                    x = x + 1
                else:
                    y += 1
                    WorkList.append(
                        admin_class.model(id=row[0], company=row[1],model=row[2],size=row[3],device_statuses=row[4]))
            else:
                z += 1
        import_status = {'seccuss':y,'skip':x,'error':z}
        admin_class.model.objects.bulk_create(WorkList)
        return import_status


fileFunc = FileFunc()