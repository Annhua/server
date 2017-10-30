

from repository import models
class NIC(object):
    def __init__(self,server_obj,server_dict):
        self.server_obj=server_obj
        self.nic_dict=server_dict
        self.temps=[]

    def exec(self):
        # 配置nic信息
        nic_obj =self.nic_dict['data']
        nic_list = self.server_obj.nic.values('name')
        new_nic_obj = set(self.nic_dict['data'].keys())
        old_nic_obj = {nic['name'] for nic in nic_list}
        # print(new_nic_obj)
        # print(old_nic_obj)
        app_nic = new_nic_obj - old_nic_obj
        del_nic = old_nic_obj - new_nic_obj
        same_nic = new_nic_obj & old_nic_obj
        if app_nic:
            self.add_nic(app_nic,nic_obj)

        if del_nic:
            self.del_nic(del_nic)

        if same_nic:
            self.same_nic_key(same_nic,nic_obj)

        if self.temps:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(self.temps))
        # 增加nic信息
    def add_nic(self,app_nic,nic_obj):
        for item in app_nic:
            values = nic_obj[item]
            values['server_obj'] = self.server_obj
            models.NIC.objects.create(**values)
            conent = "nic增加信息[%s]" % item
            self.temps.append(conent)
            # print(temps)

        # 删除硬盘信息
    def del_nic(self,del_nic):
        for item in del_nic:
            conent = "nic删除信息[%s]" % item
            models.NIC.objects.filter(server_obj=self.server_obj, name__in=item).delete()
            self.temps.append(conent)

    def same_nic_key(self,same_nic,nic_obj):
        for name in same_nic:
            value = nic_obj[name]
            obj = models.NIC.objects.filter(server_obj=self.server_obj, name=name).first()
            for k, new_val in value.items():
                old_val = getattr(obj, k)
                if old_val != new_val:
                    conent = "名称%s的网卡的%s由%s变更为%s" % (name, k, old_val, new_val)
                    self.temps.append(conent)
                    setattr(obj, k, new_val)
            obj.save()

