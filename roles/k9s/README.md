# Ansible Role: K9S

Ansible Role for K9S Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "K9S::INSTALL - Ensure K9S Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.k9s
      vars:
        k9s_version: "v0.32.5"
```
