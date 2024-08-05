| Type	   | Status			|
|:---          |     :---:      |
| Sanity Checks | [![Sanity Checks](https://github.com/kube-cloud/ansible-collection-general/actions/workflows/sanity-checks.yml/badge.svg)](https://github.com/kube-cloud/ansible-collection-general/actions/workflows/sanity-checks.yml)     |
| Collection Publish | [![Collection Publish](https://github.com/kube-cloud/ansible-collection-general/actions/workflows/publish-collection.yml/badge.svg)](https://github.com/kube-cloud/ansible-collection-general/actions/workflows/publish-collection.yml)        |

# Ansible Collection : General (kube_cloud.general)

An Ansible Collection of modules and plugins that target General usages (HA Proxy, Sonarqube, Jenkins, Nexus, and Others Installation and Configuration on Linux Based Operating Systems).

## Included content

### Modules

Name | Description
---- | -----------
[kube_cloud.general.haproxy.backend](https://github.com/kube-cloud/ansible-collection-general/blob/develop/docs/haproxy.backend_module.rst)| Install and Configure HA Proxy.
[kube_cloud.general.haproxy.transaction](https://github.com/kube-cloud/ansible-collection-general/blob/develop/docs/haproxy.transaction_module.rst)| Validate and Cancel HA Proxy Dataplane API Transaction.

## Build This Collection

### Sanity Check

```bash
ansible-test sanity --python 3.8
```


## Installing this collection

### Python Requirements

- requests

### Ansible Dependencies

- community.general (>=4.0.0)

### Command

You can install the ``kube_cloud.general`` collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install kube_cloud.general
```

You can also include it in a `requirements.yml` file using the format:

```yaml
---
collections:
  - name: kube_cloud.general
```

and install it with command :

```bash
ansible-galaxy collection install -r requirements.yml
```

## Contributing to this collection

- [Issues](https://github.com/kube-cloud/ansible-collection-general/issues)
- [Pull Requests](https://github.com/kube-cloud/ansible-collection-general/pulls)

## Roadmap


## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
