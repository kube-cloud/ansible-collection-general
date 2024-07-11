
**************************
kube_cloud.general.haproxy.backend
**************************

**Install and Configure HA Proxy on Linux Based OS.**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------
- Install and Configure HA Proxy.

Requirements
------------
The below requirements are needed on the host that executes this module.

- community.general: 4.0.0+

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th colspan="1">Type</th>
            <th colspan="1">Required</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th colspan="1">Example</th>
            <th width="100%">Description</th>
        </tr>
        <tr>
            <td colspan="1">base_url</td>
            <td>str</td>
            <td>Yes</td>
            <td></td>
            <td>http://localhost:5555</td>
            <td>HA Proxy Dataplane API Base URL</td>
        </tr>
        <tr>
            <td colspan="1">username</td>
            <td>str</td>
            <td>Yes</td>
            <td></td>
            <td>admin</td>
            <td>HA Proxy Dataplane API Administrator Username</td>
        </tr>
        <tr>
            <td colspan="1">password</td>
            <td>str</td>
            <td>Yes</td>
            <td></td>
            <td>admin</td>
            <td>HA Proxy Dataplane API Administrator Password</td>
        </tr>
        <tr>
            <td colspan="1">api_version</td>
            <td>str</td>
            <td>No</td>
            <td>v2</td>
            <td>v1</td>
            <td>HA Proxy Dataplane API Version</td>
        </tr>
        <tr>
            <td colspan="1">transaction_id</td>
            <td>str</td>
            <td>No</td>
            <td></td>
            <td>88a7601b-6960-4263-873f-b5e3040c80a2</td>
            <td>HA Proxy Dataplane API Transaction (if your operation is embedded in existing TX)</td>
        </tr>
        <tr>
            <td colspan="1">name</td>
            <td>str</td>
            <td>Yes</td>
            <td></td>
            <td>jenkins-backend-service</td>
            <td>HA Proxy Backend Name</td>
        </tr>
        <tr>
            <td colspan="1">mode</td>
            <td>str</td>
            <td>Yes</td>
            <td>
                <ul style="margin: 0; padding: 0"><b>Choices:</b>
                    <li><b>HTTP</b></li>
                    <li>TCP</li>
                </ul>
            </td>
            <td>HTTP</td>
            <td>HA Proxy Backend Mode</td>
        </tr>
        <tr>
            <td colspan="1">balance</td>
            <td>dict</td>
            <td>No</td>
            <td></td>
            <td>
                <pre>
                    <code>
    balance:
        algorithm: roundrobin
        hdr_use_domain_only: false
        uri_path_only: false
        uri_whole: true
                    </code>
                </pre>
            </td>
            <td>HA Proxy Backend Balancing Configuration</td>
        </tr>
        <tr>
            <td colspan="1">httpchk_params</td>
            <td>dict</td>
            <td>No</td>
            <td></td>
            <td>
                <pre>
                    <code>
    httpchk_params:
        method: GET
        uri: "/login"
        version: "HTTP/1.1"
                    </code>
                </pre>
            </td>
            <td>HA Proxy Backend Inline HTTP Healtcheck Configuration</td>
        </tr>
        <tr>
            <td colspan="1">httpchk</td>
            <td>dict</td>
            <td>No</td>
            <td></td>
            <td>
                <pre>
                    <code>
    http_health_check:
        type: "http"
        method: "GET"
        uri: "/health"
        uri_log_format: "%[req.hdr(Host)]%[url]"
        var_expr: "some_expression"
        var_format: "some_format"
        var_name: "some_variable"
        var_scope: "some_scope"
        version: "HTTP/1.1"
        via_socks4: false
        port: 80
        port_string: "8080"
        proto: "HTTP"
        send_proxy: true
        sni: "example.com"
        ssl: true
        status_code: "200"
        tout_status: "L7TOUT"
        match: "status"
        headers:
            - name: "Host"
            value: "example.com"
            - name: "User-Agent"
            value: "haproxy"
        body: "Expected response body"
        body_log_format: "%[res.body]"
        check_comment: "Health check"
        default: false
        error_status: "L7RSP"
        addr: "192.168.1.1"
        ok_status: "L7OK"
                    </code>
                </pre>
            </td>
            <td>HA Proxy Backend Server HTTP Healtcheck Configuration</td>
        </tr>
        <tr>
            <td colspan="1">state</td>
            <td>str</td>
            <td>No</td>
            <td>
                <ul style="margin: 0; padding: 0"><b>Choices:</b>
                    <li><b>present</b></li>
                    <li>absent</li>
                </ul>
            </td>
            <td>committed</td>
            <td>HA Proxy Dataplane API Transaction Management (Commit or Cancel)</td>
        </tr>
    </table>

Examples
--------

.. code-block:: yaml

    - name: "Create HA Proxy Backend"
      kube_cloud.general.haproxy.backend:
        base_url: "http://localhost:5555"
        username: "admin"
        password: "admin"
        api_version: "v2"
        name: "jira-backend-service"
        mode: 'HTTP'
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
      kube_cloud.general.haproxy.backend:
        base_url: "http://localhost:5555"
        username: "admin"
        password: "admin"
        api_version: "v2"
        name: "jira-backend-service"
        mode: 'HTTP'
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
        state: 'absent'


Authors
~~~~~~~

- Jean-Jacques ETUNE NGI (jetune@kube-cloud.com)
