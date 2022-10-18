"""sharepointsites tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_sharepointsites.streams import (
    sharepointsitesStream,
    ListStream,
)


class Tapsharepointsites(Tap):
    """sharepointsites tap class."""
    name = "tap-sharepointsites"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=False,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.mysample.com",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        return [ListStream(tap=self, name=list_name, path = f"lists/{ list_name }/items?expand=fields") for list_name in self.config['lists']]


if __name__ == "__main__":
    Tapsharepointsites.cli()
