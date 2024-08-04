from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from enum import Enum


# Base Enumeration
class BaseEnum(str, Enum):

    # Create Instance
    @classmethod
    def create(cls, value: str):

        # Inf Value is None
        if value is None:

            # Return None
            return None

        # Iterate on Enum members
        for member in cls:

            # If member match on value
            if member.name == value.upper() or member.value.upper == value.upper:

                # Return the Member
                return member

        # Return None
        return None

    # Return Name List
    @classmethod
    def names(cls):

        # return Name List
        return [e.name for e in cls]

    # Return Values List
    @classmethod
    def values(cls):

        # return Value List
        return [e.value for e in cls]
