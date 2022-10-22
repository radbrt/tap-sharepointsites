"""Tests standard tap features using the built-in SDK tests library."""

from tap_sharepointsites.tap import Tapsharepointsites
from .configuration.sample_catalog import sample_catalog

import json

SAMPLE_CONFIG = {
    "api_url": "https://graph.microsoft.com/v1.0/sites/example.sharepoint.com:/sites/demo:/",  # noqa
    "lists": ["list1", "list2"],
}


def test_cli_prints() -> None:
    # Initialize with basic config
    tap1 = Tapsharepointsites(config=SAMPLE_CONFIG, parse_env_config=True)
    # Test CLI prints
    tap1.print_version()
    tap1.print_about()
    tap1.print_about(format="json")


def test_discovery() -> None:
    # catalog1 = _get_tap_catalog(tap_class, config or {})
    catalog1 = json.loads(sample_catalog)
    # Reset and re-initialize with an input catalog
    tap2 = Tapsharepointsites(
        config=SAMPLE_CONFIG, parse_env_config=True, catalog=catalog1
    )
    assert tap2


# def _test_stream_connections() -> None:
#     # Initialize with basic config
#     tap1: Tap = tap_class(config=config, parse_env_config=True)
#     tap1.run_connection_test()


# def _test_pkeys_in_schema() -> None:
#     """Verify that primary keys are actually in the stream's schema."""
#     tap = tap_class(config=config, parse_env_config=True)
#     for name, stream in tap.streams.items():
#         pkeys = stream.primary_keys or []
#         schema_props = set(stream.schema["properties"].keys())
#         for pkey in pkeys:
#             error_message = (
#                 f"Coding error in stream '{name}': "
#                 f"primary_key '{pkey}' is missing in schema"
#             )
#             assert pkey in schema_props, error_message


# def _test_state_partitioning_keys_in_schema() -> None:
#     """Verify that state partitioning keys are actually in the stream's schema."""
#     tap = tap_class(config=config, parse_env_config=True)
#     for name, stream in tap.streams.items():
#         sp_keys = stream.state_partitioning_keys or []
#         schema_props = set(stream.schema["properties"].keys())
#         for sp_key in sp_keys:
#             assert sp_key in schema_props, (
#                 f"Coding error in stream '{name}': state_partitioning_key "
#                 f"'{sp_key}' is missing in schema"
#             )


# def _test_replication_keys_in_schema() -> None:
#     """Verify that the replication key is actually in the stream's schema."""
#     tap = tap_class(config=config, parse_env_config=True)
#     for name, stream in tap.streams.items():
#         rep_key = stream.replication_key
#         if rep_key is None:
#             continue
#         schema_props = set(stream.schema["properties"].keys())
#         assert rep_key in schema_props, (
#             f"Coding error in stream '{name}': replication_key "
#             f"'{rep_key}' is missing in schema"
#         )
