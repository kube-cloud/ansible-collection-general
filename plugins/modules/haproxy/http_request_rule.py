# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: http_request_rule
version_added: "1.0.0"
short_description: Manage HTTP Request Rules
description:
    - Used to Manage HA Proxy HTTP Request Rules
    - Create, Update and Delete HA Proxy HTTP Request Rules
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
    parent_name:
        description:
            - The Rule Parent Name
        required: true
        type: str
    parent_type:
        description:
            - The Rule Parent Type
        required: true
        type: str
        choices: ['backend', 'frontend']
    index:
        description:
            - The HTTP Request Rule Config Field index
        required: false
        type: int
    type:
        description:
            - The HTTP Request Rule Config Field type
        required: false
        type: str
        choices: [
            "ADD_ACL", "ADD_HEADER", "ALLOW", "AUTH", "CACHE_USE", "CAPTURE", "DEL_ACL", "DEL_HEADER",
            "DEL_MAP", "DENY", "DISABLE_L7_RETRY", "DO_RESOLVE", "EARLY_HINT", "LUA", "NORMALIZE_URI",
            "REDIRECT", "REJECT", "REPLACE_HEADER", "REPLACE_PATH", "REPLACE_PATHQ", "REPLACE_URI",
            "REPLACE_VALUE", "RETURN", "SC_ADD_GPC", "SC_INC_GPC", "SC_INC_GPC0", "SC_INC_GPC1",
            "SC_SET_GPT0", "SEND_SPOE_GROUP", "SET_DST", "SET_DST_PORT", "SET_HEADER", "SET_LOG_LEVEL",
            "SET_MAP", "SET_MARK", "SET_METHOD", "SET_NICE", "SET_PATH", "SET_PATHQ", "SET_PRIORITY_CLASS",
            "SET_PRIORITY_OFFSET", "SET_QUERY", "SET_SRC", "SET_SRC_PORT", "SET_TIMEOUT", "SET_TOS",
            "SET_URI", "SET_VAR", "SILENT_DROP", "STRICT_MODE", "TARPIT", "TRACK_SC0", "TRACK_SC1",
            "TRACK_SC2", "UNSET_VAR", "USE_SERVICE", "WAIT_FOR_BODY", "WAIT_FOR_HANDSHAKE", "SET_BANDWIDTH_LIMIT"
        ]
    acl_file:
        description:
            - The HTTP Request Rule Config Field acl_file
        required: false
        type: str
    acl_keyfmt:
        description:
            - The HTTP Request Rule Config Field acl_keyfmt
        required: false
        type: str
    auth_realm:
        description:
            - The HTTP Request Rule Config Field auth_realm
        required: false
        type: str
    bandwidth_limit_limit:
        description:
            - The HTTP Request Rule Config Field bandwidth_limit_limit
        required: false
        type: str
    bandwidth_limit_name:
        description:
            - The HTTP Request Rule Config Field bandwidth_limit_name
        required: false
        type: str
    bandwidth_limit_period:
        description:
            - The HTTP Request Rule Config Field bandwidth_limit_period
        required: false
        type: str
    capture_id:
        description:
            - The HTTP Request Rule Config Field capture_id
        required: false
        type: int
    capture_len:
        description:
            - The HTTP Request Rule Config Field capture_len
        required: false
        type: int
    capture_sample:
        description:
            - The HTTP Request Rule Config Field capture_sample
        required: false
        type: str
    cond:
        description:
            - The HTTP Request Rule Config Field cond
        required: false
        type: str
        choices: ["IF", "UNLESS"]
    cond_test:
        description:
            - The HTTP Request Rule Config Field cond_test
        required: false
        type: str
    deny_status:
        description:
            - The HTTP Request Rule Config Field deny_status
        required: false
        type: int
    expr:
        description:
            - The HTTP Request Rule Config Field expr
        required: false
        type: str
    hdr_format:
        description:
            - The HTTP Request Rule Config Field hdr_format
        required: false
        type: str
    hdr_match:
        description:
            - The HTTP Request Rule Config Field hdr_match
        required: false
        type: str
    hdr_method:
        description:
            - The HTTP Request Rule Config Field hdr_method
        required: false
        type: str
    hdr_name:
        description:
            - The HTTP Request Rule Config Field hdr_name
        required: false
        type: str
    hint_format:
        description:
            - The HTTP Request Rule Config Field hint_format
        required: false
        type: str
    hint_name:
        description:
            - The HTTP Request Rule Config Field hint_name
        required: false
        type: str
    log_level:
        description:
            - The HTTP Request Rule Config Field log_level
        required: false
        type: str
        choices: [
            "EMERG", "ALERT", "CRIT", "ERR", "WARNING",
            "NOTICE", "INFO", "DEBUG", "SILENT"
        ]
    lua_action:
        description:
            - The HTTP Request Rule Config Field lua_action
        required: false
        type: str
    lua_params:
        description:
            - The HTTP Request Rule Config Field lua_params
        required: false
        type: str
    map_file:
        description:
            - The HTTP Request Rule Config Field map_file
        required: false
        type: str
    map_keyfmt:
        description:
            - The HTTP Request Rule Config Field map_keyfmt
        required: false
        type: str
    map_valuefmt:
        description:
            - The HTTP Request Rule Config Field map_valuefmt
        required: false
        type: str
    mark_value:
        description:
            - The HTTP Request Rule Config Field mark_value
        required: false
        type: str
    method_fmt:
        description:
            - The HTTP Request Rule Config Field method_fmt
        required: false
        type: str
    nice_value:
        description:
            - The HTTP Request Rule Config Field nice_value
        required: false
        type: int
    normalizer:
        description:
            - The HTTP Request Rule Config Field normalizer
        required: false
        type: str
        choices: [
            "FRAGMENT_ENCODE", "FRAGMENT_STRIP", "PATH_MERGE_SLASHES", "PATH_STRIP_DOT",
            "PATH_STRIP_DOTDOT", "PERCENT_DECODE_UNRESERVED", "PERCENT_TO_UPPERCASE",
            "QUERY_SORT_BY_NAME"
        ]
    normalizer_full:
        description:
            - The HTTP Request Rule Config Field normalizer_full
        required: false
        type: bool
    normalizer_strict:
        description:
            - The HTTP Request Rule Config Field normalizer_strict
        required: false
        type: bool
    path_fmt:
        description:
            - The HTTP Request Rule Config Field path_fmt
        required: false
        type: str
    path_match:
        description:
            - The HTTP Request Rule Config Field path_match
        required: false
        type: str
    protocol:
        description:
            - The HTTP Request Rule Config Field protocol
        required: false
        type: str
        choices: ["IPV4", "IPV6"]
    redir_code:
        description:
            - The HTTP Request Rule Config Field redir_code
        required: false
        type: int
    redir_option:
        description:
            - The HTTP Request Rule Config Field redir_option
        required: false
        type: str
    redir_type:
        description:
            - The HTTP Request Rule Config Field redir_type
        required: false
        type: str
        choices: [
            "LOCATION", "PREFIX", "SCHEME"
        ]
    redir_value:
        description:
            - The HTTP Request Rule Config Field redir_value
        required: false
        type: str
    resolvers:
        description:
            - The HTTP Request Rule Config Field resolvers
        required: false
        type: str
    return_content:
        description:
            - The HTTP Request Rule Config Field return_content
        required: false
        type: str
    return_content_type:
        description:
            - The HTTP Request Rule Config Field return_content_type
        required: false
        type: str
    return_status_code:
        description:
            - The HTTP Request Rule Config Field return_status_code
        required: false
        type: int
    state:
        description:
        - The Transaction State
        required: false
        choices: ['present', 'absent']
        default: 'present'
        type: str
