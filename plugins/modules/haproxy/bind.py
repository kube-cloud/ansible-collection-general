# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: bind
version_added: "1.0.0"
short_description: Manage Binds
description:
  - Used to Manage HA Proxy Bind
  - Create and Delete HA Proxy Binds
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
  parent_name:
    description:
      - The HA Proxy Bind Parent Name
    required: true
    type: str
  parent_type:
    description:
      - The HA Proxy Bind Parent Type
    required: false
    default: 'frontend'
    choices: ['backend', 'frontend']
    type: str
  name:
    description:
      - The HA Proxy Bind Name
    required: true
    type: str
  address:
    description:
      - The HA Proxy Bind Address
    required: false
    type: str
  port:
    description:
      - The HA Proxy Bind Port
    required: false
    type: int
  maxconn:
    description:
      - The HA Proxy Bind Maxconn
    required: false
    type: int
  ssl:
    description:
      - The HA Proxy Bind ssl
    required: false
    type: bool
  ssl_cafile:
    description:
      - The HA Proxy Bind ssl ca file
    required: false
    type: str
  ssl_certificate:
    description:
      - The HA Proxy Bind ssl certificate
    required: false
    type: str
  ssl_max_ver:
    description:
      - The HA Proxy Bind ssl max version
    required: false
    choices: ['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
    type: str
  ssl_min_ver:
    description:
      - The HA Proxy Bind ssl min version
    required: false
    choices: ['SSLv3', 'TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
    type: str
  strict_sni:
    description:
      - The HA Proxy Bind ssl srting sni
    required: false
    type: bool
  tcp_user_timeout:
    description:
      - The HA Proxy Bind tcp user timeout
    required: false
    type: int
  tfo:
    description:
      - The HA Proxy Bind tfo
    required: false
    type: bool
  thread:
    description:
      - The HA Proxy Bind thread
    required: false
    type: str
  tls_ticket_keys:
    description:
      - The HA Proxy Bind tls_ticket_keys
    required: false
    type: str
  transparent:
    description:
      - The HA Proxy Bind transparent
    required: false
    type: bool
  uid:
    description:
      - The HA Proxy Bind uid
    required: false
    type: str
  user:
    description:
      - The HA Proxy Bind user
    required: false
    type: str
  v4v6:
    description:
      - The HA Proxy Bind v4v6
    required: false
    type: bool
  v6only:
    description:
      - The HA Proxy Bind v6only
    required: false
    type: bool
  no_alpn:
    description:
      - The HA Proxy Bind no_alpn
    required: false
    type: bool
  no_ca_names:
    description:
      - The HA Proxy Bind no_ca_names
    required: false
    type: bool
  no_sslv3:
    description:
      - The HA Proxy Bind no_sslv3
    required: false
    type: bool
  no_tls_tickets:
    description:
      - The HA Proxy Bind no_tls_tickets
    required: false
    type: bool
  no_tlsv10:
    description:
      - The HA Proxy Bind no_tlsv10
    required: false
    type: bool
  no_tlsv11:
    description:
      - The HA Proxy Bind no_tlsv11
    required: false
    type: bool
  no_tlsv12:
    description:
      - The HA Proxy Bind no_tlsv12
    required: false
    type: bool
  no_tlsv13:
    description:
      - The HA Proxy Bind no_tlsv13
    required: false
    type: bool
  force_sslv3:
    description:
      - The HA Proxy Bind force_sslv3
    required: false
    type: bool
  force_tlsv10:
    description:
      - The HA Proxy Bind force_tlsv10
    required: false
    type: bool
  force_tlsv11:
    description:
      - The HA Proxy Bind force_tlsv11
    required: false
    type: bool
  force_tlsv12:
    description:
      - The HA Proxy Bind force_tlsv12
    required: false
    type: bool
  force_tlsv13:
    description:
      - The HA Proxy Bind force_tlsv13
    required: false
    type: bool
  generate_certificates:
    description:
      - The HA Proxy Bind generate_certificates
    required: false
    type: bool
  crt_list:
    description:
      - The HA Proxy Bind crt_list
    required: false
    type: str
  ca_ignore_err:
    description:
      - The HA Proxy Bind ca_ignore_err
    required: false
    type: str
  ca_sign_file:
    description:
      - The HA Proxy Bind ca_sign_file
    required: false
    type: str
  ca_sign_pass:
    description:
      - The HA Proxy Bind ca_sign_pass
    required: false
    type: str
  ca_verify_file:
    description:
      - The HA Proxy Bind ca_verify_file
    required: false
    type: str
  ciphers:
    description:
      - The HA Proxy Bind ciphers
    required: false
    type: str
  ciphersuites:
    description:
      - The HA Proxy Bind ciphersuites
    required: false
    type: str
  client_sigalgs:
    description:
      - The HA Proxy Bind client_sigalgs
    required: false
    type: str
  crl_file:
    description:
      - The HA Proxy Bind crl_file
    required: false
    type: str
  crt_ignore_err:
    description:
      - The HA Proxy Bind crt_ignore_err
    required: false
    type: str
  curves:
    description:
      - The HA Proxy Bind curves
    required: false
    type: str
  defer_accept:
    description:
      - The HA Proxy Bind defer_accept
    required: false
    type: str
  accept_proxy:
    description:
      - The HA Proxy Bind accept_proxy
    required: false
    type: bool
  allow_0rtt:
    description:
      - The HA Proxy Bind allow_0rtt
    required: false
    type: bool
  alpn:
    description:
      - The HA Proxy Bind alpn
    required: false
    type: str
  verify:
    description:
      - The HA Proxy Bind SSL Verify
    required: false
    choices: ['none', 'required', 'optional']
    type: str
  level:
    description:
      - The HA Proxy Bind level
    required: false
    choices: ['user', 'operator', 'admin']
    type: str
  transaction_id:
    description:
      - The Transaction ID (If need to execute action as part of API Transaction)
    required: false
    default: ""
    type: str
  force_reload:
    description:
      - Force reload HA Proxy Configuration
    required: false
    default: true
    type: bool
  state:
    description:
      - The Transaction State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Create HA Proxy Bind"
  kube_cloud.haproxy.bind:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: 'http'
    parent_name: "test_frontend"
    parent_type: "frontend"
    address: "*"
    port: 80
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    state: 'present'

- name: "Create HA Proxy Bind"
  kube_cloud.haproxy.bind:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: 'http'
    parent_name: "test_frontend"
    parent_type: "frontend"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_binds import BindClient
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.haproxy.models import Bind
from ...module_utils.haproxy.enums import Requirement, SSLVersion, FrontendLevel
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Bind
def get_bind(client: BindClient, name: str, parent_name: str, parent_type: str):

    try:

        # Call Client
        return client.get_bind(
            name=name,
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError:

        # Return None
        return None


# Update Bind
def update_bind(module: AnsibleModule, client: BindClient, transaction_id: str, name: str,
                parent_name: str, parent_type: str, bind: Bind, force_reload: bool):

    try:

        # Call Client
        return client.update_bind(
            name=name,
            bind=bind,
            transaction_id=transaction_id,
            parent_name=parent_name,
            parent_type=parent_type,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Bind] - Failed Update HA Proxy Bind (Name : {0}, Parent : {1}:{2}): {3}".format(
                name,
                parent_name,
                parent_type,
                api_error
            )
        )


# Create Bind
def create_bind(module: AnsibleModule, client: BindClient, transaction_id: str, bind: Bind, parent_name: str, parent_type: str, force_reload: bool):

    try:

        # Call Client
        return client.create_bind(
            bind=bind,
            parent_name=parent_name,
            parent_type=parent_type,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Bind] - Failed Create HA Proxy Bind (Name : {0}, Parent : {1}:{2}): {3}".format(
                bind.name,
                parent_name,
                parent_type,
                api_error
            )
        )


