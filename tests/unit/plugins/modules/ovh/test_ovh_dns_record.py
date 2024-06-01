from __future__ import (absolute_import, division, print_function)
from ansible_collections.kubecloud.general.plugins.modules.ovh.dns.ovh_dns_record import run_module
from ansible.module_utils.basic import AnsibleModule
from mock import patch


__metaclass__ = type


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


# Test Domain
ZONE = "kube-cloud.com"


# Test Record Type
RECORD_TYPE = "A"


# Test Record Name
RECORD_NAME = "demo.test"


# Test Record Value
RECORD_VALUE = "172.16.2.10"


# Test Record TTL
RECORD_TTL = 60


# Test Record ID
RECORD_ID = "1"


# Configure le retour de la méthode get pour les paramètres spécifiques
def mock_ovh_client_get(url, **kwargs):
    if url == OVH_ZONE_URI:
        return [ZONE]
    if url == GET_OVH_RECORD_ID_URI.format(ZONE) and kwargs == {'fieldType': RECORD_TYPE, 'subDomain': RECORD_NAME}:
        return [RECORD_ID]
    if url == OVH_RECORD_URI.format(ZONE, RECORD_ID):
        return {"target": RECORD_VALUE, "ttl": RECORD_TTL}
    return {}


# Test ADD Record
def test_ovh_dns_record_add(mocker):

    # Ansible Module Mock
    mock_module = mocker.patch("ansible.module_utils.basic.AnsibleModule")

    # OVH Client Mock
    mock_client = mocker.patch("ovh.Client")

    # Simule les arguments passés au module
    mock_module.return_value.params = {
        "endpoint": "ovh-eu",
        "application_key": "fake_key",
        "application_secret": "fake_secret",
        "consumer_key": "fake_consumer",
        "domain": ZONE,
        "record_type": RECORD_TYPE,
        "record_name": RECORD_NAME,
        "target": RECORD_VALUE,
        "ttl": RECORD_TTL,
        "state": "present"
    }

    # Configure Clien Mock
    mock_client.get.side_effect = mock_ovh_client_get

    # Execute Module
    run_module(mock_module, mock_client)

    # Assert on result
    mock_module.return_value.exit_json.assert_called_once_with(changed=False)
