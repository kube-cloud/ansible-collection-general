# Ansible Role: HELM

Ansible Role for HELM Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "HELM::INSTALL - Ensure HELM Installed and Configured"
    ansible.builtin.include_role:
      name: kube_cloud.general.helm
    vars:
      helm_version: "v3.15.3"
```
