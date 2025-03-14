proxy
====

A POC of a reverse-proxy, which sits in front of Prometheus, intercepts requests to the Prometheus API and adds project=<project_id> labels to each query based on the keystone token received with the request.

Originally the code was Aodh.

Only the /api/v1/query API endpoint is implemented.

This is just a rough POC, which works on my devstack VM, some additional modifications may be required in different environments.

To install
----------
Create the proxy user
```
openstack user create --domain default --password-prompt proxy # password = secret
openstack role add --project service --user proxy admin
openstack service create --name proxy --description "Telemetry" metering
```

Put the following in /etc/proxy/proxy.conf

```
[DEFAULT]
debug = True
transport_url = rabbit://stackrabbit:secret@192.168.122.169:5672/
enable_evaluation_results_metrics = True

[oslo_messaging_notifications]
topics = notifications

[service_credentials]
auth_url = http://192.168.122.169/identity
region_name = RegionOne
project_name = service
password = secret
project_domain_id = default
user_domain_id = default
username = proxy
auth_type = password

[keystone_authtoken]
memcached_servers = localhost:11211
cafile = /opt/stack/data/ca-bundle.pem
project_domain_name = Default
project_name = service
user_domain_name = Default
password = secret
username = proxy
auth_url = http://192.168.122.169/identity
interface = public
auth_type = password

[database]
connection = mysql+pymysql://root:secret@127.0.0.1/aodh?charset=utf8&plugin=dbcounter

[oslo_policy]
policy_file = policy.yaml
```

Put this into /var/www/proxy/app
```
"""Use this file for deploying the API under mod_wsgi.

See http://pecan.readthedocs.org/en/latest/deployment.html for details.
"""
from proxy.api import app

application = app.build_wsgi_app(argv=[])
```

Put this into /etc/httpd/conf.d/proxy.conf
```
Listen 8043

<VirtualHost *:8043>
    WSGIDaemonProcess proxy processes=2 threads=10 user=stack display-name=%{GROUP} 
    WSGIProcessGroup proxy
    WSGIScriptAlias / /var/www/proxy/app
    WSGIApplicationGroup %{GLOBAL}
    <IfVersion >= 2.4>
        ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/httpd/proxy.log
    CustomLog /var/log/httpd/proxy_access.log combined
</VirtualHost>

WSGISocketPrefix /var/run/httpd
```

Install the proxy with
```
sudo python setup.py install --prefix=/usr/local
```

Restart httpd
```
sudo systemctl restart httpd
```

curl the api with
```
export OS_CLOUD=devstack-admin
export TOKEN=`openstack token issue -c id -f value`
curl -H "X-Auth-Token: $TOKEN" http://192.168.122.169:8045/api/v1/query?query=ceilometer_image_size
```

Observe the logs with
```
sudo cat /var/log/httpd/proxy.log
```
