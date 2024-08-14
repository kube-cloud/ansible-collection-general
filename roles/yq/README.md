# Ansible Role: YQ

Ansible Role for YQ Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "YQ::INSTALL - Ensure YQ Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.yq
      vars:
        yq_version: "v4.44.3"
```
