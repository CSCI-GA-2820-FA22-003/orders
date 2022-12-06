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