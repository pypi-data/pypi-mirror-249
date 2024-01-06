# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
# Copyright 2016, 2017, 2018 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# dsgen.utils

import json

from .base import DSBase, SettingBase
from .message import MSG_FORMAT_ERROR_LOADING_JSON


class DSGenerator(DSBase):
    '''
    I should be subclassed for Django project setting, and my
    instance methods should override module-level reference:
    `__dir__` => `get_config_field_list`
    `__getattr__` => get_config_value`
    '''

    def __init__(self, json_path=None):
        '''
        :param json_path: (string)
        '''
        super().__init__()
        self.site_config = dict()

        if json_path is not None:
            try:
                with open(json_path, 'r') as json_f:
                    self.site_config.update(
                        json.load(json_f)
                    )
            except Exception:
                from django.core.exceptions import ImproperlyConfigured  # noqa
                msg = MSG_FORMAT_ERROR_LOADING_JSON.format(fp=json_path)
                bad_config = ImproperlyConfigured(msg)
                raise bad_config  # pylint: disable=W0707

            self.site_json_path = json_path
        self.collect_apps()

    def get_config_field_list(self):
        '''
        :return: (list of string)
        '''

        attr_fields = [ attr for attr in dir(self) if attr.isupper() ]
        dict_fields = list(self.site_config.keys())
        dict_extra_fields = [ each for each in dict_fields if each not in attr_fields ]
        # rvalue;
        all_fields = list()
        all_fields.extend(attr_fields)
        all_fields.extend(dict_extra_fields)
        return all_fields

    def get_config_value(self, name):
        '''
        :param name: (string)
        '''

        if name.startswith('_'):
            value = globals().get(name)
        else:
            value = getattr(
                self,
                name,
                self.site_config.get(name)
            )
        return value


class DSetting(SettingBase):
    '''
    I should be subclassed for Django app setting

    subclass MUST declare the following attributes:
    - `DEFAULT` (dict)
    - `SETTING_NAME` (string)
    '''

    def __init__(self):
        super().__init__()
        self._default = self.DEFAULT
        self._cache_key = set()
        from django.conf import settings as _ds_conf  # noqa
        self._ds_conf = _ds_conf

    @property
    def site_conf(self):
        if '_site' not in self.__dict__:
            _conf = getattr(
                self._ds_conf,
                self.SETTING_NAME,
                dict()
            )
            setattr(
                self,
                '_site',
                _conf
            )
        return self.__dict__['_site']
