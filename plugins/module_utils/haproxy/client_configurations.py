from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import is_2xx

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class ConfigurationClient:
    """
    Client for interacting with the HAProxy Data Plane API for Configuration.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Backends URI
    CONFIG_VERSION_URI = "services/haproxy/configuration/version"

    # URL Format
    URL_TEMPLATE = "{base_url}/{version}/{uri}"

    def __init__(self, base_url: str, api_version: str, auth):
        """
        Initializes the HAProxyClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the HAProxy Data Plane API.
            api_version (str): The HAProxy Data Plane API Version (v1 or v2)
            auth (HTTPBasicAuth): The Authentication Configuration
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[ConfigurationClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[ConfigurationClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version if api_version else "v2"

        # Initialize Basic Authentication
        self.auth = auth

    def get_configuration_version(self):
        """
        Get HAProxy Configuration Version.

        Returns:
            integer: Configuration Version.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CONFIG_VERSION_URI,
            version=self.api_version
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()