'''

EXAMPLES = r'''
- name: "Create HA Proxy HTTP Request Rule"
  kube_cloud.haproxy.http_request_rule:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    index: 0
    parent_name: "test_frontend"
    parent_type: "frontend"
    cond: "IF"
    cond_test: "{ path /admin.php } !{ src 192.168.50.20/24 }"
    type: "DENY"
    state: 'present'

- name: "Delete HA Proxy HTTP Request Rule"
  kube_cloud.haproxy.http_request_rule:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    index: 0
    parent_name: "test_frontend"
    parent_type: "frontend"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_http_request_rules import HttpRequestRuleClient
from ...module_utils.haproxy.models import HttpRequestRule
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.commons import filter_none
from ...module_utils.haproxy.enums import HttpRequestRuleType, ConditionType, LogLevel
from ...module_utils.haproxy.enums import HttpRequestRuleNormalizerType, IPProtocol, RedirectType

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Rule
def get_rule(client: HttpRequestRuleClient, index: int, parent_name: str, parent_type: str):

    try:

        # Call Client
        return client.get_rule(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError:

        # Return None
        return None


# Update Rule
def update_rule(module: AnsibleModule, client: HttpRequestRuleClient, transaction_id: str,
                index: int, parent_name: str, parent_type: str, rule: HttpRequestRule, force_reload: bool):

    try:

        # Call Client
        return client.update_rule(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type,
            force_reload=force_reload,
            rule=rule,
            transaction_id=transaction_id
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Rule] - Failed Update HA Proxy Rule (Index : {0}, Parent : {1}:{2}): {3}".format(
                index,
                parent_name,
                parent_type,
                api_error
            )
        )


