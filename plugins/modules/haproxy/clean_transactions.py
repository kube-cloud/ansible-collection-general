# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: clean_transactions
version_added: "1.0.0"
short_description: Clean Transactions
description:
  - Used to Clear All HA Proxy Dataplane API Transactions
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
'''

EXAMPLES = r'''
- name: "Commit HA Proxy Dataplane API Transaction"
  kube_cloud.haproxy.clean_transactions:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_transactions import TransactionClient
from ...module_utils.haproxy.client import haproxy_client

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Cancel All Transaction
def cancel_transactions(module: AnsibleModule, client: TransactionClient):

    try:

        # Call Client
        return client.cancel_transactions()

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Cancel All Transaction] - Failed Cancel All HA Proxy Dataplane API Transactions : {0}".format(
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
        api_version=dict(type='str', required=False, default='v2')
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
def run_module(module: AnsibleModule, client: TransactionClient):

    # Cancel All Pending Transactions
    cleaned_transactions = cancel_transactions(
        module=module,
        client=client
    )

    # Module Response : Changed
    module.exit_json(
        changed=True,
        cleaned=cleaned_transactions,
        msg="Transactions are Cleaned"
    )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).transaction

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
