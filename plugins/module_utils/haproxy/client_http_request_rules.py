from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .commons import filter_none, is_2xx
from .models import HttpRequestRule
from .client_configurations import ConfigurationClient

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class HttpRequestRuleClient:
    """
    Client for interacting with the HAProxy Data Plane API for HttpRequestRule.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # HttpRequestRules URI
    HTTP_RQ_RULES_URI = "services/haproxy/configuration/http_request_rules"

    # Get HttpRequestRule URI
    RQ_RULE_URI = "services/haproxy/configuration/http_request_rules/{index}"

    # GET HttpRequestRule URI Template
    GET_RQ_RULE_URI_TEMPLATE = "{http_rq_rule_uri}?parent_type={parent_type}&parent_name={parent_name}"

    # HttpRequestRule URI Template with Transaction ID
    RQ_RULE_URI_TEMPLATE_TX = "{http_rq_rule_uri}?transaction_id={transaction_id}&parent_type={parent_type}&parent_name={parent_name}"

    # HttpRequestRule URI Template with Config Version and Force Reload
    RQ_RULE_URI_TEMPLATE_VERSION = "{http_rq_rule_uri}?version={config_version}&force_reload={force_reload}&parent_type={parent_type}&parent_name={parent_name}"

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
            raise ValueError("[HttpRequestRuleClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[HttpRequestRuleClient] - Initialization failed : 'auth' is required")

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

    def get_rules(self):
        """
        Retrieves the list of HttpRequestRules from the HAProxy Data Plane API.

        Returns:
            list: A list of HttpRequestRules in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.HTTP_RQ_RULES_URI,
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

    def get_rule(self, index: int, parent_name: str, parent_type: str = 'backend'):
        """
        Retrieves the details of given HttpRequestRule (name) from the HAProxy Data Plane API.

        Args:
            index (int): The Index of the HttpRequestRule to retrieve details for.
            parent_name (str): The name of the HttpRequestRule Parent
            parent_type (str): The Type of the HttpRequestRule Parent

        Returns:
            dict: Details of HttpRequestRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_RQ_RULE_URI_TEMPLATE.format(
                http_rq_rule_uri=self.RQ_RULE_URI.format(index=index),
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

    def create_rule(self, rule: HttpRequestRule, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Create a HttpRequestRule on HAProxy API.

        Args:
            rule (HttpRequestRule): The Rule to create.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the HttpRequestRule Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created HttpRequestRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_TX.format(
                http_rq_rule_uri=self.HTTP_RQ_RULES_URI,
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_VERSION.format(
                http_rq_rule_uri=self.HTTP_RQ_RULES_URI,
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_http_rq_rule_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(rule),
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

    def update_rule(self, index: int, rule: HttpRequestRule, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Update a HttpRequestRule on HAProxy API.

        Args:
            index (int): The HttpRequestRule Index
            rule (HttpRequestRule): The rule to update.
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the HttpRequestRule Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created HttpRequestRule in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_TX.format(
                http_rq_rule_uri=self.RQ_RULE_URI.format(index=index),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_VERSION.format(
                http_rq_rule_uri=self.RQ_RULE_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_http_rq_rule_uri,
            version=self.api_version
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(rule),
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

    def delete_rule(self, index: int, transaction_id: str, parent_name: str, parent_type: str = 'backend', force_reload: bool = True):
        """
        Delete a HttpRequestRule on HAProxy API.

        Args:
            index (str): The rule Index
            transaction_id (str): Started Transaction ID
            parent_name (str): The name of the HttpRequestRule Parent
            parent_type (str): The Type of the Parent
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Transaction IF is Provided
        if transaction_id and transaction_id.strip():

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_TX.format(
                http_rq_rule_uri=self.RQ_RULE_URI.format(index=index),
                transaction_id=transaction_id,
                parent_name=parent_name,
                parent_type=parent_type
            )

        else:

            # Get Configuration Version
            config_version = self.configuration.get_configuration_version()

            # Initialize URI
            create_http_rq_rule_uri = self.RQ_RULE_URI_TEMPLATE_VERSION.format(
                http_rq_rule_uri=self.RQ_RULE_URI.format(index=index),
                config_version=config_version,
                force_reload=force_reload,
                parent_name=parent_name,
                parent_type=parent_type
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=create_http_rq_rule_uri,
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
