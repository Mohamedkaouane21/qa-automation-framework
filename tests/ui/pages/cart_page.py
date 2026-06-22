"""SauceDemo cart page."""

from __future__ import annotations

from playwright.sync_api import Page

from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.checkout_button = page.locator('[data-test="checkout"]')

    def item_count(self) -> int:
        return self.items.count()

    def contains(self, product_name: str) -> bool:
        return product_name in self.item_names.all_inner_texts()

    def checkout(self):
        from .checkout_page import CheckoutPage

        self.checkout_button.click()
        return CheckoutPage(self.page)
