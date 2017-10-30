import datetime
from repository import models
class Basic(object):
    def __init__(self,server_obj,basic_key,board_key):
        self.server_obj=server_obj
        self.basic_key=basic_key
        self.boaed_key=board_key
        self.temps = []
        if self.temps:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(self.temps))

    def exec(self):


        temp = {}  # 获取新的主机详细信息
        basic_obj = self.basic_key['data']
        board_obj = self.boaed_key['data']
        temp.update(basic_obj)
        temp.update(board_obj)

        # 数据库更改主机的详细信息
        # server_obj = models.Server.objects.filter(hostname=self.server_obj.hostname).first()
        for i, new_values in temp.items():
            old_values = getattr(self.server_obj, i)
            if new_values != old_values:
                conent = "[%s]的[%s]由[%s]更改为[%s]" % (self.server_obj.hostname, i, old_values, new_values)
                self.temps.append(conent)
                setattr(self.server_obj, i, new_values)


        self.server_obj.latest_date=datetime.datetime.now()#设置调取主机的时间信息
        self.server_obj.save()
        # if self.temps:
        #     models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(self.temps))
            # 删除主机的详细信息

            # if not server_obj:
            #     temp = {}
            #     basic_obj = self.basic_key['data']
            #     board_obj = self.boaed_key['data']
            #     temp.update(basic_obj)
            #     temp.update(board_obj)
            #     server_obj = models.Server.objects.create(**temp)
            #
            #     # 配置nic用户信息
            #     nic_obj = server_dict['nic']['data']
            #     for k, v in nic_obj.items():
            #         v['name'] = k
            #         v['server_obj'] = server_obj
            #         models.NIC.objects.create(**v)
            #     # 配置disk信息
            #     disk_obj = server_dict['disk']['data']
            #     for i in disk_obj.values():
            #         i['server_obj'] = server_obj
            #         models.Disk.objects.create(**i)
            #     # 配置momory的信息
            #     memory = server_dict['memory']['data']
            #     for i in memory.values():
            #         i['server_obj'] = server_obj
            #         models.Memory.objects.create(**i)
            # else: