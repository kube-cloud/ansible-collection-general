# Ansible Role: ACME Certificate (OVH DNS Challenge)

Ansible Role for ACME Certificate Management With OVH DNS Challenge

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "Generate ACME/Letsencrypt Certificate with OVH DNS Challenge"
    ansible.builtin.import_role:
    name: kube_cloud.general.ovh..acme_certificate
    vars:
        root_domain: kube-cloud.com
        common_name_subdomain: jenkins.devcentral
        dns_san_subdomains: 
            - cicd.devcentral
        email_san_subdomains: []
        uri_san_subdomains: []
        ip_san_subdomains: []
        prefixed_san_subdomains:
            - "DNS:integration.devcentral"
        acme_version: 2
        acme_directory: https://acme-v02.api.letsencrypt.org/directory
        acme_certificate_remaining_days: 10
        acme_account_key_src: "__PROVIDE_LETSECRYPT_ACCOUNT_KEY__"
        acme_account_email: administrator@kube-cloud.com
        acme_base_path: "/etc/letsecnrypt/live"
        acme_cert_owner: root
        acme_cert_group: root
        acme_cert_permissions: "0755"
        acme_selevel: _default
        acme_serole: _default
        acme_setype: _default
        acme_seuser: _default
        acme_private_key_backup: true
        acme_private_key_cipher: auto
        acme_private_key_curve: secp384r1
        acme_private_key_force_regenerate: false
        acme_private_key_format: auto_ignore
        acme_private_key_format_mismatch: regenerate
        acme_private_key_passphrase:
        acme_private_key_regenerate: full_idempotence
        acme_private_key_return_content: false
        acme_private_key_crypto_backend: auto
        acme_private_key_size: 4096
        acme_private_key_type: RSA
        acme_csr_backup: true
        acme_csr_country_name: "FR"
        acme_csr_locality_name: "SEINE-ET-MARNE"
        acme_csr_organization_name: "KubeCloud"
        acme_csr_organizational_unit_name: "DPEP - Digital Products Engineering and Platform"
        acme_csr_email_address: "contact@kube-cloud.com"
        acme_csr_digest: sha256
        acme_csr_key_usage:
            - digitalSignature
            - keyAgreement
        acme_csr_key_usage_critical: false
        acme_csr_extended_key_usage:
            - clientAuth
        acme_csr_extended_key_usage_critical: false
        acme_csr_create_subject_key_identifier: false
        acme_csr_force_regenerate: false
        ovh_endpoint: ovh-eu
        ovh_application_key: "__PROVIDE_APPLICATION_KEY__"
        ovh_application_secret: "__PROVIDE_APPLICATION_SECRET__"
        ovh_consumer_key: "__PROVIDE_CONSUMER_KEY__"
        acme_cert_file_path_var: "acme_cert_file"
        acme_fullchain_cert_file_path_var: "acme_fullchain_cert_file"
        acme_intermediate_cert_file_path_var: "acme_intermediate_cert_file"
        acme_csr_file_path_var: "acme_csr_file"
        acme_private_key_file_path_var: "acme_private_key_file"
```
