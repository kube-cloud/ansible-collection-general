from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class AlmAccessTokenClient:
    """
    Client for Initialize ALM Access Token with the Sonarqube API.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Update ALM Access Token URI
    POST_ACCESS_TOKEN_URI = "api/alm_integrations/set_pat?almSetting={alm_name}&pat={token}"

    # URL Format
    URL_TEMPLATE = "{base_url}/{uri}"

    def __init__(self, base_url: str, auth):
        """
        Initializes the SonarQube API Client with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the Sonarqube API.
            auth (HTTPBasicAuth): The Authentication Configuration
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("SetAccessTokenAlmClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[SetAccessTokenAlmClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def set_access_token(self, alm_name: str = None, access_token: str = '', token_username: str = None) -> dict:
        """
        Update ALM Access Token on SonarQube API.

        Args:
            alm_name (str): The ALM Name.
            access_token (str): The ALM Token.
            username (str): The ALM Username.

        Returns:
            dift: Operation Result.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If alm_name is None
        if alm_name is None or alm_name.strip() == "":

            # Raise Value Exception
            raise ValueError("[SetAccessTokenAlmClient] : 'alm_name' is required")

        # If access_token is None
        if access_token is None or access_token.strip() == "":

            # Raise Value Exception
            raise ValueError("[SetAccessTokenAlmClient] : 'access_token' is required")

        # Build Parameter
        uri = self.POST_ACCESS_TOKEN_URI.format(
            alm_name=alm_name.strip(),
            token=access_token.strip()
        )

        # If Username is provided
        if token_username is not None and len(token_username.strip()) > 0:

            # Add Username Parameter
            uri = "{uri}&username={token_username}".format(
                uri=uri,
                token_username=token_username.strip()
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=uri
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return {
                "status": response.status_code
            }

        else:

            # Raise Exception
            response.raise_for_status()
