from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx
from ...module_utils.sonarqube.models import AlmSettingsGitlab

try:
    import requests
    from requests.exceptions import HTTPError
    from urllib.parse import quote
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class AlmSettingsGitlabClient:
    """
    Client for interacting with the Sonarqube API for AlmSettingsGitlab.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Get Settings List URI
    GET_ALL_SETTINGS_URI = "api/alm_settings/list_definitions"

    # Create Setting URI
    CREATE_SETTING_URI = "api/alm_settings/create_gitlab?{parameters}"

    # Update Setting URI
    UPDATE_SETTING_URI = "api/alm_settings/update_gitlab?{parameters}"

    # Delete Setting URI
    DELETE_SETTING_URI = "api/alm_settings/delete?key={key}"

    # URL Format
    URL_TEMPLATE = "{base_url}/{uri}"

    def __init__(self, base_url: str, auth):
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
            raise ValueError("AlmSettingsGitlabClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[AlmSettingsGitlabClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def get_setting(self, key: str = '') -> AlmSettingsGitlab:
        """
        Retrieves the details of given AlmSettingsGitlab from the Sonarqube API.

        Args:
            key (str): The Key of the AlmSettingsGitlab to Retrieve

        Returns:
            AlmSettingsGitlab: Details of AlmSettingsGitlab in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user key is None
        if len(key.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[AlmSettingsGitlabClient] - Retrieve : 'key' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_ALL_SETTINGS_URI
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract Settings
            settings = response.json().get(AlmSettingsGitlab.DEVOPS_PLAFORM.value, [])

            # Find Setting by Key
            setting = next((item for item in settings if item.get('key', '') == key.strip()), None)

            # If List is empty
            if setting is None:

                # Raise Exception
                raise HTTPError(
                    "{code} - AlmSettingsGitlab not Found (Key : {key})".format(
                        code="404",
                        key=key
                    )
                )

            # Return JSON
            return AlmSettingsGitlab.from_api_response(response=setting)

        else:

            # Raise Exception
            response.raise_for_status()

    def create_setting(self, setting: AlmSettingsGitlab = None, encode_parameters: bool = True) -> AlmSettingsGitlab:
        """
        Create a AlmSettingsGitlab on SonarQube API.

        Args:
            setting (AlmSettingsGitlab): The AlmSettingsGitlab to Create.

        Returns:
            AlmSettingsGitlab: Details of Created AlmSettingsGitlab in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If setting is None
        if setting is None:

            # Raise Value Exception
            raise ValueError("[AlmSettingsGitlabClient] - creation : 'setting' details are required")

        # Build Parameter
        parameter = "key={key}&url={url}&personalAccessToken={token}".format(
            key=quote(string=setting.key, safe="") if encode_parameters else setting.key,
            url=quote(string=setting.url, safe="") if encode_parameters else setting.url,
            token=quote(string=setting.personal_access_token, safe="") if encode_parameters else setting.personal_access_token
        )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CREATE_SETTING_URI.format(
                parameters=parameter
            )
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return setting

        else:

            # Raise Exception
            response.raise_for_status()

    def update_setting(self, setting: AlmSettingsGitlab = None, encode_parameters: bool = True) -> AlmSettingsGitlab:
        """
        Update a AlmSettingsGitlab on SonarQube API.

        Args:
            setting (AlmSettingsGitlab): The AlmSettingsGitlab to Update.

        Returns:
            AlmSettingsGitlab: Details of Updated AlmSettingsGitlab in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If setting is None
        if setting is None:

            # Raise Value Exception
            raise ValueError("[AlmSettingsGitlabClient] - Update : 'setting' details are required")

        # Build Parameter
        parameter = "key={key}&url={url}&personalAccessToken={token}".format(
            key=quote(string=setting.key, safe="") if encode_parameters else setting.key,
            url=quote(string=setting.url, safe="") if encode_parameters else setting.url,
            token=quote(string=setting.personal_access_token, safe="") if encode_parameters else setting.personal_access_token
        )

        # If new_key is provided
        if setting.new_key:

            # Add New Key
            parameter = "{parameter}&newKey={newKey}".format(
                parameter=parameter,
                newKey=quote(string=setting.new_key, safe="") if encode_parameters else setting.new_key
            )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.UPDATE_SETTING_URI.format(
                parameters=parameter
            )
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return setting

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_setting(self, key: str = ''):
        """
        Delete AlmSettingsGitlab from the Sonarqube API.

        Args:
            login (str): The Login of the AlmSettingsGitlab to Delete

        Returns:
            dict: Details of Operation in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user login is None
        if len(key.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[AlmSettingsGitlabClient] - Delete : 'key' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_SETTING_URI.format(
                key=key.strip()
            )
        )

        # Execute Request
        response = requests.post(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
