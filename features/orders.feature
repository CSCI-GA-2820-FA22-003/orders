Feature: The order service back-end
    As an Order Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my orders

Background:
    Given the following orders
        | name       | address  |
        | order1     | addr1    |
        | order2     | addr2    |
        | order3     | addr3    |
        | order4     | addr4    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Orders Resource" in the title
    And I should not see "404 Not Found"

Scenario: Create an Order
    When I visit the "Home Page"
    And I set the "Order Name" to "Order1"
    And I set the "Order Addr" to "Addr1"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: Update an Order
    When I visit the "Home Page"
    And I press the "Update-Tab" button
    And I set the "Update Order ID" to "<base> + 1"
    And I set the "Update Order Name" to "Order11"
    And I set the "Update Order Addr" to "Addr11"
    And I press the "Update" button
    Then I should see the message "Success"

Scenario: List All Order
    When I visit the "Home Page"
    And I press the "Listall-Tab" button
    And I press the "Listall" button
    Then I should see "addr1" in the row includes "order1" of "List" table
    Then I should see "addr2" in the row includes "order2" of "List" table
    Then I should see "addr3" in the row includes "order3" of "List" table
    Then I should see "addr4" in the row includes "order4" of "List" table

Scenario: Delete An Order
    When I visit the "Home Page"
    And I press the "Delete-Tab" button
    And I set the "Delete Order ID" to "<base> + 1"
    And I press the "Delete" button
    Then I should see the message "Success"

Scenario: Delete An Non-existent Order
    When I visit the "Home Page"
    And I press the "Delete-Tab" button
    And I set the "Delete Order ID" to "<base> + 5"
    And I press the "Delete" button
    Then I should see the message "not found"

Scenario: Create An Item
    When I visit the "Home Page"
    And I press the "Create-Item-Tab" button
    And I set the "Item ID" to "1"
    And I set the "Item Order ID" to "<base> + 1"
    And I set the "Item Product ID" to "233"
    And I set the "Item Price" to "100"
    And I set the "Item Quantity" to "2"
    And I set the "Item Status" to "good"
    And I press the "Create-Item" button
    Then I should see the message "Success"

Scenario: List All Item Of And Order
    When I visit the "Home Page"
    And I press the "Create-Item-Tab" button
    And I set the "Item ID" to "2"
    And I set the "Item Order ID" to "<base> + 1"
    And I set the "Item Product ID" to "233"
    And I set the "Item Price" to "100"
    And I set the "Item Quantity" to "2"
    And I set the "Item Status" to "good"
    And I press the "Create-Item" button
    And I press the "Listall-Item-Tab" button
    And I set the "Order Id Items" to "<base> + 1"
    And I press the "Listall-Item" button
    Then I should see "233" in the row includes "100" of "List item" table

Scenario: Update An Item
    When I visit the "Home Page"
    And I press the "Create-Item-Tab" button
    And I set the "Item ID" to "1"
    And I set the "Item Order ID" to "<base> + 1"
    And I set the "Item Product ID" to "233"
    And I set the "Item Price" to "100"
    And I set the "Item Quantity" to "2"
    And I set the "Item Status" to "good"
    And I press the "Create-Item" button
    And I copy the item ID from flash message
    And I press the "Update-Item-Tab" button
    And I paste the "Update Item ID" field
    And I set the "Order ID Update" to "<base> + 1"
    And I set the "Update Product ID" to "233"
    And I set the "Update Item Price" to "100"
    And I set the "Update Item Quantity" to "2"
    And I set the "Update Item Status" to "bad"
    And I press the "Update-Item" button
    Then I should see the message "Success"

Scenario: Delete An Item
    When I visit the "Home Page"
    And I press the "Create-Item-Tab" button
    And I set the "Item ID" to "1"
    And I set the "Item Order ID" to "<base> + 1"
    And I set the "Item Product ID" to "233"
    And I set the "Item Price" to "100"
    And I set the "Item Quantity" to "2"
    And I set the "Item Status" to "good"
    And I press the "Create-Item" button
    And I copy the item ID from flash message
    And I press the "Delete-Item-Tab" button
    And I paste the "Item ID Delete" field
    And I set the "Order ID Delete" to "<base> + 1"
    And I press the "Delete-Item" button
    Then I should see the message "Success"
