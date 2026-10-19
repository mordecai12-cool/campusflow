# AI Learning Log

## Engineer A — Mordecai Otit Marvellous

### Interaction 1

Used AI to understand how ticket priority should be calculated. The priority rules were implemented and manually tested with different urgency levels and affected-user counts.

### Interaction 2

Used AI to understand Python unittest and how to create meaningful test cases. Created tests for priority calculation, validation, assignment, workflow, and storage.

### Interaction 3

AI suggested testing the application with invalid inputs. We tested blank titles, invalid categories, invalid urgency, zero affected users, and negative affected users. All tests behaved as expected.

### Interaction 4 — Rejecting an incorrect AI suggestion

I asked AI whether a resolved ticket should be allowed to receive a new note while remaining resolved.

AI suggested that a resolved ticket could accept a new note and remain resolved.

I rejected the suggestion because the project requirements state that notes can only be added to `open` or `in_progress` tickets. A resolved ticket must first be reopened.

I independently verified the rule by running:

`python3 -m unittest tests.test_tickets.TestTickets.test_resolved_ticket_rejects_note_until_reopened -v`

The test passed successfully with `OK`.

This helped me understand that I should compare AI suggestions with the project requirements instead of automatically accepting them. I also learned how to use a specific unit test to verify the required behavior.

## AI Correction and Verification

During the current development session, Engineer A — Mordecai Marvellous personally evaluated an AI suggestion that a resolved ticket could accept a new note while remaining resolved.

The suggestion was rejected because the requirements state that notes are only allowed on `open` and `in_progress` tickets. A resolved ticket must first be reopened.

Mordecai then independently ran:

`python3 -m unittest tests.test_tickets.TestTickets.test_resolved_ticket_rejects_note_until_reopened -v`

The test passed with `OK`.

This is a new verification performed during the current development session and is not presented as a historical experiment.

## Assistant Execution Records

The following records describe work performed by the AI assistant and are retained for technical traceability. They are not claimed as Engineer A's or Engineer B's independent experiments.

The assistant inspected the repository, reproduced validation and workflow issues, generated fixes and regression tests, and ran tests, syntax checks and demos. The corresponding evidence is preserved in the repository's test-output, review, integration and refactor documentation.

Previous assistant execution records may contain references to earlier team members or earlier versions of the project. Those records should not be interpreted as current team attribution.

## Current Team

- **Engineer A — Mordecai Otit Marvellous**
- **Engineer B — Ina Isah**
