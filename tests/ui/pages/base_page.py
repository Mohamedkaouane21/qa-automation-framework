"""Base class shared by all page objects."""

from __future__ import annotations

from playwright.sync_api import Page


class BasePage:
    """Holds the Playwright `page` and small shared helpers.

    Page objects expose intent-level methods (login, add_to_cart) and keep all
    selectors in one place, so tests never touch raw locators.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    @staticmethod
    def slug(product_name: str) -> str:
        """SauceDemo derives data-test ids from the product name.

        "Sauce Labs Backpack" -> "sauce-labs-backpack"
        """
        return product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
