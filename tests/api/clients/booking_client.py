"""HTTP client for the restful-booker API.

Wraps httpx so tests speak the booking domain ("create_booking") instead of raw
HTTP. Handles auth-token retrieval and is resilient to the target being a free
Heroku dyno that may be cold-starting (retries + a wake-up ping).
"""

from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


class BookingClient:
    def __init__(self, base_url: str, timeout_ms: int = 15000) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout_ms / 1000,
            headers={"Accept": "application/json"},
        )

    # --- lifecycle ---------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    @retry(
        retry=retry_if_exception_type(httpx.TransportError),
        stop=stop_after_attempt(5),
        wait=wait_fixed(3),
        reraise=True,
    )
    def ping(self) -> httpx.Response:
        """Health check (also wakes a sleeping Heroku dyno). Returns 201."""
        return self._client.get("/ping")

    # --- auth --------------------------------------------------------------
    def auth(self, username: str, password: str) -> str:
        """Return an auth token for write operations."""
        resp = self._client.post("/auth", json={"username": username, "password": password})
        resp.raise_for_status()
        token = resp.json().get("token")
        if not token:
            raise RuntimeError(f"auth failed: {resp.text}")
        return token

    # --- bookings ----------------------------------------------------------
    def create_booking(self, payload: dict) -> httpx.Response:
        return self._client.post(
            "/booking", json=payload, headers={"Content-Type": "application/json"}
        )

    def get_booking(self, booking_id: int) -> httpx.Response:
        return self._client.get(f"/booking/{booking_id}")

    def get_booking_ids(self, **params: Any) -> httpx.Response:
        return self._client.get("/booking", params=params or None)

    def update_booking(self, booking_id: int, payload: dict, token: str) -> httpx.Response:
        return self._client.put(
            f"/booking/{booking_id}",
            json=payload,
            headers={"Content-Type": "application/json", "Cookie": f"token={token}"},
        )

    def patch_booking(self, booking_id: int, payload: dict, token: str) -> httpx.Response:
        return self._client.patch(
            f"/booking/{booking_id}",
            json=payload,
            headers={"Content-Type": "application/json", "Cookie": f"token={token}"},
        )

    def delete_booking(self, booking_id: int, token: str) -> httpx.Response:
        return self._client.delete(f"/booking/{booking_id}", headers={"Cookie": f"token={token}"})
