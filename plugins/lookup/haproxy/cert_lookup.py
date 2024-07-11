# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
name: cert_lookup
version_added: "1.0.0"
short_description: Get HA Proxy Managed Certificate
description:
  - Used to Get HA Proxy Managed Certificate
requirements:
  - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
  base_url:
    description:
      - The HA Proxy Dataplane API Base URL
    required: true
    type: str
  username:
    description:
      - The HA Proxy Dataplane API Admin Username
    required: true
    type: str
  password:
    description:
      - The HA Proxy Dataplane API Password
    required: true
    type: str
  api_version:
    description:
      - The HA Proxy Dataplane API Version
    required: false
    default: 'v2'
    type: str
  name:
    description:
      - The Certificate Name
    required: true
    type: str
'''

EXAMPLES = r'''
- name: "Get HA Proxy Certificate"
  ansible.builtin.debug: msg="{{item}}"
  crt: "{{ lookup('kube_cloud.general.haproxy.cert_lookup',base_url='http://localhost:5555',username='adm',password='adm',api_version='v2',name='test.pem') }}"
'''

RETURN = '''
_raw:
  description: HA Proxy Certificate Details
  type: dict
'''


from ansible.plugins.lookup import LookupBase
from ...module_utils.haproxy.client import haproxy_client


class LookupModule(LookupBase):

    # Execute Plugin
    def run(self, terms, variables, **kwargs):

        # Build Client
        client = haproxy_client(kwargs).ssl_certificate

        # Create and return Transaction
        return [client.get_certificate(name=kwargs["name"])]
