from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx
from ...module_utils.sonarqube.models import Group

try:
    import requests
    from requests.exceptions import HTTPError
    from ..sonarqube.client_group_global_permissions import GroupGlobalPermissionClient
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class GroupClient:
    """
    Client for interacting with the Sonarqube API for Group.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Définir la constante pour application/json
    CONTENT_TYPE_MERGE_JSON = "application/merge-patch+json"

    # Get Group URI (Return List so that find the right group that match)
    GET_GROUP_URI = "api/v2/authorizations/groups?q={name}"

    # Create Group URI
    CREATE_GROUP_URI = "api/v2/authorizations/groups"

    # Update Group URI
    UPDATE_GROUP_URI = "api/v2/authorizations/groups/{id_update}"

    # Delete Group URI
    DELETE_GROUP_URI = "api/v2/authorizations/groups/{id_delete}"

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
            raise ValueError("GroupClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

        # Intialize Global Permission Client
        self.global_permission_client = GroupGlobalPermissionClient(
            base_url=base_url,
            auth=auth
        )

    def get_group(self, name: str = '') -> Group:
        """
        Retrieves the details of given Group from the Sonarqube API.

        Args:
            name (str): The name of the Group to Retrieve

        Returns:
            Group: Details of Group in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group name is None
        if len(name.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Group Retrieve : 'name' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_GROUP_URI.format(
                name=name.strip()
            )
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract List
            groups = response.json()['groups']

            # If List is empty
            if len(groups) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - Group not Found (Name : {name})".format(
                        code="404",
                        name=name
                    )
                )

            # Return JSON
            return Group.from_api_response(response=groups[0])

        else:

            # Raise Exception
            response.raise_for_status()

    def create_group(self, group: Group = None) -> Group:
        """
        Create a Group on SonarQube API.

        Args:
            group (Group): The Group to Create.

        Returns:
            Group: Details of Created Group in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group is None
        if group is None:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Group creation : 'group' details are required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CREATE_GROUP_URI
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            json=group.to_api_json(),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Initialize Global Permissions
            self.global_permission_client.initialize_permissions(
                group_name=group.group_name,
                permission_names=group.global_permissions
            )

            # Return JSON
            return Group.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def update_group(self, group: Group = None) -> Group:
        """
        Update a Group on SonarQube API.

        Args:
            group (Group): The Group to Update.

        Returns:
            Group: Details of Updated Group in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group is None
        if group is None:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Group Update : 'group' details are required")

        # If group name is None
        if group.group_name is None or not group.group_name or len(group.group_name.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Group Update : 'group_name' is required")

        # Find The Group
        existing_group = self.get_group(group.group_name.strip())

        # Get Group ID
        group_id = existing_group.group_id

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.UPDATE_GROUP_URI.format(
                id_update=group_id
            )
        )

        # Execute Request
        response = requests.patch(
            url=url,
            auth=self.auth,
            json=group.to_api_json(),
            headers={
                "Content-Type": self.CONTENT_TYPE_MERGE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Initialize Global Permissions
            self.global_permission_client.initialize_permissions(
                group_name=group.group_name,
                permission_names=group.global_permissions
            )

            # Return JSON
            return Group.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_group(self, name: str = ''):
        """
        Delete Group from the Sonarqube API.

        Args:
            name (str): The Login of the Group to Delete

        Returns:
            dict: Details of Operation in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group name is None
        if len(name.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupClient] - Group Delete : 'name' is required")

        # Find The Group
        existing_group = self.get_group(name.strip())

        # Get Group ID
        group_id = existing_group.group_id

        # Clean Global Permissions
        self.global_permission_client.delete_all_permissions(
            group_name=name.strip()
        )

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_GROUP_URI.format(
                id_delete=group_id
            )
        )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
