from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons import is_2xx
from .models import Project
from .models import ImportDopProjectSpec
from .models import DevOpsPlatform

try:
    import requests
    from requests.exceptions import HTTPError
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class ProjectClient:
    """
    Client for Project Management with the Sonarqube API.

    Attributes:
        base_url (str): The base URL of the Sonarqube API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # URL Format
    URL_TEMPLATE = "{base_url}/{uri}"

    # Search Project URI
    SEARCH_PROJECT_BY_KEY_URI = "api/projects/search?projects={project_key}&ps=1&p=1"

    # Delete Project URI
    DELETE_PROJECT_BY_KEY = "api/projects/bulk_delete?projects={project_key}"

    # Import Project from DOP URI
    IMPORT_DOP_PROJECT_URI = "api/v2/dop-translation/bound-projects"

    # Get All DOPs
    GET_ALL_DOP_URI = "api/v2/dop-translation/dop-settings"

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
            raise ValueError("ProjectClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[ProjectClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Basic Authentication
        self.auth = auth

    def get_dop(self, dop_key: str = '') -> DevOpsPlatform:
        """
        Retrieves the details of given DevOps Platform from the Sonarqube API.

        Args:
            dop_key (str): The DOP Key

        Returns:
            DevOpsPlatform: Details of DOP in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If dop key is None
        if len(dop_key.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[ProjectClient] - DOP Retrieve : 'dop_key' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.GET_ALL_DOP_URI
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract List
            dops = response.json()['dopSettings']

            # Find DOP in the List
            dop = next((dop for dop in dops if dop.get('key', '') == dop_key.strip()), None)

            # If List is empty
            if dop is None:

                # Raise Exception
                raise HTTPError(
                    "{code} - DevOpsPlatform not Found (Key : {key})".format(
                        code="404",
                        key=dop_key
                    )
                )

            # Return JSON
            return DevOpsPlatform.from_api_response(response=dop)

        else:

            # Raise Exception
            response.raise_for_status()

    def get_project(self, project_key: str = '') -> DevOpsPlatform:
        """
        Retrieves the details of given Project from the Sonarqube API.

        Args:
            project_key (str): The Project Key

        Returns:
            Project: Details of Project in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If project key is None
        if len(project_key.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[ProjectClient] - Project Retrieve : 'project_key' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.SEARCH_PROJECT_BY_KEY_URI.format(
                project_key=project_key.strip()
            )
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If HTTP Result is OK
        if is_2xx(response.status_code):

            # Extract List
            projects = response.json()['components']

            # If List is empty
            if len(projects) == 0:

                # Raise Exception
                raise HTTPError(
                    "{code} - Project not Found (Key : {key})".format(
                        code="404",
                        key=project_key
                    )
                )

            # Return JSON
            return Project.from_api_response(response=projects[0])

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_project(self, project_key: str = '') -> Project:
        """
        Delete Project from the Sonarqube API.

        Args:
            project_key (str): The Project Key

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # If project key is None
        if len(project_key.strip()) == 0:

            # Raise Value Exception
            raise ValueError("[ProjectClient] - Project Delete : 'project_key' is required")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.DELETE_PROJECT_BY_KEY.format(
                project_key=project_key.strip()
            )
        )

        # Execute Request
        response = requests.post(url, auth=self.auth)

        # If Object Exists
        if not is_2xx(response.status_code):

            # Raise Exception
            response.raise_for_status()

    def import_dop_project(self, project_spec: ImportDopProjectSpec = None) -> dict:

        # If Project Specification is None
        if project_spec is None:

            # Raise Value Exception
            raise ValueError("[ProjectClient] - DOP Project Import : 'project_spec' is required")

        # Find DevOps Platform
        dop = self.get_dop(dop_key=project_spec.dev_ops_platform_key)

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.IMPORT_DOP_PROJECT_URI
        )

        # Execute Request
        response = requests.post(
            url=url,
            auth=self.auth,
            json=project_spec.to_api_json(dop_id=dop.id),
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON
            }
        )

        # If OK
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()
