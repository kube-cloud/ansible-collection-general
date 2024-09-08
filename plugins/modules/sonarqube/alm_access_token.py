# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: alm_access_token
version_added: "1.0.0"
short_description: Update ALM Access Token
description:
  - Used to Update ALM Access Token
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
  alm_name:
    description:
      - The SonarQube ALM Name
    required: true
    type: str
  access_token:
    description:
      - The SonarQube ALM Access Token
    required: true
    type: str
  token_username:
    description:
      - The SonarQube ALM Token Username
    required: false
    type: str
  state:
    description:
      - The Token State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Initialize SonarQube ALM Access Token"
  kube_cloud.general.sonarqube.alm_access_token:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    alm_name: "github_connector"
    access_token: "XXRATTUQX091E45TG"
    state: 'present'

- name: "Create SonarQube ALM Setting Azure"
  kube_cloud.general.sonarqube.alm_access_token:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    alm_name: "github_connector"
    access_token: "XXRATTUQX091E45TG"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import AlmAccessTokenClient, sonarqube_client
from ...module_utils.commons import filter_none
from ...module_utils.sonarqube.models import AlmToken

try:
    from requests import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Set Access Token
def set_alm_token(
    module: AnsibleModule,
    client: AlmAccessTokenClient,
    alm_token: AlmToken
):

    try:

        # Call Client
        return client.set_access_token(
            alm_name=alm_token.alm_name,
            access_token=alm_token.access_token,
            token_username=alm_token.token_username
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Set ALM Token] - Failed Set Token [{0}/{1}({2}) : {3}]".format(
                alm_token.alm_name,
                alm_token.access_token,
                alm_token.username if alm_token.username else '',
                str(api_error)
            )
        )


# Delete Access Token
def delete_setting(
    module: AnsibleModule,
    client: AlmAccessTokenClient,
    alm_name: str
):

    try:

        # Call Client
        return client.set_access_token(
            alm_name=alm_name,
            access_token="@__NO_ACCESS_TOKEN__@",
            token_username=None
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete ALM Token] - Failed Delete Token [{0}) : {1}]".format(
                alm_name,
                str(api_error)
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        alm_name=dict(type='str', required=True, no_log=False),
        access_token=dict(type='str', required=True, no_log=True),
        token_username=dict(type='str', required=False, no_log=True),
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


# Build Requested Instance from Configuration
def build_requested_instance(params: dict) -> AlmToken:

    # Base Parameters Name
    base_param_names = [
        "alm_name", "access_token", "token_username"
    ]

    # Build Requested Instance
    return AlmToken(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: AlmAccessTokenClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    alm_token = build_requested_instance(module.params)

    # If Requested State is 'present'
    if state == 'present':

        # Update ALM Token
        set_alm_token(
            module=module,
            client=client,
            alm_token=alm_token
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(alm_token),
            msg="[{0}/{1}] Has been Setted".format(alm_token.alm_name, alm_token.access_token)
        )

    # If Requested State is 'absent'
    if state == 'absent':

        # Delete Instance
        delete_setting(
            module=module,
            client=client,
            alm_name=alm_token.alm_name
        )

        # Exit Module
        module.exit_json(
            msg="[{0}]'s Token Has been Invalidated".format(alm_token.alm_name),
            changed=True,
            instance=filter_none(alm_token)
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).alm_access_token

    # Execute Module
    run_module(module, client)


# If file is executed directly
if __name__ == '__main__':

    # Launch Entrypoint
    main()
