"""App Center branches API wrappers."""

import logging
import os
import json
from typing import Iterator, List, Optional, Dict
from urllib.parse import quote_plus

import deserialize

from appcenter.client import AppCenterDerivedClient
from appcenter.models import (
    BranchList,
    BuildInfo)

class AppCenterBranchesClient(AppCenterDerivedClient):
    """Wrapper around the App Center versions APIs.

    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """
    
    BUILD_CONFIG = {
        'trigger': 'manual',
        'environmentVariables': [],
        'signed': False,
        'testsEnabled': False,
        'badgeIsEnabled': False,
        'toolsets': {
        'buildscripts': {},
        'android': {
            'module': 'app',
            'buildVariant': 'release',
            'isRoot': False,
            'runTests': False,
            'runLint': False,
            'automaticSigning': False,
            'buildBundle': False,
            'gradleWrapperPath': 'gradlew'
            },
        'javascript': {
            'nodeVersion': '6.x',
            'packageJsonPath': 'package.json',
            'runTests': False
        }
        },
        'artifactVersioning': {
        'buildNumberFormat': 'timestamp'
        }
    }

    def __init__(self, token: str, owner_name: str, 
                 app_name: str, parent_logger: logging.Logger) -> None:
        super().__init__("branches", token, owner_name, app_name, parent_logger)
        
    def all(self) -> Iterator[BranchList]:
        """List all branches.

        :returns: An iterator of BranchResponse
        """

        self.log.info(
            f"Returning all branches: {self.owner_name}/{self.app_name}"
        )

        request_url = self.generate_url(owner_name=self.owner_name,
                                        app_name=self.app_name)
        request_url += f"/branches?"

        response = self.get(request_url, retry_count=3)

        return deserialize.deserialize(List[BranchList], response.json())
    
    def build(
        self,
        branch_name: str,
        commit: str
    ) -> BuildInfo:
        """Trigger build for specific branch

        :returns: BuildInfo

        """
        
        branch_name = quote_plus(branch_name)
        request_url = self.generate_url(owner_name=self.owner_name,
                                        app_name=self.app_name)

        # First we need to set build configuration
        config_request_url = request_url + f"/branches/{branch_name}/config"
        try:
            self.post(config_request_url, data=self.BUILD_CONFIG)
        except:
            self.put(config_request_url, data=self.BUILD_CONFIG)

        # And now actual build start request
        request_url += f"/branches/{branch_name}/builds"

        params = list({ "sourceVersion": commit, "debug": "true" })

        response = self.post(request_url, data={"params": params})

        return deserialize.deserialize(BuildInfo, response.json())

    def build_info(
        self,
        build_id: int,
    ) -> BuildInfo:
        """Returns build info

        :returns: BuildInfo

        """

        request_url = self.generate_url(owner_name=self.owner_name,
                                        app_name=self.app_name)
        request_url += f"/builds/{build_id}"

        response = self.get(request_url, retry_count=3)

        return deserialize.deserialize(BuildInfo, response.json())

    def builds(
        self,
        branch_name: str,
    ) -> Iterator[BuildInfo]:
        """List all builds for branch.

        :returns: An iterator of BuildList
        """
        
        branch_name = quote_plus(branch_name)
        request_url = self.generate_url(owner_name=self.owner_name,
                                        app_name=self.app_name)
        request_url += f"/branches/{branch_name}/builds"

        response = self.get(request_url, retry_count=3)

        return deserialize.deserialize(List[BuildInfo], response.json())

    def build_log_link(self, build_id: int) -> str:
        """
        Return link to build log

        :returns: String URL
        """

        request_url = self.generate_url(owner_name=self.owner_name,
                                        app_name=self.app_name)
        request_url += f"/builds/{build_id}/downloads/logs" 

        response = self.get(request_url, retry_count=3)

        return response.json().get('uri')
