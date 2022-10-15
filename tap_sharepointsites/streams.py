"""Stream type classes for tap-sharepointsites."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_sharepointsites.client import sharepointsitesStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ListStream(sharepointsitesStream):
    """Define custom stream."""
    name = "lists"
    path = ""
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("@odata.etag", th.StringType),
        th.Property("createdDateTime", th.StringType),
        th.Property("eTag", th.StringType),
        th.Property("id", th.StringType),
        th.Property("lastModifiedDateTime", th.StringType),
        th.Property("webUrl", th.StringType),
        # th.Property("createdBy", th.StringType),
        # th.Property("lastModifiedBy", th.StringType),
        # th.Property("parentReference", th.StringType),      
        # th.Property("contentType", th.StringType),
        # th.Property("fields@odata.context", th.StringType),
        # th.Property("fields", th.StringType),
    ).to_dict()
