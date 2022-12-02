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
    And I set the "Name" to "Order1"
    And I set the "Addr" to "Addr1"
    And I press the "Create" button
    Then I should see the message "Success"