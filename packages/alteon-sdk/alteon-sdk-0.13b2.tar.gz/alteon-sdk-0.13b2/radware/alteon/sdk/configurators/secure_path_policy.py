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
# @author: Michal Greenberg, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewSecurePathClassesTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError


class SecurePathPolicyParameters(RadwareParametersStruct):
    secure_path_id: str
    name: Optional[str]
    secure_path_policy_status: Optional[EnumSecurePathStatus]
    bot_manager_status: Optional[EnumBotMngStatus]
    api_key: Optional[str]
    application_id: Optional[str]
    file_extensions_to_bypass: Optional[str]
    methods_to_bypass: Optional[str]
    bypass_when_query_present: Optional[EnumSecurePathQueryBypass]
    maximum_request_size: Optional[int]


    def __init__(self, index: int = None):
        self.secure_path_id = index
        self.name = None
        self.secure_path_policy_status = None
        self.bot_manager_status = None
        self.api_key = None
        self.application_id = None
        self.file_extensions_to_bypass = None
        self.methods_to_bypass = None
        self.bypass_when_query_present = None
        self.maximum_request_size = None

bean_map = {
    SlbNewSecurePathClassesTable: dict(
        struct=SecurePathPolicyParameters,
        direct=True,
        attrs=dict(
            Id='secure_path_id',
            Name='name',
            EnaDis='secure_path_policy_status',
            BotMng='bot_manager_status',
            Token='api_key',
            AppId='application_id',
            FileBypass='file_extensions_to_bypass',
            MethodBypass='methods_to_bypass',
            QueryBypass='bypass_when_query_present',
            MaxRequestSize='maximum_request_size',
        )
    )
}


class SecurePathPolicyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SecurePathPolicyParameters]

    def __init__(self, alteon_connection):
        super(SecurePathPolicyConfigurator, self).__init__(bean_map, alteon_connection)        
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: SecurePathPolicyParameters) -> SecurePathPolicyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SecurePathPolicyParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSecurePathClassesTable, parameters)


