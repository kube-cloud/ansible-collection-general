from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from .enums import EnableDisableEnum, LoadBalancingAlgorithm, CookieType
from .enums import WebSocketProtocol, HealthCheckType, TimeoutStatus
from .enums import ErrorStatus, OkStatus, HttpMethod, ProxyProtocol, FrontendLevel
from .enums import CompressionAlgorithm, SSLVersion, Requirement, MatchType
from .enums import AdvancedHealthCheckType, MySqlVersionCheckType, ConditionType
from .enums import HttpRequestRuleType, LogLevel, HttpRequestRuleNormalizerType
from .enums import IPProtocol, RedirectType


# Load Balancing Configuration
@dataclass
class Balance:
    """
    Represents a load balancing algorithm configuration.
    Refer at : `https://www.haproxy.com/documentation/dataplaneapi/community/#post-/services/haproxy/configuration`

    Attributes:
        algorithm (str): The balancing algorithm (e.g., "roundrobin", "leastconn", "static-rr", "first", "source", "uri", "url_param", "hdr", "random", etc...).
        hash_expression (str): The hash expression used for hash-based balancing.
        hdr_name (str): The header name for header-based balancing.
        hdr_use_domain_only (bool): Whether to use only the domain part of the header for header-based balancing.
        random_draws (int): The number of random draws for random-based balancing.
        rdp_cookie_name (str): The name of the cookie for RDP cookie-based balancing.
        uri_depth (int): The URI depth for URI-based balancing.
        uri_len (int): The URI length for URI-based balancing.
        uri_path_only (bool): Whether to use only the path part of the URI for URI-based balancing.
        uri_whole (bool): Whether to use the entire URI for URI-based balancing.
        url_param (str): The URL parameter name for URL parameter-based balancing.
        url_param_check_post (int): The number of URL parameters to consider from POST data for URL parameter-based balancing.
        url_param_max_wait (int): The maximum wait time for a URL parameter-based balancing response.
    """
    algorithm: LoadBalancingAlgorithm
    hash_expression: Optional[str] = None
    hdr_name: Optional[str] = None
    hdr_use_domain_only: Optional[bool] = None
    random_draws: Optional[int] = None
    rdp_cookie_name: Optional[str] = None
    uri_depth: Optional[int] = None
    uri_len: Optional[int] = None
    uri_path_only: Optional[bool] = None
    uri_whole: Optional[bool] = None
    url_param: Optional[str] = None
    url_param_check_post: Optional[int] = None
    url_param_max_wait: Optional[int] = None

    def __post_init__(self):

        # Check Algorithm
        if not self.algorithm:
            raise ValueError("The 'algorithm' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the Balance object.
        """
        return str(self.__dict__)


# Backend Cookie Configuration
@dataclass
class Cookie:
    """
    Represents a session cookie configuration.
    Refer at : `https://www.haproxy.com/documentation/dataplaneapi/community/#post-/services/haproxy/configuration`

    Attributes:
        attr (List[Dict[str, str]], optional): List of attribute values for the cookie.
        domain (List[Dict[str, str]], optional): List of domain values for the cookie.
        dynamic (bool, optional): Whether the cookie is dynamic.
        httponly (bool, optional): Whether the cookie is HTTP-only.
        indirect (bool, optional): Whether the cookie is indirect.
        maxidle (int, optional): Maximum idle time for the cookie.
        maxlife (int, optional): Maximum life time for the cookie.
        name (str, required): The name of the cookie.
        nocache (bool, optional): Whether the cookie is no-cache.
        postonly (bool, optional): Whether the cookie is post-only.
        preserve (bool, optional): Whether the cookie is preserved.
        secure (bool, optional): Whether the cookie is secure.
        type (str, optional): The type of the cookie.
    """
    name: str
    attr: List[Dict[str, str]] = field(default_factory=list)
    domain: List[Dict[str, str]] = field(default_factory=list)
    dynamic: Optional[bool] = None
    httponly: Optional[bool] = None
    indirect: Optional[bool] = None
    maxidle: Optional[int] = None
    maxlife: Optional[int] = None
    nocache: Optional[bool] = None
    postonly: Optional[bool] = None
    preserve: Optional[bool] = None
    secure: Optional[bool] = None
    type: CookieType = CookieType.REWRITE

    def __post_init__(self):

        # Check Name
        if not self.name:
            raise ValueError("[Cookie] - The 'name' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the Cookie object.
        """
        return str(self.__dict__)


# Backend Configuration
@dataclass
class Server:
    """
    Represents a server configuration with various parameters.

    Attributes:
        name (str, required): The name of the server.
        address (str, required): The IP address or hostname of the server.
        port (int, required): The port number on which the server listens.
        status (EnableDisableEnum, required): The current status of the server (enabled/disabled).
        layer (Layer, required): The network layer the server operates on (Layer 4/Layer 7).
        ssl_version (SSLVersion, required): The SSL/TLS version used by the server.
        action (ActionType, required): The action type associated with the server.
        requirement (Requirement, required): The requirement level for the server.
        verify (str, optional): Additional verification parameter.
        verifyhost (str, optional): Parameter for verifying the host.
        weight (int, optional): The weight of the server for load balancing.
        track (str, optional): Tracking parameter for the server.
        ws (str, optional): Web socket related parameter.
        check (str, optional): Health check parameter.
        health_check_address (str, optional): The address used for health checks.
        health_check_port (int, optional): The port used for health checks.
        max_reuse (int, optional): Maximum number of reuses.
        maxconn (int, optional): Maximum number of connections.
        maxqueue (int, optional): Maximum number of queued connections.
        minconn (int, optional): Minimum number of connections.
    """
    name: str
    address: str
    port: int
    verify: Optional[Requirement] = None
    verifyhost: Optional[str] = None
    weight: Optional[int] = None
    track: Optional[str] = None
    ws: Optional[WebSocketProtocol] = None
    check: Optional[EnableDisableEnum] = None
    health_check_address: Optional[str] = None
    health_check_port: Optional[int] = None
    max_reuse: Optional[int] = None
    maxconn: Optional[int] = None
    maxqueue: Optional[int] = None
    minconn: Optional[int] = None
    npn: Optional[str] = None
    fall: Optional[int] = None
    rise: Optional[int] = None
    inter: Optional[int] = None
    fastinter: Optional[int] = None
    error_limit: Optional[int] = None
    health_check_address: Optional[str] = None
    health_check_port: Optional[int] = None
    pool_low_conn: Optional[int] = None
    pool_max_conn: Optional[int] = None
    pool_purge_delay: Optional[int] = None
    proto: Optional[str] = None
    redir: Optional[str] = None
    resolve_opts: Optional[str] = None
    resolvers: Optional[str] = None
    ssl_cafile: Optional[str] = None
    ssl_certificate: Optional[str] = None
    tcp_ut: Optional[int] = None
    track: Optional[int] = None
    maintenance: Optional[EnableDisableEnum] = None
    no_sslv3: Optional[EnableDisableEnum] = None
    no_tlsv10: Optional[EnableDisableEnum] = None
    no_tlsv11: Optional[EnableDisableEnum] = None
    no_tlsv12: Optional[EnableDisableEnum] = None
    no_tlsv13: Optional[EnableDisableEnum] = None
    no_verifyhost: Optional[EnableDisableEnum] = None
    stick: Optional[EnableDisableEnum] = None
    tfo: Optional[EnableDisableEnum] = None
    send_proxy_v2_ssl: Optional[EnableDisableEnum] = None
    send_proxy_v2_ssl_cn: Optional[EnableDisableEnum] = None
    ssl_reuse: Optional[EnableDisableEnum] = None
    ssl: Optional[EnableDisableEnum] = None
    ssl_max_ver: Optional[SSLVersion] = None
    ssl_min_ver: Optional[SSLVersion] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.name:
            raise ValueError("[Server] - The 'name' field is required.")


# HTTP HealthCheck Configuration
@dataclass
class HttpHealthCheck:
    """
    Represents a health check configuration in HAProxy.

    Attributes:
        type (HealthCheckType): The type of health check.
        method (Optional[str]): The method used for the health check.
        uri (Optional[str]): The URI used for the health check.
        uri_log_format (Optional[str]): The log format for the URI.
        var_expr (Optional[str]): The expression for the variable.
        var_format (Optional[str]): The format for the variable.
        var_name (Optional[str]): The name of the variable.
        var_scope (Optional[str]): The scope of the variable.
        version (Optional[str]): The version for the health check.
        via_socks4 (Optional[bool]): Whether to use SOCKS4.
        port (Optional[int]): The port number for the health check.
        port_string (Optional[str]): The port number as a string.
        proto (Optional[str]): The protocol used for the health check.
        send_proxy (Optional[bool]): Whether to send proxy protocol.
        sni (Optional[str]): The SNI for the health check.
        ssl (Optional[bool]): Whether to use SSL.
        status_code (Optional[str]): The status code for the health check.
        tout_status (Optional[TimeoutStatus]): The timeout status.
        match (Optional[MatchType]): The match type for the health check.
        headers (Optional[List[Dict[str, str]]]): The headers for the health check.
        body (Optional[str]): The body content for the health check.
        body_log_format (Optional[str]): The log format for the body.
        check_comment (Optional[str]): The comment for the health check.
        default (Optional[bool]): Whether this is the default health check.
        error_status (Optional[ErrorStatus]): The error status for the health check.
        addr (Optional[str]): The address for the health check.
        ok_status (Optional[OkStatus]): The OK status for the health check.
    """

    type: HealthCheckType
    method: Optional[str] = None
    uri: Optional[str] = None
    uri_log_format: Optional[str] = None
    var_expr: Optional[str] = None
    var_format: Optional[str] = None
    var_name: Optional[str] = None
    var_scope: Optional[str] = None
    version: Optional[str] = None
    via_socks4: Optional[bool] = None
    port: Optional[int] = None
    port_string: Optional[str] = None
    proto: Optional[str] = None
    send_proxy: Optional[bool] = None
    sni: Optional[str] = None
    ssl: Optional[bool] = None
    status_code: Optional[str] = None
    tout_status: Optional[TimeoutStatus] = None
    match: Optional[MatchType] = None
    headers: Optional[List[Dict[str, str]]] = None
    body: Optional[str] = None
    body_log_format: Optional[str] = None
    check_comment: Optional[str] = None
    default: Optional[bool] = None
    error_status: Optional[ErrorStatus] = None
    addr: Optional[str] = None
    ok_status: Optional[OkStatus] = None


# HTTP check parameters Configuration
@dataclass
class HttpCheckParams:
    """
    Represents the HTTP check parameters for a HAProxy backend.

    Attributes:
        method (Optional[HttpCheckMethod]): The HTTP method used for the health check.
        uri (str): The URI used for the health check.
        version (str): The HTTP version.
    """
    method: HttpMethod
    uri: str
    version: str = "HTTP/1.1"

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.method:
            raise ValueError("[HttpCheckParams] - The 'method' field is required.")

        if not self.uri:
            raise ValueError("[HttpCheckParams] - The 'uri' field is required.")


# Error Location
@dataclass
class ErrorLoc:
    code: int
    url: str

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.code:
            raise ValueError("[ErrorLoc] - The 'code' field is required.")

        # Ajoutez ici des validations si nécessaire
        if not self.url:
            raise ValueError("[ErrorLoc] - The 'url' field is required.")


# Error File
@dataclass
class ErrorFile:
    code: int
    file: str

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.code:
            raise ValueError("[ErrorFile] - The 'code' field is required.")

        # Ajoutez ici des validations si nécessaire
        if not self.file:
            raise ValueError("[ErrorFile] - The 'file' field is required.")


# /BackendFrontend Compression
@dataclass
class Compression:
    algorithms: Optional[List[CompressionAlgorithm]] = field(default_factory=list)
    offload: Optional[bool] = None
    types: Optional[List[str]] = field(default_factory=list)


# Backend/Frontend Forwarded For
@dataclass
class ForwardFor:
    enabled: EnableDisableEnum
    header: Optional[str] = None
    ifnone: Optional[bool] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.enabled:
            raise ValueError("[ForwardFor] - The 'enabled' field is required.")


# Backend Check Params for MySQL
@dataclass
class MySqlCheckParams:
    client_version: MySqlVersionCheckType
    username: Optional[str] = None


# Backend Check Params for Posgres
@dataclass
class PostgresSqlCheckParams:
    username: Optional[str] = None


# Backend Check Params for SMTP
@dataclass
class SmtpCheckParams:
    domain: Optional[str] = None
    hello: Optional[str] = None


# Backend Redispatch
@dataclass
class Redispatch:
    enabled: EnableDisableEnum
    interval: Optional[int] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.enabled:
            raise ValueError("[Redispatch] - The 'enabled' field is required.")


# Backend Ignore Persist
@dataclass
class IgnorePersist:
    cond: ConditionType
    cond_test: str

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.cond:
            raise ValueError("[IgnorePersist] - The 'cond' field is required.")

        # Ajoutez ici des validations si nécessaire
        if not self.cond_test:
            raise ValueError("[IgnorePersist] - The 'cond_test' field is required.")


# HTTP Request Rule Configuration
@dataclass
class HttpRequestRule:
    index: int
    type: Optional[HttpRequestRuleType] = None
    acl_file: Optional[str] = None
    acl_keyfmt: Optional[str] = None
    auth_realm: Optional[str] = None
    bandwidth_limit_limit: Optional[str] = None
    bandwidth_limit_name: Optional[str] = None
    bandwidth_limit_period: Optional[str] = None
    capture_id: Optional[int] = None
    capture_len: Optional[int] = None
    capture_sample: Optional[str] = None
    cond: Optional[ConditionType] = None
    cond_test: Optional[str] = None
    deny_status: Optional[int] = None
    expr: Optional[str] = None
    hdr_format: Optional[str] = None
    hdr_match: Optional[str] = None
    hdr_method: Optional[str] = None
    hdr_name: Optional[str] = None
    hint_format: Optional[str] = None
    hint_name: Optional[str] = None
    log_level: Optional[LogLevel] = None
    lua_action: Optional[str] = None
    lua_params: Optional[str] = None
    map_file: Optional[str] = None
    map_keyfmt: Optional[str] = None
    map_valuefmt: Optional[str] = None
    mark_value: Optional[str] = None
    method_fmt: Optional[str] = None
    nice_value: Optional[int] = None
    normalizer: Optional[HttpRequestRuleNormalizerType] = None
    normalizer_full: Optional[bool] = None
    normalizer_strict: Optional[bool] = None
    path_fmt: Optional[str] = None
    path_match: Optional[str] = None
    protocol: Optional[IPProtocol] = None
    redir_code: Optional[int] = None
    redir_option: Optional[str] = None
    redir_type: Optional[RedirectType] = None
    redir_value: Optional[str] = None
    resolvers: Optional[str] = None
    return_content: Optional[str] = None
    return_content_type: Optional[str] = None
    return_status_code: Optional[int] = None


# Backend Configuration
@dataclass
class Backend:
    name: str
    mode: Optional[ProxyProtocol] = None
    balance: Optional[Balance] = None
    httpchk: Optional[HttpHealthCheck] = None
    httpchk_params: Optional[HttpCheckParams] = None
    ignore_persist: Optional[IgnorePersist] = None
    abortonclose: Optional[EnableDisableEnum] = None
    accept_invalid_http_response: Optional[EnableDisableEnum] = None
    adv_check: Optional[AdvancedHealthCheckType] = None
    allbackups: Optional[EnableDisableEnum] = None
    bind_process: Optional[str] = None
    check_timeout: Optional[int] = None
    checkcache: Optional[EnableDisableEnum] = None
    compression: Optional[Compression] = None
    connect_timeout: Optional[int] = None
    description: Optional[str] = None
    disabled: Optional[bool] = None
    enabled: Optional[bool] = None
    error_files: Optional[List[ErrorFile]] = field(default_factory=list)
    errorloc302: Optional[ErrorLoc] = None
    errorloc303: Optional[ErrorLoc] = None
    external_check: Optional[EnableDisableEnum] = None
    external_check_command: Optional[str] = None
    external_check_path: Optional[str] = None
    fullconn: Optional[int] = None
    nolinger: Optional[EnableDisableEnum] = None
    forwardfor: Optional[ForwardFor] = None
    mysql_check_params: Optional[MySqlVersionCheckType] = None
    pgsql_check_params: Optional[PostgresSqlCheckParams] = None
    prefer_last_server: Optional[EnableDisableEnum] = None
    queue_timeout: Optional[int] = None
    redispatch: Optional[Redispatch] = None
    retries: Optional[int] = None
    retry_on: Optional[str] = None
    server_fin_timeout: Optional[int] = None
    server_state_file_name: Optional[str] = None
    server_timeout: Optional[int] = None
    smtpchk_params: Optional[SmtpCheckParams] = None
    splice_auto: Optional[EnableDisableEnum] = None
    splice_request: Optional[EnableDisableEnum] = None
    splice_response: Optional[EnableDisableEnum] = None
    spop_check: Optional[EnableDisableEnum] = None
    srvtcpka: Optional[EnableDisableEnum] = None
    srvtcpka_cnt: Optional[int] = None
    srvtcpka_idle: Optional[int] = None
    srvtcpka_intvl: Optional[int] = None
    independent_streams: Optional[EnableDisableEnum] = None
    log_health_checks: Optional[EnableDisableEnum] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.name:
            raise ValueError("[Backend] - The 'name' field is required.")


# Frontend Configuration
@dataclass
class Frontend:
    name: str
    mode: Optional[ProxyProtocol] = None
    default_backend: Optional[str] = None
    log_format: Optional[str] = None
    description: Optional[str] = None
    log_format_sd: Optional[str] = None
    log_tag: Optional[str] = None
    logsap: Optional[EnableDisableEnum] = None
    maxconn: Optional[int] = None
    nolinger: Optional[EnableDisableEnum] = None
    socket_stats: Optional[EnableDisableEnum] = None
    splice_auto: Optional[EnableDisableEnum] = None
    splice_request: Optional[EnableDisableEnum] = None
    splice_response: Optional[EnableDisableEnum] = None
    httplog: Optional[bool] = None
    httpslog: Optional[EnableDisableEnum] = None
    error_log_format: Optional[str] = None
    enabled: Optional[bool] = None
    errorloc302: Optional[ErrorLoc] = None
    errorloc303: Optional[ErrorLoc] = None
    error_files: Optional[List[ErrorFile]] = field(default_factory=list)
    compression: Optional[Compression] = None
    forwardfor: Optional[ForwardFor] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.name:
            raise ValueError("[Frontend] - The 'name' field is required.")


# Bind Configuration
@dataclass
class Bind:
    name: str
    address: Optional[str] = None
    port: Optional[int] = None
    maxconn: Optional[int] = None
    ssl: Optional[bool] = None
    ssl_cafile: Optional[str] = None
    ssl_certificate: Optional[str] = None
    ssl_max_ver: Optional[SSLVersion] = None
    ssl_min_ver: Optional[SSLVersion] = None
    strict_sni: Optional[bool] = None
    tcp_user_timeout: Optional[int] = None
    tfo: Optional[bool] = None
    thread: Optional[str] = None
    tls_ticket_keys: Optional[str] = None
    transparent: Optional[bool] = None
    uid: Optional[str] = None
    user: Optional[str] = None
    v4v6: Optional[bool] = None
    v6only: Optional[bool] = None
    verify: Optional[Requirement] = None
    no_alpn: Optional[bool] = None
    no_ca_names: Optional[bool] = None
    no_sslv3: Optional[bool] = None
    no_tls_tickets: Optional[bool] = None
    no_tlsv10: Optional[bool] = None
    no_tlsv11: Optional[bool] = None
    no_tlsv12: Optional[bool] = None
    no_tlsv13: Optional[bool] = None
    force_sslv3: Optional[bool] = None
    force_tlsv10: Optional[bool] = None
    force_tlsv11: Optional[bool] = None
    force_tlsv12: Optional[bool] = None
    force_tlsv13: Optional[bool] = None
    generate_certificates: Optional[bool] = None
    level: Optional[FrontendLevel] = None
    crt_list: Optional[str] = None
    ca_ignore_err: Optional[str] = None
    ca_sign_file: Optional[str] = None
    ca_sign_pass: Optional[str] = None
    ca_verify_file: Optional[str] = None
    ciphers: Optional[str] = None
    ciphersuites: Optional[str] = None
    client_sigalgs: Optional[str] = None
    crl_file: Optional[str] = None
    crt_ignore_err: Optional[str] = None
    curves: Optional[str] = None
    defer_accept: Optional[str] = None
    accept_proxy: Optional[bool] = None
    allow_0rtt: Optional[bool] = None
    alpn: Optional[str] = None

    def __post_init__(self):

        # Ajoutez ici des validations si nécessaire
        if not self.name:
            raise ValueError("[Bind] - The 'name' field is required.")


# ACL Configuration
@dataclass
class Acl:
    acl_name: str
    criterion: str
    index: int
    value: str


# Backend Switching Rule Configuration
@dataclass
class BackendSwitchingRule:
    cond: ConditionType
    cond_test: str
    index: int
    name: str
