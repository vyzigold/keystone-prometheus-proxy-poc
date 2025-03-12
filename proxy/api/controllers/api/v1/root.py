#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2013 IBM Corp.
# Copyright 2013 eNovance <licensing@enovance.com>
# Copyright Ericsson AB 2013. All rights reserved
# Copyright 2014 Hewlett-Packard Company
# Copyright 2015 Huawei Technologies Co., Ltd.
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


import collections
from oslo_log import log
import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan
import requests
import json

from proxy.api.controllers.api.v1 import base
from proxy.api import rbac
from proxy.i18n import _
from proxy import profiler

LOG = log.getLogger(__name__)

class V1Controller(base.Base):
    """Version 1 API controller root."""

    @pecan.expose(content_type='application/json')
    def query(self, query):
        """Return all metrics"""
        enriched = self._enrich_query(query, "12345")
        result = requests.get(url = "http://localhost:9090/api/v1/query", params={'query': query}).text
        return result

