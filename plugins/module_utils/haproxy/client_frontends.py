from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import Frontend
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class FrontendClient:
    """
    Client for interacting with the HAProxy Data Plane API for Frontend.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Frontends URI
    FRONTENDS_URI = "services/haproxy/configuration/frontends"

    # Frontend URI
    FRONTEND_URI = "services/haproxy/configuration/frontends/{name}"

    # Frontend URI Template with Transaction ID
    FRONTEND_URI_TEMPLATE_TX = "{frontend_uri}?transaction_id={transaction_id}"

    # Frontend URI Template with Config Version and Force Reload
    FRONTEND_URI_TEMPLATE_VERSION = "{frontend_uri}?version={config_version}&force_reload={force_reload}"

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
            raise ValueError("[FrontendClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[FrontendClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version if api_version else "v2"

        # Initialize Basic Authentication
        self.auth = auth

        # Initialize Configuration Client
        self.configuration = ConfigurationClient(
            base_url=base_url,
            api_version=api_version,
            auth=auth
        )

    def get_frontends(self):
        """
        Retrieves the list of Frontends from the HAProxy Data Plane API.

        Returns:
            list: A list of Frontends in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.FRONTENDS_URI,
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

    def get_frontend(self, name: str):
        """
        Retrieves the details of given Frontend (name) from the HAProxy Data Plane API.

        Args:
            name (str): The name of the frontend to retrieve details for.

        Returns:
            dict: Details of Frontend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.FRONTEND_URI.format(name=name),
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

    def create_frontend(self, frontend: Frontend, transaction_id: str, force_reload: bool = True):
        """
        Create a Frontend on HAProxy API.

        Args:
            frontend (Frontend): The frontend to create.
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Frontend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_TX.format(
                frontend_uri=self.FRONTENDS_URI,
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_VERSION.format(
                frontend_uri=self.FRONTENDS_URI,
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_frontend_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(frontend),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            },
            auth=self.auth
        )

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def update_frontend(self, name: str, frontend: Frontend, transaction_id: str, force_reload: bool = True):
        """
        Update a Frontend on HAProxy API.

        Args:
            name (str): The Frontend Name
            frontend (Frontend): The frontend to create.
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Frontend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_TX.format(
                frontend_uri=self.FRONTEND_URI.format(name=name),
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_VERSION.format(
                frontend_uri=self.FRONTEND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_frontend_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(frontend),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            },
            auth=self.auth
        )

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_frontend(self, name: str, transaction_id: str, force_reload: bool = True):
        """
        Delete a Frontend on HAProxy API.

        Args:
            name (str): The Frontend Name
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_TX.format(
                frontend_uri=self.FRONTEND_URI.format(name=name),
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_frontend_uri = self.FRONTEND_URI_TEMPLATE_VERSION.format(
                frontend_uri=self.FRONTEND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_frontend_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.delete(
            url=url,
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            },
            auth=self.auth
        )

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
