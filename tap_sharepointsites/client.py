"""REST client handling, including sharepointsitesStream base class."""
import requests
from pathlib import Path
from typing import Any, Dict, Optional, Iterable
from datetime import datetime
from urllib.parse import parse_qsl
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

import logging
from singer_sdk.pagination import BaseHATEOASPaginator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
LOGGER = logging.getLogger("Some logger")


class GraphHATEOASPaginator(BaseHATEOASPaginator):
    """Basic paginator"""

    def get_next_url(self, response):
        """Returning the URL for next page"""

        return response.json().get("@odata.nextLink")


class sharepointsitesStream(RESTStream):
    """sharepointsites stream class."""

    # OR use a dynamic url_base:
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$.value[*]"  # Or override `parse_response`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        if self.config.get("client_id"):
            creds = ManagedIdentityCredential(client_id=self.config["client_id"])
        else:
            creds = DefaultAzureCredential()

        token = creds.get_token("https://graph.microsoft.com/.default")

        return BearerTokenAuthenticator.create_for_stream(self, token=token.token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_new_paginator(self):
        """Return paginator class"""
        return GraphHATEOASPaginator()

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return next page link or None"""
        if next_page_token:
            return dict(parse_qsl(next_page_token.query))
        return {}

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""

        row["_loaded_at"] = datetime.utcnow()
        return row
