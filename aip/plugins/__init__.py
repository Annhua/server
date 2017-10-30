from django.shortcuts import render,HttpResponse
from django.conf import settings
from repository import models
import importlib
from .basic import Basic
class Plugins(object):
    def __init__(self):
        self.settings=settings.PLUGIN_ITEMS
        self.basic_key='basic'
        self.board_key='board'
        print(self.basic_key)


    def process(self,server_dict):
        ret = {'code': 1, 'msg': None}
        hostname = server_dict['basic']['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        print('=====================',server_obj)


        if not server_obj:
            ret['code']=4
            return ret
        #直接传入参数

        obj = Basic(server_obj, server_dict[self.basic_key], server_dict[self.board_key])
        obj.exec()

            # return HttpResponse('请求错误')
        # else:
            #使用内存。网卡等走的流程
        for i,v in self.settings.items():

            try:
                class_obj,class_name=v.rsplit('.',maxsplit=1)

                module=importlib.import_module(class_obj)
                print(module)
                rets=getattr(module,class_name)
                print(rets)


                obj=rets(server_obj,server_dict[i])

                obj.exec()
                print(obj.exec())

            except  Exception as e:
                ret['code']=4
        return ret






