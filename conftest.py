"""Root pytest configuration shared by every test layer."""

from __future__ import annotations


def pytest_configure(config):
    """Belt-and-braces marker registration (also declared in pytest.ini)."""
    config.addinivalue_line(
        "markers", 'req(id): link a test to a requirement ID, e.g. req("REQ-UI-01")'
    )
