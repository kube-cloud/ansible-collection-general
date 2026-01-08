# Ansible Role: FLUXCD

Ansible Role for FLUXCD Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "FLUXCD::INSTALL - Ensure FLUXCD Installed and Configured"
    ansible.builtin.include_role:
      name: kube_cloud.general.fluxcd
    vars:
      fluxcd_version: "2.7.5"
```
