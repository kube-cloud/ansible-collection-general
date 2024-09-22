# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: backend_switching_rule
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
    rule_frontend:
        description:
        - The Backend Switching Rule Frontend
        required: true
        type: str
    rule_cond:
        description:
        - The Backend Switching Rule Condition Type
        required: false
        choices: ['if', 'unless']
        type: str
    rule_cond_test:
        description:
        - The Backend Switching Rule Condition
        required: false
        type: str
    rule_name:
        description:
        - The Backend Switching Rule Name
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
- name: "Create HA Proxy Backend Switching Rule"
  kube_cloud.general.haproxy.backend_switching_rule:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    rule_frontend: "test_frontend"
    rule_cond: "if"
    rule_cond_test: "is_exemple_acl"
    rule_name: "jira-service-backend"
    state: 'present'

- name: "Delete HA Proxy Backend Switching Rule"
  kube_cloud.general.haproxy.backend_switching_rule:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    rule_name: 'test_rule'
    rule_frontend: "test_frontend"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_backend_switching_rules import BackendSwitchingRuleClient
from ...module_utils.haproxy.models import BackendSwitchingRule
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.haproxy.enums import ConditionType
from ...module_utils.commons import filter_none
from typing import List

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return BE Switching Rule
def get_rule(client: BackendSwitchingRuleClient, index: int, frontend_name: str):

    try:

        # Call Client
        return client.get_backend_switching_rule(
            index=index,
            frontend_name=frontend_name
        )

    except HTTPError:

        # Return None
        return None


# Find and Return BE Switching Rules
def get_rules(client: BackendSwitchingRuleClient, frontend_name: str = '') -> List[BackendSwitchingRule]:

    try:

        # Call Client
        return client.get_backend_switching_rules(
            frontend_name=frontend_name.strip()
        )

    except HTTPError:

        # Return None
        return []


# Update BE Switching Rule
def update_rule(module: AnsibleModule, client: BackendSwitchingRuleClient, transaction_id: str,
                index: int, frontend_name: str, rule: BackendSwitchingRule, force_reload: bool):

    try:

        # Call Client
        return client.update_backend_switching_rule(
            index=index,
            frontend_name=frontend_name,
            force_reload=force_reload,
            besr=rule,
            transaction_id=transaction_id
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Rule] - Failed Update HA Proxy Rule (Index : {0}, Frontend : {1}): {2}".format(
                index,
                frontend_name,
                api_error
            )
        )


# Create BE Switching Rule
def create_rule(module: AnsibleModule, client: BackendSwitchingRuleClient, transaction_id: str, frontend_name: str,
                rule: BackendSwitchingRule, force_reload: bool):

    try:

        # Call Client
        return client.create_backend_switching_rule(
            besr=rule,
            transaction_id=transaction_id,
            force_reload=force_reload,
            frontend_name=frontend_name
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Rule] - Failed Create HA Proxy Rule ({0}, Frontend : {1}): {2}".format(
                rule,
                frontend_name,
                api_error
            )
        )


# Delete BE Switching Rule
def delete_rule(module: AnsibleModule, client: BackendSwitchingRuleClient, transaction_id: str, index: int, frontend_name: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_backend_switching_rule(
            index=index,
            frontend_name=frontend_name,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Rule] - Failed Delete HA Proxy Rule (Index : {0}, Frontend : {1}): {2}".format(
                index,
                frontend_name,
                api_error
            )
        )


def find_rule_by_name(rules: List[BackendSwitchingRule], name: str = '') -> BackendSwitchingRule:

    # If List is Not Provided
    if rules is None:

        # Return None
        return None

    # Build name to compare
    p_name = name.strip().lower()

    # Iterate on rules List
    for rule in rules:

        # Build Rule Name
        rule_name = rule.name.strip().lower() if rule.name else ''

        # If Name are same
        if rule_name == p_name:

            # Return ACL
            return rule

    # Return None
    return None


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True, no_log=False),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        api_version=dict(type='str', required=False, default='v2', no_log=False),
        transaction_id=dict(type='str', required=False, default='', no_log=False),
        force_reload=dict(type='bool', required=False, default=True, no_log=False),
        rule_frontend=dict(type='str', required=True, no_log=False),
        rule_cond=dict(type='str', required=False, choices=['if', 'unless'], no_log=False),
        rule_cond_test=dict(type='str', required=False, no_log=False),
        rule_name=dict(type='str', required=False, no_log=False),
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


# Build Requested Rule from Configuration
def build_requested_rule(params: dict) -> BackendSwitchingRule:

    # Build Requested Instance
    return BackendSwitchingRule(
        cond=ConditionType.create(params.get('rule_cond', None)),
        cond_test=params.get('rule_cond_test', None),
        name=params.get('rule_name', None)
    )


# Porcess Module Execution
def run_module(module: AnsibleModule, client: BackendSwitchingRuleClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Rule Frontend Name
    rule_frontend = module.params['rule_frontend']

    # Build Requested Instance
    rule = build_requested_rule(module.params)

    # Get Liste of Rules
    rules = get_rules(
        client=client,
        frontend_name=rule_frontend
    )

    # Rules Size
    rule_size = len(rules)

    # Find Existing Instance
    existing_instance = find_rule_by_name(
        rules=rules,
        name=rule.name
    )

    # If Instance Exists
    if existing_instance:

        # Initialize Index
        rule.index = existing_instance.index

    else:

        # Add Index
        rule.index = (rule_size - 1) if rule_size > 0 else 0

    # If Requested State is 'present' and Instance Already exists
    if existing_instance and state == 'present':

        # If Existing Instance match requested Instance
        if existing_instance == rule:

            # Initialize response (No Change)
            module.exit_json(
                msg="Rule [Frontend : {0}/{1}, Name : {2}] Not Changed".format(
                    rule_frontend,
                    rule.name,
                    rule.index
                ),
                instance=filter_none(existing_instance),
                frontend=rule_frontend,
                changed=False
            )

        # Update Existing Instance
        update_rule(
            module=module,
            client=client,
            transaction_id=transaction_id,
            rule=rule,
            index=rule.index,
            frontend_name=rule_frontend,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(rule),
            frontend=rule_frontend,
            msg="Rule [Frontend : {0}, Name : {1}/{2}] Has Been Updated".format(
                rule_frontend,
                rule.name,
                rule.index
            )
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_instance and state == 'present':

        # Create Instance
        create_rule(
            module=module,
            client=client,
            transaction_id=transaction_id,
            force_reload=force_reload,
            frontend_name=rule_frontend,
            rule=rule
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(rule),
            frontend=rule_frontend,
            msg="Rule [Frontend : {0}, Name : {1}/{2}] Has Been Created".format(
                rule_frontend,
                rule.name,
                rule.index
            )
        )

    # If Requested State is 'absent' and Instance exists
    if existing_instance and state == 'absent':

        # Delete Instance
        delete_rule(
            module=module,
            client=client,
            transaction_id=transaction_id,
            force_reload=force_reload,
            index=rule.index,
            frontend_name=rule_frontend
        )

        # Exit Module
        module.exit_json(
            changed=True,
            instance=rule,
            frontend=rule_frontend,
            msg="Rule [Frontend : {0}, Name : {1}/{2}] Has Been Deleted".format(
                rule_frontend,
                rule.name,
                rule.index
            )
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="Rule Not Found [Frontend : {0}, Name : {1}/{2}]".format(
                rule_frontend,
                rule.name,
                rule.index
            ),
            instance=filter_none(rule),
            frontend=rule_frontend,
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).besr

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
