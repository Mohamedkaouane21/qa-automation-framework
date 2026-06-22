Feature: SauceDemo checkout
  As a registered shopper
  I want to buy a product end to end
  So that I receive an order confirmation

  @ui @smoke
  Scenario: Successful checkout of a single item
    Given a logged-in standard user
    When the user adds "Sauce Labs Backpack" to the cart
    And the user completes checkout with name "Mohamed" "Kaouane" and zip "75000"
    Then the order is confirmed with a thank-you message
