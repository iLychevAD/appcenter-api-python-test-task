#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""App Center API wrapper."""

import json
import logging
import re
import time
from typing import Any, ClassVar, Dict, List, Optional

import requests

#from appcenter.analytics import AppCenterAnalyticsClient
#from appcenter.crashes import AppCenterCrashesClient
#from appcenter.versions import AppCenterVersionsClient
from appcenter.branches import AppCenterBranchesClient


class AppCenterClient:
    """Class responsible for getting data from App Center through REST calls.

    :param str access_token: The access token to use for authentication. Leave as None to use KeyVault
    """

    log: logging.Logger
    token: str
    owner_name: str
    app_name: str

    #analytics: AppCenterAnalyticsClient
    #crashes: AppCenterCrashesClient
    #versions: AppCenterVersionsClient
    branches: AppCenterBranchesClient

    def __init__(
        self, *, access_token: str, owner_name: str, app_name: str,
        parent_logger: Optional[logging.Logger] = None
    ) -> None:
        """Initialize the AppCenterClient with the application id and the token."""

        if parent_logger is None:
            self.log = logging.getLogger("appcenter")
        else:
            self.log = parent_logger.getChild("appcenter")

        self.token = access_token
        self.owner_name = owner_name
        self.app_name = app_name
        #self.analytics = AppCenterAnalyticsClient(self.token, self.log)
        #self.crashes = AppCenterCrashesClient(self.token, self.log)
        self.branches = AppCenterBranchesClient(self.token, self.owner_name, self.app_name, self.log)
