# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: backend
version_added: "1.0.0"
short_description: Manage Backends
description:
  - Used to Manage HA Proxy Backend
  - Create and Delete HA Proxy Bacnekends
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
      - The HA Proxy Backend Name
    required: true
    type: str
  mode:
    description:
      - The HA Proxy Backend Mode
    required: false
    choices: ['HTTP', 'TCP']
    default: 'HTTP'
    type: str
  adv_check:
    description:
      - The HA Proxy Backend Advance Check
    required: false
    choices: [
      'SSL_HELLO_CHK', 'SMTPCHK', 'HTTPCHK',
      'REDIS_CHECK', 'TCP_CHECK', 'PGSQL_CHECK',
      'MYSQL_CHECK', 'LDAP_CHECK'
    ]
    type: str
  balance:
    description:
      - The HA Proxy Backend Load Balancing
    required: false
    type: dict
  httpchk:
    description:
      - The HA Proxy Backend Default HealthCheck Configuration
    required: false
    type: dict
  httpchk_params:
    description:
      - The HA Proxy Backend HealthCheck Configuration
    required: false
    type: dict
  pgsql_check_params:
    description:
      - The HA Proxy Backend Postgres Healtcheck Configuration
    required: false
    type: dict
  ignore_persist:
    description:
      - The HA Proxy Backend Ignore Persists
    required: false
    type: dict
  abortonclose:
    description:
      - The HA Proxy Backend Abord On Close
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  accept_invalid_http_response:
    description:
      - The HA Proxy Backend Accept Invalid HTTP Response
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  allbackups:
    description:
      - The HA Proxy Backend All Backup
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  checkcache:
    description:
      - The HA Proxy Backend Check Cache
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  external_check:
    description:
      - The HA Proxy Backend External Check
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  nolinger:
    description:
      - The HA Proxy Backend No Linger
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  prefer_last_server:
    description:
      - The HA Proxy Backend Prefer Last Server
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  splice_auto:
    description:
      - The HA Proxy Backend Splice Automatically
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  splice_request:
    description:
      - The HA Proxy Backend Splice Request
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  splice_response:
    description:
      - The HA Proxy Backend Splice Response
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  spop_check:
    description:
      - The HA Proxy Backend Spop Check
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  srvtcpka:
    description:
      - The HA Proxy Backend Server TCP KA
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  independent_streams:
    description:
      - The HA Proxy Backend Independant Stream
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  log_health_checks:
    description:
      - The HA Proxy Backend Log Health
    required: false
    choices: ['ENABLED', 'DISABLED']
    type: str
  bind_process:
    description:
      - The HA Proxy Backend for bind_process
    required: false
    type: str
  check_timeout:
    description:
      - The HA Proxy Backend for check_timeout
    required: false
    type: int
  connect_timeout:
    description:
      - The HA Proxy Backend for connect_timeout
    required: false
    type: int
  description:
    description:
      - The HA Proxy Backend for description
    required: false
    type: str
  disabled:
    description:
      - The HA Proxy Backend for disabled
    required: false
    type: bool
  enabled:
    description:
      - The HA Proxy Backend for enabled
    required: false
    type: bool
  external_check_command:
    description:
      - The HA Proxy Backend for external_check_command
    required: false
    type: str
  external_check_path:
    description:
      - The HA Proxy Backend for external_check_path
    required: false
    type: str
  fullconn:
    description:
      - The HA Proxy Backend for fullconn
    required: false
    type: int
  queue_timeout:
    description:
      - The HA Proxy Backend for queue_timeout
    required: false
    type: int
  retries:
    description:
      - The HA Proxy Backend for retries
    required: false
    type: int
  retry_on:
    description:
      - The HA Proxy Backend for retry_on
    required: false
    type: str
  server_fin_timeout:
    description:
      - The HA Proxy Backend for server_fin_timeout
    required: false
    type: int
  server_state_file_name:
    description:
      - The HA Proxy Backend for server_state_file_name
    required: false
    type: str
  server_timeout:
    description:
      - The HA Proxy Backend for server_timeout
    required: false
    type: int
  srvtcpka_cnt:
    description:
      - The HA Proxy Backend for srvtcpka_cnt
    required: false
    type: int
  srvtcpka_idle:
    description:
      - The HA Proxy Backend for srvtcpka_idle
    required: false
    type: int
  srvtcpka_intvl:
    description:
      - The HA Proxy Backend for srvtcpka_intvl
    required: false
    type: int
  forwardfor:
    description:
      - The HA Proxy Backend Forwarded For
    required: false
    type: dict
  stats_options:
    description:
      - The HA Proxy Backend Stats Options
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
      - The Transaction State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Create HA Proxy Backend"
  kube_cloud.haproxy.backend:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jira-backend-service"
    mode: 'HTTP'
    adv_check: 'HTTPCHK'
    balance:
      algorithm: roundrobin
      hdr_use_domain_only: false
      uri_path_only: false
      uri_whole: true
    httpchk_params:
      method: GET
      uri: "/login"
      version: "HTTP/1.1"
    transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
    state: 'present'

