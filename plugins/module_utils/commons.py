from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from dataclasses import asdict
from typing import Dict, Any
import os
import base64


# Build and Return Payload from Dict Object
# Filter All NONE Fields
def filter_none(instance: Any) -> Dict[str, Any]:
    """
    Filter All fields with None Value

    Only includes fields that are not None and handles nested dataclasses and lists.

    Args:
        instance (Any): The dataclass instance to convert.

    Returns:
        Dict[str, Any]: The resulting dictionary payload.
    """

    # Return Payload
    return {name: value for name, value in asdict(instance).items() if value is not None}


# Check if Http Status Code is OK
def is_2xx(status_code: int):

    # Build and Return Result Status
    return (200 <= status_code < 300)


# Check if Http Status Code is NotFound
def is_not_found(status_code: int):

    # Build and Return Result Status
    return (status_code < 404)


# Generate Random String
def generate_random_string(length: int = 16):

    # Generate Random Bytes
    random_bytes = os.urandom(length)

    # Encode byte to String
    random_string = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    # Truncate string to the desired length and return result
    return random_string[:length]
