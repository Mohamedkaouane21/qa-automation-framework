"""Step definitions binding checkout.feature to the existing Page Object Model.

Demonstrates BDD (Gherkin) on top of the same POM the UI layer uses -- no
duplicated automation logic (REQ-BDD-01).
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from config.settings import get_settings
from tests.ui.pages.login_page import LoginPage

# Bind every scenario in the feature file.
scenarios("features/checkout.feature")

pytestmark = [pytest.mark.bdd, pytest.mark.req("REQ-BDD-01")]


@pytest.fixture
def bag() -> dict:
    """Mutable bag to pass page objects between steps.

    Named `bag` (not `context`) to avoid shadowing pytest-playwright's
    `context` BrowserContext fixture.
    """
    return {}


@given("a logged-in standard user")
def logged_in(page, bag):
    settings = get_settings()
    page.set_default_timeout(settings.default_timeout_ms)
    login = LoginPage(page, settings.ui_base_url).open()
    bag["inventory"] = login.login(settings.ui_username, settings.ui_password)


@when(parsers.parse('the user adds "{product}" to the cart'))
def add_product(bag, product):
    bag["inventory"].add_to_cart(product)


@when(
    parsers.parse('the user completes checkout with name "{first}" "{last}" and zip "{zip_code}"')
)
def complete_checkout(bag, first, last, zip_code):
    checkout = bag["inventory"].open_cart().checkout()
    checkout.fill_information(first, last, zip_code).finish()
    bag["checkout"] = checkout


@then("the order is confirmed with a thank-you message")
def order_confirmed(bag):
    assert "thank you" in bag["checkout"].confirmation_message().lower()
