# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: acl
version_added: "1.0.0"
short_description: Manage ACLs
description:
    - Used to Manage HA Proxy ACLs
    - Create, Update and Delete HA Proxy ACLs
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
    acl_parent_name:
        description:
        - The ACL Parent Name
        required: true
        type: str
    acl_parent_type:
        description:
        - The ACL Parent Type
        required: true
        type: str
        choices: ['backend', 'frontend']
    acl_name:
        description:
        - The ACL Name
        required: false
        default: ""
        type: str
    acl_criterion:
        description:
        - The ACL Criterion
        required: false
        default: ""
        type: str
    acl_value:
        description:
        - The ACL Value
        required: false
        default: ""
        type: str
    state:
        description:
        - The Transaction State
        required: false
        choices: ['present', 'absent']
        default: 'present'
        type: str
'''

EXAMPLES = r'''
- name: "Create HA Proxy ACL"
  kube_cloud.general.haproxy.acl:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    acl_parent_name: "test_frontend"
    acl_parent_type: "frontend"
    acl_name: "is_example"
    acl_criterion: "req.hdr(Host)"
    acl_value: "example.com"
    state: 'present'

- name: "Cancel HA Proxy Dataplane API Transaction"
  kube_cloud.general.haproxy.acl:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    acl_parent_name: "test_frontend"
    acl_parent_type: "frontend"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_acls import AclClient
from ...module_utils.haproxy.models import Acl
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.haproxy.commons import filter_none
from typing import List

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return ACL
def get_acl(client: AclClient, index: int, parent_name: str, parent_type: str):

    try:

        # Call Client
        return client.get_acl(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError:

        # Return None
        return None


# Find and Return ACLs
def get_acls(client: AclClient, parent_name: str, parent_type: str) -> List[Acl]:

    try:

        # Call Client
        return client.get_acls(
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError:

        # Return None
        return []


# Update ACL
def update_acl(module: AnsibleModule, client: AclClient, transaction_id: str, index: int, parent_name: str, parent_type: str, acl: Acl, force_reload: bool):

    try:

        # Call Client
        return client.update_acl(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type,
            force_reload=force_reload,
            acl=acl,
            transaction_id=transaction_id
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update ACL] - Failed Update HA Proxy ACL (Index : {0}, Parent : {1}:{2}): {3}".format(
                index,
                parent_name,
                parent_type,
                api_error
            )
        )


# Create ACL
def create_acl(module: AnsibleModule, client: AclClient, transaction_id: str, parent_name: str, parent_type: str, acl: Acl, force_reload: bool):

    try:

        # Call Client
        return client.create_acl(
            acl=acl,
            transaction_id=transaction_id,
            force_reload=force_reload,
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create ACL] - Failed Update HA Proxy ACL (ACL : {0}, Parent : {1}:{2}): {3}".format(
                acl,
                parent_name,
                parent_type,
                api_error
            )
        )


# Delete Backend
def delete_acl(module: AnsibleModule, client: AclClient, transaction_id: str, index: int, parent_name: str, parent_type: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_acl(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete ACL] - Failed Delete HA Proxy ACL (Index : {0}, Parent : {1}:{2}): {3}".format(
                index,
                parent_name,
                parent_type,
                api_error
            )
        )


def find_acl_by_name(acls: List[Acl], name: str = ''):

    # If List is Not Provided
    if acls is None:

        # Return None
        return None

    # Build name to compare
    p_name = name.strip().lower()

    # Iterate on ACLs List
    for acl in acls:

        # Build ACL Name
        acl_name = acl.acl_name.strip().lower() if acl.acl_name else ''

        # If Name are same
        if acl_name == p_name:

            # Return ACL
            return acl

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
        acl_parent_name=dict(type='str', required=True),
        acl_parent_type=dict(type='str', required=True, choices=['frontend', 'backend']),
        acl_name=dict(type='str', required=False, default=''),
        acl_criterion=dict(type='str', required=False, default=''),
        acl_value=dict(type='str', required=False, default=''),
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


