# Testing

BlekingePoGO supports both unit- and integration-testing.
Integration-testing currently only works local due to Discord integration.

## Integration-test
Is tied to the command ?test which can only be run in the developer server.
Runs every command the bot has implemented and asserts their functionality.

## Unit-test
Unit-testing is implemented using the pytest framework.
These tests also run remote on each push event.

Run locally with:
pytest
pytest -v
