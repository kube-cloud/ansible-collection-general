# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: group_global_permissions
version_added: "1.0.0"
short_description: Manage Groups Global Permissions
description:
  - Used to Manage Sonarqube Groups Global Permissions
  - Create and Delete Sonarqube Groups Global Permissions
requirements:
  - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
  base_url:
    description:
      - The Sonarqube API Base URL
    required: true
    type: str
  username:
    description:
      - The Sonarqube API Admin Username
    required: true
    type: str
  password:
    description:
      - The Sonarqube API Password
    required: true
    type: str
  group_name:
    description:
      - The SonarQube Group Name
    required: true
    type: str
  permission_name:
    description:
      - The SonarQube Permission Name
    required: true
    type: str
    choices: [
        'admin', 'gateadmin', 'profileadmin', 'provisioning',
        'scan', 'applicationcreator'
    ]
  state:
    description:
      - The Transaction State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Create SonarQube Group Global Permissions"
  kube_cloud.general.sonarqube.group_global_permissions:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    group_name: "developers"
    permission_name: 'gateadmin'
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import GroupGlobalPermissionClient, sonarqube_client
from ...module_utils.sonarqube.models import GroupGlobalPermission
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Create Group Permission
def create_permission(
    module: AnsibleModule,
    client: GroupGlobalPermissionClient,
    permission: GroupGlobalPermission
):

    try:

        # Call Client
        return client.create_permission(permission=permission)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Group Permission] - Failed Create SonarQube Permission [{0}]: {1}".format(
                permission,
                api_error
            )
        )


# Delete Group Permission
def delete_permission(
    module: AnsibleModule,
    client: GroupGlobalPermissionClient,
    permission: GroupGlobalPermission
):

    try:

        # Call Client
        return client.delete_permission(
            permission=permission
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Group Permission] - Failed Delete SonarQube Group Permission ([{0}]): {1}".format(
                permission,
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
        group_name=dict(type='str', required=True),
        permission_name=dict(type='str', required=True, choices=GroupGlobalPermission.AVAILABLE_PERMISSIONS, no_log=False),
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
        return sonarqube_client(module.params)

    except ValueError:

        # Set Module Error
        module.fail_json(
            msg="[Build Client] - Failed Build Sonarqube API Client"
        )


# Build Requested Permission from Configuration
def build_requested_permission(params: dict) -> GroupGlobalPermission:

    # Base Parameters Name
    base_param_names = [
        "group_name", "permission_name"
    ]

    # Build Requested Instance
    return GroupGlobalPermission(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: GroupGlobalPermissionClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    permission = build_requested_permission(module.params)

    # If Requested State is 'present' and Instance Already exists
    if state == 'present':

        # Update Existing Instance
        create_permission(
            module=module,
            client=client,
            permission=permission
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(permission),
            msg="Permission Has Been Created/Updated [{0}]".format(permission)
        )

    # If Requested State is 'absent' and Instance exists
    if state == 'absent':

        # Delete Instance
        delete_permission(
            module=module,
            client=client,
            permission=permission
        )

        # Exit Module
        module.exit_json(
            msg="Permission Has been Deleted [{0}]".format(permission),
            changed=True
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).group_global_permission

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
