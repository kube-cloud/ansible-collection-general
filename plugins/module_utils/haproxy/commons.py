from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from dataclasses import asdict
from typing import Dict, Any


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

    return (200 <= status_code < 300)
