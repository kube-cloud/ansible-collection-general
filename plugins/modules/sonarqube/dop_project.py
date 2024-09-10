# (c) 2024, Jean-Jacques ETUNE NGI <jetune@kube-cloud.com>
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = '''
---
module: dop_project
version_added: "1.0.0"
short_description: Manage DevOps Platform Projects
description:
  - Used to Manage DevOps Platform Projects
requirements:
  - requests
author: Jean-Jacques ETUNE NGI (@jetune) <jetune@kube-cloud.com>
options:
  base_url:
    description:
      - The Sonarqube API Base URL
    required: true
    type: str
  username:
    description:
      - The Sonarqube API Admin Username
    required: true
    type: str
  password:
    description:
      - The Sonarqube API Password
    required: true
    type: str
  project_key:
    description:
      - The SonarQube Project Key
    required: true
    type: str
  project_name:
    description:
      - The SonarQube Project Name
    required: true
    type: str
  dev_ops_platform_key:
    description:
      - The SonarQube DevOps Platform Key
    required: true
    type: str
  repository_identifier:
    description:
      - The SonarQube DevOps Repository ID
    required: true
    type: str
  monorepo:
    description:
      - The SonarQube DevOps Mono Repository Status
    required: true
    type: bool
  project_identifier:
    description:
      - The SonarQube DevOps Project Identifier
    required: false
    type: str
  state:
    description:
      - The Token State
    required: false
    choices: ['present', 'absent']
    default: 'present'
    type: str
'''

EXAMPLES = r'''
- name: "Import DevOps Platform Project"
  kube_cloud.general.sonarqube.dop_project:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    project_key: "kc-is-security-openvpn-service-provisioner"
    project_name: "kc-is-security-openvpn-service-provisioner"
    dev_ops_platform_key: "github-connector"
    repository_identifier: "kube-cloud/kc-is-security-openvpn-service-provisioner"
    monorepo: true
    state: 'present'

- name: "Delete DevOps Platform Project"
  kube_cloud.general.sonarqube.dop_project:
    base_url: "http://localhost:9000"
    username: "admin"
    password: "admin"
    project_key: "kc-is-security-openvpn-service-provisioner"
    project_name: "kc-is-security-openvpn-service-provisioner"
    dev_ops_platform_key: "github-connector"
    repository_identifier: "kube-cloud/kc-is-security-openvpn-service-provisioner"
    monorepo: true
    state: 'absent'
'''

from ansible.module_utils.basic import AnsibleModule
from ...module_utils.sonarqube.client import ProjectClient, sonarqube_client
from ...module_utils.sonarqube.models import ImportDopProjectSpec
from ...module_utils.sonarqube.models import Project
from ...module_utils.sonarqube.models import DevOpsPlatform
from ...module_utils.commons import filter_none

try:
    from requests import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# Find and Return DOP
def get_dop(client: ProjectClient, dop_key: str) -> DevOpsPlatform:

    try:

        # Call Client
        return client.get_dop(dop_key=dop_key)

    except HTTPError:

        # Return None
        return None


# Find and Return Project
def get_project(client: ProjectClient, project_key: str) -> Project:

    try:

        # Call Client
        return client.get_project(project_key=project_key)

    except HTTPError:

        # Return None
        return None


# Create Project
def import_project(module: AnsibleModule, client: ProjectClient, project_spec: ImportDopProjectSpec):

    try:

        # Call Client
        return client.import_dop_project(project_spec=project_spec)

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Import Project] - Failed Import DOP Project [{0}]: {1}".format(
                project_spec,
                api_error
            )
        )


# Delete Project
def delete_project(module: AnsibleModule, client: ProjectClient, project_key: str):

    try:

        # Call Client
        return client.delete_project(
            project_key=project_key
        )

    except HTTPError as api_error:

        # Set Module Error
        module.fail_json(
            msg="[Delete Project] - Failed Delete DOP Project (Login : {0}): {1}".format(
                project_key,
                api_error
            )
        )


# Instantiate Ansible Module
def build_ansible_module():

    # Build Module Arguments Specification
    module_specification = dict(
        base_url=dict(type='str', required=True),
        username=dict(type='str', required=True, no_log=True),
        password=dict(type='str', required=True, no_log=True),
        project_key=dict(type='str', required=True, no_log=False),
        project_name=dict(type='str', required=True, no_log=False),
        dev_ops_platform_key=dict(type='str', required=True, no_log=False),
        repository_identifier=dict(type='str', required=True, no_log=False),
        monorepo=dict(type='bool', required=True, no_log=False),
        project_identifier=dict(type='str', required=False, default=None, no_log=False),
        state=dict(type='str', required=False, default='present', choices=['present', 'absent'])
    )

    # Build ansible Module
    return AnsibleModule(
        argument_spec=module_specification,
        supports_check_mode=True
    )


# Instantiate Ansible Module
def build_client(module: AnsibleModule):

    try:

        # Build Client from Module
        return sonarqube_client(module.params)

    except ValueError:

        # Set Module Error
        module.fail_json(
            msg="[Build Client] - Failed Build Sonarqube API Client"
        )


# Build Requested DOP Project Import Spec
def build_requested_import_dop_project_spec(params: dict) -> ImportDopProjectSpec:

    # Base Parameters Name
    base_param_names = [
        "project_key", "project_name", "dev_ops_platform_key",
        "repository_identifier", "monorepo", "project_identifier"
    ]

    # Build Requested Instance
    spec = ImportDopProjectSpec(
        **{k: v for k, v in params.items() if v is not None and k in base_param_names}
    )

    # Build Requested Instance
    return spec


# Porcess Module Execution
def run_module(module: AnsibleModule, client: ProjectClient):

    # Extract State
    state = module.params['state']

    # Build Requested Instance
    input_spec = build_requested_import_dop_project_spec(module.params)

    # Find Existing Instance
    existing_resource = get_project(
        client=client,
        project_key=input_spec.project_key
    )

    # If Requested State is 'present' and Instance Already exists
    if existing_resource and state == 'present':

        # Initialize response (No Change)
        module.exit_json(
            msg="Project [{0}] Not Changed".format(existing_resource.key),
            instance=filter_none(existing_resource),
            changed=False
        )

    # If Requested State is 'present' and Instance don't exists
    if not existing_resource and state == 'present':

        # Create Instance
        result = import_project(
            module=module,
            client=client,
            project_spec=input_spec
        )

        # Initialize Module Response : Changed
        module.exit_json(
            changed=True,
            instance=result,
            msg="[{0}] Has been Created".format(input_spec.project_key)
        )

    # If Requested State is 'absent' and Instance exists
    if existing_resource and state == 'absent':

        # Delete Instance
        delete_project(
            module=module,
            client=client,
            project_key=input_spec.project_key
        )

        # Exit Module
        module.exit_json(
            msg="[{0}] Has been Deleted".format(input_spec.project_key),
            changed=True
        )

    # If Requested State is 'absent' and Instance don't exists
    else:

        # Initialize Response : No Change
        module.exit_json(
            msg="[{0}] Not Found".format(input_spec.project_key),
            changed=False
        )


# Entrypoint Function
def main():

    # Build Module
    module = build_ansible_module()

    # Build Client from Module
    client = build_client(module).project

    # Execute Module
    run_module(module, client)


# If file is executed directly (pythos ovh_dns_record.py [not imported])
if __name__ == '__main__':

    # Launch Entrypoint
    main()
