# Review and merge checklist

This is an AI-assisted refactor proposed under the requirement to review
before merge. It is not a record of a completed human review or personal learning.
PR: https://github.com/mordecai12-cool/campusflow2/pull/9.

## Code to review

- engineer_a/tickets.py: _next_ticket_id reads the highest numeric ID and
  returns a new ID. create_ticket calls it only after input validation.
- engineer_b/workflow.py: _validate_transition checks lifecycle and assignment
  before update_status mutates the stored record. Public signatures are unchanged.
- engineer_a/tests/test_tickets.py: an invalid creation after reloading T999
  preserves records; the next successful creation uses T1000 and saves/reloads.
- engineer_b/tests/test_workflow.py: after reopening, skipped/same-status moves
  preserve records; a second complete lifecycle retains assignment and reports correctly.

The two new scenarios passed before refactoring. After refactoring the assistant
ran 97 tests, all seven requirement probes, syntax checks and the temporary-data
demo successfully. Outputs are in refactor-test-output.txt and refactor-demo-output.txt.

## Mordecai's actual review

Read the final PR's Files changed and use a separate checkout to run its code:

```sh
git fetch origin
git worktree add --detach ../campusflow-refactor-review origin/refactor/3-validation-and-ticket-ids
cd ../campusflow-refactor-review
git rev-parse HEAD
python3 -m unittest discover -s . -t . -v
python3 -m compileall -q main.py run.py campusflow engineer_a engineer_b tests
python3 run.py --demo
```

Leave two substantive observations in your own words based on inspection and
checks you actually performed. Useful areas: failed-creation state/ID behavior,
second-lifecycle assignment and transition protection, and compatibility of
the shared record-based and list-based interfaces. If there are blocking
problems, request changes; inspect fixes before approving the final head.

Submit the review from mordecai12-cool. Michael cannot approve his own PR;
the assistant cannot provide Mordecai's personal approval using Michael's
connection. Merge only after the actual approval and passing final checks.

## Individual evidence still to supply

Each fellow supplies actual prompts, predictions, experiments/results and a
verified improvement/correction/rejection for three learning entries. Discuss
the five implemented contracts and record real names, date and decisions in
design-decisions.md. These entries are pending until the fellows provide them.

The assistant has now implemented the two example refactors suggested in the
handoff guide. These completed AI changes are not personal tasks for a fellow
to claim unchanged. Each person still needs their own genuine code/test change
or verifiable evidence of actual earlier independently completed work. A
separate PR under Mordecai's account is needed for the full cross-review process.

## After approval and merge

Fetch latest main into a clean checkout and run the full tests, syntax checks
and demo. Record its actual SHA/output and update the submission form with
the final SHA if it changes. The current published main SHA is still
28ad65a106e8e90bbd666f426ab05aff8271e524 until a new merge occurs.
Historical unreviewed merges remain part of the audit record.
