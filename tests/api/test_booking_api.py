"""REST API tests against restful-booker (REQ-API-01..10)."""

import pytest

from src import schema_validator as sv
from src.data_builders import build_booking
from tests.api import schemas

pytestmark = pytest.mark.api


@pytest.mark.smoke
@pytest.mark.req("REQ-API-10")
def test_healthcheck_ping(api):
    resp = api.ping()
    assert resp.status_code == 201


@pytest.mark.smoke
@pytest.mark.req("REQ-API-01")
def test_auth_returns_token(token):
    assert isinstance(token, str) and len(token) > 0


@pytest.mark.smoke
@pytest.mark.req("REQ-API-02")
def test_create_booking(api):
    payload = build_booking(firstname="Create")
    resp = api.create_booking(payload)
    assert resp.status_code == 200
    body = resp.json()
    sv.validate(body, schemas.CREATE_BOOKING_RESPONSE)
    assert body["booking"]["firstname"] == "Create"


@pytest.mark.smoke
@pytest.mark.req("REQ-API-03")
def test_get_booking_by_id(api, created_booking):
    booking_id = created_booking["bookingid"]
    resp = api.get_booking(booking_id)
    assert resp.status_code == 200
    body = resp.json()
    sv.validate(body, schemas.BOOKING)
    assert body["firstname"] == created_booking["booking"]["firstname"]


@pytest.mark.regression
@pytest.mark.req("REQ-API-04")
def test_get_all_booking_ids(api):
    resp = api.get_booking_ids()
    assert resp.status_code == 200
    sv.validate(resp.json(), schemas.BOOKING_IDS)


@pytest.mark.regression
@pytest.mark.req("REQ-API-05")
def test_update_booking_with_token(api, token, created_booking):
    booking_id = created_booking["bookingid"]
    updated = build_booking(firstname="Updated", lastname="Name")
    resp = api.update_booking(booking_id, updated, token)
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "Updated"


@pytest.mark.regression
@pytest.mark.req("REQ-API-06")
def test_partial_update_booking(api, token, created_booking):
    booking_id = created_booking["bookingid"]
    resp = api.patch_booking(booking_id, {"firstname": "Patched"}, token)
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "Patched"


@pytest.mark.regression
@pytest.mark.req("REQ-API-07")
def test_delete_booking_then_not_found(api, token):
    # Self-contained: create, delete, confirm gone (don't use auto-cleanup fixture).
    booking_id = api.create_booking(build_booking()).json()["bookingid"]
    deleted = api.delete_booking(booking_id, token)
    assert deleted.status_code == 201
    assert api.get_booking(booking_id).status_code == 404


@pytest.mark.regression
@pytest.mark.req("REQ-API-08")
def test_update_without_token_is_forbidden(api, created_booking):
    booking_id = created_booking["bookingid"]
    # No token cookie -> restful-booker rejects with 403.
    resp = api.update_booking(booking_id, build_booking(), token="")
    assert resp.status_code == 403


@pytest.mark.regression
@pytest.mark.req("REQ-API-09")
def test_created_booking_matches_schema(api):
    resp = api.create_booking(build_booking())
    assert sv.is_valid(resp.json(), schemas.CREATE_BOOKING_RESPONSE)
