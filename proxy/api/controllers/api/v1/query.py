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

from proxy.api.controllers.api.v1 import base
from proxy.api import rbac
from proxy.i18n import _
from proxy import profiler

LOG = log.getLogger(__name__)


@profiler.trace_cls('api')
class QueryController(object):
    """Manages the metrics api endpoint"""

    @pecan.expose(content_type='application/json', route="/")
    def get(self, query):
        """Return all metrics"""
        #return '{"status":"success","data":{"resultType":"vector","result":[{"metric":{"__name__":"ceilometer_image_size","counter":"image.size","image":"6b51fba6-8b74-4bd4-be53-25e509ea0aaf","instance":"localhost:9101","job":"ceilometer","project":"2dd8edd6c8c24f49bf04670534f6b357","publisher":"ceilometer","resource":"6b51fba6-8b74-4bd4-be53-25e509ea0aaf","resource_name":"Fedora-Cloud-Base-37-1.7.x86_64","server_group":"none","type":"size","unit":"B"},"value":[1741716003.305,"492830720"]},{"metric":{"__name__":"ceilometer_image_size","counter":"image.size","image":"828ab616-8904-48fb-a4bb-d037473cee7d","instance":"localhost:9101","job":"ceilometer","project":"2dd8edd6c8c24f49bf04670534f6b357","publisher":"ceilometer","resource":"828ab616-8904-48fb-a4bb-d037473cee7d","resource_name":"cirros-0.6.2-x86_64-disk","server_group":"none","type":"size","unit":"B"},"value":[1741716003.305,"21430272"]}]}}'
        return query
