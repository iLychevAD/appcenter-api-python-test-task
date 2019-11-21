"""Data type models"""

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import datetime
import enum
from typing import Any, Dict, List, Optional

import deserialize

class BuildInfo:
    id: int
    buildNumber: str
    status: str
    result: Optional[str]
    startTime: Optional[str]
    finishTime: Optional[str]
    logLink: Optional[str]

class BranchCommit:
    sha: str
    url: str

class BranchListItem:
    name: str
    commit: BranchCommit
    build: Optional[BuildInfo]

class BranchList:
    branch: BranchListItem
