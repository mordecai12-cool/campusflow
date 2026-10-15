# Baseline Check

python3 -m unittest discover -s tests -v

* 67 tests ran
* 67 passed
* 0 failures
* 0 errors

## Behaviours Tested

**Invalid affected users:** When affected_users is 0/negative numbers/invalid types, the system rejects the input, shows an error message, and continues without changing the existing ticket collection.

**Invalid/unknown ticket ID:** the system should handle the input safely without crashing or creating an undefined state.

**Corrupted JSON:** The system catches the JSON error, prevents a crash, and preserves the existing data instead of deleting or overwriting it.

## Improvement Needs

- Add stronger centralized validation and safe status/assignment changes.
- Add structured ticket notes with validation and persistence.
- Add ticket search and combined filtering.
- Improve reports with status, priority, category, and resolution analytics.
- Strengthen JSON loading and ticket/note ID continuity.
- Add more meaningful tests for the new requirements.