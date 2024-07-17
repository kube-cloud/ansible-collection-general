from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List, Optional
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

        # Check Algorithm
        if not self.algorithm:
            raise ValueError("The 'algorithm' field is required.")

    def __str__(self):
        """
        Returns a dictionary representation of the Balance object.
        """
        return str(self.__dict__)
