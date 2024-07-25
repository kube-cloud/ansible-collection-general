from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Dict, Optional, Type
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
            (self.value is None or len(self.value.strip()) == 0) and
            (self.values is None or len(self.values) == 0)
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


# Group Definition
@dataclass
class Group:
    """
    Represents SonarQube Group.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api_v2#/authorizations/groups--post`

    Attributes:
        group_name (str): The SonarQube Group Name.
        group_id (str): The SonarQube Group Internal ID.
        group_description (str) : The SonarQube Group Description.
    """
    group_name: str
    group_id: Optional[str] = None
    group_description: Optional[str] = None
    global_permissions: List[str] = field(default_factory=list)

    def __post_init__(self):

        # Check user_login
        if not self.group_name:
            raise ValueError("The 'group_name' field is required.")

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
            "name": self.group_name,
            "description": self.group_description
        }

    def __eq__(self, other):

        # If Class is not Instance of Group
        if not isinstance(other, Group):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "group_name", None) == getattr(other, "group_name", None) and
            getattr(self, "group_description", None) == getattr(other, "group_description", None) and
            set(getattr(self, "global_permissions", [])) == set(getattr(other, "global_permissions", []))
        )

    @classmethod
    def from_api_response(cls: Type['Group'], response: dict) -> 'Group':
        """
        Returns a dictionary representation Compliant with Create User API Model.
        """
        return Group(
            group_id=response['id'],
            group_name=response['name'],
            group_description=response['description']
        )


# User Definition
@dataclass
class User:
    """
    Represents SonarQube User.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api_v2#/users-management/users--post`

    Attributes:
        user_login (str): The SonarQube User login.
        user_name (str): The SonarQube User Name (Last and First Names).
        user_id (str): The SonarQube User Internal ID.
        user_email (str): The SonarQube User Email.
        user_password (str): The SonarQube User password.
        user_local (bool) : The SonarQube User Local or External Status
        user_scm_accounts (list): The SonarQube User SCM Accounts.
        user_groups (list): The SonarQube User Groups
    """
    user_login: str
    user_name: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_password: Optional[str] = None
    user_local: Optional[bool] = None
    user_scm_accounts: List[str] = field(default_factory=list)
    user_groups: List[str] = field(default_factory=list)

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
            set(getattr(self, "user_scm_accounts", [])) == set(getattr(other, "user_scm_accounts", [])) and
            set(getattr(self, "user_groups", [])) == set(getattr(other, "user_groups", []))
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


# Group Membership Definition
@dataclass
class GroupMembership:
    """
    Represents SonarQube Group Membership.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api_v2#/authorizations/group-memberships--post`

    Attributes:
        id (str): The SonarQube Membership ID
        user_id (str): The SonarQube User ID.
        group_id (str): The SonarQube Group ID.
    """
    user_id: str
    group_id: str
    id: Optional[str] = ''

    def __post_init__(self):

        # Check user_id
        if not self.user_id:
            raise ValueError("The 'user_id' field is required.")

        # Check group_id
        if not self.group_id:
            raise ValueError("The 'group_id' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the object.
        """
        return str(self.__dict__)

    def to_api_json(self) -> dict:
        """
        Returns a dictionary representation Compliant with Create API Model.
        """
        return {
            "userId": self.user_id,
            "groupId": self.group_id
        }

    def __eq__(self, other):

        # If Class is not Instance of GroupMembership
        if not isinstance(other, GroupMembership):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "id", '') == getattr(other, "id", '') and
            getattr(self, "user_id", '') == getattr(other, "user_id", '') and
            getattr(self, "group_id", '') == getattr(other, "group_id", '')
        )

    @classmethod
    def from_api_response(cls: Type['GroupMembership'], response: dict) -> 'GroupMembership':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return GroupMembership(
            id=response['id'],
            group_id=response['groupId'],
            user_id=response['userId']
        )

    @classmethod
    def from_api_responses(cls: Type['GroupMembership'], responses: List[Dict[str, str]]) -> 'List[GroupMembership]':
        """
        Returns a List of Memberships from API Responses.
        """

        # Initialize Membership List
        memberships = []

        # If No Responses Provided
        if responses is None:

            # Initialize Response
            responses = []

        # Iterate on Responses
        for response in responses:

            # Extract User/Group ID
            user_id = response.get('userId', '')
            group_id = response.get('groupId', '')

            # If User ID and group ID provided
            if len(user_id.strip()) > 0 and len(group_id.strip()) > 0:

                # Append Membership
                memberships.append(GroupMembership.from_api_response(response=response))

        # Return Memberships
        return memberships


# Group Global Permissions
@dataclass
class GroupGlobalPermission:
    """
    Represents SonarQube Group Global Permissions.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/permissions`

    Attributes:
        group_name (str): The SonarQube Group Name.
        permission (str): The SonarQube Permission Name.
    """

    # Définir la constante pour application/json
    AVAILABLE_PERMISSIONS = [
        "admin",
        "gateadmin",
        "profileadmin",
        "provisioning",
        "scan",
        "applicationcreator"
    ]

    group_name: str
    permission_name: str

    def __post_init__(self):

        # Check group_name
        if not self.group_name:
            raise ValueError("The 'group_name' field is required.")

        # Check permission_name
        if not self.permission_name:
            raise ValueError("The 'permission_name' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the object.
        """
        return str(self.__dict__)

    def to_api_json(self) -> dict:
        """
        Returns a dictionary representation Compliant with Create API Model.
        """
        return {
            "groupName": self.group_name,
            "permission": self.permission_name
        }

    @classmethod
    def from_api_response(cls: Type['GroupGlobalPermission'], response: dict) -> 'GroupGlobalPermission':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return GroupGlobalPermission(
            group_name=response['groupName'],
            permission_name=response['permission']
        )

    def __eq__(self, other):

        # If Class is not Instance of GroupGlobalPermission
        if not isinstance(other, GroupGlobalPermission):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "group_name", '') == getattr(other, "group_name", '') and
            getattr(self, "permission_name", '') == getattr(other, "permission_name", '')
        )
