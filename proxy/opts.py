#
# Copyright 2025 Red Hat, Inc
# Copyright 2014-2015 eNovance
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import itertools

from keystoneauth1 import loading

import proxy.api
import proxy.keystone_client
import proxy.service


def list_opts():
    return [
        ('DEFAULT',
         itertools.chain(
             proxy.service.OPTS)),
        ('api',
         itertools.chain(
             proxy.api.OPTS)),
        ('service_credentials', proxy.keystone_client.OPTS),
    ]


def list_keystoneauth_opts():
    # NOTE(sileht): the configuration file contains only the options
    # for the password plugin that handles keystone v2 and v3 API
    # with discovery. But other options are possible.
    return [('service_credentials', (
            loading.get_auth_common_conf_options() +
            loading.get_auth_plugin_conf_options('password')))]
