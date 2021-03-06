"""Base definition for App Center clients."""

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import time
from typing import Any, Callable, Dict, Optional, Tuple, BinaryIO

import requests

from appcenter.constants import API_BASE_URL

class AppCenterDerivedClient:
    """Base definition for App Center clients.

    :param name: The name of the derived client
    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """

    def __init__(self, name: str, token: str, 
                 owner_name:str, app_name: str, 
                 parent_logger: logging.Logger) -> None:
        self.log = parent_logger.getChild(name)
        self.token = token
        self.owner_name = owner_name
        self.app_name = app_name

    def generate_url(self, *, version: str = "0.1", owner_name: str, app_name: str) -> str:
        """Generate a URL to use for querying the API.

        :param str version: The API version to hit
        :param str owner_name: The name of the owner of the app
        :param str app_name: The name of the app

        :returns: A generated URL base
        """

        url = f"{API_BASE_URL}/v{version}/apps/{owner_name}/{app_name}"
        self.log.debug(f"Generated URL: {url}")
        return url

    def get(self, url: str, *, retry_count: int = 0) -> requests.Response:
        """Perform a GET request to a url

        :param url: The URL to run the GET on
        :param int retry_count: The number of retries remaining if we got a 202 last time

        :returns: The raw response

        :raises Exception: If the request fails with a non 200 status code
        """
        response = requests.get(url, headers={"X-API-Token": self.token})

        if response.status_code == 202 and retry_count > 0:
            self.log.info(
                f"202 response. Sleeping for 10 seconds before invoking App Center again..."
            )
            time.sleep(10)
            return self.get(url, retry_count=retry_count - 1)

        if response.status_code != 200:
            raise Exception(f"App Center request failed: {url} Error: {response.text}")

        return response

    def patch(self, url: str, *, data: Any) -> requests.Response:
        """Perform a PATCH request to a url

        :param url: The URL to run the POST on
        :param data: The JSON serializable data to send

        :returns: The raw response

        :raises Exception: If the request fails with a non 200 status code
        """
        response = requests.patch(
            url, headers={"X-API-Token": self.token, "Content-Type": "application/json"}, json=data
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"App Center request failed: {url} Error: {response.text}")

        return response

    def post(self, url: str, *, data: Any) -> requests.Response:
        """Perform a POST request to a url

        :param url: The URL to run the POST on
        :param data: The JSON serializable data to send

        :returns: The raw response

        :raises Exception: If the request fails with a non 200 status code
        """
        response = requests.post(
            url, headers={"X-API-Token": self.token, "Content-Type": "application/json"}, json=data
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"App Center request failed: {url} Error: {response.text}")
            
        return response
            
            
    def put(self, url: str, *, data: Any) -> requests.Response:
        """Perform a PUT request to a url

        :param url: The URL to run the POST on
        :param data: The JSON serializable data to send

        :returns: The raw response

        :raises Exception: If the request fails with a non 200 status code
        """
        response = requests.put(
            url, headers={"X-API-Token": self.token, "Content-Type": "application/json"}, json=data
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"App Center request failed: {url} Error: {response.text}")

        return response
