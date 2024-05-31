from __future__ import (absolute_import, division, print_function)

import pytest

from ansible_collections.kubecloud.general.plugins.modules.ovh.dns.ovh_dns_record import run_module

__metaclass__ = type


@pytest.fixture
def mock_module(mocker):

    # Build and Return Mocked nsible Main Module
    return mocker.patch('ansible.module_utils.basic.AnsibleModule')


# Test ADD Record
def test_ovh_dns_record_add(mock_module):
    # Simule les arguments passés au module
    mock_module.return_value.params = {
        'application_key': 'fake_key',
        'application_secret': 'fake_secret',
        'consumer_key': 'fake_consumer',
        'domain': 'example.com',
        'record_type': 'A',
        'record_name': 'www',
        'record_value': '192.0.2.1',
        'state': 'present'
    }

    # Exécute le module
    run_module()

    # Vérifie que le module a retourné le résultat attendu
    mock_module.return_value.exit_json.assert_called_once_with(changed=True)


# Test Remove Record
def test_ovh_dns_record_remove(mock_module):
    mock_module.return_value.params = {
        'application_key': 'fake_key',
        'application_secret': 'fake_secret',
        'consumer_key': 'fake_consumer',
        'domain': 'example.com',
        'record_type': 'A',
        'record_name': 'www',
        'state': 'absent'
    }

    run_module()
    mock_module.return_value.exit_json.assert_called_once_with(changed=True)
