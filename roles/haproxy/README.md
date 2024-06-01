# Ansible Role: HA Proxy

Ansible Role for HA Proxy Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

# Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "({{ ansible_distribution }}) HAPROXY::INSTALL - Ensure HA Proxy Installed and Configured"
    ansible.builtin.import_role:
    name: haproxy
    vars:
        haproxy_socket_path: "/var/lib/haproxy/stats"
        haproxy_chroot_path: "/var/lib/haproxy"
        haproxy_socket_mode: "777"
        haproxy_socket_level: "admin"
        haproxy_user: "haproxy"
        haproxy_group: "haproxy"
        haproxy_ca_base: "/etc/ssl/certs"
        haproxy_crt_base: "/etc/ssl/private"
        haproxy_global_vars: []
        haproxy_connect_timeout: 5000
        haproxy_client_timeout: 50000
        haproxy_server_timeout: 50000
        haproxy_custom_timeouts: []
        haproxy_global_errors: []
        haproxy_stats:
            description: "HA Proxy Statistics Front End"
            bind: "localhost:9000"
            custom_properties:
                - "stats enable"
                - "stats uri /"
                - "stats refresh 10s"
                - "stats http-request allow"
        haproxy_frontends:
            name: ovpn-udp-1194
            description: OpenVPN AS UDP Front End
            bind: '*:1194'
            mode: tcp
            custom_properties: []
            backend: ''
        haproxy_backends:
            - name: ovpn-udp-1194
              description: OpenVPN AS UDP Front End
              mode: tcp
              upstream_balance: roundrobin
              upstream_default_config: inter 5s fall 3 rise 2
              custom_properties:
                - timeout server 10s
                - timeout connect 10s
                - timeout client 1m
              upstream_servers:
                - upstream_host: ovpn-vm.oprm.kube-cloud.com
                  upstream_port: '1194'
                  upstream_check: true
              upstream_custom_attribute: ''
              haproxy_dataplane:
                enabled: true
                config_file: /etc/haproxy/dataplaneapi.yml
                version: 2.9.3
                name: kc-is-ops-haproxy-api
                mode: single
                api:
                scheme:
                    - http
                host: 0.0.0.0
                port: 5555
                transaction:
                    transaction_dir: /tmp/haproxy
                custom_properties:
                    - 'cleanup_timeout: 10s'
                    - 'graceful_timeout: 15s'
                    - 'max_header_size: 1MiB'
                    - 'socket_path: /var/run/data-plane.sock'
                    - 'debug_socket_path: /var/run/dataplane-debug.sock'
                    - 'keep_alive: 3m'
                    - 'read_timeout: 30s'
                    - 'write_timeout: 60s'
                    - 'show_system_info: false'
                haproxy:
                service_name: haproxy
                config_file: /etc/haproxy/haproxy.cfg
                bin: /usr/sbin/haproxy
                reload_delay: 5
                reload_strategy: custom
                reload_retention: 1
                reload_cmd: service haproxy reload
                restart_cmd: service haproxy restart
                status_cmd: service haproxy status
                file_logs:
                path: /var/log/dataplanepi.log
                level: info
                format: json
                types:
                    - app
                    - access
                console_logs:
                enabled: true
                level: info
                format: json
                types:
                    - app
                    - access
                syslog_logs:
                enabled: false
                address: 127.0.0.1
                protocol: protocol
                tag: dataplaneapi
                syslog_level: debug
                facility: local0
                level: debug
                format: text
                types:
                    - app
                    - access
```
* 