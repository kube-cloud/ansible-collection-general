from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx
from ...module_utils.sonarqube.models import User

try:
    import requests
    from requests.exceptions import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class UserClient:
    """
    Client for interacting with the Sonarqube API for User.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Définir la constante pour application/json
    CONTENT_TYPE_MERGE_JSON = "application/merge-patch+json"

    # Get User URI (Return List so that find the right user that match)
    GET_USER_URI = "api/v2/users-management/users?q={login}"

    # Create User URI
    CREATE_USER_URI = "api/v2/users-management/users"

    # Update User URI
    UPDATE_USER_URI = "api/v2/users-management/users/{id_update}"

    # Delete User URI
    DELETE_USER_URI = "api/v2/users-management/users/{id_delete}"

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
            raise ValueError("UserClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[UserClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def get_user(self, login: str = '') -> User:
        """
        Retrieves the details of given User from the Sonarqube API.

        Args:
            login (str): The Login of the User to Retrieve

        Returns:
            User: Details of User in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user login is None
        if len(login.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Retrieve : 'login' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_USER_URI.format(
                login=login.strip()
            )
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract List
            users = response.json()['users']

            # If List is empty
            if len(users) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - User not Found (Login : {login})".format(
                        code="404",
                        login=login
                    )
                )

            # Return JSON
            return User.from_api_response(response=users[0])

        else:

            # Raise Exception
            response.raise_for_status()

    def create_user(self, user: User = None) -> User:
        """
        Create a User on SonarQube API.

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
            uri=self.CREATE_USER_URI
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            json=user.to_api_json(),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
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
        Update a User on SonarQube API.

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

        # If user login is None
        if user.user_login is None or not user.user_login or len(user.user_login.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Update : 'user_login' is required")

        # Find The User
        existing_user = self.get_user(user.user_login.strip())

        # Get User ID
        user_id = existing_user.user_id

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.UPDATE_USER_URI.format(
                id_update=user_id
            )
        )

        # Execute Request
        response = requests.patch(
            url=url,
            auth=self.auth,
            json=user.to_api_json(),
            headers={
                "Content-Type": self.CONTENT_TYPE_MERGE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return User.from_api_response(response=response.json())

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_user(self, login: str = ''):
        """
        Delete User from the Sonarqube API.

        Args:
            login (str): The Login of the User to Delete

        Returns:
            dict: Details of Operation in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If user login is None
        if len(login.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[UserClient] - User Delete : 'login' is required")

        # Find The User
        existing_user = self.get_user(login.strip())

        # Get User ID
        user_id = existing_user.user_id

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_USER_URI.format(
                id_delete=user_id
            )
        )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()