# Build Requested ACL from Configuration
def build_requested_acl(params: dict) -> Acl:

    # Build Requested Instance
    return Acl(
        acl_name=params['acl_name'],
        criterion=params['acl_criterion'],
        value=params['acl_value']
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: AclClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # ACL Parent Name
    acl_parent_name = module.params['acl_parent_name']

    # ACL Parent Type
    acl_parent_type = module.params['acl_parent_type']

    # Build Requested Instance
    acl = build_requested_acl(module.params)

    # Get Liste of ACLs
    acls = get_acls(
        client=client,
        parent_name=acl_parent_name,
        parent_type=acl_parent_type
    )

    # ACLs Size
    acl_size = len(acls)

    # Find Existing Instance
    existing_instance = find_acl_by_name(
        acls=acls,
        name=acl.acl_name
    )

    # If Instance Exists
    if existing_instance:

        # Initialize Index
        acl.index = existing_instance.index

    else:

        # Add Index
        acl.index = (acl_size - 1) if acl_size > 0 else 0

    # If Requested State is 'present' and Instance Already exists
    if existing_instance and state == 'present':

        # If Existing Instance match requested Instance
        if existing_instance == acl:

            # Initialize response (No Change)
            module.exit_json(
                msg="ACL [Parent : {0}/{1}, Name : {2}/{3}] Not Changed".format(
                    acl_parent_name,
                    acl_parent_type,
                    acl.acl_name,
                    acl.index
                ),
                instance=filter_none(acl),
                acl_parent_name=acl_parent_name,
                acl_parent_type=acl_parent_type,
                changed=False
            )

        # Update Existing Instance
        update_acl(
            module=module,
            client=client,
            transaction_id=transaction_id,
            acl=acl,
            index=acl.index,
            parent_name=acl_parent_name,
            parent_type=acl_parent_type,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(acl),
            acl_parent_name=acl_parent_name,
            acl_parent_type=acl_parent_type,
            msg="ACL [Parent : {0}/{1}, Name : {2}/{3}] Has Been Updated".format(
                acl_parent_name,
                acl_parent_type,
                acl.acl_name,
                acl.index
            )
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_instance and state == 'present':

        # Create Instance
        create_acl(
            module=module,
            client=client,
            transaction_id=transaction_id,
            force_reload=force_reload,
            parent_name=acl_parent_name,
            parent_type=acl_parent_type,
            acl=acl
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(acl),
            acl_parent_name=acl_parent_name,
            acl_parent_type=acl_parent_type,
            msg="ACL [Parent : {0}/{1}, Name : {2}/{3}] Has Been Created".format(
                acl_parent_name,
                acl_parent_type,
                acl.acl_name,
                acl.index
            )
        )

    # If Requested State is 'absent' and Instance exists
    if existing_instance and state == 'absent':

        # Delete Instance
        delete_acl(
            module=module,
            client=client,
            transaction_id=transaction_id,
            force_reload=force_reload,
            index=acl.index,
            parent_name=acl_parent_name,
            parent_type=acl_parent_type
        )

        # Exit Module
        module.exit_json(
            changed=True,
            instance=acl,
            acl_parent_name=acl_parent_name,
            acl_parent_type=acl_parent_type,
            msg="ACL [Parent : {0}/{1}, Name : {2}/{3}] Has Been Deleted".format(
                acl_parent_name,
                acl_parent_type,
                acl.acl_name,
                existing_instance.index
            )
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="ACL Not Found [Parent : {0}/{1}, Name : {2}]".format(
                acl_parent_name,
                acl_parent_type,
                acl.acl_name
            ),
            instance=filter_none(acl),
            acl_parent_name=acl_parent_name,
            acl_parent_type=acl_parent_type,
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).acl

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
