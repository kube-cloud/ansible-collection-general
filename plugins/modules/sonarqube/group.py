# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: group
version_added: "1.0.0"
short_description: Manage Groups
description:
  - Used to Manage Sonarqube Groups
  - Create, Update and Delete Sonarqube Groups
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
  group_description:
    description:
      - The SonarQube Group Description
    required: false
    type: str
    default: ''
  global_permissions:
    description:
      - The SonarQube Group Global Permissions
    required: false
    type: list
    elements: str
    choices: [
        'admin', 'gateadmin', 'profileadmin', 'provisioning',
        'scan', 'applicationcreator'
    ]
    default: []
  state:
    description:
      - The Transaction State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Create SonarQube Group"
  kube_cloud.general.sonarqube.group:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    group_name: "developers"
    group_description: "KubeCloud Developer"
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import GroupClient, sonarqube_client
from ...module_utils.sonarqube.models import Group, GroupGlobalPermission
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Groups
def get_group(client: GroupClient, name: str) -> Group:

    try:

        # Call Client
        return client.get_group(name=name)

    except HTTPError:

        # Return None
        return None


# Update Group
def update_group(module: AnsibleModule, client: GroupClient, group: Group) -> Group:

    try:

        # Call Client
        return client.update_group(group=group)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Group] - Failed Update SonarQube Group [{0}]: {1}".format(
                group,
                api_error
            )
        )


# Create Group
def create_group(module: AnsibleModule, client: GroupClient, group: Group):

    try:

        # Call Client
        return client.create_group(group=group)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Group] - Failed Create SonarQube Group [{0}]: {1}".format(
                group,
                api_error
            )
        )


# Delete Group
def delete_group(module: AnsibleModule, client: GroupClient, name: str):

    try:

        # Call Client
        return client.delete_group(
            name=name
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Group] - Failed Delete SonarQube Group (Name : {0}): {1}".format(
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
        group_name=dict(type='str', required=True),
        group_description=dict(type='str', required=False, default=''),
        global_permissions=dict(
            type='list',
            elements='str',
            required=False,
            default=[],
            no_log=False,
            choices=GroupGlobalPermission.AVAILABLE_PERMISSIONS
        ),
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


# Build Requested Group from Configuration
def build_requested_group(params: dict) -> Group:

    # Base Parameters Name
    base_param_names = [
        "group_name", "group_description", "global_permissions"
    ]

    # Build Requested Instance
    return Group(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: GroupClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    group = build_requested_group(module.params)

    # Find Existing Instance
    existing_group = get_group(
        client=client,
        name=group.group_name
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_group and state == 'present':

        # If Existing Instance match requested Instance
        if existing_group == group:

            # Initialize response (No Change)
            module.exit_json(
                msg="Group [{0}] Not Changed".format(group.group_name),
                changed=False
            )

        # Update Existing Instance
        update_group(
            module=module,
            client=client,
            group=group
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(group),
            msg="Group [{0}] Has Been Updated".format(group)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_group and state == 'present':

        # Create Instance
        create_group(
            module=module,
            client=client,
            group=group
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(group),
            msg="[{0}] Has been Created".format(group)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_group and state == 'absent':

        # Delete Instance
        delete_group(
            module=module,
            client=client,
            name=group.group_name
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(group.group_name),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(group.group_name),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).group

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
