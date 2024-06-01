from __future__ import (absolute_import, division, print_function)
from ansible_collections.kubecloud.general.plugins.modules.ovh.dns.ovh_dns_record import run_module
from ansible.module_utils.basic import AnsibleModule
import pytest

try:
    import ovh
    from ovh.exceptions import APIError
    HAS_OVH = True
except ImportError:
    HAS_OVH = False


__metaclass__ = type


@pytest.fixture
def mock_module(mocker):

    # Build and Return Mocked nsible Main Module
    return mocker.patch('ansible.module_utils.basic.AnsibleModule')


@pytest.fixture
def mock_ovh_client(mocker):

    # Build and Return Mocked nsible Main Module
    return mocker.patch('ovh.Client')


# Test ADD Record
def test_ovh_dns_record_add(mock_module:AnsibleModule, mock_client:ovh.Client):

    # Simule les arguments passés au module
    mock_module.return_value.params = {
        "endpoint": "ovh-eu",
        "application_key": "fake_key",
        "application_secret": "fake_secret",
        "consumer_key": "fake_consumer",
        "domain": 'kube-cloud.com',
        "record_type": "A",
        "record_name": "ovpn",
        "target": "192.0.2.1",
        "state": "present"
    }

    # Execute Module
    run_module(mock_module, mock_client)

    # Assert on result
    mock_module.return_value.exit_json.assert_called_once_with(changed=True)


# Test Remove Record
def test_ovh_dns_record_remove(mock_module:AnsibleModule, mock_client:ovh.Client):
    mock_module.return_value.params = {
        "endpoint": "ovh-eu",
        "application_key": "fake_key",
        "application_secret": "fake_secret",
        "consumer_key": "fake_consumer",
        "domain": 'kube-cloud.com',
        "record_type": "A",
        "record_name": "ovpn",
        "target": "192.0.2.1",
        "state": "absent"
    }

    # Execute Module
    run_module(mock_module, mock_client)

    # Assert on result
    mock_module.return_value.exit_json.assert_called_once_with(changed=True)
