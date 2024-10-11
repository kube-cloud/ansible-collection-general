from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_user import UserClient
from ..commons_security import HttpTokenAuth


class Client:
    """
    Client for interacting with the Gitlab API.

    Attributes:
        base_url (str): The base URL of the Gitlab API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    def __init__(self, base_url: str, token: str):
        """
        Initializes the GitlabClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the Gitlab API.
            token (str): The Token for HTTP basic authentication.
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[GitlabClient] - Initialization failed : 'base_url' is required")

        # If token is not Provided
        if not token:

            # Raise Value Exception
            raise ValueError("[GitlabClient] - Initialization failed : 'token' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = HttpTokenAuth(token=token)

        # Initialize User Client
        self.user = UserClient(
            base_url=base_url,
            auth=self.auth
        )


# Build and Return Gitlab Client from Dictionnary Vars
def gitlab_client(params: dict):

    # Required Module Keys
    credential_keys = [
        'base_url',
        'token'
    ]

    # Match Required Keys with Parameters (Build Boolean array)
    credential_parameters = [cred_key in params for cred_key in credential_keys]

    # If All Credentials keyx are present in Module Parameters
    if not all(credential_parameters):

        # Error Message for Module
        raise ValueError("Missing Client API Parameters")

    # Build and Return Client
    return Client(**{credential: params[credential] for credential in credential_keys})
