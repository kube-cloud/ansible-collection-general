from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_settings import SettingsClient
from .client_user import UserClient

try:
    from requests.auth import HTTPBasicAuth     # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class Client:
    """
    Client for interacting with the SonarQube API.

    Attributes:
        base_url (str): The base URL of the SonarQube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initializes the SonarQubeClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the SonarQube API.
            username (str): The username for HTTP basic authentication.
            password (str): The password for HTTP basic authentication.
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'base_url' is required")

        # If Username is not Provided
        if not username:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'username' is required")

        # If Password is not Provided
        if not password:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'password' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = HTTPBasicAuth(username, password)

        # Initialize Settings Client
        self.settings = SettingsClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize User Client
        self.user = UserClient(
            base_url=base_url,
            auth=self.auth
        )


# Build and Return Sonarqube Client from Dictionnary Vars
def sonarqube_client(params: dict):

    # Required Module Keys
    credential_keys = [
        'base_url',
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
