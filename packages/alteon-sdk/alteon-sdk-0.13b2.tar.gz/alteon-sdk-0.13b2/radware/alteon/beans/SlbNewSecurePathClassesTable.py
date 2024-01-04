
from radware.sdk.beans_common import *


class EnumSecurePathStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2
    unsupported = 2147483647

class EnumBotMngStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2
    unsupported = 2147483647

class EnumSecurePathQueryBypass(BaseBeanEnum):
    enabled = 1
    disabled = 2
    unsupported = 2147483647

class EnumSecurePathDelete(BaseBeanEnum):
    other = 1
    delete = 2
    unsupported = 2147483647


class SlbNewSecurePathClassesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.EnaDis = EnumSecurePathStatus.enum(kwargs.get('EnaDis', None))
        self.BotMng = EnumBotMngStatus.enum(kwargs.get('BotMng', None))
        self.Token = kwargs.get('Token', None)
        self.AppId = kwargs.get('AppId', None)
        self.FileBypass = kwargs.get('FileBypass', None)
        self.MethodBypass = kwargs.get('MethodBypass', None)
        self.QueryBypass = EnumSecurePathQueryBypass.enum(kwargs.get('QueryBypass', None))
        self.MaxRequestSize = kwargs.get('MaxRequestSize', None)
        self.Del = EnumSecurePathDelete.enum(kwargs.get('Del', None))

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

