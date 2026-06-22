"""Unit tests for the test-data builders (REQ-UNIT-05)."""

import pytest

from src.data_builders import build_booking


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-05")
def test_build_booking_has_required_fields():
    booking = build_booking()
    for field in ("firstname", "lastname", "totalprice", "depositpaid", "bookingdates"):
        assert field in booking
    assert set(booking["bookingdates"]) == {"checkin", "checkout"}


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-05")
def test_build_booking_applies_overrides():
    booking = build_booking(firstname="Alice", totalprice=999)
    assert booking["firstname"] == "Alice"
    assert booking["totalprice"] == 999
    # untouched defaults remain
    assert booking["lastname"] == "Kaouane"


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-05")
def test_build_booking_returns_independent_dicts():
    a = build_booking()
    b = build_booking()
    a["firstname"] = "Mutated"
    assert b["firstname"] == "Mohamed"
