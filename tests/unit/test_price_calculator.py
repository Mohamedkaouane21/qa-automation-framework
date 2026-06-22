"""Unit tests for the cart price calculator (REQ-UNIT-01..03)."""

from decimal import Decimal

import pytest

from src import price_calculator as pc


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-01")
def test_subtotal_sums_prices():
    assert pc.subtotal([29.99, 9.99, 15.99]) == Decimal("55.97")


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-01")
def test_subtotal_empty_cart_is_zero():
    assert pc.subtotal([]) == Decimal("0.00")


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-01")
def test_subtotal_rejects_negative_price():
    with pytest.raises(ValueError):
        pc.subtotal([10.0, -1.0])


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-02")
def test_tax_is_eight_percent():
    # 100.00 * 0.08 = 8.00
    assert pc.tax([100.0]) == Decimal("8.00")


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-02")
def test_tax_rounds_half_up():
    # subtotal 12.49 -> tax 0.9992 -> rounds to 1.00
    assert pc.tax([12.49]) == Decimal("1.00")


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-03")
def test_total_is_subtotal_plus_tax():
    # subtotal 55.97, tax 4.4776 -> 4.48, total 60.45
    assert pc.total([29.99, 9.99, 15.99]) == Decimal("60.45")


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-03")
def test_total_with_custom_rate():
    assert pc.total([100.0], rate=Decimal("0.20")) == Decimal("120.00")
