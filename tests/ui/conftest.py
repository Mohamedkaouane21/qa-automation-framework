"""Fixtures for the UI test layer.

Relies on pytest-playwright for the `page` fixture and for failure artifacts.
Run UI tests with these flags (also wired into the Makefile and CI) to capture
debugging evidence only when a test fails:

    --screenshot=only-on-failure --video=retain-on-failure \
    --tracing=retain-on-failure --output=reports/ui-artifacts
"""

from __future__ import annotations

import pytest

from config.settings import get_settings
from tests.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture
def login_page(page, settings) -> LoginPage:
    """A fresh, opened login page for each test."""
    page.set_default_timeout(settings.default_timeout_ms)
    return LoginPage(page, settings.ui_base_url).open()


@pytest.fixture
def inventory_page(login_page, settings):
    """Shortcut: already logged in as the standard user, on the inventory page."""
    return login_page.login(settings.ui_username, settings.ui_password)
