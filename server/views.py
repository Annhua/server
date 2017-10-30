from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
# Create your views here.
import json
from django.db.models import Q

from repository import models
from utils.page import Pagination
from django.middleware.csrf import get_token
#  服务器信息
def server(request):
    # request.META['CSRF_COOKIE_USED']=True
    get_token(request)
    return render(request,'server.html')

def server_obj(request):
    if request.method == "GET":
        search_config = [
            {'name': 'hostname__contains', 'title': '主机名', 'type': 'input'},
            {'name': 'cabinet_num', 'title': "机柜号", 'type': 'input'},
            {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},
        ]
        table_config=[
            {
                'p': None,
                'display': True,
                'title': '选择',
                'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
                'attr': {'class': 'c1', 'nid': '@id'},
            },
            {
                'p': 'id',
                'display': False,
                'title': 'ID',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
                'attr': {'class': 'c1', 'nid': '@id'},
            },
            {
                'p':'hostname',
                'display': True,
                'title':'主机',
                'text': {'tpl': '{a1}', 'kwargs': {'a1':'@hostname'}},
                'attr': {'class': 'c1','edit':'true','origin':'@hostname','name':'hostname'},
            },
            {
               'p':'sn',
                'display': True,
                'title':'序列化',
                'text': {'tpl': '{a1}', 'kwargs': {'a1':'@sn'}},
                'attr': {'class': 'c1','edit':'true','origin':"@sn",'name':'sn'},
            },
            {
                'p':'os_platform',
                'display': True,
                'title':'系统',
                'text': {'tpl': '{a1}', 'kwargs': {'a1':'@os_platform'}},
                'attr': {'class': 'c1','edit':'true','origin':'@os_platform','name':'os_platform'},
            },
            {
                'p': 'business_unit__name',
                'display': True,
                'title': '业务线',
                'text': {'tpl': '{a1}', 'kwargs': {'a1':'@business_unit__name'}},
                'attr': {'class': 'c1'},
            },
            {
                'p': 'server_status_id',
                "display": True,
                'title': '服务器状态',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
                'attr': {'class': 'c1', 'edit': 'true', 'edit-type': 'select', 'choice-key': 'status_choices',
                         'origin': '@server_status_id', 'name': 'server_status_id'},
            },
            {
                'p': None,
                "display": True,
                'title': '操作',
                'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ',
                         'kwargs': {'nid': '@id', 'uid': '@id'}},
            }
        ]
        values=[]
        for item in table_config:

            item['p'] and values.append(item['p'])


        # 获取后端的搜索条件
        condition_dict = json.loads(request.GET.get('condition'))
        # print(condition_dict)

        con = Q()
        for k, v in condition_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item,))
            con.add(temp, 'AND')


            # 获取用户请求的页码
        current_page = request.GET.get('pageNum')
        total_item_count = models.Server.objects.all().count()

        page_obj = Pagination(current_page, total_item_count,per_page_count=2)



        server_dict=models.Server.objects.filter(con).values(*values)[page_obj.start:page_obj.end]#取的数据应该也是动态生成的
        # print(server_dict)
        response={
            'search_config':search_config,
            'server_dict':list(server_dict),
            'table_config':table_config,
            'global_choices_dict':{
                'status_choices':models.Server.server_status_choices
            },
            'page_html':page_obj.page_html_js()

        }



        return JsonResponse(response)

    elif request.method=='PUT':
        list_dict = json.loads(request.body.decode('utf-8'))
        response={'status':True,'msg':None}

        for item in list_dict:
            try:
                nid=item.pop('nid')
                models.Server.objects.filter(id=nid).update(**item)
            except Exception as e:
                response['status']=False
                response['msg']=str(e)

        return HttpResponse(json.dumps(response))

    elif request.method=='DELETE':
        list_obj=json.loads(request.body.decode('utf-8'))
        print(list_obj)
        response={'status':True,'msg':None}
        for val in list_obj:
            try:
                models.Server.objects.filter(id=val).delete()
            except Exception as e:
                response['status']=False
                response['msg']=str(e)


        return HttpResponse(json.dumps(response))

#  硬盘信息
def disk(request):
    return render(request,'disk.html')

def disk_obj(request):
    table_config=[
        {
            'p': None,
            'display':True,
            'title': '选择',
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
        {
            'p': 'id',
            'display': False,
            'title': 'ID',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
        },
        {
            'p':'slot',
            'display': True,
            'title':'槽位',
            'text': {'tpl': '{a1}', 'kwargs': {'a1':'@slot'}}
        },
        {
           'p':'model',
            'display': True,
            'title':'磁盘型号',
            'text': {'tpl': '{a1}', 'kwargs': {'a1':'@model'}}
        },
        {
            'p':'capacity',
            'display': True,
            'title':'磁盘容量',
            'text': {'tpl': '{a1}', 'kwargs': {'a1':'@capacity'}}
        },
        {
            'p': 'pd_type',
            'display': True,
            'title': '磁盘类型',
            'text': {'tpl': '{a1}', 'kwargs': {'a1':'@pd_type'}}
        },
        {
            'p': 'server_obj',
            'display': True,
            'title': '服务器信息',
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@server_obj__hostname'}}
        }
    ]
    values=[]
    for item in table_config:

        item['p'] and values.append(item['p'])
    disk_dict=models.Disk.objects.values(*values)#取的数据应该也是动态生成的
    p=models.Disk.objects.values('server_obj__hostname')
    print(p)
    response={
        'server_dict':list(disk_dict),
        'table_config':table_config
    }
    return JsonResponse(response)


def row(server_list):
    for row2 in server_list:
        for item in models.Server.server_status_choices:
            if item[0]==row2['server_status_id']:
                row2['server_status_id_name'] = item[1]
                break
        yield row2


def test(request):
    # server_list=models.Server.objects.all()
    # for row in server_list:
    #     print(row.server_status_id,row.get_server_status_id_display())
    # server_list=models.Server.objects.values('hostname','server_status_id')
    # print(server_list)
    for row in server_list:#<QuerySet [{'hostname': 'c1.com', 'server_status_id': 2}]>
        for item in models.Server.server_status_choices:#(1, '上架')(2, '在线')(3, '离线')(4, '下架')
            if item[0]== row['server_status_id']:
                row['server_status_id_name']=item[1]
    print(server_list)


    return  render(request,'ceshi.html')