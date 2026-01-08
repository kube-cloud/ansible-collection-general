# Ansible Role: FLUX-CLI

Ansible Role for FLUX-CLI Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "FLUX-CLI::INSTALL - Ensure FLUX-CLI Installed and Configured"
    ansible.builtin.include_role:
      name: kube_cloud.general.fluxcli
    vars:
      fluxcd_version: "2.7.5"
```
