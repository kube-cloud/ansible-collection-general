from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import filter_none, is_2xx
from ..commons_security import HttpTokenAuth
from ...module_utils.gitlab.models import User
from typing import List

try:
    import requests
    from requests.exceptions import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class UserClient:
    """
    Client for interacting with the Gitlab API for User.

    Attributes:
        base_url (str): The base URL of the Gitlab API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Get User By Name URI (Return List so that extract the First One)
    GET_USER_BY_NAME_URI = "users?username={username}"

    # Create User URI
    CREATE_USER_URI = "users"

    # Update User URI
    UPDATE_USER_URI = "users/{user_id}"

    # Delete User URI
    DELETE_USER_URI = "users/{id_delete}"

    # URL Format
    URL_TEMPLATE = "{base_url}/api/{version}/{uri}"

    def __init__(self, base_url: str, api_version: str, auth: HttpTokenAuth):
        """
        Initializes the UserClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the Gitlab API.
            api_version (str): The Gitlab API Version (v1 or v2)
            auth (HttpTokenAuth): The Authentication Configuration
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[UserClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[UserClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version if api_version else "v4"

        # Initialize Basic Authentication
        self.auth = auth

    def get_user_by_name(self, username: str = '') -> User:
        """
        Retrieves the detail of User from the Gitlab API.

        Args:
            username (str): The Login of the User to retrieve details for.

        Returns:
            User: The User details.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user username is Empty or Blank
        if len(username.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Retrieve : 'username' is required and must be not blank")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            version=self.api_version,
            uri=self.GET_USER_BY_NAME_URI.format(
                username=username.strip()
            )
        )

        # Execute Request
        response = requests.get(
            url=url,
            headers={
                "Authorization": self.auth.get_auth_header_value()
            }
        )

        # If Object Exists
        if is_2xx(response.status_code):

            # Extract List
            users = response.json()

            # If List is empty
            if len(users) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - User not Found (Username : {username})".format(
                        code="404",
                        username=username
                    )
                )

            # Return JSON
            return User.from_api_response(users[0])

        else:

            # Raise Exception
            response.raise_for_status()

    def create_user(self, user: User = None) -> User:
        """
        Create a User on Gitlab API.

        Args:
            user (User): The User to Create.

        Returns:
            User: Details of Created User in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user is None
        if user is None:

            # Raise Value Exception
            raise ValueError("[UserClient] - User creation : 'user' details are required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            version=self.api_version,
            uri=self.CREATE_USER_URI
        )

        # Execute Request
        response = requests.post(
            url=url,
            json=filter_none(user),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON,
                "Authorization": self.auth.get_auth_header_value()
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return User.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def update_user(self, user: User = None) -> User:
        """
        Update a User on Gitlab API.

        Args:
            user (User): The User to Update.

        Returns:
            User: Details of Updated User in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user is None
        if user is None:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Update : 'user' details are required")

        # Find The User
        existing_user = self.get_user_by_name(username=user.username.strip())

        # Get User ID
        user_id = existing_user.id

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            version=self.api_version,
            uri=self.UPDATE_USER_URI.format(
                user_id=user_id
            )
        )

        # Execute Request
        response = requests.put(
            url=url,
            json=filter_none(user),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON,
                "Authorization": self.auth.get_auth_header_value()
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return User.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_user(self, username: str = ''):
        """
        Delete User from the Gitlab API.

        Args:
            username (str): The Login of the User to Delete

        Returns:
            dict: Details of Operation in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user username is None
        if len(username.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Delete : 'username' is required")

        # Find The User
        existing_user = self.get_user_by_name(username=username.strip())

        # Get User ID
        user_id = existing_user.id

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_USER_URI.format(
                id_delete=user_id
            )
        )

        # Execute Request
        response = requests.delete(
            url=url,
            headers={
                "Authorization": self.auth.get_auth_header_value()
            }
        )

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
