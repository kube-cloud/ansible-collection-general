# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: transaction
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
  transaction_id:
    description:
      - The Transaction ID
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
    choices: ['committed', 'cancelled']
    default: 'committed'
    type: str
'''

EXAMPLES = r'''
- name: "Commit HA Proxy Dataplane API Transaction"
  kube_cloud.haproxy.transaction:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    state: 'committed'

- name: "Cancel HA Proxy Dataplane API Transaction"
  kube_cloud.haproxy.transaction:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    state: 'cancelled'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_transactions import TransactionClient
from ...module_utils.haproxy.client import haproxy_client

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Commit Transaction
def commit_transaction(module: AnsibleModule, client: TransactionClient, transaction_id: str, force_reload: bool):

    try:

        # Call Client
        return client.commit_transaction(
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Commit Transaction] - Failed Commit HA Proxy Dataplane API Transaction (ID : {0}, Reload : {1}): {2}".format(
                transaction_id,
                force_reload,
                api_error
            )
        )


# Cancel Transaction
def cancel_transaction(module: AnsibleModule, client: TransactionClient, transaction_id: str):

    try:

        # Call Client
        return client.cancel_transaction(
            transaction_id=transaction_id
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Cancel Transaction] - Failed Cancel HA Proxy Dataplane API Transaction (ID : {0}): {1}".format(
                transaction_id,
                api_error
            )
        )


# Get Transaction
def get_transaction(client: TransactionClient, transaction_id: str):

    try:

        # Call Client
        return client.get_transaction(
            transaction_id=transaction_id
        )

    except HTTPError:

        # Return None
        return None


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        api_version=dict(type='str', required=False, default='v2'),
        transaction_id=dict(type='str', required=False, default=''),
        force_reload=dict(type='bool', required=False, default=True),
        state=dict(type='str', required=False, default='committed', choices=['committed', 'cancelled'])
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

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Find Existing Instance
    existing_instance = get_transaction(
        client=client,
        transaction_id=transaction_id
    )

    # If Requested State is 'committed' and Instance Already exists
    if existing_instance and state == 'committed':

        # Commit Existing Instance
        commit_transaction(
            module=module,
            client=client,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            msg="Transaction [ID : {0}, Reload : {1}] Has Been Committed".format(transaction_id, force_reload)
        )

    # If Requested State is 'committed' and Instance Not exists
    if not existing_instance and state == 'committed':

        # Module Response : Changed
        module.fail_json(
            msg="Transaction [ID : {0}] Not Found".format(transaction_id)
        )

    # If Requested State is 'cancelled' and Instance exists
    if existing_instance and state == 'cancelled':

        # Delete Instance
        cancel_transaction(
            module=module,
            client=client,
            transaction_id=transaction_id
        )

        # Exit Module
        module.exit_json(
            msg="Transaction [ID : {0}] Has been Cancelled".format(transaction_id),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="Transaction [ID : {0}] Not Found".format(transaction_id),
            changed=False
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
