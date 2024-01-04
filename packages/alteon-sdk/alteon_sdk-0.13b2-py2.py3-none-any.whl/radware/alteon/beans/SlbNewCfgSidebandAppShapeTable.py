from radware.sdk.beans_common import *

class EnumAppShapeDelete(BaseBeanEnum):
    other = 1
    delete = 2
    unsupported = 2147483647

class SlbNewCfgSidebandAppShapeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SidebandIndex = kwargs.get('SidebandIndex', None)
        self.Priority = kwargs.get('Priority', None)
        self.Index = kwargs.get('Index', None)
        self.Delete = EnumAppShapeDelete.enum(kwargs.get('Delete', None)) 


    def get_indexes(self):
        return self.SidebandIndex, self.Priority,
    
    @classmethod
    def get_index_names(cls):
        return 'SidebandIndex', 'Priority',