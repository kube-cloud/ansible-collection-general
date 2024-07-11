from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import Backend
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class BackendClient:
    """
    Client for interacting with the HAProxy Data Plane API for Backend.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Backends URI
    BACKENDS_URI = "services/haproxy/configuration/backends"

    # Backend URI
    BACKEND_URI = "services/haproxy/configuration/backends/{name}"

    # Backend URI Template with Transaction ID
    BACKEND_URI_TEMPLATE_TX = "{backend_uri}?transaction_id={transaction_id}"

    # Backend URI Template with Config Version and Force Reload
    BACKEND_URI_TEMPLATE_VERSION = "{backend_uri}?version={config_version}&force_reload={force_reload}"

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
            raise ValueError("[BackendClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[BackendClient] - Initialization failed : 'auth' is required")

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

    def get_backends(self):
        """
        Retrieves the list of Backends from the HAProxy Data Plane API.

        Returns:
            list: A list of Backends in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.BACKENDS_URI,
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

    def get_backend(self, name: str):
        """
        Retrieves the details of given Backend (name) from the HAProxy Data Plane API.

        Args:
            name (str): The name of the Backend to retrieve details for.

        Returns:
            dict: Details of Backend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.BACKEND_URI.format(name=name),
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

    def create_backend(self, backend: Backend, transaction_id: str, force_reload: bool = True):
        """
        Create a Backend on HAProxy API.

        Args:
            backend (Backend): The backend to create.
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Backend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_TX.format(
                backend_uri=self.BACKENDS_URI,
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_VERSION.format(
                backend_uri=self.BACKENDS_URI,
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_backend_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(backend),
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

    def update_backend(self, name: str, backend: Backend, transaction_id: str, force_reload: bool = True):
        """
        Update a Backend on HAProxy API.

        Args:
            name (str): The Backend Name
            backend (Backend): The backend to create.
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Backend in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_TX.format(
                backend_uri=self.BACKEND_URI.format(name=name),
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_VERSION.format(
                backend_uri=self.BACKEND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_backend_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(backend),
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

    def delete_backend(self, name: str, transaction_id: str, force_reload: bool = True):
        """
        Delete a Backend on HAProxy API.

        Args:
            name (str): The Backend Name
            transaction_id (str): Started Transaction ID
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_TX.format(
                backend_uri=self.BACKEND_URI.format(name=name),
                transaction_id=transaction_id
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_backend_uri = self.BACKEND_URI_TEMPLATE_VERSION.format(
                backend_uri=self.BACKEND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_backend_uri,
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
