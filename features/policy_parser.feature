Feature: Confirming that the policy parser form displays

    Scenario: check that the form displays
        When I go to the policy parser
        Then I should see the policy parser
    Scenario: check that link to "education" works
        When I click the "education" link
        Then I should see the "education" page