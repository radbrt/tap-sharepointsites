"""REST client handling, including sharepointsitesStream base class."""
import re
import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached
from urllib.parse import parse_qsl
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
import re
import logging
from singer_sdk.pagination import BaseHATEOASPaginator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
LOGGER = logging.getLogger("Some logger")


class GraphHATEOASPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        return response.json().get('@odata.nextLink')


class sharepointsitesStream(RESTStream):
    """sharepointsites stream class."""

    # TODO: Set the API's base URL here:
    # url_base = "https://graph.microsoft.com/v1.0/"
    # https://graph.microsoft.com/{version}/{resource}?{query-parameters}

    # OR use a dynamic url_base:
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        
        return self.config["api_url"]

    records_jsonpath = "$.value[*]"  # Or override `parse_response`.
    #next_page_token_jsonpath = "$.'@odata.nextLink'"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""

        if self.config.get("client_id"):
            creds = ManagedIdentityCredential(client_id=self.config["client_id"])
        else:
            creds = DefaultAzureCredential()

        token = creds.get_token("https://graph.microsoft.com/.default")

        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token.token
        )


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
        return GraphHATEOASPaginator()

    # def get_next_page_token(
    #     self, response: requests.Response, previous_token: Optional[Any]
    # ) -> Optional[Any]:
    #     """Return a token for identifying next page or None if no more pages."""
    #     # TODO: If pagination is required, return a token which can be used to get the
    #     #       next page. If this is the final page, return "None" to end the
    #     #       pagination loop.

    #     # nextpage = extract_jsonpath(self.next_page_token_jsonpath, input=response.json())
    #     nextpage = response.json().get("@odata.nextLink")
    #     if nextpage:
    #         base_token = re.findall(r"\$skiptoken=(.*)", nextpage)[-1]
    #         return {"$skiptoken": base_token}
    #         # return f"$skiptoken={base_token}"
    #     else:
    #         return None


    # def get_url_params(
    #     self, context: Optional[dict], next_page_token: Optional[Any]
    # ) -> Dict[str, Any]:
    #     """Return a dictionary of values to be used in URL parameterization."""
    #     params: dict = {}
    #     if next_page_token:
    #         params["page"] = next_page_token
    #     if self.replication_key:
    #         params["sort"] = "asc"
    #         params["order_by"] = self.replication_key
    #     return params


    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
        ) -> Dict[str, Any]:
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
        # TODO: Delete this method if not needed.
        # regex replace strange key names

        # def subsub(keyname):
        #     r1 = re.sub(r'[^a-zA-Z0-9]', '_', keyname)
        #     r2 = re.sub(r'$[a-zA-Z]+', '_', r1)
        #     return r2
        # LOGGER.info(row)
        # row = {re.sub(r'[^a-zA-Z0-9]', '_', k): v for k, v in row.items()}
        # LOGGER.info(row)
        return row
