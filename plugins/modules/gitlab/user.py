# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: user
version_added: "1.0.0"
short_description: User Management
description:
    - Used to Create, Update, Delete User Password
requirements:
    - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
    base_url:
        description:
        - The Gitlab API Base URL
        required: true
        type: str
    access_token:
        description:
        - The Gitlab API Admin Access Token
        required: true
        type: str
    password:
        description:
        - The Gitlab API User Password
        required: true
        type: str
'''

EXAMPLES = r'''
- name: "Update Gitlab User Password"
  kube_cloud.general.gitlab.update_user_password:
    base_url: "http://localhost:9000"
    access_token: "glat_cv182gTX22lMnB8876"
    password: "admin"
'''

from ansible.module_utils.basic import AnsibleModule