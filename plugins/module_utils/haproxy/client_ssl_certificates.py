from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from .client_configurations import ConfigurationClient
from .commons import is_2xx

try:
    import requests
    import os
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


class SslCertificateClient:
    """
    Client for interacting with the HAProxy Data Plane API for SSL Certificates Storage.

    Attributes:
        base_url (str): The base URL of the HAProxy Data Plane API.
        auth (HTTPBasicAuth): The HTTP basic authentication credentials.
    """

    # Définir la constante pour application/json
    CONTENT_TYPE_JSON = "application/json"

    # Certificates URI
    CERTIFICATES_URI = "services/haproxy/storage/ssl_certificates"

    # Certificate URI
    CERTIFICATE_URI = "services/haproxy/storage/ssl_certificates/{name}"

    # Certificate URI Template with force reload
    CERTIFICATE_URI_TEMPLATE = "{certificate_uri}?force_reload={force_reload}"

    # URL Format
    URL_TEMPLATE = "{base_url}/{version}/{uri}"

    def __init__(self, base_url: str, api_version: str, auth):
        """
        Initializes the HAProxyClient with the given base URL and credentials.

        Args:
            base_url (str): The base URL (scheme://host:port) of the HAProxy Data Plane API.
            api_version (str): The HAProxy Data Plane API Version (v1 or v2)
            auth (HTTPBasicAuth): The Authentication Configuration
        Raises:
            ValueError: If any of the required parameters are not provided.
        """

        # If Base URL is not Provided
        if not base_url:

            # Raise Value Exception
            raise ValueError("[SSLCertificateClient] - Initialization failed : 'base_url' is required")

        # If auth is not Provided
        if not auth:

            # Raise Value Exception
            raise ValueError("[SSLCertificateClient] - Initialization failed : 'auth' is required")

        # Initialize Base URL
        self.base_url = base_url.rstrip('/')

        # Initialize Version
        self.api_version = api_version if api_version else "v2"

        # Initialize Basic Authentication
        self.auth = auth

        # Initialize Configuration Client
        self.configuration = ConfigurationClient(
            base_url=base_url,
            api_version=api_version,
            auth=auth
        )

    def get_certificates(self):
        """
        Retrieves the list of Servers from the HAProxy Data Plane API.

        Returns:
            list: A list of SSL Certificates in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CERTIFICATES_URI,
            version=self.api_version
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def get_certificate(self, name: str):
        """
        Retrieves the details of given SSL Certificate (name) from the HAProxy Data Plane API.

        Args:
            name (str): The name of the SSL Certificate to retrieve details for.

        Returns:
            dict: Details of Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CERTIFICATE_URI.format(name=name),
            version=self.api_version
        )

        # Execute Request
        response = requests.get(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def create_certificate(self, name: str, path: str, force_reload: bool = True):
        """
        Create a Server on HAProxy API.

        Args:
            name (str): The Certificate Name
            path (str): The Certificate Local Path to create (Upload).
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Check Name Parameter
        if not name or name.strip() == "":

            # Raise Value Error
            raise ValueError("The 'name' parameter is required and cannot be blank.")

        # Check Path Parameter
        if not path or path.strip() == "":

            # Raise Value Error
            raise ValueError("The 'path' parameter is required and cannot be blank.")

        # Check File existence
        if not os.path.isfile(path.strip()):

            # Raise Custom Error
            raise FileNotFoundError("File to Upload is Not Found : {path}".format(path=path))

        # Prepare File to Upload
        files = {
            'file_upload': (name.strip(), open(path.strip(), 'rb'))
        }

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CERTIFICATE_URI_TEMPLATE.format(
                certificate_uri=self.CERTIFICATES_URI,
                force_reload=force_reload
            ),
            version=self.api_version
        )

        try:

            # Execute Request
            response = requests.post(
                url=url,
                files=files,
                auth=self.auth
            )

        finally:

            # Close File
            files['file_upload'][1].close()

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def update_certificate(self, name: str, path: str, force_reload: bool = True):
        """
        Update a Server on HAProxy API.

        Args:
            name (str): The Certificate Name
            path (str): The Certificate Local Path to create (Upload).
            force_reload (bool): Force Reload HA Proxy Configuration (used if no Transaction ID Provided)

        Returns:
            dict: Details of Created Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Check Name Parameter
        if not name or name.strip() == "":

            # Raise Value Error
            raise ValueError("[Update Certificate] - The 'name' parameter is required and cannot be blank.")

        # Check Path Parameter
        if not path or path.strip() == "":

            # Raise Value Error
            raise ValueError("The 'path' parameter is required and cannot be blank.")

        # Check File existence
        if not os.path.isfile(path.strip()):

            # Raise Custom Error
            raise FileNotFoundError("File to Upload is Not Found : {path}".format(path=path))

        # Read Fie content
        with open(path.strip(), 'r') as file:

            # Read Content
            certificate_content = file.read()

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CERTIFICATE_URI_TEMPLATE.format(
                certificate_uri=self.CERTIFICATE_URI.format(name=name.strip()),
                force_reload=force_reload
            ),
            version=self.api_version
        )

        # Define Request Headers
        headers = {
            'Content-Type': 'text/plain'
        }

        # Execute request
        response = requests.put(url, data=certificate_content, headers=headers, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return response.json()

        else:

            # Raise Exception
            response.raise_for_status()

    def delete_certificate(self, name: str, force_reload: bool = True):
        """
        Delete a Certificate on HAProxy API.

        Args:
            name (str): The name of the SSL Certificate to delete.

        Returns:
            dict: Details of Server in JSON format.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """

        # Check Name Parameter
        if not name or name.strip() == "":

            # Raise Value Error
            raise ValueError("The 'name' parameter is required and cannot be blank.")

        # Build the Operation URL
        url = self.URL_TEMPLATE.format(
            base_url=self.base_url,
            uri=self.CERTIFICATE_URI_TEMPLATE.format(
                certificate_uri=self.CERTIFICATE_URI.format(name=name.strip()),
                force_reload=force_reload
            ),
            version=self.api_version
        )

        # Execute Request
        response = requests.delete(url, auth=self.auth)

        # If Object Exists
        if is_2xx(response.status_code):

            # Return JSON
            return {
                "name": name,
                "status": "deleted"
            }

        else:

            # Raise Exception
            response.raise_for_status()
