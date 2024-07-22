from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Optional, Type
from dataclasses import dataclass, field


# Settings Configuration
@dataclass
class Setting:
    """
    Represents SonarQube Global Settings configuration.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api/api/settings`

    Attributes:
        key (str): The SonarQube Setting Key (e.g., "sonar.core.serverBaseURL", etc...).
        component (str): The SonarQube Setting Component Key (e.g. my_project_key).
        value (str): The SonarQube Setting Value.
        values (list): The SonarQube Setting Values (For Multi-Value Field).
    """
    key: str
    component: Optional[str] = None
    value: Optional[str] = None
    values: List[str] = field(default_factory=list)

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("The 'key' field is required.")

        # Compute Invalid Value
        invalid_setting = (
            self.value is None or
            len(self.value.strip()) == 0 or
            self.values is None or
            len(self.values) == 0
        )

        # If Value and Values are Not Provided or Empty
        if invalid_setting:
            raise ValueError("No Value Provided for the Key [{0}]".format(
                self.key
            ))

    def __str__(self):
        """
        Returns a dictionary representation of the Balance object.
        """
        return str(self.__dict__)


# User Definition
@dataclass
class User:
    """
    Represents SonarQube User.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api_v2#/users-management/users--post`

    Attributes:
        user_login (str): The SonarQube User login.
        user_password (str): The SonarQube User password.
        user_email (str): The SonarQube User Email.
        user_name (str): The SonarQube User Name (Last and First Names).
        user_local (bool) : The SonarQube User Local or External Status
        user_scm_accounts (list): The SonarQube User SCM Accounts.
    """
    user_login: str
    user_name: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_password: Optional[str] = None
    user_local: Optional[bool] = None
    user_scm_accounts: List[str] = field(default_factory=list)

    def __post_init__(self):

        # Check user_login
        if not self.user_login:
            raise ValueError("The 'user_login' field is required.")

        # Check user_name
        if not self.user_name:
            raise ValueError("The 'user_name' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the Balance object.
        """
        return str(self.__dict__)

    def to_api_json(self) -> dict:
        """
        Returns a dictionary representation Compliant with Create User API Model.
        """
        return {
            "email": self.user_email,
            "local": self.user_local,
            "login": self.user_login,
            "name": self.user_name,
            "password": self.user_password,
            "scmAccounts": self.user_scm_accounts
        }

    def __eq__(self, other):

        # If Class is not Instance of User
        if not isinstance(other, User):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "user_login", None) == getattr(other, "user_login", None) and
            getattr(self, "user_name", None) == getattr(other, "user_name", None) and
            getattr(self, "user_email", None) == getattr(other, "user_email", None) and
            getattr(self, "user_password", None) == getattr(other, "user_password", None) and
            set(getattr(self, "user_scm_accounts", [])) == set(getattr(other, "user_scm_accounts", []))
        )

    @classmethod
    def from_api_response(cls: Type['User'], response: dict) -> 'User':
        """
        Returns a dictionary representation Compliant with Create User API Model.
        """
        return User(
            user_id=response['id'],
            user_login=response['login'],
            user_name=response['name'],
            user_email=response['email'],
            user_local=response['local'],
            user_scm_accounts=response['scmAccounts']
        )
