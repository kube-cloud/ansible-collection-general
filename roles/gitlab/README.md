# Ansible Role: Sonarqube

Ansible Role for Sonarqube Installation.

## Supported OS

* CentOS 6/7/8
* RedHat 6/7
* Ubuntu Trusty/Xenial/Bionic/Jammy

# Usage

Install Collection `ansible-galaxy collections install kube_cloud.general`

```yaml
- name: "SONARQUBE::INSTALL - Ensure Sonarqube Installed and Configured"
    ansible.builtin.import_role:
    name: sonarqube
    vars:
        sonar_db_embedded: false
        sonar_db_embedded_port: 9092
        sonar_db_user: "sonar"
        sonar_db_pass: "sonar"
        sonar_jdbc_url: "jdbc:postgresql://localhost/sonar"
        sonar_jdbc_maxactive: 60
        sonar_jdbc_maxidle: 5
        sonar_jdbc_minidle: 2
        sonar_jdbc_maxwait: 5000
        sonar_jdbc_min_evictable_idle_time_millis: 600000
        sonar_jdbc_time_between_eviction_runs_millis: 30000
        sonar_web_java_opts: "-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError -Djava.net.preferIPv4Stack=true"
        sonar_web_java_additional_opts: ""
        sonar_web_host: 0.0.0.0
        sonar_web_context: ""
        sonar_web_port: 9000
        sonar_web_http_max_threads: 50
        sonar_web_http_min_threads: 5
        sonar_web_http_accept_count: 25
        sonar_ajp_port: -1
        sonar_ce_java_opts: "-Xmx512m -Xms128m -XX:+HeapDumpOnOutOfMemoryError -Djava.net.preferIPv4Stack=true"
        sonar_ce_java_additional_opts: ""
        sonar_ce_worker_count: 1
        sonar_search_java_opts: "-Xmx1G -Xms1G -Xss256k -Djava.net.preferIPv4Stack=true -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+HeapDumpOnOutOfMemoryError"
        sonar_search_java_additional_opts: ""
        sonar_search_port: 9001
        sonar_search_host: 127.0.0.1
        sonar_updatecenter_activate: true
        http_proxy_host: ""
        http_proxy_port: ""
        https_proxy_host: ""
        https_proxy_port: ""
        http_auth_ntlm_domain: ""
        socks_proxy_host: ""
        socks_proxy_port: ""
        http_proxy_user: ""
        http_proxy_password: ""
        sonar_log_level: "INFO"
        sonar_log_rolling_policy: "time:yyyy-MM-dd"
        sonar_log_max_files: 7
        sonar_web_access_logs_enable: true
        sonar_web_access_logs_pattern: "%i{X-Forwarded-For} %l %u [%t] \"%r\" %s %b \"%i{Referer}\" \"%i{User-Agent}\""
```
