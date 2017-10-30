from django.shortcuts import render,HttpResponse,redirect

import json
# Create your views here.
from repository import models
from aip.plugins import Plugins
import hashlib
import time

from datetime import date

from django.db.models import Q

def md5(args):
    hs=hashlib.md5()
    hs.update(args.encode('utf-8'))
    return hs.hexdigest()

key='rtttttey'
server_dict={}
def test(request):
    server_time=time.time()

    auth_heard_val=request.META.get('HTTP_AUTH_API')
    ret_obj,time_obj=auth_heard_val.split('|')
    k='%s|%s'%(key,time_obj)
    ret=md5(k)
    client_time=float(time_obj)

    #第一关：
    if (client_time+5) < server_time:
        print(22)
        return HttpResponse('ok')
    #第二关
    if ret == ret_obj:
        print(222)
        return HttpResponse('ok')
    #第三关
    if server_dict.get(ret_obj):
        return HttpResponse('来过了')
    server_dict['ret_obj']=client_time




def server(request):
    if request.method=='GET':
        current_date=date.today()
        #获取当日为采集的主机列表
        host_list=models.Server.objects.filter(Q(Q(latest_date=None)|Q(latest_date__date__lt=current_date))&
                                               Q(server_status_id=2)).values('hostname')

        host_list=list(host_list)
        print(host_list)
        return HttpResponse(json.dumps(host_list))


    if request.method=='POST':
        server_dict=json.loads(request.body.decode('utf-8'))
        if not server_dict['basic']['status']:
            return HttpResponse('iiiiiiiii')

        # hostname=server_dict['basic']['data']['hostname']
        # server_obj=models.Server.objects.filter(hostname=hostname).first()

        cls=Plugins()
        response=cls.process(server_dict)
        print('====',response)
        print(type(response))
        return HttpResponse(json.dumps(response))

    # print(server_obj)
    # if not server_dict['basic']['status']:
    #     return HttpResponse('请求错误')
    # if not server_obj:
    #     temp={}
    #     basic_obj=server_dict['basic']['data']
    #     board_obj=server_dict['board']['data']
    #     temp.update(basic_obj)
    #     temp.update(board_obj)
    #     server_obj=models.Server.objects.create(**temp)
    #
    #     #配置nic用户信息
    #     nic_obj=server_dict['nic']['data']
    #     for k,v in nic_obj.items():
    #         v['name']=k
    #         v['server_obj']=server_obj
    #         models.NIC.objects.create(**v)
    #     #配置disk信息
    #     disk_obj=server_dict['disk']['data']
    #     for i in disk_obj.values():
    #         i['server_obj']=server_obj
    #         models.Disk.objects.create(**i)
    #     #配置momory的信息
    #     memory=server_dict['memory']['data']
    #     for i in  memory.values():
    #         i['server_obj']=server_obj
    #         models.Memory.objects.create(**i)
    # else:
    #     #有主机信息更改主机信息
    #     temp = {}#获取新的主机详细信息
    #     basic_obj = server_dict['basic']['data']
    #     board_obj = server_dict['board']['data']
    #     temp.update(basic_obj)
    #     temp.update(board_obj)
    #     #数据库更改主机的详细信息
    #     server_obj = models.Server.objects.filter(hostname=hostname).first()
    #     temps=[]
    #     for i ,new_values in temp.items():
    #         old_values=getattr(server_obj,i)
    #         if new_values !=old_values:
    #             conent="[%s]的[%s]由[%s]更改为[%s]"%(hostname,i,old_values,new_values)
    #             temps.append(conent)
    #             setattr(server_obj,i,new_values)
    #     server_obj.save()
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj,content=';'.join(temps),creator_id=request.user)
    #     #删除主机的详细信息
    #
    #     #配置disk详细信息
    #     disk_obj=server_dict['disk']['data']
    #     new_disk_keys=set(disk_obj.keys())
    #     disk_list=models.Disk.objects.all()
    #     old_disk_keys={item.slot for item in disk_list}
    #     # print(old_disk_keys)
    #     app_disk=new_disk_keys - old_disk_keys
    #     del_disk = old_disk_keys - new_disk_keys
    #     same_disk = new_disk_keys & old_disk_keys
    #     #增加硬盘信息
    #     for i in app_disk:
    #         obj=disk_obj[i]
    #         obj['server_obj']=server_obj
    #         models.Disk.objects.create(**obj)
    #         conent="Disk增加信息[%s]"%obj
    #         temps.append(conent)
    #     # print(temps)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj,content=';'.join(temps),creator_id=request.user)
    #
    #     #删除硬盘信息
    #     for i in del_disk:
    #         conent = "Disk删除硬盘信息[%s]" % (disk_obj[i])
    #         models.Disk.objects.filter(slot__in=i).delete()
    #         temps.append(conent)
    #         print(conent)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps), creator_id=request.user)
    #
    #     #共同相同：same_disk
    #     for i in same_disk:
    #         new_values=disk_obj[i]
    #         disk_f = models.Disk.objects.filter(slot=i).first()
    #         for i,new_values_new in new_values.items():
    #             old_values = getattr(disk_f, i)
    #             if new_values_new!=old_values:
    #                 setattr(disk_f,i,new_values_new)
    #                 conent="[%s]的[%s]由[%s]更改为[%s]"%(i,i,old_values,new_values_new)
    #                 temps.append(conent)
    #     disk_f.save()
    #     if temp:
    #         models.ServerRecord.objects.create(server_obj=server_obj,content=';'.join(temps))
    #
    #     #更新memory信息
    #     memory_obj = server_dict['memory']['data']
    #     new_memory_keys = set(memory_obj.keys())
    #     memory_list = models.Memory.objects.all()
    #     old_memory_keys = {item.slot for item in memory_list}
    #     # print(old_disk_keys)
    #     app_memory = new_memory_keys - old_memory_keys
    #     del_memory= old_memory_keys - new_memory_keys
    #     same_memory = new_memory_keys & old_memory_keys
    #     # 增加硬盘信息
    #     temps=[]
    #     for i in app_memory:
    #         obj = memory_obj[i]
    #         obj['server_obj'] = server_obj
    #         models.Memory.objects.create(**obj)
    #         conent = "memory增加信息[%s]" % obj
    #         temps.append(conent)
    #     # print(temps)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps),
    #                                            )
    #
    #     # 删除硬盘信息
    #     for i in del_memory:
    #         conent = "Disk删除硬盘信息[%s]" % (memory_obj[i])
    #         models.Memory.objects.filter(slot__in=i).delete()
    #         temps.append(conent)
    #         # print(conent)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps),
    #                                            )
    #
    #     # 共同相同：same_disk
    #     for i in same_memory:
    #         new_values = memory_obj[i]
    #         memory_f = models.Memory.objects.filter(slot=i).first()
    #         for i, new_values_new in new_values.items():
    #             old_values = getattr(memory_f, i)
    #             if new_values_new != old_values:
    #                 setattr(memory_f, i, new_values_new)
    #                 conent = "[%s]的[%s]由[%s]更改为[%s]" % (i, i, old_values, new_values_new)
    #                 temps.append(conent)
    #     memory_f.save()
    #     # if temp:
    #     #     models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps))
    #
    #
    #     #配置nic信息
    #     nic_obj=server_dict['nic']['data']
    #     nic_list=server_obj.nic.values('name')
    #     new_nic_obj=set(server_dict['nic']['data'].keys())
    #     old_nic_obj={nic['name'] for nic in nic_list}
    #     print(new_nic_obj)
    #     print(old_nic_obj)
    #     app_nic = new_nic_obj - old_nic_obj
    #     del_nic = old_nic_obj - new_nic_obj
    #     same_nic = new_nic_obj & old_nic_obj
    #     #增加nic信息
    #     for item in app_nic:
    #         values=nic_obj[item]
    #         values['server_obj']=server_obj
    #         models.NIC.objects.create(**values)
    #         conent = "nic增加信息[%s]" %item
    #         temps.append(conent)
    #         # print(temps)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps))
    #
    #     #删除硬盘信息
    #
    #     for item in del_nic:
    #         conent="nic删除信息[%s]"%item
    #         models.NIC.objects.filter(server_obj=server_obj,name__in=item).delete()
    #         temps.append(conent)
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps))
    #
    #     for name in same_nic:
    #         value = nic_obj[name]
    #         obj = models.NIC.objects.filter(server_obj=server_obj, name=name).first()
    #         for k, new_val in value.items():
    #             old_val = getattr(obj, k)
    #             if old_val != new_val:
    #                 conent= "名称%s的网卡的%s由%s变更为%s" % (name, k, old_val, new_val)
    #                 temps.append(conent)
    #                 setattr(obj, k, new_val)
    #     obj.save()
    #     if temps:
    #         models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps))

    # return HttpResponse('ok')

import xlrd

myWorkbook=xlrd.open_workbook('yy.xlsx')
mySheets=myWorkbook.sheets()  #获取工作表中的list
