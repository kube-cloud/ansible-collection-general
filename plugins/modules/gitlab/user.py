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
short_description: User Management
description:
    - Used to Create, Update, Delete User
requirements:
    - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
    base_url:
        description:
        - The Gitlab API Base URL
        required: true
        type: str
    access_token:
        description:
        - The Gitlab API Admin Access Token
        required: true
        type: str
    username:
        description:
        - The User Login.
        required: true
        type: str
    password:
        description:
        - The User Password (For Creation).
        required: true
        type: str
    name:
        description:
        - The User Name.
        required: true
        type: str
    user_state:
        description:
        - The User State.
        required: false
        default: 'active'
        type: str
    locked:
        description:
        - The User Locked Flag.
        required: false
        default: false
        type: bool
    avatar_url:
        description:
        - The User Avatar URL.
        required: false
        type: str
    web_url:
        description:
        - The User Web URL.
        required: false
        type: str
    created_at:
        description:
        - The User Creation Date.
        required: false
        type: str
    bio:
        description:
        - The User BIO.
        required: false
        type: str
    location:
        description:
        - The User Location.
        required: false
        type: str
    public_email:
        description:
        - The User Public Email.
        required: false
        type: str
    skype:
        description:
        - The User Skype ID.
        required: false
        type: str
    linkedin:
        description:
        - The User LinkedIn ID.
        required: false
        type: str
    twitter:
        description:
        - The User Twitter Profile ID.
        required: false
        type: str
    discord:
        description:
        - The User Discord.
        required: false
        type: str
    website_url:
        description:
        - The User Website URL.
        required: false
        type: str
    organization:
        description:
        - The User Organization.
        required: false
        type: str
    job_title:
        description:
        - The User Job Title.
        required: false
        type: str
    pronouns:
        description:
        - The User Pronouns.
        required: false
        type: str
    bot:
        description:
        - The User Bot Flag.
        required: false
        type: bool
    last_sign_in_at:
        description:
        - The User Last Sign In Date.
        required: false
        type: str
    confirmed_at:
        description:
        - The User Confirmation Date.
        required: false
        type: str
    last_activity_on:
        description:
        - The User Last Activity Date.
        required: false
        type: str
    email:
        description:
        - The User Private Email.
        required: true
        type: str
    theme_id:
        description:
        - The User Theme ID.
        required: false
        type: str
    color_scheme_id:
        description:
        - The User Color Scheme ID.
        required: false
        type: str
    projects_limit:
        description:
        - The User Project Limit.
        required: false
        type: str
    current_sign_in_at:
        description:
        - The User Current Sign In Date.
        required: false
        type: str
    can_create_group:
        description:
        - The User Create Group Enabled Flag.
        required: false
        type: bool
    can_create_project:
        description:
        - The User Create Project Enabled Flag.
        required: false
        type: bool
    two_factor_enabled:
        description:
        - The User Two Factor Enabled Flag.
        required: false
        type: bool
    external:
        description:
        - The User External Flag.
        required: false
        type: bool
    private_profile:
        description:
        - The User Private Profile Flag.
        required: false
        type: bool
    commit_email:
        description:
        - The User Commit Email.
        required: false
        type: str
    is_admin:
        description:
        - The User Admin Flag.
        required: false
        type: bool
    admin:
        description:
        - The User Admin Flag (Used for Creation).
        required: false
        type: bool
    auditor:
        description:
        - The User Auditor Flag (Used for Creation).
        required: false
        type: bool
    note:
        description:
        - The User Admin Note (Used for Creation).
        required: false
        type: str
    skip_confirmation:
        description:
        - The User Skip Confirmation Flag (Used for Creation).
        required: false
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
- name: "Update Gitlab User Password"
  kube_cloud.general.gitlab.update_user_password:
    base_url: "http://localhost:9000"
    access_token: "glat_cv182gTX22lMnB8876"
    password: "admin"
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.gitlab.client import UserClient, gitlab_client, Client
from ...module_utils.gitlab.models import User
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Users
def get_user(client: UserClient, username: str) -> User:

    try:

        # Call Client
        return client.get_user_by_name(username=username)

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
            msg="[Update User] - Failed Update Gitlab User [{0}]: {1}".format(
                user.username,
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
            msg="[Create User] - Failed Create Gitlab User [{0}]: {1}".format(
                user.username,
                api_error
            )
        )


