
**************************
kube_cloud.haproxy.transaction
**************************

**Validate and Cancel HA Proxy Dataplane API Transaction.**

Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

Synopsis
--------
- Validate and Cancel HA Proxy Dataplane API Transaction.

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
            <td colspan="1">force_reload</td>
            <td>bool</td>
            <td>No</td>
            <td>
                <ul style="margin: 0; padding: 0"><b>Choices:</b>
                    <li><b>true</b></li>
                    <li>false</li>
                </ul>
            </td>
            <td>true</td>
            <td>HA Proxy Dataplane API Transaction Forcing reload config after Commit</td>
        </tr>
        <tr>
            <td colspan="1">state</td>
            <td>str</td>
            <td>No</td>
            <td>
                <ul style="margin: 0; padding: 0"><b>Choices:</b>
                    <li><b>committed</b></li>
                    <li>cancelled</li>
                </ul>
            </td>
            <td>committed</td>
            <td>HA Proxy Dataplane API Transaction Management (Commit or Cancel)</td>
        </tr>
    </table>

Examples
--------

.. code-block:: yaml

    - name: "Commit HA Proxy Backend"
      kube_cloud.general.haproxy.transaction:
        base_url: "http://localhost:5555"
        username: "admin"
        password: "admin"
        api_version: "v2"
        transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
        force_reload: true
        state: 'committed'

    - name: "Create HA Proxy Backend"
      kube_cloud.general.haproxy.transaction:
        base_url: "http://localhost:5555"
        username: "admin"
        password: "admin"
        api_version: "v2"
        transaction_id: "88a7601b-6960-4263-873f-b5e3040c80a2"
        state: 'cancelled'

Authors
~~~~~~~

- Jean-Jacques ETUNE NGI (jetune@kube-cloud.com)
