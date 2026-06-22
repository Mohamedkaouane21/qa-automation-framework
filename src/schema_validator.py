"""Thin wrapper around jsonschema used by the API layer.

Centralises JSON Schema validation so API tests can assert response *shape*
(contract testing) in one line, and so the behaviour is itself unit-tested.
"""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


def validate(instance: Any, schema: dict) -> None:
    """Raise ValidationError if `instance` does not satisfy `schema`."""
    Draft202012Validator(schema).validate(instance)


def is_valid(instance: Any, schema: dict) -> bool:
    """Boolean variant for assertions that don't need the error detail."""
    try:
        validate(instance, schema)
        return True
    except ValidationError:
        return False
