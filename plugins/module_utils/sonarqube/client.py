from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_settings import SettingsClient
from .client_user import UserClient
from .client_group import GroupClient
from .client_group_global_permissions import GroupGlobalPermissionClient
from .client_group_membership import GroupMembershipClient
from .client_alm_settings_github import AlmSettingsGithubClient
from .client_alm_settings_gitlab import AlmSettingsGitlabClient
from .client_alm_settings_azure import AlmSettingsAzureClient
from .client_alm_settings_bitbucket import AlmSettingsBitbucketClient
from .client_alm_settings_bitbucket_cloud import AlmSettingsBitbucketCloudClient
from .client_alm_access_token import AlmAccessTokenClient

try:
    from requests.auth import HTTPBasicAuth     # type: ignore
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class Client:
    """
    Client for interacting with the SonarQube API.

    Attributes:
        base_url (str): The base URL of the SonarQube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initializes the SonarQubeClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the SonarQube API.
            username (str): The username for HTTP basic authentication.
            password (str): The password for HTTP basic authentication.
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'base_url' is required")

        # If Username is not Provided
        if not username:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'username' is required")

        # If Password is not Provided
        if not password:

            # Raise Value Exception
            raise ValueError("[SonarQubeClient] - Initialization failed : 'password' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = HTTPBasicAuth(username, password)

        # Initialize Settings Client
        self.settings = SettingsClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize User Client
        self.user = UserClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize Group Client
        self.group = GroupClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize Group Membership Client
        self.membership = GroupMembershipClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize Group Membership Client
        self.group_global_permission = GroupGlobalPermissionClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize ALM Settings Github Client
        self.alm_settings_github = AlmSettingsGithubClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize ALM Settings Gitlab Client
        self.alm_settings_gitlab = AlmSettingsGitlabClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize ALM Settings Azure Client
        self.alm_settings_azure = AlmSettingsAzureClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize ALM Settings Bitbucket Client
        self.alm_settings_bitbucket = AlmSettingsBitbucketClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize ALM Settings Bitbucket Cloud Client
        self.alm_settings_bitbucket_cloud = AlmSettingsBitbucketCloudClient(
            base_url=base_url,
            auth=self.auth
        )

        # Initialize Access Token ALM Client
        self.alm_access_token = AlmAccessTokenClient(
            base_url=base_url,
            auth=self.auth
        )


# Build and Return Sonarqube Client from Dictionnary Vars
def sonarqube_client(params: dict):

    # Required Module Keys
    credential_keys = [
        'base_url',
        'username',
        'password'
    ]

    # Match Required Keys with Parameters (Build Boolean array)
    credential_parameters = [cred_key in params for cred_key in credential_keys]

    # If All Credentials keyx are present in Module Parameters
    if not all(credential_parameters):

        # Error Message for Module
        raise ValueError("Missing Client API Parameters")

    # Build and Return Client
    return Client(**{credential: params[credential] for credential in credential_keys})