# Delete Bind
def delete_bind(module: AnsibleModule, client: BindClient, transaction_id: str, name: str, parent_name: str, parent_type: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_bind(
            name=name,
            parent_name=parent_name,
            parent_type=parent_type,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Bind] - Failed Delete HA Proxy Bind (Name : {0}, Parent : {1}:{2}): {3}".format(
                name,
                parent_name,
                parent_type,
                api_error
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True, no_log=False),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        api_version=dict(type='str', required=False, default='v2', no_log=False),
        parent_name=dict(type='str', required=True, no_log=False),
        parent_type=dict(type='str', required=False, default='frontend', choices=['frontend', 'backend'], no_log=False),
        name=dict(type='str', required=True, no_log=False),
        address=dict(type='str', required=False, no_log=False),
        port=dict(type='int', required=False, no_log=False),
        maxconn=dict(type='int', required=False, no_log=False),
        ssl=dict(type='bool', required=False, no_log=False),
        ssl_cafile=dict(type='str', required=False, no_log=False),
        ssl_certificate=dict(type='str', required=False, no_log=False),
        strict_sni=dict(type='bool', required=False, no_log=False),
        tcp_user_timeout=dict(type='int', required=False, no_log=False),
        tfo=dict(type='bool', required=False, no_log=False),
        thread=dict(type='str', required=False, no_log=False),
        tls_ticket_keys=dict(type='str', required=False, no_log=True),
        transparent=dict(type='bool', required=False, no_log=False),
        uid=dict(type='str', required=False, no_log=False),
        user=dict(type='str', required=False, no_log=False),
        v4v6=dict(type='bool', required=False, no_log=False),
        v6only=dict(type='bool', required=False, no_log=False),
        no_alpn=dict(type='bool', required=False, no_log=False),
        no_ca_names=dict(type='bool', required=False, no_log=False),
        no_sslv3=dict(type='bool', required=False, no_log=False),
        no_tls_tickets=dict(type='bool', required=False, no_log=False),
        no_tlsv10=dict(type='bool', required=False, no_log=False),
        no_tlsv11=dict(type='bool', required=False, no_log=False),
        no_tlsv12=dict(type='bool', required=False, no_log=False),
        no_tlsv13=dict(type='bool', required=False, no_log=False),
        force_sslv3=dict(type='bool', required=False, no_log=False),
        force_tlsv10=dict(type='bool', required=False, no_log=False),
        force_tlsv11=dict(type='bool', required=False, no_log=False),
        force_tlsv12=dict(type='bool', required=False, no_log=False),
        force_tlsv13=dict(type='bool', required=False, no_log=False),
        generate_certificates=dict(type='bool', required=False, no_log=False),
        crt_list=dict(type='str', required=False, no_log=False),
        ca_ignore_err=dict(type='str', required=False, no_log=False),
        ca_sign_file=dict(type='str', required=False, no_log=False),
        ca_sign_pass=dict(type='str', required=False, no_log=True),
        ca_verify_file=dict(type='str', required=False, no_log=False),
        ciphers=dict(type='str', required=False, no_log=False),
        ciphersuites=dict(type='str', required=False, no_log=False),
        client_sigalgs=dict(type='str', required=False, no_log=False),
        crl_file=dict(type='str', required=False, no_log=False),
        crt_ignore_err=dict(type='str', required=False, no_log=False),
        curves=dict(type='str', required=False, no_log=False),
        defer_accept=dict(type='str', required=False, no_log=False),
        accept_proxy=dict(type='bool', required=False, no_log=False),
        allow_0rtt=dict(type='bool', required=False, no_log=False),
        alpn=dict(type='str', required=False, no_log=False),
        transaction_id=dict(type='str', required=False, default='', no_log=False),
        force_reload=dict(type='bool', required=False, default=True, no_log=False),
        verify=dict(type='str', required=False, choices=[enum.value for enum in Requirement], no_log=False),
        ssl_max_ver=dict(type='str', required=False, choices=[enum.value for enum in SSLVersion], no_log=False),
        ssl_min_ver=dict(type='str', required=False, choices=[enum.value for enum in SSLVersion], no_log=False),
        level=dict(type='str', required=False, choices=[enum.value for enum in FrontendLevel], no_log=False),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
    )

    # Build ansible Module
    return AnsibleModule(
        argument_spec=module_specification,
        supports_check_mode=True
    )