# Delete User
def delete_user(module: AnsibleModule, client: UserClient, username: str):

    try:

        # Call Client
        return client.delete_user(
            username=username
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete User] - Failed Delete Gitlab User (Login : {0}): {1}".format(
                username,
                api_error
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True, no_log=False),
        access_token=dict(type='str', required=True, no_log=False),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        name=dict(type='str', required=True, no_log=False),
        user_state=dict(type='str', required=False, default='active', no_log=False),
        locked=dict(type='bool', required=False, default=False, no_log=False),
        avatar_url=dict(type='str', required=False, default=None, no_log=False),
        web_url=dict(type='str', required=False, default=None, no_log=False),
        created_at=dict(type='str', required=False, default=None, no_log=False),
        bio=dict(type='str', required=False, default=None, no_log=False),
        location=dict(type='str', required=False, default=None, no_log=False),
        public_email=dict(type='str', required=False, default=None, no_log=False),
        skype=dict(type='str', required=False, default=None, no_log=False),
        linkedin=dict(type='str', required=False, default=None, no_log=False),
        twitter=dict(type='str', required=False, default=None, no_log=False),
        discord=dict(type='str', required=False, default=None, no_log=False),
        website_url=dict(type='str', required=False, default=None, no_log=False),
        organization=dict(type='str', required=False, default=None, no_log=False),
        job_title=dict(type='str', required=False, default=None, no_log=False),
        pronouns=dict(type='str', required=False, default=None, no_log=False),
        bot=dict(type='bool', required=False, default=None, no_log=False),
        last_sign_in_at=dict(type='str', required=False, default=None, no_log=False),
        confirmed_at=dict(type='str', required=False, default=None, no_log=False),
        last_activity_on=dict(type='str', required=False, default=None, no_log=False),
        email=dict(type='str', required=True, no_log=False),
        theme_id=dict(type='str', required=False, default=None, no_log=False),
        color_scheme_id=dict(type='str', required=False, default=None, no_log=False),
        projects_limit=dict(type='str', required=False, default=None, no_log=False),
        current_sign_in_at=dict(type='str', required=False, default=None, no_log=False),
        can_create_group=dict(type='bool', required=False, default=None, no_log=False),
        can_create_project=dict(type='bool', required=False, default=None, no_log=False),
        two_factor_enabled=dict(type='bool', required=False, default=None, no_log=False),
        external=dict(type='bool', required=False, default=None, no_log=False),
        private_profile=dict(type='bool', required=False, default=None, no_log=False),
        commit_email=dict(type='str', required=False, default=None, no_log=False),
        is_admin=dict(type='bool', required=False, default=None, no_log=False),
        admin=dict(type='bool', required=False, default=None, no_log=False),
        auditor=dict(type='bool', required=False, default=None, no_log=False),
        note=dict(type='str', required=False, default=None, no_log=False),
        skip_confirmation=dict(type='bool', required=False, default=None, no_log=False),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
    )

    # Build ansible Module
    return AnsibleModule(
        argument_spec=module_specification,
        supports_check_mode=True
    )


# Instantiate Ansible Module
def build_client(module: AnsibleModule) -> Client:

    try:

        # Build Client from Module
        return gitlab_client(module.params)

    except ValueError:

        # Set Module Error
        module.fail_json(
            msg="[Build Client] - Failed Build Gitlab API Client"
        )


# Build Requested User from Configuration
def build_requested_user(params: dict) -> User:

    # Module Specification Property Names
    base_param_names = [
        "base_url", "access_token", "username", "password", "name",
        "user_state", "locked", "avatar_url", "web_url", "created_at",
        "bio", "location", "public_email", "skype", "linkedin",
        "twitter", "discord", "website_url", "organization",
        "job_title", "pronouns", "bot", "last_sign_in_at",
        "confirmed_at", "last_activity_on", "email", "theme_id",
        "color_scheme_id", "projects_limit", "current_sign_in_at",
        "can_create_group", "can_create_project", "two_factor_enabled",
        "external", "private_profile", "commit_email", "is_admin",
        "admin", "auditor", "note", "skip_confirmation"
    ]

    # Build Requested Instance
    return User(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, user_client: UserClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    user = build_requested_user(module.params)

    # Find Existing Instance
    existing_user = get_user(
        client=user_client,
        username=user.username
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_user and state == 'present':

        # Update Existing Instance
        update_user(
            module=module,
            client=user_client,
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
            client=user_client,
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
            client=user_client,
            username=user.username
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(user.username),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(user.username),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module)

    # Execute Module
    run_module(
        module=module,
        user_client=client.user
    )


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
