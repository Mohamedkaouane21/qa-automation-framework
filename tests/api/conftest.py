"""Fixtures for the API test layer."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from config.settings import get_settings
from tests.api.clients.booking_client import BookingClient


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def api(settings) -> Iterator[BookingClient]:
    """Session-scoped client. Pings once to wake a cold Heroku dyno."""
    client = BookingClient(settings.api_base_url, settings.default_timeout_ms)
    client.ping()  # warm up / fail fast if target is unreachable
    yield client
    client.close()


@pytest.fixture(scope="session")
def token(api, settings) -> str:
    return api.auth(settings.api_username, settings.api_password)


@pytest.fixture
def created_booking(api):
    """Create a booking and clean it up afterwards (best effort)."""
    from src.data_builders import build_booking

    resp = api.create_booking(build_booking())
    resp.raise_for_status()
    body = resp.json()
    yield body
    # restful-booker resets periodically; deletion is best-effort cleanup.
    try:
        settings = get_settings()
        tok = api.auth(settings.api_username, settings.api_password)
        api.delete_booking(body["bookingid"], tok)
    except Exception:
        pass
