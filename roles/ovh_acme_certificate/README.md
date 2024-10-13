# Ansible Role: ACME Certificate (OVH DNS Challenge)

Ansible Role for ACME Certificate Management With OVH DNS Challenge

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

## Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: Provision Let's Encrypt certificate
  hosts: localhost
  gather_facts: false

  tasks:

    # Ensure Main Configuration Blocs Facts are Extracted
    - name: "SSL - Ensure Main Configuration Blocs Facts are Extracted"
      ansible.builtin.set_fact:
        vault_svc_ovh:
          endpoint: ovh-eu
          application_name: ovh-kubecloud-terraform-provisionner
          application_description: OVH Terraform Provisionner
          application_key: <OVH_APPLICATION_KEY>
          application_secret: <OVH_APPLICATION_SECRET>
          consumer_key: <OVH_CONSUMER_KEY>

    # Ensure Specific Configuration Facts are Defined
    - name: "SSL - Ensure Specific Configuration Facts are Defined"
      ansible.builtin.set_fact:
        svc_access_name: <CERT_SUB_DOMAIN>
        svc_access_root_domain: <CERT_ROOT_DOMAIN>
        consul_svc_acme:
          version: 2
          directory: https://acme-v02.api.letsencrypt.org/directory
          certificate_remaining_days: 90
          base_path: "{{ playbook_dir }}/target/letencrypt"
          cert_owner: <CERT_OS_OWNER>
          cert_group: <CERT_OS_GROUP>
          cert_permissions: '0755'
          selevel: _default
          serole: _default
          setype: _default
          seuser: _default
          private_key_backup: true
          private_key_cipher: auto
          private_key_curve: secp384r1
          private_key_force_regenerate: false
          private_key_format: auto_ignore
          private_key_format_mismatch: regenerate
          private_key_passphrase: ''
          private_key_regenerate: full_idempotence
          private_key_return_content: false
          private_key_crypto_backend: auto
          private_key_size: 4096
          private_key_type: RSA
          csr_backup: true
          csr_country_name: FR
          csr_locality_name: <CSR_LOCALITU>
          csr_organization_name: <CSR_ORGANIZATION>
          csr_organizational_unit_name: <CSR_ORGANIZATIONAL_UNIT>
          csr_email_address: <CSR_EMAIL>
          csr_digest: sha256
          csr_key_usage:
            - digitalSignature
            - keyAgreement
          csr_key_usage_critical: false
          csr_extended_key_usage:
            - clientAuth
          csr_extended_key_usage_critical: false
          csr_create_subject_key_identifier: false
          csr_force_regenerate: false
          dns_san_subdomains: []
          email_san_subdomains: []
          uri_san_subdomains: []
          ip_san_subdomains: []
          prefixed_san_subdomains: ''
        acme_configuration:
          account_key_pem: <ACME_ACCOUNT_KEY>
          email_address: <ACME_ACCOUNT_EMAIL>
          external_account_binding: []
          id: https://acme-v02.api.letsencrypt.org/acme/acct/1552771337
          registration_url: https://acme-v02.api.letsencrypt.org/acme/acct/1552771337

    # Ensure Certificate is Provisioned on Letsencrypt
    - name: "DEMO - SSL - Ensure Certificate is Provisioned on Letsencrypt"
      ansible.builtin.include_role:
        name: kube_cloud.general.ovh_acme_certificate
      vars:
        ovh_endpoint: "{{ vault_svc_ovh.endpoint }}"
        ovh_application_key: "{{ vault_svc_ovh.application_key }}"
        ovh_application_secret: "{{ vault_svc_ovh.application_secret }}"
        ovh_consumer_key: "{{ vault_svc_ovh.consumer_key }}"
        root_domain: "{{ svc_access_root_domain }}"
        common_name_subdomain: "{{ svc_access_name }}"
        dns_san_subdomains: "{{ consul_svc_acme.dns_san_subdomains }}"
        email_san_subdomains: "{{ consul_svc_acme.email_san_subdomains }}"
        uri_san_subdomains: "{{ consul_svc_acme.uri_san_subdomains }}"
        ip_san_subdomains: "{{ consul_svc_acme.ip_san_subdomains }}"
        prefixed_san_subdomains: "{{ consul_svc_acme.prefixed_san_subdomains }}"
        acme_version: "{{ consul_svc_acme.version }}"
        acme_directory: "{{ consul_svc_acme.directory }}"
        acme_certificate_remaining_days: "{{ consul_svc_acme.certificate_remaining_days }}"
        acme_account_key_content: "{{ acme_configuration['account_key_pem'] }}"
        acme_account_email: "{{ acme_configuration['email_address'] }}"
        acme_base_path: "{{ consul_svc_acme.base_path }}"
        acme_cert_owner: "{{ consul_svc_acme.cert_owner }}"
        acme_cert_group: "{{ consul_svc_acme.cert_group }}"
        acme_cert_permissions: "{{ consul_svc_acme.cert_permissions }}"
        acme_selevel: "{{ consul_svc_acme.selevel }}"
        acme_serole: "{{ consul_svc_acme.serole }}"
        acme_setype: "{{ consul_svc_acme.setype }}"
        acme_seuser: "{{ consul_svc_acme.seuser }}"
        acme_private_key_backup: "{{ consul_svc_acme.private_key_backup }}"
        acme_private_key_cipher: "{{ consul_svc_acme.private_key_cipher }}"
        acme_private_key_curve: "{{ consul_svc_acme.private_key_curve }}"
        acme_private_key_force_regenerate: "{{ consul_svc_acme.private_key_force_regenerate }}"
        acme_private_key_format: "{{ consul_svc_acme.private_key_format }}"
        acme_private_key_format_mismatch: "{{ consul_svc_acme.private_key_format_mismatch }}"
        acme_private_key_regenerate: "{{ consul_svc_acme.private_key_regenerate }}"
        acme_private_key_return_content: "{{ consul_svc_acme.private_key_return_content }}"
        acme_private_key_crypto_backend: "{{ consul_svc_acme.private_key_crypto_backend }}"
        acme_private_key_size: "{{ consul_svc_acme.private_key_size }}"
        acme_private_key_type: "{{ consul_svc_acme.private_key_type }}"
        acme_csr_backup: "{{ consul_svc_acme.csr_backup }}"
        acme_csr_country_name: "{{ consul_svc_acme.csr_country_name }}"
        acme_csr_locality_name: "{{ consul_svc_acme.csr_locality_name }}"
        acme_csr_organization_name: "{{ consul_svc_acme.csr_organization_name }}"
        acme_csr_organizational_unit_name: "{{ consul_svc_acme.csr_organizational_unit_name }}"
        acme_csr_email_address: "{{ consul_svc_acme.csr_email_address }}"
        acme_csr_digest: "{{ consul_svc_acme.csr_digest }}"
        acme_csr_key_usage: "{{ consul_svc_acme.csr_key_usage }}"
        acme_csr_key_usage_critical: "{{ consul_svc_acme.csr_key_usage_critical }}"
        acme_csr_extended_key_usage: "{{ consul_svc_acme.csr_extended_key_usage }}"
        acme_csr_extended_key_usage_critical: "{{ consul_svc_acme.csr_extended_key_usage_critical }}"
        acme_csr_create_subject_key_identifier: "{{ consul_svc_acme.csr_create_subject_key_identifier }}"
        acme_csr_force_regenerate: "{{ consul_svc_acme.csr_force_regenerate }}"
        acme_cert_file_path_var: "acme_cert_file"
        acme_fullchain_cert_file_path_var: "acme_fullchain_cert_file"
        acme_intermediate_cert_file_path_var: "acme_intermediate_cert_file"
        acme_csr_file_path_var: "acme_csr_file"
        acme_private_key_file_path_var: "acme_private_key_file"
        acme_fullchain_cert_and_key_file_path_var: "acme_fullchain_cert_and_key_file"
