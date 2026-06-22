"""SauceDemo inventory (products) page."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.container = page.locator(".inventory_list")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.item_prices = page.locator(".inventory_item_price")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def is_loaded(self) -> bool:
        return self.container.is_visible()

    def add_to_cart(self, product_name: str) -> InventoryPage:
        self.page.locator(f'[data-test="add-to-cart-{self.slug(product_name)}"]').click()
        return self

    def remove_from_cart(self, product_name: str) -> InventoryPage:
        self.page.locator(f'[data-test="remove-{self.slug(product_name)}"]').click()
        return self

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def sort_by(self, value: str) -> InventoryPage:
        """value e.g. 'lohi' (price low to high), 'hilo', 'az', 'za'."""
        self.sort_dropdown.select_option(value)
        return self

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def open_cart(self):
        from .cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page)

    def logout(self) -> None:
        self.menu_button.click()
        expect(self.logout_link).to_be_visible()
        self.logout_link.click()
