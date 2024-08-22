# Ansible Role: Terraform

Ansible Role for TF Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "TF::INSTALL - Ensure TF Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.terraform
      vars:
        terraform_version: "1.9.5"
```