# Create Rule
def create_rule(module: AnsibleModule, client: HttpRequestRuleClient, transaction_id: str,
                parent_name: str, parent_type: str, rule: HttpRequestRule, force_reload: bool):

    try:

        # Call Client
        return client.create_rule(
            rule=rule,
            transaction_id=transaction_id,
            force_reload=force_reload,
            parent_name=parent_name,
            parent_type=parent_type
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Rule] - Failed Update HA Proxy Rule (Rule : {0}, Parent : {1}:{2}): {3}".format(
                rule,
                parent_name,
                parent_type,
                api_error
            )
        )


# Delete Rule
def delete_rule(module: AnsibleModule, client: HttpRequestRuleClient, transaction_id: str,
                index: int, parent_name: str, parent_type: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_rule(
            index=index,
            parent_name=parent_name,
            parent_type=parent_type,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Rule] - Failed Delete HA Proxy Rule (Index : {0}, Parent : {1}:{2}): {3}".format(
                index,
                parent_name,
                parent_type,
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
        api_version=dict(type='str', required=False, default='v2'),
        transaction_id=dict(type='str', required=False, default=''),
        force_reload=dict(type='bool', required=False, default=True),
        parent_name=dict(type='str', required=True),
        parent_type=dict(type='str', required=True, choices=['frontend', 'backend']),
        index=dict(type='int', required=False),
        type=dict(type='str', required=False, choices=HttpRequestRuleType.names()),
        acl_file=dict(type='str', required=False),
        acl_keyfmt=dict(type='str', required=False, no_log=True),
        auth_realm=dict(type='str', required=False),
        bandwidth_limit_limit=dict(type='str', required=False),
        bandwidth_limit_name=dict(type='str', required=False),
        bandwidth_limit_period=dict(type='str', required=False),
        capture_id=dict(type='int', required=False),
        capture_len=dict(type='int', required=False),
        capture_sample=dict(type='str', required=False),
        cond=dict(type='str', required=False, choices=ConditionType.names()),
        cond_test=dict(type='str', required=False),
        deny_status=dict(type='int', required=False),
        expr=dict(type='str', required=False),
        hdr_format=dict(type='str', required=False),
        hdr_match=dict(type='str', required=False),
        hdr_method=dict(type='str', required=False),
        hdr_name=dict(type='str', required=False),
        hint_format=dict(type='str', required=False),
        hint_name=dict(type='str', required=False),
        log_level=dict(type='str', required=False, choices=LogLevel.names()),
        lua_action=dict(type='str', required=False),
        lua_params=dict(type='str', required=False),
        map_file=dict(type='str', required=False),
        map_keyfmt=dict(type='str', required=False, no_log=True),
        map_valuefmt=dict(type='str', required=False),
        mark_value=dict(type='str', required=False),
        method_fmt=dict(type='str', required=False),
        nice_value=dict(type='int', required=False),
        normalizer=dict(type='str', required=False, choices=HttpRequestRuleNormalizerType.names()),
        normalizer_full=dict(type='bool', required=False),
        normalizer_strict=dict(type='bool', required=False),
        path_fmt=dict(type='str', required=False),
        path_match=dict(type='str', required=False),
        protocol=dict(type='str', required=False, choices=IPProtocol.names()),
        redir_code=dict(type='int', required=False),
        redir_option=dict(type='str', required=False),
        redir_type=dict(type='str', required=False, choices=RedirectType.names()),
        redir_value=dict(type='str', required=False),
        resolvers=dict(type='str', required=False),
        return_content=dict(type='str', required=False),
        return_content_type=dict(type='str', required=False),
        return_status_code=dict(type='int', required=False),
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


# Build Requested Http Request Rule from Configuration
def build_requested_rule(params: dict) -> HttpRequestRule:

    # Base Parameters Name
    base_param_names = [
        "index", "acl_file", "acl_keyfmt", "auth_realm", "bandwidth_limit_limit",
        "bandwidth_limit_name", "bandwidth_limit_period", "capture_id", "capture_len",
        "capture_sample", "cond_test", "deny_status", "expr", "hdr_format", "hdr_match",
        "hdr_method", "hdr_name", "hint_format", "hint_name", "lua_action", "lua_params",
        "map_file", "map_keyfmt", "map_valuefmt", "mark_value", "method_fmt", "nice_value",
        "normalizer_full", "normalizer_strict", "path_fmt", "path_match", "redir_code",
        "redir_option", "redir_value", "resolvers", "return_content", "return_content_type",
        "return_status_code"
    ]

    # Build Requested Instance
    rule = HttpRequestRule(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Optional Initialization : mode
    rule.type = HttpRequestRuleType.create(params.get('type', None))
    rule.cond = ConditionType.create(params.get('cond', None))
    rule.log_level = LogLevel.create(params.get('log_level', None))
    rule.normalizer = HttpRequestRuleNormalizerType.create(params.get('normalizer', None))
    rule.protocol = IPProtocol.create(params.get('protocol', None))
    rule.redir_type = RedirectType.create(params.get('redir_type', None))

    # Build Requested Instance
    return rule


# Porcess Module Execution
def run_module(module: AnsibleModule, client: HttpRequestRuleClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Rule Parent Name
    parent_name = module.params['parent_name']

    # Rule Parent Type
    parent_type = module.params['parent_type']

    # Build Requested Instance
    rule = build_requested_rule(module.params)

    # Find Existing Instance
    existing_instance = get_rule(
        client=client,
        index=rule.index,
        parent_name=parent_name,
        parent_type=parent_type
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_instance and state == 'present':

        # If Existing Instance match requested Instance
        if existing_instance == rule:

            # Initialize response (No Change)
            module.exit_json(
                msg="Rule [Parent : {0}/{1}, Index : {2}] Not Changed".format(
                    parent_name,
                    parent_type,
                    rule.index
                ),
                changed=False,
                instance=filter_none(rule),
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Update Existing Instance
        update_rule(
            module=module,
            client=client,
            transaction_id=transaction_id,
            rule=rule,
            index=rule.index,
            parent_name=parent_name,
            parent_type=parent_type,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(rule),
            parent_name=parent_name,
            parent_type=parent_type,
            msg="Rule [Parent : {0}/{1}, Name : {2}] Has Been Updated".format(
                parent_name,
                parent_type,
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
            parent_name=parent_name,
            parent_type=parent_type,
            rule=rule
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(rule),
            parent_name=parent_name,
            parent_type=parent_type,
            msg="Rule [Parent : {0}/{1}, Name : {2}] Has Been Created".format(
                parent_name,
                parent_type,
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
            parent_name=parent_name,
            parent_type=parent_type
        )

        # Exit Module
        module.exit_json(
            changed=True,
            instance=rule,
            parent_name=parent_name,
            parent_type=parent_type,
            msg="Rule [Parent : {0}/{1}, Name : {2}] Has Been Deleted".format(
                parent_name,
                parent_type,
                rule.index
            )
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="Rule Not Found [Parent : {0}/{1}, Name : {2}]".format(
                parent_name,
                parent_type,
                rule.index
            ),
            changed=False,
            instance=filter_none(rule),
            parent_name=parent_name,
            parent_type=parent_type
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).request_rule

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
