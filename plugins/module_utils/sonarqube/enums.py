from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ..commons_enum import BaseEnum


# Define an enumeration for Available DevOps Platform
class DevOpsPlatform(BaseEnum):
    """
    Represents Available DevOps Platform.

    Attributes:
        GITHUB (str): Github Platform.
        GITLAB (str): Gitlab Platform.
        AZURE (str): Azure DevOps Platform.
        BITBUCKET (str): Atlassian Bitbucket Self-Maaged Platform.
        BITBUCKET_CLOUD (str): Atlassian Bitbucket Cloud Platform.
    """
    GITHUB = "github"
    GITLAB = "gitlab"
    AZURE = "azure"
    BITBUCKET = "bitbucket"
    BITBUCKET_CLOUD = "bitbucketcloud"


# Define an enumeration for Project Visibility
class ProjectVisibility(BaseEnum):
    """
    Represents Project Visibility.

    Attributes:
        PUBLIC (str): Public Project.
        PRIVATE (str): Private Project.
    """
    PUBLIC = "public"
    PRIVATE = "private"


# Define an enumeration for Project Code Definition Type
class ProjectCodeDefinitionType(BaseEnum):
    """
    Represents Project Visibility.

    Attributes:
        PREVIOUS_VERSION (str): Previous version.
        NUMBER_OF_DAYS (str): Number f Days.
        REFERENCE_BRANCH (str): Reference Branch.
    """
    PREVIOUS_VERSION = "PREVIOUS_VERSION"
    NUMBER_OF_DAYS = "NUMBER_OF_DAYS"
    REFERENCE_BRANCH = "REFERENCE_BRANCH"
