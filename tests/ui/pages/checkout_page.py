"""SauceDemo checkout pages (information + overview + completion)."""

from __future__ import annotations

from decimal import Decimal

from playwright.sync_api import Page, expect

from .base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Step one: customer information
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error = page.locator('[data-test="error"]')
        # Step two: overview
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        # Completion
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill_information(self, first: str, last: str, postal: str) -> CheckoutPage:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()
        return self

    def error_message(self) -> str:
        expect(self.error).to_be_visible()
        return self.error.inner_text()

    @staticmethod
    def _money(label_text: str) -> Decimal:
        # "Item total: $29.99" / "Tax: $2.40" / "Total: $32.39"
        return Decimal(label_text.split("$")[1])

    def displayed_subtotal(self) -> Decimal:
        return self._money(self.subtotal_label.inner_text())

    def displayed_tax(self) -> Decimal:
        return self._money(self.tax_label.inner_text())

    def displayed_total(self) -> Decimal:
        return self._money(self.total_label.inner_text())

    def finish(self) -> CheckoutPage:
        self.finish_button.click()
        return self

    def confirmation_message(self) -> str:
        expect(self.complete_header).to_be_visible()
        return self.complete_header.inner_text()
