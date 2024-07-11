from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import BackendSwitchingRule
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class BackendSwitchingRuleClient:
    """
    Client for interacting with the HAProxy Data Plane API for BackendSwitchingRule.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # BackendSwitchingRules URI
    BACKEND_SWITCHING_RULES_URI = "services/haproxy/configuration/backend_switching_rules"

    # Get BackendSwitchingRule URI
    BACKEND_SWITCHING_RULE_URI = "services/haproxy/configuration/backend_switching_rules/{index}"

    # GET BackendSwitchingRule URI Template
    GET_BACKEND_SWITCHING_RULE_URI_TEMPLATE = "{besr_uri}?frontend={frontend_name}"

    # BackendSwitchingRule URI Template with Transaction ID
    BACKEND_SWITCHING_RULE_URI_TEMPLATE_TX = "{besr_uri}?transaction_id={transaction_id}&frontend={frontend_name}"

    # BackendSwitchingRule URI Template with Config Version and Force Reload
    BACKEND_SWITCHING_RULE_URI_TEMPLATE_VERSION = "{besr_uri}?version={config_version}&force_reload={force_reload}&frontend={frontend_name}"

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
            raise ValueError("[BackendSwitchingRuleClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[BackendSwitchingRuleClient] - Initialization failed : 'auth' is required")

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

    def get_backend_switching_rules(self):
        """
        Retrieves the list of BackendSwitchingRules from the HAProxy Data Plane API.

        Returns:
            list: A list of BackendSwitchingRules in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.BACKEND_SWITCHING_RULES_URI,
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

    def get_backend_switching_rule(self, index: int, frontend_name: str):
        """
        Retrieves the details of given BackendSwitchingRule (name) from the HAProxy Data Plane API.

        Args:
            index (int): The Index of the BackendSwitchingRule to retrieve details for.
            frontend_name (str): The name of the Frontend Parent

        Returns:
            dict: Details of BackendSwitchingRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_BACKEND_SWITCHING_RULE_URI_TEMPLATE.format(
                besr_uri=self.BACKEND_SWITCHING_RULE_URI.format(index=index),
                frontend_name=frontend_name
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

    def create_backend_switching_rule(self, besr: BackendSwitchingRule, transaction_id: str, frontend_name: str, force_reload: bool = True):
        """
        Create a BackendSwitchingRule on HAProxy API.

        Args:
            besr (BackendSwitchingRule): The Bacnebd Switching Rule to create.
            transaction_id (str): Started Transaction ID
            frontend_name (str): The name of the Frontend Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created BackendSwitchingRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_TX.format(
                besr_uri=self.BACKEND_SWITCHING_RULES_URI,
                transaction_id=transaction_id,
                frontend_name=frontend_name
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_VERSION.format(
                besr_uri=self.BACKEND_SWITCHING_RULES_URI,
                config_version=config_version,
                force_reload=force_reload,
                frontend_name=frontend_name
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_besr_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(besr),
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

    def update_backend_switching_rule(self, index: int, besr: BackendSwitchingRule, transaction_id: str, frontend_name: str, force_reload: bool = True):
        """
        Update a BackendSwitchingRule on HAProxy API.

        Args:
            index (int): The BackendSwitchingRule Index
            besr (BackendSwitchingRule): The Bacnebd Switching Rule to create.
            transaction_id (str): Started Transaction ID
            frontend_name (str): The name of the Frontend Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created BackendSwitchingRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_TX.format(
                besr_uri=self.BACKEND_SWITCHING_RULE_URI.format(index=index),
                transaction_id=transaction_id,
                frontend_name=frontend_name
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_VERSION.format(
                besr_uri=self.BACKEND_SWITCHING_RULE_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                frontend_name=frontend_name
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_besr_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(besr),
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

    def delete_backend_switching_rule(self, index: int, transaction_id: str, frontend_name: str, force_reload: bool = True):
        """
        Delete a BackendSwitchingRule on HAProxy API.

        Args:
            index (str): The BackendSwitchingRule Index
            transaction_id (str): Started Transaction ID
            transaction_id (str): Started Transaction ID
            frontend_name (str): The name of the Frontend Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_TX.format(
                besr_uri=self.BACKEND_SWITCHING_RULE_URI.format(index=index),
                transaction_id=transaction_id,
                frontend_name=frontend_name
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_besr_uri = self.BACKEND_SWITCHING_RULE_URI_TEMPLATE_VERSION.format(
                besr_uri=self.BACKEND_SWITCHING_RULE_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                frontend_name=frontend_name
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_besr_uri,
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
