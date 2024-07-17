# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: settings
version_added: "1.0.0"
short_description: Manage Settings
description:
  - Used toManage Sonarqube Settings
  - Create, Update and Delete Sonarqube Settings
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
  key:
    description:
      - The SonarQube Setting Key
    required: true
    type: str
  component:
    description:
      - The SonarQube Setting Component Key
    required: false
    default: ''
    type: str
  value:
    description:
      - The SonarQube Setting Value
    required: false
    default: ''
    type: str
  values:
    description:
      - The SonarQube Setting Values (For Multi-Value Field)
    required: false
    type: list
    elements: str
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
- name: "Create SonarQube Setting"
  kube_cloud.haproxy.backend:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    component: "my_project"
    key: "sonar.core.serverBaseURL"
    value: 'https://sonarqube.yoursite.com'
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import SettingsClient, sonarqube_client
from ...module_utils.sonarqube.models import Setting
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Settings
def get_setting(client: SettingsClient, key: str, component: str):

    try:

        # Call Client
        return client.get_setting(key=key, component=component)

    except HTTPError:

        # Return None
        return None


# Update Setting
def update_setting(module: AnsibleModule, client: SettingsClient, key: str, component: str, value: str, values: list):

    try:

        # Call Client
        return client.update_setting(
            key=key,
            component=component,
            value=value,
            values=values
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Setting] - Failed Update SonarQube Setting (Key : {0}/{1} : [{2}]): {3}".format(
                key,
                component,
                value,
                api_error
            )
        )


# Create Setting
def create_setting(module: AnsibleModule, client: SettingsClient, key: str, component: str, value: str, values: list):

    try:

        # Call Client
        return client.create_setting(
            key=key,
            component=component,
            value=value,
            values=values
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Setting] - Failed Create SonarQube Setting (Key : {0}/{1} : [{2}]): {3}".format(
                key,
                component,
                value,
                api_error
            )
        )


# Delete Setting
def delete_setting(module: AnsibleModule, client: SettingsClient, key: str, component: str):

    try:

        # Call Client
        return client.delete_setting(
            key=key,
            component=component
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Setting] - Failed Delete SonarQube Setting (Key : {0}/{1}): {2}".format(
                key,
                component,
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
        key=dict(type='str', required=True, no_log=True),
        component=dict(type='str', required=False, default=''),
        value=dict(type='str', required=False, default=''),
        values=dict(type='list', elements='str', required=False, default=[]),
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


# Build Requested Setting from Configuration
def build_requested_setting(params: dict) -> Setting:

    # Base Parameters Name
    base_param_names = [
        "key", "component", "value", "values"
    ]

    # Build Requested Instance
    setting = Setting(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Return Setting
    return setting


# Porcess Module Execution
def run_module(module: AnsibleModule, client: SettingsClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    setting = build_requested_setting(module.params)

    # Find Existing Instance
    existing_setting = get_setting(
        client=client,
        key=setting.key,
        component=setting.component
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_setting and state == 'present':

        # If Existing Instance match requested Instance
        if existing_setting == setting:

            # Initialize response (No Change)
            module.exit_json(
                msg="Setting [{0}] Not Changed".format(setting.key),
                changed=False
            )

        # Update Existing Instance
        update_setting(
            module=module,
            client=client,
            key=setting.key,
            component=setting.component,
            value=setting.value,
            values=setting.values
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(setting),
            msg="Setting [{0}] Has Been Updated".format(setting.key)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_setting and state == 'present':

        # Create Instance
        create_setting(
            module=module,
            client=client,
            key=setting.key,
            component=setting.component,
            value=setting.value,
            values=setting.values
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(setting),
            msg="[{0}] Has been Created".format(setting.key)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_setting and state == 'absent':

        # Delete Instance
        delete_setting(
            module=module,
            client=client,
            key=setting.key,
            component=setting.component
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(setting.key),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(setting.key),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).backend

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
