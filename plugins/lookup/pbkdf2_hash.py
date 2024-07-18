# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
name: pbkdf2_hash
version_added: "1.0.0"
short_description: Generate PBKDF2 Hash
description:
  - Used to Generate PBKDF2 Hash
requirements:
  - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
  password:
    description:
      - The Source Password to Derive
    required: true
    type: str
  salt:
    description:
      - The Salt Value
    required: false
    type: str
    default: ''
  rounds:
    description:
      - The Derivation Ieration Rounds
    required: false
    type: int
    default: 100000
'''

EXAMPLES = r'''
- name: "Get Password Hash"
  ansible.builtin.debug: msg="{{item}}"
  hash_pw: "{{ lookup('kube_cloud.general.pbkdf2_hash',password='my_pass',salt='random-salt',rounds=100000) }}"
'''

RETURN = '''
_raw:
  description: Hash Password Structure
  type: dict
'''


from ansible.plugins.lookup import LookupBase
from base64 import b64encode
from passlib.hash import pbkdf2_sha512
from passlib.utils.binary import ab64_decode
from ..module_utils.commons import generate_random_string


class LookupModule(LookupBase):

    # Execute Plugin
    def run(self, terms, variables, **kwargs):

        # Check Passord Key
        if 'password' not in kwargs or not kwargs['password'] or kwargs['password'].strip() == '':

            # Raise Error
            raise ValueError("The Field 'password' is Mandatory.")

        # Extact Parameters
        password = str(kwargs['password']).strip()

        # Extract Salt or Generate Random Salt
        salt = str(kwargs.get('salt', generate_random_string(16)))

        # Extract Rounds or Get default
        rounds = kwargs.get('rounds', 100000)

        # Build Hash Array
        hash_array = pbkdf2_sha512.hash(password, salt=salt.encode(), rounds=rounds).split('$')

        # Compute Encoded Salt
        salt_encoded = b64encode(ab64_decode(hash_array[3])).decode()

        # Compute Encoded Password
        password_encoded = b64encode(ab64_decode(hash_array[4])).decode()

        # Build Single Line Password
        password_single_line = "${prolog}${rounds}${salt_encoded}${password_encoded}".format(
            prolog="pbkdf2-sha512",
            rounds=rounds,
            salt_encoded=salt_encoded,
            password_encoded=password_encoded
        )

        # Create and return Transaction
        return {
            "password_original": password,
            "salt_original": salt,
            "salt": salt_encoded,
            "password_single_line": password_single_line,
            "password_crypted": password_single_line.split('$')[2] + '$' + password_encoded,
            "rounds": password_single_line.split('$')[2],
            "hash_derivation": "PBKDF2",
            "hash_algoritm": "SHA512"
        }
