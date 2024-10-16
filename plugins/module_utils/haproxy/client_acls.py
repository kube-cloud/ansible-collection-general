from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ...module_utils.commons import filter_none, is_2xx
from .models import Acl
from .client_configurations import ConfigurationClient
from typing import List

try:
    import requests
    from requests.exceptions import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class AclClient:
    """
    Client for interacting with the HAProxy Data Plane API for Acl.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Acls URI
    ACLS_URI = "services/haproxy/configuration/acls"

    # Get Acl By Name URI
    GET_ACL_BY_NAME_URI = "{acl_uri}?parent_type={parent_type}&parent_name={parent_name}&acl_name={acl_name}"

    # Get Acl URI
    ACL_URI = "services/haproxy/configuration/acls/{index}"

    # GET Acl URI Template
    GET_ACL_URI_TEMPLATE = "{acl_uri}?parent_type={parent_type}&parent_name={parent_name}"

    # Acl URI Template with Transaction ID
    ACL_URI_TEMPLATE_TX = "{acl_uri}?transaction_id={transaction_id}&parent_type={parent_type}&parent_name={parent_name}"

    # Acl URI Template with Config Version and Force Reload
    ACL_URI_TEMPLATE_VERSION = "{acl_uri}?version={config_version}&force_reload={force_reload}&parent_type={parent_type}&parent_name={parent_name}"

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
            raise ValueError("[AclClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[AclClient] - Initialization failed : 'auth' is required")

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

    def get_acls(self, parent_name: str, parent_type: str = 'backend') -> List[Acl]:
        """
        Retrieves the list of Acls from the HAProxy Data Plane API.

        Returns:
            list: A list of Acls in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_ACL_URI_TEMPLATE.format(
                acl_uri=self.ACLS_URI,
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
            return Acl.from_api_responses(response.json()['data'])

        else:

            # Raise Exception
            response.raise_for_status()

    def get_acl_by_name(self, acl_name: str, parent_name: str, parent_type: str = 'backend') -> Acl:
        """
        Retrieves the details of given Acl (name) from the HAProxy Data Plane API.

        Args:
            name (str): The Name of the Acl to retrieve details for.
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Acl Parent

        Returns:
            dict: Details of Acl in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_ACL_BY_NAME_URI.format(
                acl_uri=self.ACLS_URI,
                parent_type=parent_type,
                parent_name=parent_name,
                acl_name=acl_name
            ),
            version=self.api_version
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Extract Datas
            acls = response.json()['data']

            # If List is empty
            if len(acls) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - No ACL Found (Name : {acl_name}({parent_name}/{parent_type})".format(
                        code="404",
                        acl_name=acl_name,
                        parent_name=parent_name,
                        parent_type=parent_type
                    )
                )

            # Return JSON
            return Acl.from_api_response(acls[0])

        else:

            # Raise Exception
            response.raise_for_status()

    def get_acl(self, index: int, parent_name: str, parent_type: str = 'backend'):
        """
        Retrieves the details of given Acl (name) from the HAProxy Data Plane API.

        Args:
            index (int): The Index of the Acl to retrieve details for.
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Acl Parent

        Returns:
            dict: Details of Acl in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_ACL_URI_TEMPLATE.format(
                acl_uri=self.ACL_URI.format(index=index),
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

    def create_acl(self, acl: Acl, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Create a Acl on HAProxy API.

        Args:
            acl (Acl): The acl to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Acl in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_acl_uri = self.ACL_URI_TEMPLATE_TX.format(
                acl_uri=self.ACLS_URI,
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_acl_uri = self.ACL_URI_TEMPLATE_VERSION.format(
                acl_uri=self.ACLS_URI,
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_acl_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(acl),
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

    def update_acl(self, index: int, acl: Acl, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Update a Acl on HAProxy API.

        Args:
            index (int): The Acl Index
            acl (Acl): The acl to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the Acl Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Acl in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_acl_uri = self.ACL_URI_TEMPLATE_TX.format(
                acl_uri=self.ACL_URI.format(index=index),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_acl_uri = self.ACL_URI_TEMPLATE_VERSION.format(
                acl_uri=self.ACL_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_acl_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(acl),
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

    def delete_acl(self, index: int, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Delete a Acl on HAProxy API.

        Args:
            index (str): The Acl Index
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
            delete_acl_uri = self.ACL_URI_TEMPLATE_TX.format(
                acl_uri=self.ACL_URI.format(index=index),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            delete_acl_uri = self.ACL_URI_TEMPLATE_VERSION.format(
                acl_uri=self.ACL_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=delete_acl_uri,
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
