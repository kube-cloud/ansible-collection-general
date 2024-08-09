# Ansible Role: K3S

Ansible Role for K3S Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "K3S::INSTALL - Ensure K3S Installed and Configured"
    ansible.builtin.include_role:
        name: kube_cloud.general.k3s
      vars:
        k3s_version: "v1.29.7+k3s1"
        k3s_install_options: "--debug"
        k3s_data_dir: "/"
```
