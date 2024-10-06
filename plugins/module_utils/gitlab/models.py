from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Dict, Optional, Type
from dataclasses import dataclass, field


# Load Balancing Configuration
@dataclass
class User:
    """
    Represents a User.

    Attributes:
        id (int): The User ID.
        username (str): The User Login.
        password (str): The User Password.
        name (str): The User Name.
        state (str): The User State.
        locked (bool): The User Locked Flag.
        avatar_url (str): The User Avatar URL.
        web_url (str): The User Web URL.
        created_at (str): The User Creation Date.
        bio (str): The User BIO.
        location (str): The User Location.
        public_email (str): The User Public Email.
        skype (str): The User Skype ID.
        linkedin (str): The User LinkedID ID.
        twitter (str): The User Twitter Profile ID.
        discord (str): The User Discord.
        website_url (str): The User Website URL.
        organization (str): The User Organization.
        job_title (str): The User Job Title.
        pronouns (str): The User Pronouns.
        bot (bool): The User Bot Flag.
        last_sign_in_at (str): The User Last Sign In Date.
        confirmed_at (str): The User Confirmation Date.
        last_activity_on (str): The User Last Activity Date.
        email (str): The User Privte Email.
        theme_id (str): The User Theme ID.
        color_scheme_id (str): The User Color Scheme ID.
        projects_limit (str): The User Project Limit.
        current_sign_in_at (str): The User Current Sign In Date.
        can_create_group (bool): The User Create Group Enabled Flag.
        can_create_project (bool): The User Create Project Enabled Flag.
        two_factor_enabled (bool): The User Two Factor Enabled Flag.
        external (bool): The User External Flag.
        private_profile (bool): The User Private Profile Flag.
        commit_email (str): The User Commit Email.
        is_admin (bool): The User Admin Flag.
        admin (bool): The User Admin Flag (For Creation).
        auditor (bool): The User Auditor Flag (For Creation).
        note (str): The User Admin Note (For Creation).
        skip_confirmation (bool): The User Skip Confirmation Flag (For Creation).

    """
    id: Optional[int] = field(default=None)                        # The User ID.
    username: str                                                  # The User Login.
    password: Optional[str] = field(default=None)                  # The User Password (For Creation).
    name: str                                                      # The User Name.
    state: Optional[str] = field(default=None)                     # The User State.
    locked: Optional[bool] = field(default=None)                   # The User Locked Flag.
    avatar_url: Optional[str] = field(default=None)                # The User Avatar URL.
    web_url: Optional[str] = field(default=None)                   # The User Web URL.
    created_at: Optional[str] = field(default=None)                # The User Creation Date.
    bio: Optional[str] = field(default=None)                       # The User BIO.
    location: Optional[str] = field(default=None)                  # The User Location.
    public_email: Optional[str] = field(default=None)              # The User Public Email.
    skype: Optional[str] = field(default=None)                     # The User Skype ID.
    linkedin: Optional[str] = field(default=None)                  # The User LinkedIn ID.
    twitter: Optional[str] = field(default=None)                   # The User Twitter Profile ID.
    discord: Optional[str] = field(default=None)                   # The User Discord.
    website_url: Optional[str] = field(default=None)               # The User Website URL.
    organization: Optional[str] = field(default=None)              # The User Organization.
    job_title: Optional[str] = field(default=None)                 # The User Job Title.
    pronouns: Optional[str] = field(default=None)                  # The User Pronouns.
    bot: Optional[bool] = field(default=None)                      # The User Bot Flag.
    last_sign_in_at: Optional[str] = field(default=None)           # The User Last Sign In Date.
    confirmed_at: Optional[str] = field(default=None)              # The User Confirmation Date.
    last_activity_on: Optional[str] = field(default=None)          # The User Last Activity Date.
    email: str                                                     # The User Private Email.
    theme_id: Optional[str] = field(default=None)                  # The User Theme ID.
    color_scheme_id: Optional[str] = field(default=None)           # The User Color Scheme ID.
    projects_limit: Optional[str] = field(default=None)            # The User Project Limit.
    current_sign_in_at: Optional[str] = field(default=None)        # The User Current Sign In Date.
    can_create_group: Optional[bool] = field(default=None)         # The User Create Group Enabled Flag.
    can_create_project: Optional[bool] = field(default=None)       # The User Create Project Enabled Flag.
    two_factor_enabled: Optional[bool] = field(default=None)       # The User Two Factor Enabled Flag.
    external: Optional[bool] = field(default=None)                 # The User External Flag.
    private_profile: Optional[bool] = field(default=None)          # The User Private Profile Flag.
    commit_email: Optional[str] = field(default=None)              # The User Commit Email.
    is_admin: Optional[bool] = field(default=None)                 # The User Admin Flag.
    admin: Optional[bool] = field(default=None)                    # The User Admin Flag (Used for Creation).
    auditor: Optional[bool] = field(default=None)                  # The User Auditor Flag (Used for Creation).
    note: Optional[str] = field(default=None)                      # The User Admin Note (Used for Creation).
    skip_confirmation: Optional[bool] = field(default=None)        # The User Skip Configmation Flag (Used for Creation).


    def __post_init__(self):

        # Check username
        if not self.username:
            raise ValueError("The 'username' field is required.")

        # Check name
        if not self.name:
            raise ValueError("The 'name' field is required.")

        # Check email
        if not self.email:
            raise ValueError("The 'email' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the User object.
        """
        return str(self.__dict__)

    @classmethod
    def from_api_response(cls: Type['User'], response: dict) -> 'User':
        """
        Returns a dictionary representation Compliant with User API Model.
        """
        return User(
            id=response.get('id', None),
            username=response.get('username', None),
            password=response.get('password', None),
            name=response.get('name', None),
            state=response.get('state', None),
            locked=response.get('locked', None),
            avatar_url=response.get('avatar_url', None),
            web_url=response.get('web_url', None),
            created_at=response.get('created_at', None),
            bio=response.get('bio', None),
            location=response.get('location', None),
            public_email=response.get('public_email', None),
            skype=response.get('skype', None),
            linkedin=response.get('linkedin', None),
            twitter=response.get('twitter', None),
            discord=response.get('discord', None),
            website_url=response.get('website_url', None),
            organization=response.get('organization', None),
            job_title=response.get('job_title', None),
            pronouns=response.get('pronouns', None),
            bot=response.get('bot', None),
            last_sign_in_at=response.get('last_sign_in_at', None),
            confirmed_at=response.get('confirmed_at', None),
            last_activity_on=response.get('last_activity_on', None),
            email=response.get('email', None),
            theme_id=response.get('theme_id', None),
            color_scheme_id=response.get('color_scheme_id', None),
            projects_limit=response.get('projects_limit', None),
            current_sign_in_at=response.get('current_sign_in_at', None),
            can_create_group=response.get('can_create_group', None),
            can_create_project=response.get('can_create_project', None),
            two_factor_enabled=response.get('two_factor_enabled', None),
            external=response.get('external', None),
            private_profile=response.get('private_profile', None),
            commit_email=response.get('commit_email', None),
            is_admin=response.get('is_admin', None),
            admin=response.get('admin', None),
            auditor=response.get('auditor', None),
            note=response.get('note', None),
            skip_confirmation=response.get('skip_confirmation', None)
        )
