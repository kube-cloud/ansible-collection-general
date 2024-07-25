from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx
from ...module_utils.sonarqube.models import GroupGlobalPermission
from typing import List

try:
    import requests
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class GroupGlobalPermissionClient:
    """
    Client for interacting with the Sonarqube API for GroupGlobalPermission.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Add Group Global Permission URI
    CREATE_GLOBAL_PERMISSION_URI = "api/permissions/add_group?groupName={group}&permission={permission}"

    # Delete Group Global Permission URI
    DELETE_GROUP_GLOBAL_PERMISSION_URI = "api/permissions/remove_group?groupName={group}&permission={permission}"

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
            raise ValueError("GroupGlobalPermissionClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[GroupGlobalPermissionClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def create_permission(self, permission: GroupGlobalPermission = None) -> GroupGlobalPermission:
        """
        Create a GroupGlobalPermission on SonarQube API.

        Args:
            permission (GroupGlobalPermission): The Permission to Create.

        Returns:
            GroupGlobalPermission: Details of Created Permission in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If permission is None
        if permission is None:

            # Raise Value Exception
            raise ValueError("[GroupGlobalPermissionClient] - Creation : 'permission' details are required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CREATE_GLOBAL_PERMISSION_URI.format(
                group=permission.group_name.strip(),
                permission=permission.permission_name.strip()
            )
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return permission

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_permission(self, permission: GroupGlobalPermission = None):
        """
        Remove a GroupGlobalPermission on SonarQube API.

        Args:
            permission (GroupGlobalPermission): The Permission to Remove.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If permission is None
        if permission is None:

            # Raise Value Exception
            raise ValueError("[GroupGlobalPermissionClient] - Deletion : 'permission' details are required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_GROUP_GLOBAL_PERMISSION_URI.format(
                group=permission.group_name,
                permission=permission.permission_name
            )
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            }
        )

        # If Not OK
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()

    def delete_all_permissions(self, group_name: str = ''):
        """
        Delete all Group Global Permission on SonarQube API.

        Args:
            group_name (str): The Target Group Name.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If permission is None
        if len(group_name.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupGlobalPermissionClient] - RemoveAll : 'group_name' is required")

        # Iterate on Available Permission List
        for permission_name in GroupGlobalPermission.AVAILABLE_PERMISSIONS:

            # Delete Permission
            self.delete_permission(
                permission=GroupGlobalPermission(
                    group_name=group_name.strip(),
                    permission_name=permission_name
                )
            )

    def initialize_permissions(self, group_name: str = '', permission_names: list[str] = None) -> List[GroupGlobalPermission]:
        """
        Initialize Group Global Permissions from the Sonarqube API.

        Args:
            group_name (str): The Target Group Name
            permission_names (list): The Permissions Names to Associate to the Group

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group_name is blank
        if len(group_name.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupGlobalPermissionClient#initialize_permissions] : 'group_name' is required")

        # Clean Group Permissions
        self.delete_all_permissions(
            group_name=group_name
        )

        # Created Permissions
        permissions = []

        # If Given Permissions Names is not provided
        if permission_names is None:

            # Initialize to Empty
            permission_names = []

        # Iterate on Permission Names
        for permission_name in permission_names:

            # Create Global Permission
            permissions.append(
                self.create_permission(
                    permission=GroupGlobalPermission(
                        group_name=group_name.strip(),
                        permission_name=permission_name.strip()
                    )
                )
            )

        # Return permissions
        return permissions
