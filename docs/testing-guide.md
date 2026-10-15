# Testing CampusFlow

Run from the project root with Python 3.10+; no packages need installing.

```sh
python3 -m unittest discover -s . -t . -v
python3 -m compileall -q main.py run.py campusflow engineer_a engineer_b tests
python3 run.py --demo
```

Expected on the refactor branch: 97 tests and OK; the demo ends with Demo assertions passed.
Published main remains at 95 tests until the reviewed refactor is merged.
See [actual refactor results](refactor-test-output.txt).
Tests and demo use temporary storage and do not overwrite saved tickets.
The full command includes both engineer folders and the existing shared suite.
PR #2 has been merged at Michael's request; its merged main passed 66 tests.
The earlier baseline main passed 15 existing tests but failed five additional
requirement probes. Historical evidence is retained in
[main test output](main-test-output.txt), [main contract checks](main-contract-checks.txt)
and [integration contract checks](integration-contract-checks.txt).
See [source integration test output](source-integration-test-output.txt) for
the 95-test combined implementation. Final merged-main verification is also
published in the source-integration PR discussion and GitHub Actions.

Run the additional probes against a checkout without editing its records:

```sh
python3 docs/review_probes.py "$PWD"
```

After approved changes merge, fetch latest main into a clean checkout and run
the whole suite again. Record its exact SHA and actual output. Branch results
must not be presented as results from final main.

Run each responsibility separately:

```sh
python3 -m unittest tests.test_tickets -v
python3 -m unittest tests.test_workflow tests.test_reports -v
python3 -m unittest tests.test_storage tests.test_cli -v
python3 -m unittest engineer_a.tests.test_tickets engineer_b.tests.test_workflow -v
python3 -m unittest tests.test_ownership_integration -v
```

## Required scenarios and regression coverage

| Scenario | Test group |
| --- | --- |
| high/12 -> critical; high/2 -> high; low/4 -> medium; low/1 -> low | PriorityTests in test_tickets.py |
| Zero rejection without mutation or consumed ID | TicketTests in test_tickets.py |
| Unassigned cannot start | TestWorkflow in test_workflow.py |
| Assigned ticket progresses and resolves | TestWorkflow in test_workflow.py |
| Priority ordering and numeric ID ties | TestQueueAndReports in test_reports.py |
| JSON round-trip retains fields and assignment/status | StorageTests in test_storage.py |
| Unique ID after reload | StorageTests in test_storage.py and restart CLI test |

Additional tests cover Boolean/decimal counts, empty views/reports, input
normalization, unknown IDs, illegal lifecycle transitions, resolved assignment,
explicit reopening, repeated report counts, copied results, JSON schema and
key/ID duplication, invalid UTF-8, atomic-save failure and temporary cleanup.
CLI subprocess tests exercise the menu, all eight detail fields, reopening,
saving, restart, malformed startup, invalid input, EOF/Ctrl+C and the clone launcher.

For a manual check, use python3 run.py --data data/practice.json. Create a ticket,
try starting before assignment, assign it, progress then resolve it, try
reassignment, reopen it, inspect queue/report, save and restart. Compare actual
results with the documented contracts and record your own observations.
