# Ansible Role: kind

Ansible Role for Kind Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "KIND::INSTALL - Ensure Kind Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.kind
      vars:
        kubectl_version: "v0.24.0"
```
