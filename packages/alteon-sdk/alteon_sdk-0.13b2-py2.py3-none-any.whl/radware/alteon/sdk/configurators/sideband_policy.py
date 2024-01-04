#!/usr/bin/env python
# Copyright (c) 2023 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewSidebandTable import *
from radware.alteon.beans.SlbNewCfgSidebandAppShapeTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError

class AppshapeEntry(RadwareParametersStruct):
    priority: int
    name: Optional[str]

    def __init__(self, priority: int = None):
        self.priority = priority
        self.name = None

class SidebandPolicyParameters(RadwareParametersStruct):
    sideband_policy_id: str
    name: Optional[str]
    destination_port: Optional[int]
    group_id: Optional[str]
    ssl_policy: Optional[str]
    sideband_policy_state: Optional[EnumSidebandState]
    timeout: Optional[int]
    application: Optional[EnumSidebandApplic]
    client_nat_mode: Optional[EnumSidebandProxyIpMode]
    client_nat_addr: Optional[str]
    client_nat_mask: Optional[str]
    client_nat_v6_addr: Optional[str]
    client_nat_prefix: Optional[int]
    fallback_action: Optional[EnumSidebandFallback]
    preserve_client_ip: Optional[EnumSidebandClnsnat]
    appshapes: Optional[List[AppshapeEntry]]

    def __init__(self, id: str = None):
        self.sideband_policy_id = id
        self.name = None
        self.destination_port = None
        self.group_id = None
        self.ssl_policy = None
        self.sideband_policy_state = None
        self.timeout = None
        self.application = None
        self.client_nat_mode = None
        self.client_nat_addr = None
        self.client_nat_mask = None
        self.client_nat_v6_addr = None
        self.client_nat_prefix = None
        self.fallback_action = None
        self.preserve_client_ip = None
        self.appshapes = list()

bean_map = {
    SlbNewSidebandTable: dict(
        struct=SidebandPolicyParameters,
        direct=True,
        attrs=dict(
            ID='sideband_policy_id',
            Name='name',
            Port='destination_port',
            Group='group_id',
            SslPol='ssl_policy',
            EnaDis='sideband_policy_state',
            Timeout='timeout',
            Applic='application',
            ProxyIpMode='client_nat_mode',
            ProxyIpAddr='client_nat_addr',
            ProxyIpMask='client_nat_mask',
            ProxyIpv6Addr='client_nat_v6_addr',
            ProxyIpv6Prefix='client_nat_prefix',
            Fallback='fallback_action',
            Clnsnat='preserve_client_ip'
        )
    ),
    SlbNewCfgSidebandAppShapeTable: dict(
        struct=List[AppshapeEntry],
        direct=True,
        attrs=dict(
            SidebandIndex='sideband_policy_id',
            Priority='priority',
            Index='name'
        )
    )
}

auto_write_exception = [SlbNewCfgSidebandAppShapeTable]


class SidebandPolicyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SidebandPolicyParameters]

    def __init__(self, alteon_connection):
        super(SidebandPolicyConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SidebandPolicyParameters) -> SidebandPolicyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SidebandPolicyParameters, dry_run: bool) -> str:
        log.debug(' SIDEBAND UPDATE  params {0}'.format(parameters))
        #check if this is new entry
        all_configured_table_entries = self._device_api.read_all(SlbNewSidebandTable())
        result = self._lookup_current_entry(parameters, all_configured_table_entries)
        if result:
            #entry exist
            if parameters.application is not None:
                if result.Applic != parameters.application:
                    # trying to change the application which is not allowed
                    raise DeviceConfiguratorError(self.__class__, 'sideband application can not be changed for existing entry')
            
            #get the application from the entry
            application = result.Applic
        else:
            #get the application from the parameters
            application = parameters.application

        if application == EnumSidebandApplic.dns:
            if parameters.ssl_policy is not None:
                raise DeviceConfiguratorError(self.__class__, 'ssl_policy can not be configured when sideband application is DNS')
            if parameters.fallback_action is not None:
                raise DeviceConfiguratorError(self.__class__, 'fallback_action can not be configured when sideband application is DNS')
        else:
            if parameters.preserve_client_ip is not None:
                raise DeviceConfiguratorError(self.__class__, 'preserve_client_ip can not be configured when sideband application is HTTP')

        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)
        if parameters.appshapes:
            for appshape in parameters.appshapes:
                instance = self._get_bean_instance(SlbNewCfgSidebandAppShapeTable, parameters)
                instance.Index = appshape.name
                instance.Priority = appshape.priority
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: SidebandPolicyParameters, dry_run: bool) -> str:
        instance = self._get_bean_instance(SlbNewCfgSidebandAppShapeTable, parameters)
        as_indexes = [appshape.priority for appshape in parameters.appshapes]
        self._remove_device_beans_by_simple_collection(as_indexes, instance, 'Priority', dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    @staticmethod
    def _lookup_current_entry(parameters, all_configured_table_entries):
        for entry in all_configured_table_entries:
            if parameters.sideband_policy_id == entry.ID:
                return entry

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSidebandTable, parameters)