- name: "Create HA Proxy Backend"
  kube_cloud.haproxy.backend:
    base_url: "http://localhost:5555"
    username: "admin"
    password: "admin"
    api_version: "v2"
    name: "jira-backend-service"
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.haproxy.client_backends import BackendClient
from ...module_utils.haproxy.client import haproxy_client
from ...module_utils.haproxy.models import Balance, Backend, HttpHealthCheck, HttpCheckParams
from ...module_utils.haproxy.models import ForwardFor, PostgresSqlCheckParams, StatsOptions, StatsAuth
from ...module_utils.haproxy.enums import ProxyProtocol, LoadBalancingAlgorithm, HealthCheckType
from ...module_utils.haproxy.enums import MatchType, TimeoutStatus, ErrorStatus, OkStatus, HttpMethod
from ...module_utils.haproxy.enums import AdvancedHealthCheckType, EnableDisableEnum, ConditionType
from ...module_utils.haproxy.commons import filter_none

try:
    from requests import HTTPError  # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return Backend
def get_backend(client: BackendClient, name: str):

    try:

        # Call Client
        return client.get_backend(name=name)

    except HTTPError:

        # Return None
        return None


# Update Backend
def update_backend(module: AnsibleModule, client: BackendClient, transaction_id: str, name: str, backend: Backend, force_reload: bool):

    try:

        # Call Client
        return client.update_backend(
            name=name,
            backend=backend,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Backend] - Failed Update HA Proxy Backend (Name : {0} : [{1}]): {2}".format(
                name,
                backend,
                api_error
            )
        )


# Create Backend
def create_backend(module: AnsibleModule, client: BackendClient, transaction_id: str, backend: Backend, force_reload: bool):

    try:

        # Call Client
        return client.create_backend(
            backend=backend,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Backend] - Failed Create HA Proxy Backend (Name : {0} : [{1}]): {2}".format(
                backend.name,
                backend,
                api_error
            )
        )


# Delete Backend
def delete_backend(module: AnsibleModule, client: BackendClient, transaction_id: str, name: str, force_reload: bool):

    try:

        # Call Client
        return client.delete_backend(
            name=name,
            transaction_id=transaction_id,
            force_reload=force_reload
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Backend] - Failed Delete HA Proxy Backend (Name : {0}): {1}".format(
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
        api_version=dict(type='str', required=False, default='v2'),
        name=dict(type='str', required=True),
        mode=dict(type='str', required=False, default='HTTP', choices=ProxyProtocol.names()),
        adv_check=dict(type='str', required=False, choices=AdvancedHealthCheckType.names()),
        balance=dict(type='dict', required=False, default=None),
        httpchk=dict(type='dict', required=False, default=None),
        httpchk_params=dict(type='dict', required=False, default=None),
        pgsql_check_params=dict(type='dict', required=False, default=None),
        ignore_persist=dict(type='dict', required=False, default=None),
        abortonclose=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        accept_invalid_http_response=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        allbackups=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        checkcache=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        external_check=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        nolinger=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        prefer_last_server=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        splice_auto=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        splice_request=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        splice_response=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        spop_check=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        srvtcpka=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        independent_streams=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        log_health_checks=dict(type='str', required=False, choices=EnableDisableEnum.names()),
        bind_process=dict(type='str', required=False),
        check_timeout=dict(type='int', required=False),
        connect_timeout=dict(type='int', required=False),
        description=dict(type='str', required=False),
        disabled=dict(type='bool', required=False),
        enabled=dict(type='bool', required=False),
        external_check_command=dict(type='str', required=False),
        external_check_path=dict(type='str', required=False),
        fullconn=dict(type='int', required=False),
        queue_timeout=dict(type='int', required=False),
        retries=dict(type='int', required=False),
        retry_on=dict(type='str', required=False),
        server_fin_timeout=dict(type='int', required=False),
        server_state_file_name=dict(type='str', required=False),
        server_timeout=dict(type='int', required=False),
        srvtcpka_cnt=dict(type='int', required=False),
        srvtcpka_idle=dict(type='int', required=False),
        srvtcpka_intvl=dict(type='int', required=False),
        forwardfor=dict(type='dict', required=False, default=None),
        stats_options=dict(type='dict', required=False, default=None),
        transaction_id=dict(type='str', required=False, default=''),
        force_reload=dict(type='bool', required=False, default=True),
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


