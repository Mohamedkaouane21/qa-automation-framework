"""Test-data builders.

Builders produce valid-by-default payloads with optional overrides, keeping
tests readable and decoupled from the full payload shape. Used by the API and
BDD layers.
"""

from __future__ import annotations

from typing import Any


def build_booking(**overrides: Any) -> dict:
    """A restful-booker booking payload with sane defaults.

    Pass keyword overrides to vary a single field, e.g.
    ``build_booking(totalprice=250)``.
    """
    booking: dict[str, Any] = {
        "firstname": "Mohamed",
        "lastname": "Kaouane",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-07-01", "checkout": "2026-07-10"},
        "additionalneeds": "Breakfast",
    }
    booking.update(overrides)
    return booking
