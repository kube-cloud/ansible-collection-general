from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx

try:
    import requests
    from requests.exceptions import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class SettingsClient:
    """
    Client for interacting with the Sonarqube API for Acl.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Get Setting URI
    GET_SETTING_URI = "/api/settings/values/?keys={key}"

    # Create Setting URI
    CREATE_SETTING_URI = "/api/settings/set/?key={key}"

    # Delete Setting URI
    DELETE_SETTING_URI = "/api/settings/reset/?keys={key}"

    # URL Format
    URL_TEMPLATE = "{base_url}/{uri}"

    def __init__(self, base_url: str, api_version: str, auth):
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
            raise ValueError("SettingsClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[SettingsClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def get_setting(self, key: str, component: str = ''):
        """
        Retrieves the details of given Setting (key/component) from the Sonarqube API.

        Args:
            key (str): The Key of the Setting to Retrieve
            component (str): The Name of the Setting Parent Component

        Returns:
            dict: Details of Setting in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_SETTING_URI.format(
                parent_type=key
            )
        )

        # If Component is Provided
        if component and component.strip():

            # Add Component Parameter
            url = "{url}&component={component}".format(
                url=url,
                component=component
            )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Extract Settings
            settings = response.json().settings

            # If Settings is empty
            if len(settings) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - Setting not Found (Key : {key})".format(
                        code="404",
                        key=key
                    )
                )

            # Return JSON
            return settings[0]

        else:

            # Raise Exception
            response.raise_for_status()

    def create_setting(self, key: str, component: str = '', value: str = '', values: list = None):
        """
        Create a Setting on SonarQube API.

        Args:
            key (str): The setting Key.
            component (str): The setting Parent Component.
            value (str): The setting Value.
            values (list): The setting values.

        Returns:
            dict: Details of Created Setting in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If Values is None
        if values is None:

            # Initialize to Empty
            values = []

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CREATE_SETTING_URI.format(
                key=key.strip()
            )
        )

        # If Value is Provided
        if value and value.strip():

            # Add Component Parameter
            url = "{url}&value={value}".format(
                url=url,
                value=value.strip()
            )

        # If component is Provided
        if component and component.strip():

            # Add Component Parameter
            url = "{url}&component={component}".format(
                url=url,
                component=component.strip()
            )

        # If component is Provided
        if len(values) > 0:

            # Iterate on Values
            for item in values:

                # Add Item to URL
                url = "{url}&values={item}".format(
                    url=url,
                    item=item
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
                "key": key,
                "status": "created",
                "status_code": response.status_code
            }

        else:

            # Raise Exception
            response.raise_for_status()

    def update_setting(self, key: str, component: str = '', value: str = '', values: list = None):
        """
        Update a Setting on SonarQube API.

        Args:
            key (str): The setting Key.
            component (str): The setting Parent Component.
            value (str): The setting Value.
            values (list): The setting values.

        Returns:
            dict: Details of Created Setting in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Call Create Setting
        return self.create_setting(key=key, component=component, value=value, values=values)

    def delete_setting(self, key: str, component: str = ''):
        """
        Delete Setting (key) from the Sonarqube API.

        Args:
            key (str): The Key of the Setting to Retrieve
            component (str): The Name of the Setting Parent Component

        Returns:
            dict: Details of Setting in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_SETTING_URI.format(
                key=key
            )
        )

        # If Component is Provided
        if component and component.strip():

            # Add Component Parameter
            url = "{url}&component={component}".format(
                url=url,
                component=component
            )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
