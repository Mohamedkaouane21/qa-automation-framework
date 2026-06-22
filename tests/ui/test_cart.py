"""UI cart and sorting tests against SauceDemo (REQ-UI-03, 04, 05)."""

import pytest

pytestmark = pytest.mark.ui

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.req("REQ-UI-03")
def test_add_item_updates_badge_and_cart(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    assert inventory_page.cart_count() == 1
    cart = inventory_page.open_cart()
    assert cart.item_count() == 1
    assert cart.contains(BACKPACK)


@pytest.mark.regression
@pytest.mark.req("REQ-UI-04")
def test_remove_item_empties_cart(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    assert inventory_page.cart_count() == 1
    inventory_page.remove_from_cart(BACKPACK)
    assert inventory_page.cart_count() == 0


@pytest.mark.regression
@pytest.mark.req("REQ-UI-05")
def test_sort_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")
    prices = inventory_page.prices()
    assert prices == sorted(prices)
