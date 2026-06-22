"""Unit tests for the JSON Schema validator wrapper (REQ-UNIT-04)."""

import pytest
from jsonschema.exceptions import ValidationError

from src import schema_validator as sv

_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {"type": "object"},
    },
}


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-04")
def test_validate_accepts_valid_instance():
    sv.validate({"bookingid": 1, "booking": {}}, _SCHEMA)  # must not raise


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-04")
def test_validate_raises_on_missing_field():
    with pytest.raises(ValidationError):
        sv.validate({"bookingid": 1}, _SCHEMA)


@pytest.mark.unit
@pytest.mark.req("REQ-UNIT-04")
def test_is_valid_returns_bool():
    assert sv.is_valid({"bookingid": 1, "booking": {}}, _SCHEMA) is True
    assert sv.is_valid({"bookingid": "nope", "booking": {}}, _SCHEMA) is False
