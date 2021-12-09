Feature: The Shopcarts service back-end
    As a Shopcart Owner
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts and products

Background: 
     Given the following shopcarts
         | Customer ID | Product ID | Product Name | Product Price | Product Quantity |
         | 10001       | 1001       | "a"          | 100           | 1                |
         | 10002       | 1002       | "b"          | 200           | 2                |
         | 10003       | 1003       | "c"          | 300           | 3                |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcart Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Add a product to a customer's shopcart
    When I visit the "Home Page"
    And I set the "Customer ID" to "10080"
    And I set the "Product ID" to "1080"
    And I set the "Product Name" to "chrysanthemum"
    And I set the "Product Price" to "9"
    And I set the "Product Quantity" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Customer ID" to "10080"
    And I press the "Retrieve" button
    Then I should see "10080" in the "Customer ID" field
    # And I should see "1080" in the "Product ID" field
    # And I should see "chrysanthemum" in the "Product Name" field
    # And I should see "9" in the "Product Price" field
    # And I should see "2" in the "Product Quantity" field

Scenario: Update the quantity of an item in a Shopcart
    When I visit the "Home Page"
    And I set the "Customer ID" to "10001"
    And I set the "Product ID" to "1001"
    And I press the "Retrieve" button
    Then I should see "10001" in the "Customer ID" field
    And I should see "1001" in the "Product ID" field
    And I should see "a" in the "Product Name" field
    And I should see "100" in the "Product Price" field
    And I should see "1" in the "Product Quantity" field
    When I set the "Product Quantity" to "4"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Customer ID" field
    And I press the "Clear" button
    And I paste the "Customer ID" field
    And I set the "Product ID" to "1001"
    And I press the "Retrieve" button
    Then I should see "4" in the "Product Quantity" field

Scenario: Checkout a customer
    When I visit the "Home Page"
    And I set the "Customer ID" to "10080"
    And I set the "Product ID" to "1080"
    And I set the "Product Name" to "chrysanthemum"
    And I set the "Product Price" to "9"
    And I set the "Product Quantity" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Customer ID" to "10080"
    And I press the "Checkout" button
    Then the "Customer ID" field should be empty
    And the "Product ID" field should be empty
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And I should see the message "Checkout Successful for Customer: 10080"