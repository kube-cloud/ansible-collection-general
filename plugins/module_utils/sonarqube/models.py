from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Dict, Optional, Type
from dataclasses import dataclass, field
from .enums import DevOpsPlatform
from .enums import ProjectVisibility


# ALM Access Token Details
@dataclass
class AlmToken:
    """
    Represents SonarQube Global ALM Access Token.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api/api/alm_integrations/set_pat`

    Attributes:
        alm_name (str): The SonarQube ALM Name.
        access_token (str): The SonarQube ALM Token.
        username (str): The SonarQube ALM Token Username.
    """
    alm_name: str
    access_token: str
    token_username: Optional[str] = None

    def __post_init__(self):

        # Check alm_name
        if not self.alm_name:
            raise ValueError("Setting : The 'alm_name' field is required.")

        # Check access_token
        if not self.access_token:
            raise ValueError("Setting : The 'access_token' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the object.
        """
        return str(self.__dict__)


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
            raise ValueError("Setting : The 'key' field is required.")

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


# ALM Github Settings
@dataclass
class AlmSettingsGithub:
    """
    Represents SonarQube ALM Settings for Github Integration.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/alm_settings`

    Attributes:
        key (str): The SonarQube ALM Setting key.
        new_key (str): The SonarQube ALM Setting New key.
        url (str): The Github URL
        app_id (str): The SonarQube ALM Setting Application ID.
        client_id (str): The SonarQube ALM Setting Application Client ID.
        client_secret (str): The SonarQube ALM Setting Application Client Secret.
        private_key (str): The SonarQube ALM Setting Application Private Key.
        app_id (str): The SonarQube ALM Setting Application ID.
        webhook_secret (str): The SonarQube ALM Setting Webhook Secret
    """

    # Définir la constante pour application/json
    DEVOPS_PLAFORM = DevOpsPlatform.GITHUB

    # Fields
    key: str
    url: str
    app_id: str
    client_id: str
    client_secret: str
    private_key: str
    webhook_secret: Optional[str] = None
    new_key: Optional[str] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("AlmSettingsGithub : The 'key' field is required.")

        # Check url
        if not self.url:
            raise ValueError("AlmSettingsGithub : The 'url' field is required.")

        # Check app_id
        if not self.app_id:
            raise ValueError("AlmSettingsGithub : The 'app_id' field is required.")

        # Check client_id
        if not self.client_id:
            raise ValueError("AlmSettingsGithub : The 'client_id' field is required.")

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
            "key": self.key,
            "url": self.url,
            "appId": self.app_id,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "privateKey": self.private_key,
            "webhookSecret": self.webhook_secret,
            "newKey": self.new_key
        }

    @classmethod
    def from_api_response(cls: Type['AlmSettingsGithub'], response: dict) -> 'AlmSettingsGithub':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return AlmSettingsGithub(
            key=response.get('key', None),
            url=response.get('url', None),
            app_id=response.get('appId', None),
            client_id=response.get('clientId', None),
            client_secret=response.get('clientSecret', None),
            private_key=response.get('privateKey', None),
            webhook_secret=response.get('webhookSecret', None)
        )

    def __eq__(self, other):

        # If Class is not Instance of AlmSettingsGithub
        if not isinstance(other, AlmSettingsGithub):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "key", '') == getattr(other, "key", '') and
            getattr(self, "url", '') == getattr(other, "url", '') and
            getattr(self, "app_id", '') == getattr(other, "app_id", '') and
            getattr(self, "client_id", '') == getattr(other, "client_id", '') and
            getattr(self, "client_secret", '') == getattr(other, "client_secret", '') and
            getattr(self, "webhook_secret", '') == getattr(other, "webhook_secret", '')
        )


# ALM Gitlab Settings
@dataclass
class AlmSettingsGitlab:
    """
    Represents SonarQube ALM Settings for Gitlab Integration.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/alm_settings`

    Attributes:
        key (str): The SonarQube ALM Setting key.
        new_key (str): The SonarQube ALM Setting New key.
        url (str): The Gitlab URL
        personal_access_token (str): The SonarQube ALM Setting Personal Access Token.
    """

    # Définir la constante pour application/json
    DEVOPS_PLAFORM = DevOpsPlatform.GITLAB

    # Fields
    key: str
    url: str
    personal_access_token: str
    new_key: Optional[str] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("AlmSettingsGitlab : The 'key' field is required.")

        # Check url
        if not self.url:
            raise ValueError("AlmSettingsGitlab : The 'url' field is required.")

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
            "key": self.key,
            "url": self.url,
            "personalAccessToken": self.personal_access_token
        }

    @classmethod
    def from_api_response(cls: Type['AlmSettingsGitlab'], response: dict) -> 'AlmSettingsGitlab':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return AlmSettingsGitlab(
            key=response.get('key', None),
            url=response.get('url', None),
            personal_access_token=response.get('personalAccessToken', None)
        )

    def __eq__(self, other):

        # If Class is not Instance of AlmSettingsGitlab
        if not isinstance(other, AlmSettingsGitlab):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "key", '') == getattr(other, "key", '') and
            getattr(self, "url", '') == getattr(other, "url", '') and
            getattr(self, "personal_access_token", '') == getattr(other, "personal_access_token", '')
        )


# ALM Azure Settings
@dataclass
class AlmSettingsAzure:
    """
    Represents SonarQube ALM Settings for Azure Integration.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/alm_settings`

    Attributes:
        key (str): The SonarQube ALM Setting key.
        new_key (str): The SonarQube ALM Setting New key.
        url (str): The Azure URL
        personal_access_token (str): The SonarQube ALM Setting Personal Access Token.
    """

    # Définir la constante pour application/json
    DEVOPS_PLAFORM = DevOpsPlatform.AZURE

    # Fields
    key: str
    url: str
    personal_access_token: str
    new_key: Optional[str] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("AlmSettingsAzure : The 'key' field is required.")

        # Check url
        if not self.url:
            raise ValueError("AlmSettingsAzure : The 'url' field is required.")

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
            "key": self.key,
            "url": self.url,
            "personalAccessToken": self.personal_access_token
        }

    @classmethod
    def from_api_response(cls: Type['AlmSettingsAzure'], response: dict) -> 'AlmSettingsAzure':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return AlmSettingsAzure(
            key=response.get('key', None),
            url=response.get('url', None),
            personal_access_token=response.get('personalAccessToken', None)
        )

    def __eq__(self, other):

        # If Class is not Instance of AlmSettingsAzure
        if not isinstance(other, AlmSettingsAzure):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "key", '') == getattr(other, "key", '') and
            getattr(self, "url", '') == getattr(other, "url", '') and
            getattr(self, "personal_access_token", '') == getattr(other, "personal_access_token", '')
        )


# ALM Bitbucket Settings
@dataclass
class AlmSettingsBitbucket:
    """
    Represents SonarQube ALM Settings for Bitbucket Integration.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/alm_settings`

    Attributes:
        key (str): The SonarQube ALM Setting key.
        new_key (str): The SonarQube ALM Setting New key.
        url (str): The Bitbucket URL
        personal_access_token (str): The SonarQube ALM Setting Personal Access Token.
    """

    # Définir la constante pour application/json
    DEVOPS_PLAFORM = DevOpsPlatform.BITBUCKET

    # Fields
    key: str
    url: str
    personal_access_token: str
    new_key: Optional[str] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("The 'key' field is required.")

        # Check url
        if not self.url:
            raise ValueError("The 'url' field is required.")

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
            "key": self.key,
            "url": self.url,
            "personalAccessToken": self.personal_access_token
        }

    @classmethod
    def from_api_response(cls: Type['AlmSettingsBitbucket'], response: dict) -> 'AlmSettingsBitbucket':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return AlmSettingsBitbucket(
            key=response.get('key', None),
            url=response.get('url', None),
            personal_access_token=response.get('personalAccessToken', None)
        )

    def __eq__(self, other):

        # If Class is not Instance of AlmSettingsBitbucket
        if not isinstance(other, AlmSettingsBitbucket):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "key", '') == getattr(other, "key", '') and
            getattr(self, "url", '') == getattr(other, "url", '') and
            getattr(self, "personal_access_token", '') == getattr(other, "personal_access_token", '')
        )


# ALM BitbucketCloud Settings
@dataclass
class AlmSettingsBitbucketCloud:
    """
    Represents SonarQube ALM Settings for BitbucketCloud Integration.
    Refer at : `http://next.sonarqube.com/sonarqube/web_api/api/alm_settings`

    Attributes:
        key (str): The SonarQube ALM Setting key.
        new_key (str): The SonarQube ALM Setting New key.
        client_id (str): The SonarQube ALM Setting Application Client ID.
        client_secret (str): The SonarQube ALM Setting Application Client Secret.
        workspace (str): The SonarQube ALM Setting Application Workspace.
    """

    # Définir la constante pour application/json
    DEVOPS_PLAFORM = DevOpsPlatform.BITBUCKET_CLOUD

    # Fields
    key: str
    client_id: str
    client_secret: str
    workspace: str
    new_key: Optional[str] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("The 'key' field is required.")

        # Check client_id
        if not self.client_id:
            raise ValueError("The 'client_id' field is required.")

        # Check workspace
        if not self.workspace:
            raise ValueError("The 'workspace' field is required.")

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
            "key": self.key,
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "workspace": self.workspace
        }

    @classmethod
    def from_api_response(cls: Type['AlmSettingsBitbucketCloud'], response: dict) -> 'AlmSettingsBitbucketCloud':
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return AlmSettingsBitbucketCloud(
            key=response.get('key', None),
            client_id=response.get('clientId', None),
            client_secret=response.get('clientSecret', None),
            workspace=response.get('workspace', None)
        )

    def __eq__(self, other):

        # If Class is not Instance of AlmSettingsBitbucketCloud
        if not isinstance(other, AlmSettingsBitbucketCloud):

            # Return False
            return False

        # Return comparison
        return (
            getattr(self, "key", '') == getattr(other, "key", '') and
            getattr(self, "client_id", '') == getattr(other, "client_id", '') and
            getattr(self, "client_secret", '') == getattr(other, "client_secret", '') and
            getattr(self, "workspace", '') == getattr(other, "workspace", '')
        )


# DOP Informations
@dataclass
class DevOpsPlatform:
    """
    Represents SonarQube Project.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api_v2#/dop-translation/dop-settings--get`

    Attributes:
        id (str): The SonarQube DOP ID.
        type (str): The SonarQube DOP type.
        key (str): The SonarQube DOP Key.
        url (str): The SonarQube DOP URL.
        app_id (str): The SonarQube DOP AppId.
    """
    id: Optional[str] = ''
    type: Optional[str] = ''
    key: Optional[str] = ''
    url: Optional[str] = ''
    app_id: Optional[str] = ''

    @classmethod
    def from_api_response(cls: Type['DevOpsPlatform'], response: dict) -> 'DevOpsPlatform':
        """
        Build and Returns a Instance representation from with API Response.
        """
        return DevOpsPlatform(
            id=response.get('id', None),
            type=response.get('type', None),
            key=response.get('key', None),
            url=response.get('url', None),
            app_id=response.get('appId', None)
        )


# Project Informations
@dataclass
class Project:
    """
    Represents SonarQube Project.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api/api/projects`

    Attributes:
        key (str): The SonarQube Project Key.
        name (str): The SonarQube Project Name.
        qualifier (str): The SonarQube Project Qualifier.
        visibility (str): The SonarQube Project Visibility
        revision (str): The SonarQube Project Revision
        managed (bool): The SonarQube Project Management Status
    """
    key: str
    name: Optional[str] = None
    qualifier: Optional[str] = None
    visibility: Optional[ProjectVisibility] = ProjectVisibility.PUBLIC
    revision: Optional[str] = None
    managed: Optional[bool] = None

    def __post_init__(self):

        # Check key
        if not self.key:
            raise ValueError("Setting : The 'key' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the object.
        """
        return str(self.__dict__)

    @classmethod
    def from_api_response(cls: Type['Project'], response: dict) -> 'Project':
        """
        Returns a dictionary representation Compliant with Create User API Model.
        """
        return Project(
            key=response.get('key'),
            name=response.get('name', None),
            qualifier=response.get('qualifier', None),
            visibility=ProjectVisibility.create(response.get('visibility', None)),
            managed=response.get('managed', None)
        )


# Import DevOps Platform Project Specification
@dataclass
class ImportDopProjectSpec:
    """
    Represents SonarQube Search Project Parameters.
    Refer at : `https://next.sonarqube.com/sonarqube/web_api_v2#/dop-translation/bound-projects--post`

    Attributes:
        project_key (str): The SonarQube Project Key.
        project_name (str): The SonarQube Project Name.
        dev_ops_platform_key (str): The SonarQube Source DevOps Platform Key.
        repository_identifier (str): The DevOps Platform Repository Identifier
        monorepo (bool): The SonarQube Project Mono Repository Status
        project_identifier (str): The SonarQube Project Identifier
        new_code_definition_type (ProjectCodeDefinitionType): The SonarQube Project New Code Definition Type
        new_code_definition_value (str): The SonarQube Project New Code Definitio Value
    """
    project_key: str
    project_name: str
    dev_ops_platform_key: str
    repository_identifier: str
    monorepo: bool
    project_identifier: Optional[str] = None

    def __post_init__(self):

        # Check project_key
        if not self.project_key:
            raise ValueError("Setting : The 'project_key' field is required.")

        # Check project_name
        if not self.project_name:
            raise ValueError("Setting : The 'project_name' field is required.")

        # Check dev_ops_platform_key
        if not self.dev_ops_platform_key:
            raise ValueError("Setting : The 'dev_ops_platform_key' field is required.")

        # Check repository_identifier
        if not self.repository_identifier:
            raise ValueError("Setting : The 'repository_identifier' field is required.")

    def to_api_json(self, dop_id: str = '') -> dict:
        """
        Returns a dictionary representation Compliant with API Model.
        """
        return {
            "projectKey": self.project_key,
            "projectName": self.project_name,
            "devOpsPlatformSettingId": dop_id,
            "repositoryIdentifier": self.repository_identifier,
            "monorepo": self.monorepo,
            "projectIdentifier": self.project_identifier
        }
