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
