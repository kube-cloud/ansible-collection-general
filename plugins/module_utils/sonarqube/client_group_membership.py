from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx, is_not_found
from ...module_utils.sonarqube.models import GroupMembership
from typing import List

try:
    import requests
    from requests.exceptions import HTTPError
    from .client import GroupClient
    from .client import UserClient
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class GroupMembershipClient:
    """
    Client for interacting with the Sonarqube API for GroupMembership.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Get User's Memberships URI
    GET_USER_MEMBERSHIPS_URI = "api/v2/authorizations/group-memberships?userId={user_id}&pageSize={page_size}&pageIndex={page_index}"

    # Create Membership Membership URI
    CREATE_MEMBERSHIP_URI = "api/v2/authorizations/group-memberships"

    # Delete Membership URI
    DELETE_MEMBERSHIP_URI = "api/v2/authorizations/group-memberships/{id_delete}"

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
            raise ValueError("GroupMembershipClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[GroupMembershipClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

        # Initialize Group Client
        self.group_client = GroupClient(
            base_url=base_url,
            auth=auth
        )

        # Initialize User Client
        self.user_client = UserClient(
            base_url=base_url,
            auth=auth
        )

    def get_user_memberships(self, user_id: str = '', page_index: int = 1, page_size: int = 500) -> List[GroupMembership]:
        """
        Retrieves the Memberships List of a given user.

        Args:
            user_id (str): The User Identifier of the GroupMembership to Retrieve
            page_index (int): The Result Page Index (default : 1)
            page_size (int): The Result Page Size (default : 500)

        Returns:
            List[GroupMembership]: List of User's Memberships.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group name is None
        if len(user_id.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupMembershipClient] - User's Group Memberships Retrieve : 'user_id' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_USER_MEMBERSHIPS_URI.format(
                user_id=user_id.strip(),
                page_index=page_index,
                page_size=page_size
            )
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract List
            memberships = response.json()['groupMemberships']

            # If List is empty
            if len(memberships) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - No User Membership Found (Name : {user_id})".format(
                        code="404",
                        user_id=user_id
                    )
                )

            # Return JSON
            return GroupMembership.from_api_responses(responses=memberships)

        else:

            # Raise Exception
            response.raise_for_status()

    def create_membership(self, membership: GroupMembership = None) -> GroupMembership:
        """
        Create a GroupMembership on SonarQube API.

        Args:
            group (GroupMembership): The GroupMembership to Create.

        Returns:
            GroupMembership: Details of Created GroupMembership in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group is None
        if membership is None:

            # Raise Value Exception
            raise ValueError("[GroupMembershipClient] - GroupMembership creation : 'membership' details are required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CREATE_MEMBERSHIP_URI
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            json=membership.to_api_json(),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return GroupMembership.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_membership_by_id(self, id: str = ''):
        """
        Delete GroupMembership By ID from the Sonarqube API.

        Args:
            id (str): The Membership ID to Delete

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If group id is None
        if len(id.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupMembershipClient] - GroupMembership Delete : 'id' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_MEMBERSHIP_URI.format(
                id_delete=id
            )
        )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code) and not is_not_found(response.status_code):

            # Raise Exception
            response.raise_for_status()

    def delete_user_memberships(self, user_id: str, page_index: int = 1, page_size: int = 500):
        """
        Delete GroupMembership from the Sonarqube API.

        Args:
            id (str): The Membership ID to Delete

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Get User Memberships
        memberships = self.get_user_memberships(
            user_id=user_id.strip(),
            page_size=page_size,
            page_index=page_index
        )

        # Iterate on Memberships
        for membership in memberships:

            # Delete without side effects
            self.delete_membership_by_id(
                id=membership.id
            )

    def initialize_user_memberships(self, user_login: str = '', group_names: list[str] = None) -> List[GroupMembership]:
        """
        Delete GroupMembership from the Sonarqube API.

        Args:
            user_login (str): The Target User Name
            group_names (list): The Group Names to Associate to the User

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user_login is blank
        if len(user_login.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[GroupMembershipClient] - Create User Memberships : 'user_login' is required")

        # Find User
        user = self.user_client.get_user(login=user_login.strip())

        # Clean User Memberships
        self.delete_user_memberships(
            user_id=user.user_id
        )

        # Created Memberships
        memberships = []

        # If Group Names is not provided
        if group_names is None:

            # Initialize to Empty
            group_names = []

        # Iterate on Group Names
        for group_name in group_names:

            # Get Group
            group = self.group_client.get_group(name=group_name.strip())

            # Create Membership
            memberships.append(
                self.create_membership(
                    membership=GroupMembership(
                        user_id=user.user_id,
                        group_id=group.group_id
                    )
                )
            )

        # Return Memberships
        return memberships