```

## All Role Steps

```yaml
---

- name: Provision Let's Encrypt certificate
  hosts: localhost
  gather_facts: false
  vars:
    root_domain: "<TARGET_ROOT_DOMAIN>"
    subdomain: "<TARGET_SUBDOMAIN>"
    account_email: "<ACCOUNT_AMAIL>"
    ovh_endpoint: "ovh-eu"
    ovh_application_key: "<OVH_APPLICATION_KEY>"
    ovh_application_secret: "<OVH_APPLICATION_SECRET>"
    ovh_consumer_key: "<OVH_CONSUMER_KEY>"
    _acme_base_path: "./target/demo-acme-role/letsencrypt"
    _acme_directory: "https://acme-v02.api.letsencrypt.org/directory"
    _acme_account_key_src: "{{ _acme_base_path }}/account.key"
    _acme_version: 2
    _acme_cert_common_name: "{{ subdomain }}.{{ root_domain }}"
    _acme_private_key_dir: "{{ acme_base_path | regex_replace('/$', '') }}/{{ _acme_cert_common_name }}/private"
    _acme_csr_dir: "{{ acme_base_path | regex_replace('/$', '') }}/{{ _acme_cert_common_name }}/csr"
    _acme_certificate_dir: "{{ acme_base_path | regex_replace('/$', '') }}/{{ _acme_cert_common_name }}/cert"
    _acme_private_key_file: "{{ _acme_private_key_dir }}/private.pem"
    _acme_csr_file: "{{ _acme_csr_dir }}/certificate.csr"
    _acme_cert_file: "{{ _acme_certificate_dir }}/certificate.pem"
    _acme_intermediatechain_cert_file: "{{ _acme_certificate_dir }}/certificate-intermediate.pem"
    _acme_fullchain_cert_file: "{{ _acme_certificate_dir }}/certificate-fullchain.pem"
    _acme_fullchain_cert_key_file: "{{ _acme_certificate_dir }}/certificate-fullchain-and-key.pem"
    _acme_challenge: dns-01
    _acme_certificate_remaining_days: 60

  tasks:

    # Make sure that all Required Directories exists
    - name: Create directories for Let's Encrypt
      ansible.builtin.file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - "{{ acme_base_path }}"
        - "{{ _acme_csr_dir }}"
        - "{{ _acme_certificate_dir }}"
        - "{{ _acme_private_key_dir }}"

    # Generate ACME Account Key
    - name: Generate account.key if it does not exist
      community.crypto.openssl_privatekey:
        path: "{{ _acme_account_key_src }}"
        type: RSA
        size: 4096

    # Make sure ACME Account Exists
    - name: Make sure account exists and has given contacts. We agree to TOS.
      community.crypto.acme_account:
        account_key_src: "{{ _acme_account_key_src }}"
        acme_version: "{{ _acme_version }}"
        acme_directory: "{{ _acme_directory }}"
        terms_agreed: true
        contact: ["mailto:{{ account_email }}"]
        state: present

    # Generate Service Domain KEY
    - name: Generate Service Domain KEY
      community.crypto.openssl_privatekey:
        path: "{{ _acme_private_key_file }}"
        type: RSA
        size: 4096

    # Generate Open SSL CSR
    - name: Generate an OpenSSL Certificate Signing Request with Subject information
      community.crypto.openssl_csr:
        path: "{{ _acme_csr_file }}"
        privatekey_path: "{{ _acme_private_key_file }}"
        country_name: FR
        organization_name: "KubeCloud"
        email_address: "{{ account_email }}"
        common_name: "{{ _acme_cert_common_name }}"
        key_usage:
          - digitalSignature
          - keyAgreement
        extended_key_usage:
          - clientAuth

    # Be Sure Chellenge is Generated
    - name: "Create a challenge for requested certificate ({{ _acme_cert_common_name }})"
      community.crypto.acme_certificate:
        account_key_src: "{{ _acme_account_key_src }}"
        account_email: "{{ account_email }}"
        src: "{{ _acme_csr_file }}"
        cert: "{{ _acme_cert_file }}"
        challenge: "{{ _acme_challenge }}"
        acme_directory: "{{ _acme_directory }}"
        remaining_days: 90
        acme_version: "{{ _acme_version }}"
      register: acme_dns_challenge

    # Check ACME Challenge Response
    - name: Determine if acme_dns_challenge_enabled should be true
      ansible.builtin.set_fact:
        acme_dns_challenge_enabled: >-
          {{
            acme_dns_challenge.changed | default(false) and
            (acme_dns_challenge.challenge_data | default({}) | length > 0) and
            (acme_dns_challenge.challenge_data[_acme_cert_common_name] | default({}) | length > 0) and
            (acme_dns_challenge.challenge_data[_acme_cert_common_name]['dns-01'] | default({}) | length > 0)
          }}

    # Display Challenge Text
    - name: "Debug Challenge Text"
      ansible.builtin.debug:
        var: acme_dns_challenge

    # Display Challenge Enabled
    - name: "Debug Challenge Enabled"
      ansible.builtin.debug:
        var: acme_dns_challenge_enabled

    # Ensure Already Generated Files are Cleaned
    - name: "Ensure Already Generated Files are Cleaned"
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      loop:
        - "{{ _acme_fullchain_cert_key_file }}"
        - "{{ _acme_fullchain_cert_file }}"
        - "{{ _acme_cert_file }}"
        - "{{ _acme_intermediatechain_cert_file }}"
      failed_when: false

    # Ensure DNS Challenge Data Published on OVH
    - name: "Ensure DNS Challenge Data Published on OVH"
      kube_cloud.general.ovh.dns_record:
        endpoint: "{{ ovh_endpoint }}"
        application_key: "{{ ovh_application_key }}"
        application_secret: "{{ ovh_application_secret }}"
        consumer_key: "{{ ovh_consumer_key }}"
        domain: "{{ root_domain }}"
        record_name: "{{ acme_dns_challenge.challenge_data[_acme_cert_common_name][challenge].record | regex_replace('.' + root_domain + '$', '') }}"
        record_type: "TXT"
        target: "{{ acme_dns_challenge.challenge_data[_acme_cert_common_name][challenge].resource_value }}"
        state: 'present'

    # Ensure DNS Challenge Validated and Certificates Created
    - name: "[PATH] - Ensure DNS Challenge Validated and Certificates Created"
      community.crypto.acme_certificate:
        account_key_src: "{{ _acme_account_key_src }}"
        account_email: "{{ account_email }}"
        csr: "{{ _acme_csr_file }}"
        cert: "{{ _acme_cert_file }}"
        fullchain: "{{ _acme_fullchain_cert_file }}"
        chain: "{{ _acme_intermediatechain_cert_file }}"
        challenge: "{{ _acme_challenge }}"
        acme_directory: "{{ _acme_directory }}"
        remaining_days: "{{ _acme_certificate_remaining_days }}"
        acme_version: "{{ _acme_version }}"
        data: "{{ acme_dns_challenge }}"
      register: domain_challenge_validated_content

    # Ensure DNS Challenge Data Removed from OVH
    - name: "OVH::ROLE::ACME - Ensure DNS Challenge Data Removed from OVH"
      kube_cloud.general.ovh.dns_record:
        endpoint: "{{ ovh_endpoint }}"
        application_key: "{{ ovh_application_key }}"
        application_secret: "{{ ovh_application_secret }}"
        consumer_key: "{{ ovh_consumer_key }}"
        domain: "{{ root_domain }}"
        record_name: "{{ acme_dns_challenge.challenge_data[_acme_cert_common_name][challenge].record | regex_replace('.' + root_domain + '$', '') }}"
        record_type: "TXT"
        target: "__NO_NEED_TARGET__"
        state: absent
      failed_when: false

    # Ensure Fullchain Certificate and Private Key are Readed
    - name: "Ensure Fullchain Certificate and Private Key are Readed"
      ansible.builtin.command: >
        cat {{ _acme_fullchain_cert_file }} {{ _acme_private_key_file }}
      register: _acme_fullchain_cert_key_content
      changed_when: false

    # Ensure Fullchain Certificate and Private Key are Stored
    - name: "Ensure Fullchain Certificate and Private Key are Combined"
      ansible.builtin.copy:
        content: "{{ _acme_fullchain_cert_key_content.stdout }}"
        dest: "{{ _acme_fullchain_cert_key_file }}"
        mode: "0766"
      changed_when: false
```
