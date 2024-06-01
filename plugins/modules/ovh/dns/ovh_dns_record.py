#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: ovh_dns_record
version_added: "1.0.0"
short_description: Manage DNS zone records
description:
    - Used to Manage DNS Record on OVH Cloud
    - Manage All Kind of record
requirements:
    - ovh >= 0.5.0
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
    endpoint:
        description:
            - The OVH API Endpoint
        required: true
        type: str
    application_key:
        description:
            - The OVH API Application Key
        required: true
        type: str
    application_secret:
        description:
            - The OVH API Application Secret
        required: true
        type: str
    consumer_key:
        description:
            - The OVH API Consumer Key
        required: true
        type: str
    domain:
        description:
            - The targeted domain
        required: true
        type: str
    target:
        description:
            - The value of the record
            - It can be an IP, a FQDN, a text...
        required: true
        type: str
    record_name:
        description:
            - The name of record to add or delete in the zone
        required: true
        type: str
    record_type:
        description:
            - The DNS record type
        choices: ['A', 'AAAA', 'CAA', 'CNAME', 'DKIM', 'DMARC', 'DNAME', 'LOC', 'MX', 'NAPTR', 'NS', 'PTR', 'SPF', 'SRV', 'SSHFP', 'TLSA', 'TXT']
        default: A
        type: str
    state:
        description:
            - Wether to add or delete the record
        required: false
        default: present
        choices: ['present', 'absent']
        type: str
    ttl:
        description:
            - TTL associated with the DNS record
        required: false
        default: 3600
        type: int
'''

EXAMPLES = r'''
- name: "Create TXT Entrty to OVH"
  kubecloud.general.ovh.dns.ovh_dns_record:
    endpoint: "ovh-eu"
    application_key: "2566789999999999"
    application_secret: "me4567009132467nhst5"
    consumer_key: "po230O851Ujjhr3"
    domain: "kube-cloud.com"
    record_name: "demo.test"
    record_type: "TXT"
    target: "VALUE TO SET"
    state: 'present'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.kubecloud.general.plugins.module_utils.ovh import ovh_client


try:
    from ovh.exceptions import APIError
    HAS_OVH = True
except ImportError:
    HAS_OVH = False


# Porcess Module Execution
def run_module():

    # Build Module Arguments Specification
    module_specification = dict(
        endpoint=dict(type='str', required=True),
        application_key=dict(type='str', required=True, no_log=True),
        application_secret=dict(type='str', required=True, no_log=True),
        consumer_key=dict(type='str', required=True, no_log=True),
        domain=dict(type='str', required=True),
        record_name=dict(type='str', required=True),
        record_type=dict(type='str', default='A', choices=[
            'A', 'AAAA', 'CAA', 'CNAME', 'DKIM', 'DMARC', 'DNAME', 'LOC',
            'MX', 'NAPTR', 'NS', 'PTR', 'SPF', 'SRV', 'SSHFP', 'TLSA', 'TXT'
        ]),
        target=dict(type='str', required=True),
        ttl=dict(type='int', default=3600),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )

    # Build ansible Module
    module = AnsibleModule(
        argument_spec=module_specification,
        supports_check_mode=True
    )

    # If Check Mode Enabled
    if module.check_mode:
        result['changed'] = True
        module.exit_json(**result)

    # Build OVH Client from Module
    client = ovh_client(module)

    # Extract Module Parameters
    domain = module.params['domain']
    record_name = module.params['record_name']
    record_type = module.params['record_type']
    target = module.params['target']
    ttl = module.params['ttl']
    state = module.params['state']

    # OVH Record URI
    ovh_record_uri = "/domain/zone/{0}/record/{1}"

    # OVH Zone Refresh URI
    ovh_zone_refresh_uri = "/domain/zone/{0}/refresh"

    try:

        # Find OVH Account Domain
        available_domains = client.get('/domain/zone')

        # If Module domain is not managed on OVH Account
        if domain not in available_domains:

            # Set Module Error
            module.fail_json(msg="The target domain [{0}] is unknown".format(domain))

    except APIError as api_error:

        # Set Module Error
        module.fail_json(msg="[Find Zone] - Failed to call OVH API (/domain/zone) : {0}".format(api_error))

    try:

        # Find if Target record Name already exists
        existing_records = client.get(
            "/domain/zone/{0}/record".format(domain),
            fieldType=record_type,
            subDomain=record_name
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(msg="[Find Record] - Failed to call OVH API (/domain/zone/{0}/record) for record [{1}]: {2}".format(domain, record_name, api_error))

    # Requested State is 'present'
    if state == 'present':

        # If There are records summaries in previous response array
        if len(existing_records) >= 1:

            # Iterate on each array entries
            for index in existing_records:

                try:

                    # Get Current Entry Details
                    record = client.get(
                        ovh_record_uri.format(domain, index)
                    )

                    # If Entry match requested record name and target
                    if record['target'] == target or record['ttl'] == ttl:

                        # Initialize response (No Change)
                        module.exit_json(
                            msg="[{0} {1}.{2}] Not Changed".format(record_type, record_name, domain),
                            changed=False
                        )

                    else:

                        # Create record
                        result = client.put(
                            ovh_record_uri.format(domain, index),
                            fieldType=record_type,
                            subDomain=record_name,
                            target=target,
                            ttl=ttl
                        )

                        # Refresh Domain
                        client.post(
                            ovh_zone_refresh_uri.format(domain)
                        )

                        # Initialize Module Response : Changed
                        module.exit_json(
                            changed=True,
                            msg="[{0} {1}.{2}] Has been Updated".format(record_type, record_name, domain)
                        )

                except APIError as api_error:

                    # Set Module Error
                    module.fail_json(
                        msg="Failed to call OVH API: {0}".format(api_error)
                    )
        else:

            # Create record
            result = client.post(
                "/domain/zone/{0}/record".format(domain),
                fieldType=record_type,
                subDomain=record_name,
                target=target,
                ttl=ttl
            )

            # Refresh Domain
            client.post(
                ovh_zone_refresh_uri.format(domain)
            )

            # Initialize Module Response : Changed
            module.exit_json(
                changed=True,
                msg="[{0} {1}.{2}] Has been Created".format(record_type, record_name, domain),
                **result
            )

    else:

        # If Record not exists
        if not existing_records:

            # Initialize Response : No Change
            module.exit_json(
                msg="[{0} {1}.{2}] Not Found".format(record_type, record_name, domain),
                changed=False
            )

        # Initialize Deleted Record Array
        record_deleted = []

        try:

            # Iterate on existing record entries
            for index in existing_records:

                # Get Current Record Details
                record = client.get(
                    ovh_record_uri.format(domain, index)
                )

                # Delete Current Record
                client.delete(
                    ovh_record_uri.format(domain, index)
                )

                # Append Record to the Deleted Records Array
                record_deleted.append("%s IN %s %s" % (
                    record.get('subDomain'),
                    record.get('fieldType'),
                    record.get('target')
                ))

            # Refresh Domain
            client.post(
                ovh_zone_refresh_uri.format(domain)
            )

            # Exit Module
            module.exit_json(
                msg="[{0} {1}.{2}] Has been Deleted".format(record_type, record_name, domain),
                changed=True
            )

        except APIError as api_error:

            # Set Module Error
            module.fail_json(msg="Failed to call OVH API: {0}".format(api_error))


# Entrypoint Function
def main():

    # Execute Module
    run_module()


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
