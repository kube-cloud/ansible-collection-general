from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_configurations import ConfigurationClient
from .commons import is_2xx

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class TransactionClient:
    """
    Client for interacting with the HAProxy Data Plane API for Transactions.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Get All Transactions URI
    GET_ALL_TRANSACTIONS_URI = "services/haproxy/transactions"

    # Create Transaction URI
    TRANSACTION_BY_VERSION_URI = "services/haproxy/transactions?version={config_version}"

    # Validate Transaction URI
    VALIDATE_TRANSACTION_URI = "services/haproxy/transactions/{transaction_id}?force_reload={force_reload}"

    # Cancel Transaction URI
    CANCEL_TRANSACTION_URI = "services/haproxy/transactions/{transaction_id}"

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

    def create_transaction(self):
        """
        Start HAProxy Data Plane API Transaction and Details.

        Returns:
            dict: Details of HAProxy Data Plane API Transaction in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Get Configuration Version
        config_version = self.configuration.get_configuration_version()

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.TRANSACTION_BY_VERSION_URI.format(config_version=config_version),
            version=self.api_version
        )

        # Execute Request
        response = requests.post(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def get_transactions(self, config_version: str = ''):
        """
        Get All Active HAProxy Data Plane API Transaction Details.

        Args:
            config_version (str): The Transaction Configuration Version.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Get Transaction URI
        get_tx_uri = self.GET_ALL_TRANSACTIONS_URI

        # If Configuration Version is provided
        if bool(config_version and config_version.strip()):

            # Initialize TX URI
            get_tx_uri = self.TRANSACTION_BY_VERSION_URI.format(
                config_version=config_version.strip()
            )

        # Build the GET Transaction URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=get_tx_uri,
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

    def get_transaction(self, transaction_id: str):
        """
        Get HAProxy Data Plane API Transaction Details.

        Args:
            transaction_id (str): The Transaction to Fetch.
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CANCEL_TRANSACTION_URI.format(
                transaction_id=transaction_id
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

    def commit_transaction(self, transaction_id: str, force_reload: bool):
        """
        Commit HAProxy Data Plane API Transaction and Details.

        Args:
            transaction_id (str): The Transaction to Commit.
            force_reload (bool): Force HA Proxy Configuration Reload
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.VALIDATE_TRANSACTION_URI.format(
                transaction_id=transaction_id,
                force_reload=force_reload
            ),
            version=self.api_version
        )

        # Execute Request
        response = requests.put(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def cancel_transaction(self, transaction_id: str):
        """
        Cancel HAProxy Data Plane API Transaction and Details.

        Args:
            transaction_id (str): The Transaction to Commit.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CANCEL_TRANSACTION_URI.format(
                transaction_id=transaction_id
            ),
            version=self.api_version
        )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()

    def cancel_transactions(self, config_version: str = ''):
        """
        Cancel All in-progress HAProxy Data Plane API Transaction and Details.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Get Active Transactions
        active_transactions = self.get_transactions(config_version=config_version)

        # Cleaned Transactionx
        cleaned_transations = []

        # If There are Transations
        if active_transactions:

            # Iterate
            for tx in active_transactions:

                # Cancel Transaction
                self.cancel_transaction(transaction_id=tx["id"])

                # Add Cleaned TX to Array
                cleaned_transations.append(tx)

        # Return List of Cleaned TX
        return cleaned_transations
