from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import Bind
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class BindClient:
    """
    Client for interacting with the HAProxy Data Plane API for Bind.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Binds URI
    BINDS_URI = "services/haproxy/configuration/binds"

    # Bind URI
    BIND_URI = "services/haproxy/configuration/binds/{name}"

    # GET Acl URI Template
    GET_BIND_URI_TEMPLATE = "{bind_uri}?parent_type={parent_type}&parent_name={parent_name}"

    # Bind URI Template with Transaction ID
    BIND_URI_TEMPLATE_TX = "{bind_uri}?transaction_id={transaction_id}&parent_type={parent_type}&parent_name={parent_name}"

    # Bind URI Template with Config Version and Force Reload
    BIND_URI_TEMPLATE_VERSION = "{bind_uri}?version={config_version}&force_reload={force_reload}&parent_type={parent_type}&parent_name={parent_name}"

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
            raise ValueError("[BindClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[BindClient] - Initialization failed : 'auth' is required")

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

    def get_binds(self):
        """
        Retrieves the list of Binds from the HAProxy Data Plane API.

        Returns:
            list: A list of Binds in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.BINDS_URI,
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

    def get_bind(self, name: str, parent_name: str, parent_type: str = 'frontend'):
        """
        Retrieves the details of given Bind (name) from the HAProxy Data Plane API.

        Args:
            name (str): The name of the Bind to retrieve details for.
            parent_name (str): The name of the Parent
            parent_type (str): The Type of the Parent

        Returns:
            dict: Details of Bind in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_BIND_URI_TEMPLATE.format(
                bind_uri=self.BIND_URI.format(name=name),
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

    def create_bind(self, bind: Bind, transaction_id: str, parent_name: str, parent_type: str = 'frontend', force_reload: bool = True):
        """
        Create a Bind on HAProxy API.

        Args:
            bind (Bind): The bind to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Bind in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_TX.format(
                bind_uri=self.BINDS_URI,
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_VERSION.format(
                bind_uri=self.BINDS_URI,
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_bind_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(bind),
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

    def update_bind(self, name: str, bind: Bind, transaction_id: str, parent_name: str, parent_type: str = 'frontend', force_reload: bool = True):
        """
        Update a Bind on HAProxy API.

        Args:
            name (str): The Bind Name
            bind (Bind): The bind to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Bind in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_TX.format(
                bind_uri=self.BIND_URI.format(name=name),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_VERSION.format(
                bind_uri=self.BIND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_bind_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(bind),
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

    def delete_bind(self, name: str, transaction_id: str, parent_name: str, parent_type: str = 'frontend', force_reload: bool = True):
        """
        Delete a Bind on HAProxy API.

        Args:
            name (str): The Bind Name
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_TX.format(
                bind_uri=self.BIND_URI.format(name=name),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_bind_uri = self.BIND_URI_TEMPLATE_VERSION.format(
                bind_uri=self.BIND_URI.format(name=name),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_bind_uri,
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
