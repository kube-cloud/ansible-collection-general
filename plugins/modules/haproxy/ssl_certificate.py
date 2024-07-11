# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: ssl_certificate
version_added: "1.0.0"
short_description: Manage Transactions
description:
  - Used to Manage HA Proxy Dataplane API Transactions
  - Validate and Delete HA Proxy Dataplane API Transactions
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
  path:
    description:
      - The Certificate Path (Local Path)
    required: false
    default: ""
    type: str
  force_update:
    description:
      - Force Update certificate if Exists
    required: false
    default: true
    type: bool
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
- name: "Commit HA Proxy Dataplane API Transaction"
  kube_cloud.haproxy.ssl_certificate:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jenkins.devcentral.kube-cloud.com.pem"
    path: "/etc/letsencrypt/jenkins.devcentral.kube-cloud.com/cert.pem"
    force_update: true
    force_reload: true
    state: 'present'

- name: "Cancel HA Proxy Dataplane API Transaction"
  kube_cloud.haproxy.ssl_certificate:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jenkins.devcentral.kube-cloud.com.pem"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_ssl_certificates import SslCertificateClient
from ...module_utils.haproxy.client import haproxy_client

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Certificate
def get_certificate(client: SslCertificateClient, name: str):

    try:

        # Call Client
        return client.get_certificate(name=name)

    except HTTPError:

        # Return None
        return None


# Update Certificate
def update_certificate(module: AnsibleModule, client: SslCertificateClient, name: str, path: str, force_reload: bool):

    try:

        # Call Client
        return client.update_certificate(
            name=name,
            path=path,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Certificate] - Failed Update HA Proxy Certificate (Name : {0} : [{1}]): {2}".format(
                name,
                path,
                api_error
            )
        )


# Create Certificate
def create_certificate(module: AnsibleModule, client: SslCertificateClient, name: str, path: str, force_reload: bool):

    try:

        # Call Client
        return client.create_certificate(
            name=name,
            path=path,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Certificate] - Failed Create HA Proxy Certificate (Name : {0} : [{1}]): {2}".format(
                name,
                path,
                api_error
            )
        )


# Delete Certificate
def delete_certificate(module: AnsibleModule, client: SslCertificateClient, name: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_certificate(
            name=name,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Certificate] - Failed Delete HA Proxy Certificate (Name : {0}): {1}".format(
                name,
                api_error
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        api_version=dict(type='str', required=False, default='v2'),
        name=dict(type='str', required=True),
        path=dict(type='str', required=False, default=""),
        force_update=dict(type='bool', required=False, default=True),
        force_reload=dict(type='bool', required=False, default=True),
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


# Porcess Module Execution
def run_module(module: AnsibleModule, client: SslCertificateClient):

    # Extract Name
    name = module.params['name']

    # Extract Path
    path = module.params['path']

    # Extract State
    state = module.params['state']

    # Extract Force Update Existing
    force_update = module.params['force_update']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Find Existing Instance
    existing_certificate = get_certificate(
        client=client,
        name=name
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_certificate and state == 'present':

        # If Existing Instance match requested Instance
        if not force_update:

            # Initialize response (No Change)
            module.exit_json(
                msg="Certificate [{0}] Not Changed".format(
                    name
                ),
                changed=False
            )

        # Update Existing Instance
        update_certificate(
            module=module,
            client=client,
            name=name,
            path=path,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=existing_certificate,
            msg="Certificate [{0}] Has Been Updated".format(name)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_certificate and state == 'present':

        # Create Instance
        certificate = create_certificate(
            module=module,
            client=client,
            name=name,
            path=path,
            force_reload=force_reload
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=certificate,
            msg="Certificate[{0}] Has been Created".format(name)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_certificate and state == 'absent':

        # Delete Instance
        delete_certificate(
            module=module,
            client=client,
            name=name,
            force_reload=force_reload
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(name),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(name),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).ssl_certificate

    # Execute Module
    run_module(module, client)


# If file is executed directly
if __name__ == '__main__':

    # Launch Entrypoint
    main()
