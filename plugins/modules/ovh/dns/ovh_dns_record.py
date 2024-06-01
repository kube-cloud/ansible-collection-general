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
    import ovh
    from ovh.exceptions import APIError
    HAS_OVH = True
except ImportError:
    HAS_OVH = False


# OVH Zone URI
OVH_ZONE_URI = "/domain/zone"


# Zone Refresh URI
OVH_ZONE_REFRESH_URI = "/domain/zone/{0}/refresh"


# OVH Record Resource URI
OVH_RECORD_URI = "/domain/zone/{0}/record/{1}"


# OVH Record Creation Resource URI
CREATE_OVH_RECORD_URI = "/domain/zone/{0}/record"


# OVH Record ID Resource URI
GET_OVH_RECORD_ID_URI = "/domain/zone/{0}/record"


# Instantiate Ansible Module
def build_ansible_module():

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
    return AnsibleModule(
        argument_spec=module_specification,
        supports_check_mode=True
    )


# Check OVH Zone
def check_ovh_zone(module, client, zone_name):

    try:

        # Find OVH Account Domain
        available_domains = client.get(OVH_ZONE_URI)

        # If Module domain is not managed on OVH Account
        if zone_name not in available_domains:

            # Set Module Error
            module.fail_json(msg="The target domain [{0}] is unknown".format(zone_name))

    except APIError as api_error:

        # Set Module Error
        module.fail_json(msg="[Find Zone] - Failed to call OVH API (GET /domain/zone) : {0}".format(api_error))


# Refresh OVH Zone
def refresh_ovh_zone(module, client, zone_name):

    try:

        # Refresh Domain
        client.post(
            OVH_ZONE_REFRESH_URI.format(zone_name)
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(msg="[Refresh Zone] - Failed to call OVH API (POST /domain/zone/{0}/refresh) : {1}".format(zone_name, api_error))


# Find and Return OVH Record ID List
def get_ovh_record_id(module, client, domain, record_name, record_type):

    try:

        # Find if Target record Name already exists
        return client.get(
            GET_OVH_RECORD_ID_URI.format(domain),
            fieldType=record_type,
            subDomain=record_name
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(msg="[Find Record] - Failed to call OVH API (GET /domain/zone/{0}/record) for record [{1}]: {2}".format(domain, record_name, api_error))


# Find and Return OVH Record
def get_ovh_record(module, client, domain, record_id):

    try:

        # Get Current Entry Details
        return client.get(
            OVH_RECORD_URI.format(domain, record_id)
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Find Record] - Failed to call OVH API (GET /domain/zone/{0}/record/{1}) : {2}".format(domain, record_id, api_error)
        )


# Find and Return OVH Record
def create_ovh_record(
        module,
        client,
        domain,
        record_id,
        record_name,
        record_type,
        record_value,
        ttl):

    try:

        # Create record
        client.post(
            CREATE_OVH_RECORD_URI.format(domain),
            fieldType=record_type,
            subDomain=record_name,
            target=record_value,
            ttl=ttl
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Create Record] - Failed to call OVH API (POST /domain/zone/{0}/record/{1}) : {2}".format(domain, record_id, api_error)
        )


# Find and Return OVH Record
def update_ovh_record(module,
                    client,
                    domain,
                    record_id,
                    record_name,
                    record_type,
                    record_value,
                    ttl):

    try:

        # Update record
        client.put(
            OVH_RECORD_URI.format(domain, record_id),
            fieldType=record_type,
            subDomain=record_name,
            target=record_value,
            ttl=ttl
        )

    except APIError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Update Record] - Failed to call OVH API (PUT /domain/zone/{0}/record/{1}) : {2}".format(domain, record_id, api_error)
        )


# Delete OVH Record
def delete_ovh_record(module, client, domain, record_id):

    try:

        # Delete record
        client.delete(OVH_RECORD_URI.format(domain, record_id))

    except APIError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Record] - Failed to call OVH API (PUT /domain/zone/{0}/record/{1}) : {2}".format(domain, record_id, api_error)
        )


# Porcess Module Execution
def run_module(module, client):

    # Extract Module Parameters
    domain = module.params['domain']
    record_name = module.params['record_name']
    record_type = module.params['record_type']
    target = module.params['target']
    ttl = module.params['ttl']
    state = module.params['state']

    # Find OVH Domain
    check_ovh_zone(module, client, domain)

    # Find Existing Record IDs
    existing_records = get_ovh_record_id(module, client, domain, record_name, record_type)
    
    # If Requested State is 'present' and Record exists
    if state == 'present' and len(existing_records) >= 1:

        # Record ID
        record_id = existing_records[0]

        # Get Current Entry Details
        record = get_ovh_record(module, client, domain, record_id)

        # If Entry match requested record name and target
        if record['target'] == target and record['ttl'] == ttl:

            # Initialize response (No Change)
            module.exit_json(
                msg="[{0} {1}.{2}] Not Changed".format(record_type, record_name, domain),
                changed=False
            )

        # Update Record
        update_ovh_record(module, client, domain, record_id, record_name, record_type, target, ttl)

        # refresh Zone
        refresh_ovh_zone(module, client, domain)

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            msg="[{0} {1}.{2}] Has been Updated".format(record_type, record_name, domain)
        )

    # If Requested State is 'present' and Record don't exists
    if state == 'present' and not existing_records:

        # Create Record
        create_ovh_record(module, client, domain, record_id, record_name, record_type, target, ttl)

        # refresh Zone
        refresh_ovh_zone(module, client, domain)

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            msg="[{0} {1}.{2}] Has been Created".format(record_type, record_name, domain)
        )

    # If Requested State is 'absent' and Record exists
    if state == 'absent' and len(existing_records) >= 1:

        # Delete Record
        delete_ovh_record(module, client, domain, existing_records[0])

        # refresh Zone
        refresh_ovh_zone(module, client, domain)

        # Exit Module
        module.exit_json(
            msg="[{0} {1}.{2}] Has been Deleted".format(record_type, record_name, domain),
            changed=True
        )

    # If Requested State is 'absent' and Record don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0} {1}.{2}] Not Found".format(record_type, record_name, domain),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build OVH Client from Module
    client = ovh_client(module)

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
