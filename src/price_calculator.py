"""Cart price computation.

Mirrors SauceDemo's checkout maths (8% sales tax) so UI tests can assert the
displayed totals against an independent calculation instead of trusting the
page. Keeping this logic in a tested module is what gives the unit-test layer
real meaning rather than testing throwaway code.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

# SauceDemo applies an 8% tax rate at checkout.
TAX_RATE = Decimal("0.08")


def _money(value: Decimal) -> Decimal:
    """Round to 2 decimals, half-up (currency rounding)."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def subtotal(prices: list[float]) -> Decimal:
    """Sum of item prices before tax."""
    if any(p < 0 for p in prices):
        raise ValueError("prices must not be negative")
    total = sum((Decimal(str(p)) for p in prices), Decimal("0"))
    return _money(total)


def tax(prices: list[float], rate: Decimal = TAX_RATE) -> Decimal:
    """Tax owed on the subtotal."""
    return _money(subtotal(prices) * rate)


def total(prices: list[float], rate: Decimal = TAX_RATE) -> Decimal:
    """Grand total = subtotal + tax."""
    return _money(subtotal(prices) + tax(prices, rate))