# Instantiate Ansible Module
def build_client(module: AnsibleModule):

    try:

        # Build Client from Module
        return haproxy_client(module.params)

    except ValueError:

        # Set Module Error
        module.fail_json(
            msg="[Build Client] - Failed Build HA Proxy Dataplane API Client"
        )


# Build Requested Bind from Configuration
def build_requested_bind(params: dict) -> Bind:

    # Base Parameters Name
    base_param_names = [
        "name", "address", "port", "maxconn", "ssl", "ssl_cafile", "ssl_certificate", "strict_sni",
        "tcp_user_timeout", "tfo", "thread", "tls_ticket_keys", "transparent", "uid", "user", "v4v6",
        "v6only", "no_alpn", "no_ca_names", "no_sslv3", "no_tls_tickets", "no_tlsv10", "no_tlsv11",
        "no_tlsv12", "no_tlsv13", "force_sslv3", "force_tlsv10", "force_tlsv11", "force_tlsv12",
        "force_tlsv13", "generate_certificates", "crt_list", "ca_ignore_err", "ca_sign_file", "ca_sign_pass",
        "ca_verify_file", "ciphers", "ciphersuites", "client_sigalgs", "crl_file", "crt_ignore_err",
        "curves", "defer_accept", "accept_proxy", "allow_0rtt", "alpn"
    ]

    # Build Requested Instance
    bind = Bind(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Optional Initialization : verify
    bind.verify = Requirement.create(params.get('verify', None))

    # Optional Initialization : ssl_max_ver
    bind.ssl_max_ver = SSLVersion.create(params.get('ssl_max_ver', None))

    # Optional Initialization : ssl_min_ver
    bind.ssl_min_ver = SSLVersion.create(params.get('ssl_min_ver', None))

    # Optional Initialization : level
    bind.level = FrontendLevel.create(params.get('level', None))

    # Return Bind
    return bind


# Porcess Module Execution
def run_module(module: AnsibleModule, client: BindClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Extract Parent Name
    parent_name = module.params['parent_name']

    # Extract Parent Type
    parent_type = module.params['parent_type']

    # Build Requested Instance
    bind = build_requested_bind(module.params)

    # Find Existing Instance
    existing_bind = get_bind(
        client=client,
        name=bind.name,
        parent_name=parent_name,
        parent_type=parent_type
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_bind and state == 'present':

        # If Existing Instance match requested Instance
        if existing_bind == bind:

            # Initialize response (No Change)
            module.exit_json(
                msg="Bind [{0} - {1}/{2}] Not Changed".format(bind.name, parent_name, parent_type),
                changed=False,
                parent_name=parent_name,
                parent_type=parent_type,
                instance=filter_none(bind)
            )

        # Update Existing Instance
        update_bind(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=bind.name,
            parent_name=parent_name,
            parent_type=parent_type,
            bind=bind,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            parent_name=parent_name,
            parent_type=parent_type,
            instance=filter_none(bind),
            msg="Bind [{0} - {1}/{2}] Has Been Updated".format(bind.name, parent_name, parent_type)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_bind and state == 'present':

        # Create Instance
        create_bind(
            module=module,
            client=client,
            transaction_id=transaction_id,
            parent_name=parent_name,
            parent_type=parent_type,
            bind=bind,
            force_reload=force_reload
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            parent_name=parent_name,
            parent_type=parent_type,
            instance=filter_none(bind),
            msg="Bind [{0} - {1}/{2}] Has Been Created".format(bind.name, parent_name, parent_type)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_bind and state == 'absent':

        # Delete Instance
        delete_bind(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=bind.name,
            parent_name=parent_name,
            parent_type=parent_type,
            force_reload=force_reload
        )

        # Exit Module
        module.exit_json(
            msg="Bind [{0} - {1}/{2}] Has Been Deleted".format(bind.name, parent_name, parent_type),
            changed=True,
            parent_name=parent_name,
            parent_type=parent_type,
            instance=filter_none(bind)
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="Bind Not Found [{0} - {1}/{2}]".format(bind.name, parent_name, parent_type),
            changed=False,
            parent_name=parent_name,
            parent_type=parent_type,
            instance=filter_none(bind)
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).bind

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
