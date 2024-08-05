# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: alm_settings_github
version_added: "1.0.0"
short_description: Manage ALM AlmSettingsGithub for Github
description:
  - Used toManage Sonarqube ALM AlmSettingsGithub for Github
  - Create, Update and Delete Sonarqube ALM AlmSettingsGithub for Github
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
  new_key:
    description:
      - The SonarQube Setting New Key (for Update)
    required: false
    type: str
  url:
    description:
      - The SonarQube Setting Github url
    required: true
    type: str
  app_id:
    description:
      - The SonarQube Setting Application ID
    required: true
    type: str
  client_id:
    description:
      - The SonarQube Setting Application Client ID
    required: true
    type: str
  client_secret:
    description:
      - The SonarQube Setting Application Client Secret
    required: true
    type: str
  private_key:
    description:
      - The SonarQube Setting Application Private Key
    required: true
    type: str
  encode_parameters:
    description:
      - The SonarQube Setting to indicate if Module encode Private Key
    required: false
    type: bool
    default: true
  webhook_secret:
    description:
      - The SonarQube Setting Application Webhook Secret
    required: false
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
- name: "Create SonarQube ALM Setting Github"
  kube_cloud.general.sonarqube.alm_settings_github:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    key: "demo-settings-github"
    url: 'https://api.github.com'
    app_id: 'test-github-app-id'
    client_id: 'github-app-client-id'
    client_secret: 'github-app-client-secret'
    private_key: '-----BEGIN RSA PRIVATE KEY-----.....-----END RSA PRIVATE KEY-----'
    encode_parameters: true
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import AlmSettingsGithubClient, sonarqube_client
from ...module_utils.sonarqube.models import AlmSettingsGithub
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return AlmSettingsGithub
def get_setting(client: AlmSettingsGithubClient, key: str):

    try:

        # Call Client
        return client.get_setting(key=key)

    except HTTPError:

        # Return None
        return None


# Update Setting
def update_setting(
    module: AnsibleModule,
    client: AlmSettingsGithubClient,
    setting: AlmSettingsGithub,
    encode_parameters: bool
):

    try:

        # Call Client
        return client.update_setting(
            setting=setting,
            encode_parameters=encode_parameters
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Setting] - Failed Update SonarQube ALM Setting [{0}]: {1}".format(
                setting,
                api_error
            )
        )


# Create Setting
def create_setting(
    module: AnsibleModule,
    client: AlmSettingsGithubClient,
    setting: AlmSettingsGithub,
    encode_parameters: bool
):

    try:

        # Call Client
        return client.create_setting(
            setting=setting,
            encode_parameters=encode_parameters
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Setting] - Failed Create SonarQube ALM Setting [{0}]: {1}".format(
                setting,
                api_error
            )
        )


# Delete Setting
def delete_setting(module: AnsibleModule, client: AlmSettingsGithubClient, key: str):

    try:

        # Call Client
        return client.delete_setting(
            key=key
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Setting] - Failed Delete SonarQube ALM Setting (Key : {0}): {1}".format(
                key,
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
        key=dict(type='str', required=True, no_log=False),
        new_key=dict(type='str', required=False, default=None, no_log=False),
        url=dict(type='str', required=True, no_log=False),
        app_id=dict(type='str', required=True, no_log=True),
        client_id=dict(type='str', required=True, no_log=True),
        client_secret=dict(type='str', required=True, no_log=True),
        private_key=dict(type='str', required=True, no_log=True),
        encode_parameters=dict(type='bool', required=False, default=True, no_log=False),
        webhook_secret=dict(type='str', required=False, default=None, no_log=True),
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
def build_requested_setting(params: dict) -> AlmSettingsGithub:

    # Base Parameters Name
    base_param_names = [
        "key", "new_key", "url", "app_id",
        "client_id", "client_secret", "private_key",
        "webhook_secret"
    ]

    # Build Requested Instance
    setting = AlmSettingsGithub(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Return Setting
    return setting


# Porcess Module Execution
def run_module(module: AnsibleModule, client: AlmSettingsGithubClient):

    # Extract State
    state = module.params['state']

    # Extract Encode Private Key
    encode_parameters = module.params.get('encode_parameters', True)

    # Build Requested Instance
    setting = build_requested_setting(module.params)

    # Find Existing Instance
    existing_setting = get_setting(
        client=client,
        key=setting.key
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_setting and state == 'present':

        # If Existing Instance match requested Instance
        if (existing_setting == setting) and (not setting.new_key):

            # Initialize response (No Change)
            module.exit_json(
                msg="Setting [{0}] Not Changed".format(setting.key),
                changed=False,
                instance=filter_none(existing_setting)
            )

        # Update Existing Instance
        update_setting(
            module=module,
            client=client,
            setting=setting,
            encode_parameters=encode_parameters
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
            setting=setting,
            encode_parameters=encode_parameters
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
            key=setting.key
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(setting.key),
            changed=True,
            instance=filter_none(setting),
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(setting.key),
            changed=False,
            instance=filter_none(setting),
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).alm_settings_github

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