# Build Requested Backend from Configuration
def build_requested_backend(params: dict) -> Backend:

    # Base Parameters Name
    base_param_names = [
        "name", "bind_process", "check_timeout", "connect_timeout",
        "description", "disabled", "enabled", "external_check_command",
        "external_check_path", "fullconn", "queue_timeout", "retries",
        "retry_on", "server_fin_timeout", "server_state_file_name",
        "server_timeout", "srvtcpka_cnt", "srvtcpka_idle", "srvtcpka_intvl",
    ]

    # Build Requested Instance
    backend = Backend(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Optional Initialization : mode
    backend.mode = ProxyProtocol.create(params['mode'])
    backend.adv_check = AdvancedHealthCheckType.create(params.get('adv_check', None))
    backend.abortonclose = EnableDisableEnum.create(params.get('abortonclose', None))
    backend.accept_invalid_http_response = EnableDisableEnum.create(params.get('accept_invalid_http_response', None))
    backend.allbackups = EnableDisableEnum.create(params.get('allbackups', None))
    backend.checkcache = EnableDisableEnum.create(params.get('checkcache', None))
    backend.external_check = EnableDisableEnum.create(params.get('external_check', None))
    backend.nolinger = EnableDisableEnum.create(params.get('nolinger', None))
    backend.prefer_last_server = EnableDisableEnum.create(params.get('prefer_last_server', None))
    backend.splice_auto = EnableDisableEnum.create(params.get('splice_auto', None))
    backend.splice_request = EnableDisableEnum.create(params.get('splice_request', None))
    backend.splice_response = EnableDisableEnum.create(params.get('splice_response', None))
    backend.spop_check = EnableDisableEnum.create(params.get('spop_check', None))
    backend.srvtcpka = EnableDisableEnum.create(params.get('srvtcpka', None))
    backend.independent_streams = EnableDisableEnum.create(params.get('independent_streams', None))
    backend.log_health_checks = EnableDisableEnum.create(params.get('log_health_checks', None))

    # Optional Initialization : balance
    if params.get('balance', None) is not None:

        # Extract balance
        p_balance = params['balance']

        # Initialize Object
        backend.balance = Balance(
            algorithm=LoadBalancingAlgorithm.create(p_balance.get('algorithm', None)),
            hash_expression=p_balance.get('hash_expression', None),
            hdr_name=p_balance.get('hdr_name', None),
            hdr_use_domain_only=p_balance.get('hdr_use_domain_only', None),
            random_draws=p_balance.get('random_draws', None),
            rdp_cookie_name=p_balance.get('rdp_cookie_name', None),
            uri_depth=p_balance.get('uri_depth', None),
            uri_len=p_balance.get('uri_len', None),
            uri_path_only=p_balance.get('uri_path_only', None),
            uri_whole=p_balance.get('uri_whole', None),
            url_param=p_balance.get('url_param', None),
            url_param_check_post=p_balance.get('url_param_check_post', None),
            url_param_max_wait=p_balance.get('url_param_max_wait', None)
        )

    # Optional Initialization : httpchk
    if params.get('httpchk', None) is not None:

        # Extract httpchk
        p_httpchk = params['httpchk']

        # Initialize Object
        backend.adv_check = AdvancedHealthCheckType.HTTPCHK
        backend.httpchk = HttpHealthCheck(
            type=HealthCheckType.create(p_httpchk.get('type', None)),
            method=p_httpchk.get('method', None),
            uri=p_httpchk.get('uri', None),
            uri_log_format=p_httpchk.get('uri_log_format', None),
            var_expr=p_httpchk.get('var_expr', None),
            var_format=p_httpchk.get('var_format', None),
            var_name=p_httpchk.get('var_name', None),
            var_scope=p_httpchk.get('var_scope', None),
            version=p_httpchk.get('version', None),
            via_socks4=p_httpchk.get('via_socks4', None),
            port=p_httpchk.get('port', None),
            port_string=p_httpchk.get('port_string', None),
            proto=p_httpchk.get('proto', None),
            send_proxy=p_httpchk.get('send_proxy', None),
            sni=p_httpchk.get('sni', None),
            ssl=p_httpchk.get('ssl', None),
            status_code=p_httpchk.get('status_code', None),
            tout_status=TimeoutStatus.create(p_httpchk.get('tout_status', None)),
            match=MatchType.create(p_httpchk.get('match', None)),
            headers=p_httpchk.get('headers', None),
            body=p_httpchk.get('body', None),
            body_log_format=p_httpchk.get('body_log_format', None),
            check_comment=p_httpchk.get('check_comment', None),
            default=p_httpchk.get('default', None),
            error_status=ErrorStatus.create(p_httpchk.get('error_status', None)),
            ok_status=OkStatus.create(p_httpchk.get('ok_status', None))
        )

    # Optional Initialization : httpchk_params
    if params.get('httpchk_params', None) is not None:

        # Extract httpchk_params
        p_httpchk_params = params['httpchk_params']

        # Initialize Object
        backend.adv_check = AdvancedHealthCheckType.HTTPCHK
        backend.httpchk_params = HttpCheckParams(
            method=HttpMethod.create(p_httpchk_params.get('method', None)),
            uri=p_httpchk_params.get('uri', None),
            version=p_httpchk_params.get('version', None)
        )

    # Optional Initialization : pgsql_check_params
    if params.get('pgsql_check_params', None) is not None:

        # Extract pgsql_check_params
        p_pgsql_check_params = params['pgsql_check_params']

        # Initialize Object
        backend.adv_check = AdvancedHealthCheckType.PGSQL_CHECK
        backend.pgsql_check_params = PostgresSqlCheckParams(
            username=p_pgsql_check_params.get('username', None)
        )

    # Optional Initialization : forwardfor
    if params.get('forwardfor', None) is not None:

        # Extract ForwardedFor
        p_formwardfor = params['forwardfor']

        # Initialize Object
        backend.forwardfor = ForwardFor(
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
        backend.stats_options = StatsOptions(
            **{k: v for k, v in p_stats_options.items() if v is not None and k in stats_base_param_names}
        )

        # Initialize Admin Condition
        backend.stats_options.stats_admin_cond = ConditionType.create(
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
            backend.stats_options.stats_auths = stats_auths

    # Return Backend
    return backend


# Porcess Module Execution
def run_module(module: AnsibleModule, client: BackendClient):

    # Extract Trasaction ID
    transaction_id = module.params['transaction_id']

    # Extract State
    state = module.params['state']

    # Extract Force Reload
    force_reload = module.params['force_reload']

    # Build Requested Instance
    backend = build_requested_backend(module.params)

    # Find Existing Instance
    existing_backend = get_backend(
        client=client,
        name=backend.name
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_backend and state == 'present':

        # If Existing Instance match requested Instance
        if existing_backend == backend:

            # Initialize response (No Change)
            module.exit_json(
                msg="Backend [{0} - {1}] Not Changed".format(backend.name, backend.mode),
                instance=filter_none(backend),
                changed=False
            )

        # Update Existing Instance
        update_backend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=backend.name,
            backend=backend,
            force_reload=force_reload
        )

        # Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(backend),
            msg="Backend [{0} - {1}] Has Been Updated".format(backend.name, backend.mode)
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_backend and state == 'present':

        # Create Instance
        create_backend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            backend=backend,
            force_reload=force_reload
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=filter_none(backend),
            msg="[{0} - {1}] Has been Created".format(backend.name, backend.mode)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_backend and state == 'absent':

        # Delete Instance
        delete_backend(
            module=module,
            client=client,
            transaction_id=transaction_id,
            name=backend.name,
            force_reload=force_reload
        )

        # Exit Module
        module.exit_json(
            msg="[{0} - {1}] Has been Deleted".format(backend.name, backend.mode),
            instance=filter_none(backend),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0} - {1}] Not Found".format(backend.name, backend.mode),
            instance=filter_none(backend),
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
