"""SauceDemo login page."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage
from .inventory_page import InventoryPage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page)
        self.base_url = base_url
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator('[data-test="error"]')

    def open(self) -> LoginPage:
        self.page.goto(self.base_url)
        expect(self.login_button).to_be_visible()
        return self

    def login(self, username: str, password: str) -> InventoryPage:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        return InventoryPage(self.page)

    def error_message(self) -> str:
        expect(self.error).to_be_visible()
        return self.error.inner_text()
