# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
name: app_token
version_added: "1.0.0"
short_description: Create and Return Github Application Access Token
description:
    - Used to Create and Return Github Application Access Token
requirements:
    - requests
    - pyjwt >=2.9.0
    - cryptography
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
    base_url:
        description:
        - The Github API Base URL
        required: false
        type: str
        default: 'https://api.github.com'
    installation_id:
        description:
        - The Github Application Installation ID
        required: true
        type: str
    application_id:
        description:
        - The Github Application ID
        required: true
        type: str
    private_key:
        description:
        - The Github Application Private Key
        required: true
        type: str
    private_key_password:
        description:
        - The Github Application Private Key Password
        required: false
        type: str
    private_key_format:
        description:
        - The Github Application Private Key Format
        required: false
        choices: ['PEM_PKCS_1', 'PEM_PKCS_8']
        default: 'PEM_PKCS_8'
        type: str
    jwt_key_duration:
        description:
        - The Github Application JWT Key Duration
        required: false
        type: int
        default: 30
    jwt_algorithm:
        description:
        - The Github JWT Algorithm
        required: false
        type: str
        default: 'RS256'
    github_api_version:
        description:
        - The Github API Version
        required: false
        type: str
        default: '2022-11-28'
'''

EXAMPLES = r'''
- name: "Generate Github Application Access Token"
  ansible.builtin.set_fact:
    jwt_token: >
        {{
            lookup(
                'kube_cloud.general.github.app_token',
                base_url='https://api.github.com',
                installation_id: '12345678',
                private_key: '...',
                private_key_format='PEM_PKCS_8'
            )
        }}
'''

RETURN = '''
_raw:
    description: Githun Application Access Token
    type: str
'''


from ansible.plugins.lookup import LookupBase
from ...module_utils.github.enums import PrivateKeyFormat
from ...module_utils.github.client_app_access_token import AppAccessTokenClient


class LookupModule(LookupBase):

    # Execute Plugin
    def run(self, terms, variables, **kwargs):

        # Get API URL
        api_base_url = kwargs.get('base_url', 'https://api.github.com')

        # Get Installation ID
        installation_id = kwargs.get('installation_id', None)

        # Get Application ID
        application_id = kwargs.get('application_id', None)

        # Get Private Key
        private_key = kwargs.get('private_key', None)

        # Get Private Key Password
        private_key_password = kwargs.get('private_key_password', None)

        # Get Github App JWT Duration
        jwt_key_duration = kwargs.get('jwt_key_duration', 30)

        # Get Github App JWT Algorithm
        jwt_algorithm = kwargs.get('jwt_algorithm', 'RS256')

        # Get Github API Version
        github_api_version = kwargs.get('github_api_version', '2022-11-28')

        # Get Installation ID
        private_key_format = PrivateKeyFormat.create(kwargs.get('private_key_format', 'PEM_PKCS_8'))

        # If installation_id is not Provided
        if not installation_id:

            # Raise Value Exception
            raise ValueError("Initialization failed : 'installation_id' is required")

        # If private_key is not Provided
        if not private_key:

            # Raise Value Exception
            raise ValueError("Initialization failed : 'private_key' is required")

        # Build Client
        client = AppAccessTokenClient(
            api_base_url=api_base_url,
            api_version=github_api_version,
            app_installation_id=installation_id,
            app_id=application_id,
            app_private_key=private_key,
            app_private_key_password=private_key_password,
            private_key_format=private_key_format,
            jwt_key_duration=jwt_key_duration,
            jwt_algorithm=jwt_algorithm
        )

        # Create and return Access Token
        return [client.create_access_token()]
