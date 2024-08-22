# Ansible Role: kubectl

Ansible Role for KUBECTL Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "KUBECTL::INSTALL - Ensure KUBECTL Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.kubectl
      vars:
        kubectl_version: "1.9.5"
```
