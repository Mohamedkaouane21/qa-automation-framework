"""UI login tests against SauceDemo (REQ-UI-01, 02, 08)."""

import pytest

pytestmark = pytest.mark.ui

BACKPACK = "Sauce Labs Backpack"


@pytest.mark.smoke
@pytest.mark.req("REQ-UI-01")
def test_valid_login_lands_on_inventory(login_page, settings):
    inventory = login_page.login(settings.ui_username, settings.ui_password)
    assert inventory.is_loaded()


@pytest.mark.regression
@pytest.mark.req("REQ-UI-02")
def test_locked_out_user_sees_error(login_page):
    login_page.login("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.error_message().lower()


@pytest.mark.regression
@pytest.mark.req("REQ-UI-02")
def test_invalid_password_sees_error(login_page):
    login_page.login("standard_user", "wrong_password")
    assert "do not match" in login_page.error_message().lower()


@pytest.mark.regression
@pytest.mark.req("REQ-UI-08")
def test_logout_returns_to_login(inventory_page, page):
    inventory_page.logout()
    assert page.locator("#login-button").is_visible()
