Feature: Todo List UI

  Scenario: No todos on initial state
    Given the top page is opened
    Then "No todos." is displayed
    And "0 / 0 Completed" is displayed

  Scenario: Add a todo and show in list
    Given the top page is opened
    When a todo with title "Test" and description "desc" is added via the "Add Todo" button
    Then the todo list displays "Test" and "desc"
    And "0 / 1 Completed" is displayed

  Scenario: Complete a todo
    Given the top page is opened and a todo "Test" "desc" is added
    And "0 / 1 Completed" is displayed
    When the checkbox is checked
    Then "1 / 1 Completed" is displayed

  Scenario: Delete a todo
    Given the top page is opened and a todo "Test" "desc" is added
    And "0 / 1 Completed" is displayed
    When the delete button (🗑️) is clicked
    Then the todo list is empty and "0 / 0 Completed" is displayed
