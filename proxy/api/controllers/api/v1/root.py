#
# Copyright 2025 Red Hat, Inc
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


import json
from oslo_log import log
import pecan

from proxy.api.controllers.api.v1 import base

LOG = log.getLogger(__name__)


class V1Controller(base.Base):
    """Version 1 API controller root."""

    @pecan.expose(content_type='application/json')
    def query(self, query):
        """Return all metrics"""
        project_id = pecan.request.headers.get('X-Project-Id')
        tenant_enforced_query = self._enrich_query(query, project_id)
        LOG.debug("Query sent to prometheus: %s", tenant_enforced_query)
        result = self.prometheus_client._get("query", dict(query=query))
        return json.dumps(result)
