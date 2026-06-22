"""UI checkout tests against SauceDemo (REQ-UI-06, 07).

REQ-UI-06 cross-checks the totals SauceDemo displays against an independent
computation from src.price_calculator -- the unit-tested business logic -- so a
pricing regression on the site would fail the test.
"""

import pytest

from src import price_calculator as pc

pytestmark = pytest.mark.ui

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.req("REQ-UI-06")
def test_full_checkout_totals_and_confirmation(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    prices = inventory_page.prices()  # all catalogue prices

    cart = inventory_page.open_cart()
    checkout = cart.checkout()
    checkout.fill_information("Mohamed", "Kaouane", "75000")

    # Independently verify the displayed subtotal/tax/total.
    subtotal = checkout.displayed_subtotal()
    expected_tax = pc.tax([float(subtotal)])
    assert checkout.displayed_tax() == expected_tax
    assert checkout.displayed_total() == pc.total([float(subtotal)])

    checkout.finish()
    assert "thank you" in checkout.confirmation_message().lower()
    # sanity: the two chosen items exist in the catalogue prices
    assert len(prices) >= 2


@pytest.mark.regression
@pytest.mark.req("REQ-UI-07")
def test_checkout_requires_first_name(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    checkout = inventory_page.open_cart().checkout()
    checkout.fill_information("", "Kaouane", "75000")
    assert "first name is required" in checkout.error_message().lower()
