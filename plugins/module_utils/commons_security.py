from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from cryptography.hazmat.primitives.serialization import NoEncryption
    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    from cryptography.hazmat.primitives.serialization import Encoding
    from cryptography.hazmat.primitives.serialization import PrivateFormat
    import jwt
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# HTTP Token Based Authentication
class HttpTokenAuth:

    # Initialize Instance
    def __init__(
        self,
        jwt_payload: dict,
        jwt_private_key: str,
        jwt_algorithm: str
    ):

        # Build JWT
        self.jwt = jwt.encode(
            payload=jwt_payload,
            key=jwt_private_key.encode(),
            algorithm=jwt_algorithm
        )

    # Override Call function
    def get_auth_header_value(self):

        # Get Authorization Header for Request
        return "Bearer {token}".format(
            token=self.jwt
        )


# Convert Source Key to PKCS#8
def convert_to_pkcs8(
    private_key_content: str,
    key_password: str = None,
    key_encryption=None
) -> str:

    # Check Key Content
    if not private_key_content:
        raise ValueError("The 'private_key_content' is required.")

    # Local Key Encryption
    local_key_encryption = key_encryption

    # If Key Encryption is None
    if key_encryption is None:

        # Initialize with No Encryption
        local_key_encryption = NoEncryption()

    # Try to Load Private Key
    private_key = load_pem_private_key(
        data=private_key_content.encode(),
        password=key_password
    )

    # Convertir la clé en PKCS#8
    converted_key = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=local_key_encryption
    )

    # Return Key
    return converted_key.decode(encoding='utf-8')
