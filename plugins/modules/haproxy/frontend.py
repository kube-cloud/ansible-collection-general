# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: frontend
version_added: "1.0.0"
short_description: Manage Frontends
description:
  - Used to Manage HA Proxy Frontend
  - Create, Update and Delete HA Proxy Frontends
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
  name:
    description:
      - The HA Proxy Frontend Name
    required: true
    type: str
  mode:
    description:
      - The HA Proxy Frontend Mode
    required: false
    choices: ['HTTP', 'TCP']
    default: 'HTTP'
    type: str
  default_backend:
    description:
      - The HA Proxy Frontend Default Backend
    required: false
    type: str
  log_format:
    description:
      - The HA Proxy Frontend Log Format
    required: false
    type: str
  description:
    description:
      - The HA Proxy Frontend Description
    required: false
    type: str
  log_format_sd:
    description:
      - The HA Proxy Frontend  Log Format SD
    required: false
    type: str
  log_tag:
    description:
      - The HA Proxy Frontend  Log TAG
    required: false
    type: str
  logsap:
    description:
      - The HA Proxy Frontend  Log SAP
    required: false
    type: str
    choices: ['enabled', 'disabled']
  maxconn:
    description:
      - The HA Proxy Frontend  Max Connexion
    required: false
    type: int
  enabled:
    description:
      - The HA Proxy Frontend Enabled
    required: false
    type: bool
  httplog:
    description:
      - The HA Proxy Frontend HTTP Log Enabled Flag
    required: false
    type: bool
  httpslog:
    description:
      - The HA Proxy Frontend HTTPS Log Enabled Flag
    required: false
    type: str
  error_log_format:
    description:
      - The HA Proxy Frontend Error Log Format
    required: false
    type: str
  forwardfor:
    description:
      - The HA Proxy Frontend Forwarded For
    required: false
    type: dict
  stats_options:
    description:
      - The HA Proxy Frontend Stats Options
    required: false
    type: dict
  transaction_id:
    description:
      - The Transaction ID (If need to execute action as part of API Transaction)
    required: false
    default: ""
    type: str
  force_reload:
    description:
      - Force reload HA Proxy Configuration
    required: false
    default: true
    type: bool
  state:
    description:
      - The Frontend State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Create HA Proxy Frontend"
  kube_cloud.haproxy.frontend:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jira-frontend-service"
    mode: 'HTTP'
    default_backend: 'jira-backend-service'
    description: 'Frontend for JIRA Service'
    maxconn: 10
    forwardfor:
      enabled: 'enabled'
      header: 'test-header'
      ifnone: false
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    state: 'present'

- name: "Create HA Proxy Frontend"
  kube_cloud.haproxy.frontend:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jira-frontend-service"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    force_reload: true
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_frontends import FrontendClient
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.haproxy.models import Frontend, ForwardFor, StatsOptions, StatsAuth
from ...module_utils.haproxy.enums import ProxyProtocol, EnableDisableEnum, ConditionType
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Frontend
def get_frontend(client: FrontendClient, name: str):

    try:

        # Call Client
        return client.get_frontend(name=name)

    except HTTPError:

        # Return None
        return None


# Update Frontend
def update_frontend(module: AnsibleModule, client: FrontendClient, transaction_id: str, name: str, frontend: Frontend, force_reload: bool):

    try:

        # Call Client
        return client.update_frontend(
            name=name,
            frontend=frontend,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Frontend] - Failed Update HA Proxy Frontend (Name : {0} : [{1}]): {2}".format(
                name,
                frontend,
                api_error
            )
        )


# Create Frontend
def create_frontend(module: AnsibleModule, client: FrontendClient, transaction_id: str, frontend: Frontend, force_reload: bool):

    try:

        # Call Client
        return client.create_frontend(
            frontend=frontend,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Frontend] - Failed Create HA Proxy Frontend (Name : {0} : [{1}]): {2}".format(
                frontend.name,
                frontend,
                api_error
            )
        )


# Delete Frontend
def delete_frontend(module: AnsibleModule, client: FrontendClient, transaction_id: str, name: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_frontend(
            name=name,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Frontend] - Failed Delete HA Proxy Frontend (Name : {0}): {1}".format(
                name,
                api_error
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True, no_log=False),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        api_version=dict(type='str', required=False, default='v2', no_log=False),
        name=dict(type='str', required=True, no_log=False),
        mode=dict(type='str', required=False, default='HTTP', choices=['HTTP', 'TCP'], no_log=False),
        default_backend=dict(type='str', required=False, default=None, no_log=False),
        log_format=dict(type='str', required=False, default=None, no_log=False),
        description=dict(type='str', required=False, default=None, no_log=False),
        log_format_sd=dict(type='str', required=False, default=None, no_log=False),
        log_tag=dict(type='str', required=False, default=None, no_log=False),
        logsap=dict(type='str', required=False, default=None, choices=['enabled', 'disabled'], no_log=False),
        maxconn=dict(type='int', required=False, default=None, no_log=False),
        enabled=dict(type='bool', required=False, default=None, no_log=False),
        httplog=dict(type='bool', required=False, default=None, no_log=False),
        httpslog=dict(type='str', required=False, default=None, no_log=False),
        error_log_format=dict(type='str', required=False, default=None, no_log=False),
        forwardfor=dict(type='dict', required=False, default=None, no_log=False),
        stats_options=dict(type='dict', required=False, default=None, no_log=False),
        transaction_id=dict(type='str', required=False, default='', no_log=False),
        force_reload=dict(type='bool', required=False, default=True, no_log=False),
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


