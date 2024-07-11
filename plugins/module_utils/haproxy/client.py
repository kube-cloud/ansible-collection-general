from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_backends import BackendClient
from .client_frontends import FrontendClient
from .client_transactions import TransactionClient
from .client_configurations import ConfigurationClient
from .client_acls import AclClient
from .client_servers import ServerClient
from .client_backend_switching_rules import BackendSwitchingRuleClient
from .client_http_request_rules import HttpRequestRuleClient
from .client_binds import BindClient
from .client_ssl_certificates import SslCertificateClient

try:
    from requests.auth import HTTPBasicAuth     # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class Client:
    """
    Client for interacting with the HAProxy Data Plane API.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Servers URI
    SERVERS_URI = "services/haproxy/configuration/servers"

    # URL Format
    URL_TEMPLATE = "{base_url}/{version}/{uri}"

    def __init__(self, base_url: str, api_version: str, username: str, password: str):
        """
        Initializes the HAProxyClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the HAProxy Data Plane API.
            api_version (str): The HAProxy Data Plane API Version (v1 or v2)
            username (str): The username for HTTP basic authentication.
            password (str): The password for HTTP basic authentication.
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[HAProxyClient] - Initialization failed : 'base_url' is required")

        # If Username is not Provided
        if not username:

            # Raise Value Exception
            raise ValueError("[HAProxyClient] - Initialization failed : 'username' is required")

        # If Password is not Provided
        if not password:

            # Raise Value Exception
            raise ValueError("[HAProxyClient] - Initialization failed : 'password' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version if api_version else "v2"

        # Initialize Basic Authentication
        self.auth = HTTPBasicAuth(username, password)

        # Initialize Backend Client
        self.backend = BackendClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Frontend Client
        self.frontend = FrontendClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Transaction Client
        self.transaction = TransactionClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Configuration Client
        self.configuration = ConfigurationClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize ACL Client
        self.acl = AclClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Backend Switching Rule Client
        self.besr = BackendSwitchingRuleClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Bind Client
        self.bind = BindClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Server Client
        self.server = ServerClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize Http Request Rule Client
        self.request_rule = HttpRequestRuleClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )

        # Initialize SSL Certificate Client
        self.ssl_certificate = SslCertificateClient(
            base_url=base_url,
            api_version=api_version,
            auth=self.auth
        )


# Build and Return HA Proxy Client from Dictionnary Vars
def haproxy_client(params: dict):

    # Required Module Keys
    credential_keys = [
        'base_url',
        'api_version',
        'username',
        'password'
    ]

    # Match Required Keys with Parameters (Build Boolean array)
    credential_parameters = [cred_key in params for cred_key in credential_keys]

    # If All Credentials keyx are present in Module Parameters
    if not all(credential_parameters):

        # Error Message for Module
        raise ValueError("Missing Client API Parameters")

    # Build and Return Client
    return Client(**{credential: params[credential] for credential in credential_keys})
