from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import Server
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class ServerClient:
    """
    Client for interacting with the HAProxy Data Plane API for Server.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Servers URI
    SERVERS_URI = "services/haproxy/configuration/servers"

    # Get Server URI
    SERVER_URI = "services/haproxy/configuration/servers/{name}"

    # GET Server URI Template
    GET_SERVER_URI_TEMPLATE = "{server_uri}?parent_type={parent_type}&parent_name={parent_name}"

    # Server URI Template with Transaction ID
    SERVER_URI_TEMPLATE_TX = "{server_uri}?transaction_id={transaction_id}&parent_type={parent_type}&parent_name={parent_name}"

    # Server URI Template with Config Version and Force Reload
    SERVER_URI_TEMPLATE_VERSION = "{server_uri}?version={config_version}&force_reload={force_reload}&parent_type={parent_type}&parent_name={parent_name}"

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
            raise ValueError("[ServerClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[ServerClient] - Initialization failed : 'auth' is required")

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

    def get_servers(self):
        """
        Retrieves the list of Servers from the HAProxy Data Plane API.

        Returns:
            list: A list of Servers in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.SERVERS_URI,
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

    def get_server(self, name: str, parent_name: str, parent_type: str = 'backend'):
        """
        Retrieves the details of given Server (name) from the HAProxy Data Plane API.

        Args:
            name (str): The name of the Server to retrieve details for.
            parent_name (str): The name of the Server Parent
            parent_type (str): The Type of the Parent

        Returns:
            dict: Details of Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_SERVER_URI_TEMPLATE.format(
                server_uri=self.SERVER_URI.format(name=name),
                parent_type=parent_type,
                parent_name=parent_name
            ),
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

    def create_server(self, server: Server, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Create a Server on HAProxy API.

        Args:
            server (Server): The server to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Server Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_TX.format(
                server_uri=self.SERVERS_URI,
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_VERSION.format(
                server_uri=self.SERVERS_URI,
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_server_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(server),
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

    def update_server(self, name: str, server: Server, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Update a Server on HAProxy API.

        Args:
            name (str): The Server Name
            server (Server): The server to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Server Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_TX.format(
                server_uri=self.SERVER_URI.format(name=name),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_VERSION.format(
                server_uri=self.SERVER_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_server_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(server),
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

    def delete_server(self, name: str, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Delete a Server on HAProxy API.

        Args:
            name (str): The Server Name
            transaction_id (str): Started Transaction ID
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Server Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_TX.format(
                server_uri=self.SERVER_URI.format(name=name),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_server_uri = self.SERVER_URI_TEMPLATE_VERSION.format(
                server_uri=self.SERVER_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_server_uri,
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
