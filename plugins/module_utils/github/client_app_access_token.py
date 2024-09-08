from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ...module_utils.commons import is_2xx
from ...module_utils.github.enums import PrivateKeyFormat
from ...module_utils.commons_security import convert_to_pkcs8
from ...module_utils.commons_security import HttpTokenAuth

try:
    import requests
    import time
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class AppAccessTokenClient:
    """
    Client for interacting with the Github App Access Token API.

    Attributes:
        api_base_url (str): The Github API base URL (eg. https://api.github.com).
        api_version (str): The Github API Version (eg. 2022-11-28)
        app_installation_id (str): The Github App Installation ID (eg. 123456789)
        app_id (str): The Github App ID (eg. 963346)
        jwt_algorithm (str): The Temporary Generated JWT Algorithm (eg. RS256)
        auth (HttpTokenAuth): The HTTP Token authentication credentials.
    """

    # Define Content Type application/json
    CONTENT_TYPE_JSON = "application/json"

    # Define Accept
    ACCEPT = "application/vnd.github.v3+json"

    # Define API Version Header Name
    HEADER_NAME_API_VERSION = "X-GitHub-Api-Version"

    # Create Access Token URI
    CREATE_ACCESS_TOKEN_URI = "app/installations/{installation_id}/access_tokens"

    # URL Format
    URL_TEMPLATE = "{base_url}/{uri}"

    def __init__(
        self,
        app_installation_id: str,
        app_id: str,
        app_private_key: str,
        api_base_url: str = "https://api.github.com",
        api_version: str = '2022-11-28',
        private_key_format: PrivateKeyFormat = PrivateKeyFormat.PEM_PKCS_8,
        app_private_key_password: str = None,
        jwt_key_duration: int = 30,
        jwt_exp_clock_drift: int = 60,
        jwt_algorithm: str = 'RS256'
    ):
        """
        Initializes the HAProxyClient with the given base URL and credentials.

        Args:
            api_base_url (str): The Github API base URL (eg. https://api.github.com).
            api_version (str): The Github API Version (eg. 2022-11-28)
            app_installation_id (str): The Github App Installation ID (eg. 123456789)
            app_private_key (str): The Github App Private Key
            private_key_format (PrivateKeyFormat): The Github API Private Key Format (eg. PEM_PKCS_8)
            app_private_key_password (str): The Github API Private Key Password
            jwt_key_duration (int): The Temporary Generated JWT Duration (eg. 600)
            jwt_algorithm (str): The Temporary Generated JWT Algorithm (eg. RS256)
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If app_installation_id is not Provided
        if not app_installation_id:

            # Raise Value Exception
            raise ValueError("[AppAccessTokenClient] - Initialization failed : 'app_installation_id' is required")

        # If app_id is not Provided
        if not app_id:

            # Raise Value Exception
            raise ValueError("[AppAccessTokenClient] - Initialization failed : 'app_id' is required")

        # If app_private_key is not Provided
        if not app_private_key:

            # Raise Value Exception
            raise ValueError("[AppAccessTokenClient] - Initialization failed : 'app_private_key' is required")

        # Initialize Base URL
        self.api_base_url = api_base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version

        # Initialize Installation ID
        self.app_installation_id = app_installation_id

        # Initialize Application ID
        self.app_id = app_id

        # Initialize JWT Algorithm
        self.jwt_algorithm = jwt_algorithm

        # IAT
        jwt_iat = int(time.time()) - jwt_exp_clock_drift

        # Initialize Private Key
        compliant_private_key = app_private_key

        # If Key format is not PKCS#8
        if private_key_format != PrivateKeyFormat.PEM_PKCS_8:

            # Convert Key
            compliant_private_key = convert_to_pkcs8(
                private_key_content=app_private_key,
                key_password=app_private_key_password
            )

        # Initialize Auth
        self.auth = HttpTokenAuth(
            jwt_algorithm=jwt_algorithm,
            jwt_payload={
                "iss": app_id,
                "iat": jwt_iat,
                "exp": jwt_iat + jwt_key_duration,
                "alg": jwt_algorithm
            },
            jwt_private_key=compliant_private_key
        )

    # Method used to Create Github App Access Token
    def create_access_token(self) -> str:

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.api_base_url,
            uri=self.CREATE_ACCESS_TOKEN_URI.format(
                installation_id=self.app_installation_id
            )
        )

        # Execute Request
        response = requests.post(
            url=url,
            headers={
                "Content-Type": self.CONTENT_TYPE_JSON,
                "Accept": self.ACCEPT,
                "Authorization": self.auth.get_auth_header_value(),
                self.HEADER_NAME_API_VERSION: str(self.api_version)
            }
        )

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            raise ValueError("API Error : [Statue : {status}, Message : {message}]".format(
                status=response.json()["status"],
                message=response.json()["message"]
            ))
