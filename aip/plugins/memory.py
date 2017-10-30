
from repository import models
class Memory(object):
    def __init__(self,server_obj,server_dict):
        self.server_obj=server_obj
        self.server_dict=server_dict
        self.temps=[]

    def exec(self):
        # 更新memory信息
        memory_obj = self.server_dict['data']
        new_memory_keys = set(memory_obj.keys())
        memory_list = models.Memory.objects.all()
        old_memory_keys = {item.slot for item in memory_list}
        # print(old_disk_keys)
        app_memory = new_memory_keys - old_memory_keys
        del_memory = old_memory_keys - new_memory_keys
        same_memory = new_memory_keys & old_memory_keys
        # 增加硬盘信息
        if app_memory:
            self.add_memory_key( memory_obj, app_memory)

        if del_memory:
            self.del_memory_key(del_memory, memory_obj)
        if same_memory:
            self.same_memory_key(same_memory, memory_obj)
        if self.temps:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(self.temps))

    def add_memory_key(self,memory_obj,app_memory):
        for i in app_memory:
            obj = memory_obj[i]
            obj['server_obj'] = self.server_obj
            models.Memory.objects.create(**obj)
            conent = "memory增加信息[%s]" % obj
            self.temps.append(conent)
        # print(temps)
        # if temps:
        #     models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps),
        #                                        )

        # 删除硬盘信息
    def del_memory_key(self,del_memory,memory_obj):
        for i in del_memory:
            conent = "Disk删除硬盘信息[%s]" % (memory_obj[i])
            models.Memory.objects.filter(slot__in=i).delete()
            self.temps.append(conent)
            # print(conent)
        # if temps:
        #     models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps),
        #                                        )

        # 共同相同：same_disk
    def same_memory_key(self,same_memory,memory_obj):
        for i in same_memory:
            new_values = memory_obj[i]
            memory_f = models.Memory.objects.filter(slot=i).first()
            for i, new_values_new in new_values.items():
                old_values = getattr(memory_f, i)
                if new_values_new != old_values:
                    setattr(memory_f, i, new_values_new)
                    conent = "[%s]的[%s]由[%s]更改为[%s]" % (i, i, old_values, new_values_new)
                    self.temps.append(conent)
            memory_f.save()
        # if temp:
        #     models.ServerRecord.objects.create(server_obj=server_obj, content=';'.join(temps))

