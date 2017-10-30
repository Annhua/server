
from repository import models

class Disk(object):
    def __init__(self,server_obj,server_dict):
        self.server_obj=server_obj
        self.server_dict=server_dict
        self.temps=[]





    def exec(self):
        # 配置disk详细信息
        disk_obj = self.server_dict['data']
        new_disk_keys = set(disk_obj.keys())
        disk_list = models.Disk.objects.all()
        old_disk_keys = {item.slot for item in disk_list}
        # print(old_disk_keys)
        app_disk = new_disk_keys - old_disk_keys
        del_disk = old_disk_keys - new_disk_keys
        same_disk = new_disk_keys & old_disk_keys
        if app_disk:
            self.add_disk_exec(app_disk, disk_obj)

        if del_disk:
            self.del_disk_exec(del_disk,disk_obj)
        if same_disk:
            self.same_disk_exec(same_disk, disk_obj)

        if self.temps:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(self.temps))
        # 增加硬盘信息


    def add_disk_exec(self,app_disk,disk_obj):
        for i in app_disk:
            obj = disk_obj[i]
            obj['server_obj'] = self.server_obj
            models.Disk.objects.create(**obj)
            conent = "Disk增加信息[%s]" % obj
            self.temps.append(conent)


        # 删除硬盘信息
    def del_disk_exec(self,del_disk,disk_obj):
        for i in del_disk:
            conent = "Disk删除硬盘信息[%s]" % (disk_obj[i])
            models.Disk.objects.filter(slot__in=i).delete()
            self.temps.append(conent)


        # 共同相同：same_disk
    def same_disk_exec(self,same_disk,disk_obj):
        for i in same_disk:
            new_values = disk_obj[i]
            disk_f = models.Disk.objects.filter(slot=i).first()
            for i, new_values_new in new_values.items():
                old_values = getattr(disk_f, i)
                if new_values_new != old_values:
                    setattr(disk_f, i, new_values_new)
                    conent = "[%s]的[%s]由[%s]更改为[%s]" % (i, i, old_values, new_values_new)
                    self.temps.append(conent)
            disk_f.save()

