"""Stream type classes for tap-sharepointsites."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
    ObjectType
)
from tap_sharepointsites.client import sharepointsitesStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ListStream(sharepointsitesStream):
    """Define custom stream."""
    name = "lists"
    path = ""
    primary_keys = ["id"]
    replication_key = None
    schema = PropertiesList(
        Property("@odata.etag", StringType),
        Property("createdDateTime", StringType),
        Property("eTag", StringType),
        Property("id", StringType),
        Property("lastModifiedDateTime", StringType),
        Property("webUrl", StringType),
        Property("createdBy", ObjectType()),
        Property("lastModifiedBy", ObjectType()),
        Property("parentReference", ObjectType()),      
        Property("contentType", ObjectType()),
        Property("fields@odata.context", StringType),
        Property("fields",  ObjectType()),
    ).to_dict()
