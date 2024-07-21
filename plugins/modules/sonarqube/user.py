# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: user
version_added: "1.0.0"
short_description: Manage Users
description:
  - Used to Manage Sonarqube Users
  - Create, Update and Delete Sonarqube Users
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
  user_login:
    description:
      - The SonarQube User Login
    required: true
    type: str
  user_password:
    description:
      - The SonarQube User Password
    required: false
    type: str
  user_email:
    description:
      - The SonarQube User Email
    required: false
    type: str
  user_name:
    description:
      - The SonarQube User Name
    required: false
    type: str
  user_local:
    description:
      - The SonarQube User Local Status
    required: false
    default: true
    type: bool
  user_scm_accounts:
    description:
      - The SonarQube User SCM Accounts
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
- name: "Create SonarQube User"
  kube_cloud.general.sonarqube.user:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    user_login: "my_mogin"
    user_password: "my_password"
    user_email: "my_email@localhost.com"
    user_name: "Lastname Firstname"
    user_local: true
    user_scm_accounts: ['github_account', 'gitlab_account']
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import UserClient, sonarqube_client
from ...module_utils.sonarqube.models import User
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Users
def get_user(client: UserClient, login: str) -> User:

    try:

        # Call Client
        return client.get_user(login=login)

    except HTTPError:

        # Return None
        return None


# Update User
def update_user(module: AnsibleModule, client: UserClient, user: User) -> User:

    try:

        # Call Client
        return client.update_user(user=user)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update User] - Failed Update SonarQube User [{0}]: {1}".format(
                user,
                api_error
            )
        )


# Create User
def create_user(module: AnsibleModule, client: UserClient, user: User):

    try:

        # Call Client
        return client.create_user(user=user)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create User] - Failed Create SonarQube User [{0}]: {1}".format(
                user,
                api_error
            )
        )


# Delete User
def delete_user(module: AnsibleModule, client: UserClient, login: str):

    try:

        # Call Client
        return client.delete_user(
            login=login
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete User] - Failed Delete SonarQube User (Login : {0}): {1}".format(
                login,
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
        user_login=dict(type='str', required=True, no_log=True),
        user_password=dict(type='str', required=False, default=None, no_log=True),
        user_email=dict(type='str', required=False, default=None),
        user_name=dict(type='str', required=False, default=None),
        user_local=dict(type='bool', required=False, default=True),
        user_scm_accounts=dict(type='list', elements='str', required=False, default=[]),
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


# Build Requested User from Configuration
def build_requested_user(params: dict) -> User:

    # Base Parameters Name
    base_param_names = [
        "user_login", "user_password", "user_email",
        "user_name", "user_local", "user_scm_accounts"
    ]

    # Build Requested Instance
    return User(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: UserClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    user = build_requested_user(module.params)

    # Find Existing Instance
    existing_user = get_user(
        client=client,
        login=user.user_login
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_user and state == 'present':

        # If Existing Instance match requested Instance
        if existing_user == user:

            # Initialize response (No Change)
            module.exit_json(
                msg="User [{0}] Not Changed".format(user.user_login),
                changed=False
            )

        # Update Existing Instance
        update_user(
            module=module,
            client=client,
            user=user
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(user),
            msg="User [{0}] Has Been Updated".format(user)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_user and state == 'present':

        # Create Instance
        create_user(
            module=module,
            client=client,
            user=user
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(user),
            msg="[{0}] Has been Created".format(user)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_user and state == 'absent':

        # Delete Instance
        delete_user(
            module=module,
            client=client,
            login=user.user_login
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(user.user_login),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(user.user_login),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).user

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
