"""Environment-driven configuration.

Values are read from environment variables (optionally loaded from a local
`.env` file). Every field has a default pointing at the public demo targets, so
the suite is runnable out of the box on a clean checkout.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # UI target: SauceDemo
    ui_base_url: str = "https://www.saucedemo.com"
    ui_username: str = "standard_user"
    ui_password: str = "secret_sauce"

    # API target: restful-booker
    api_base_url: str = "https://restful-booker.herokuapp.com"
    api_username: str = "admin"
    api_password: str = "password123"

    # Runtime
    default_timeout_ms: int = 15000


@lru_cache
def get_settings() -> Settings:
    """Cached singleton so config is parsed once per process."""
    return Settings()
