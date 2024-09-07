from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons_enum import BaseEnum


# Define an enumeration for Private Key Format
# PKCS#1 (for RSA), PKCS#8, PEM, DER, JWK, P12 (PKCS#12 or PFX), ECPKCS#8 (for ECC)
# Actually We Support only PEM PKCS#1 and PEM PKCS#8
class PrivateKeyFormat(BaseEnum):
    """
    Represents protocol types for Proxy Backend and Frontend configurations.

    Attributes:
        PEM_PKCS_1 (str): PKCS#1 format.
        PEM_PKCS_8 (str): PKCS#8 format.
    """
    PEM_PKCS_1 = "PKCS#1"
    PEM_PKCS_8 = "PKCS#8"