# Build Requested Frontend from Configuration
def build_requested_frontend(params: dict) -> Frontend:

    # Base Parameters Name
    base_param_names = [
        "name",
        "default_backend",
        "log_format",
        "description",
        "log_format_sd",
        "log_tag",
        "maxconn",
        "enabled",
        "error_log_format",
        "httplog"
    ]

    # Build Requested Instance
    frontend = Frontend(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Optional Initialization : mode
    frontend.mode = ProxyProtocol.create(params['mode'])

    # Optional Initialization : logsap
    frontend.logsap = EnableDisableEnum.create(params['logsap'])

    # Optional Initialization : httpslog
    frontend.httpslog = EnableDisableEnum.create(params['httpslog'])

    # Optional Initialization : forwardfor
    if params['forwardfor']:

        # Extract ForwardedFor
        p_formwardfor = params['forwardfor']

        # Initialize Object
        frontend.forwardfor = ForwardFor(
            enabled=EnableDisableEnum.create(p_formwardfor.get('enabled', None)),
            header=p_formwardfor.get('header', None),
            ifnone=p_formwardfor.get('ifnone', None)
        )

    # Optional Initialization : stats_options
    if params['stats_options']:

        # Extract Stats Options
        p_stats_options = params['stats_options']

        # Base Parameters Name
        stats_base_param_names = [
            "stats_admin_cond",
            "stats_admin_cond_test",
            "stats_enable",
            "stats_hide_version",
            "stats_maxconn",
            "stats_realm",
            "stats_realm_realm",
            "stats_refresh_delay",
            "stats_show_desc",
            "stats_show_legends",
            "stats_show_modules",
            "stats_show_node_name",
            "stats_uri_prefix"
        ]

        # Build Requested Instance
        frontend.stats_options = StatsOptions(
            **{k: v for k, v in p_stats_options.items() if v is not None and k in stats_base_param_names}
        )

        # Initialize Admin Condition
        frontend.stats_options.stats_admin_cond = ConditionType.create(
            p_stats_options.get('stats_admin_cond', None)
        )

        # Optional Initialization : stats_auths
        if p_stats_options['stats_auths']:

            # Extract Stats Auth
            p_stats_auths = p_stats_options['stats_auths']

            # List if Stats Auths
            stats_auths = []

            # Iterate on List
            for p_stats_auth in p_stats_auths:

                # Append Auth
                stats_auths.append(StatsAuth(
                    user=p_stats_auth.get('user', None),
                    passwd=p_stats_auth.get('passwd', None)
                ))

            # Add Auths to Frontend Stats Options
            frontend.stats_options.stats_auths = stats_auths

    # Return Frontend
    return frontend


# Porcess Module Execution
def run_module(module: AnsibleModule, client: FrontendClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Build Requested Frontend
    frontend = build_requested_frontend(module.params)

    # Find Existing Instance
    existing_frontend = get_frontend(
        client=client,
        name=frontend.name
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_frontend and state == 'present':

        # If Existing Instance match requested Instance
        if existing_frontend == frontend:

            # Initialize response (No Change)
            module.exit_json(
                msg="Frontend [{0} - {1}] Not Changed".format(frontend.name, frontend.mode),
                instance=filter_none(frontend),
                changed=False
            )

        # Update Existing Instance
        update_frontend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=frontend.name,
            frontend=frontend,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(frontend),
            msg="Frontend [{0} - {1}] Has Been Updated".format(frontend.name, frontend.mode)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_frontend and state == 'present':

        # Create Instance
        create_frontend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            frontend=frontend,
            force_reload=force_reload
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(frontend),
            msg="[{0} - {1}] Has been Created".format(frontend.name, frontend.mode)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_frontend and state == 'absent':

        # Delete Instance
        delete_frontend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=frontend.name,
            force_reload=force_reload
        )

        # Exit Module
        module.exit_json(
            msg="[{0} - {1}] Has been Deleted".format(frontend.name, frontend.mode),
            instance=filter_none(frontend),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0} - {1}] Not Found".format(frontend.name, frontend.mode),
            instance=filter_none(frontend),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).frontend

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
