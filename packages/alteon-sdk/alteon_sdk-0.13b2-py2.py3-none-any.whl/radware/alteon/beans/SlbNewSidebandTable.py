
from radware.sdk.beans_common import *

class EnumSidebandState(BaseBeanEnum):
    enabled = 1
    disabled = 2
    unsupported = 2147483647


class EnumSidebandDelete(BaseBeanEnum):
    other = 1
    delete = 2
    unsupported = 2147483647

class EnumSidebandApplic(BaseBeanEnum):
    http = 1
    dns = 2
    unsupported = 2147483647

class EnumSidebandProxyIpMode(BaseBeanEnum):
    egress = 1
    address = 2
    unsupported = 2147483647

class EnumSidebandFallback(BaseBeanEnum):
    fallbackClosed = 1
    fallbackOpen = 2
    unsupported = 2147483647

class EnumSidebandClnsnat(BaseBeanEnum):
    enabled = 1
    disabled = 2
    unsupported = 2147483647


class SlbNewSidebandTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Port = kwargs.get('Port', None)
        self.Group = kwargs.get('Group', None)
        self.SslPol = kwargs.get('SslPol', None)
        self.EnaDis = EnumSidebandState.enum(kwargs.get('EnaDis', None))
        self.Timeout = kwargs.get('Timeout', None)
        self.Del = EnumSidebandDelete.enum(kwargs.get('Del', None))
        self.Applic = EnumSidebandApplic.enum(kwargs.get('Applic', None))
        self.ProxyIpMode = EnumSidebandProxyIpMode.enum(kwargs.get('ProxyIpMode', None))
        self.ProxyIpAddr = kwargs.get('ProxyIpAddr', None)
        self.ProxyIpMask = kwargs.get('ProxyIpMask', None)
        self.ProxyIpv6Addr = kwargs.get('ProxyIpv6Addr', None)
        self.ProxyIpv6Prefix = kwargs.get('ProxyIpv6Prefix', None)
        self.Fallback = EnumSidebandFallback.enum(kwargs.get('Fallback', None))
        self.Clnsnat = EnumSidebandClnsnat.enum(kwargs.get('Clnsnat', None))


    def get_indexes(self):
        return self.ID, 
    
    @classmethod
    def get_index_names(cls):
        return 'ID', 

