# Ansible Role: KUSTOMIZE

Ansible Role for KUSTOMIZE Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "KUSTOMIZE::INSTALL - Ensure KUSTOMIZE Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.kustomize
      vars:
        kustomize_version: "5.3.0"
```
