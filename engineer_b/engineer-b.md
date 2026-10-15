# Engineer B feature group

AI-authored code and tests, organized for study and review. This document does
not claim that a fellow personally implemented them.

Application: `engineer_b/workflow.py` and `engineer_b/reports.py`.
Tests: `engineer_b/tests/test_workflow.py`.

These modules import ticket constants and helpers from `engineer_a/tickets.py`.
The shared `main.py` calls them with the same collection used by Engineer A.
The shared storage module persists the resulting assignment and status changes.

Responsibilities: nonblank assignment; resolved-ticket protection; strict
status transitions; explicit reopening; open-only queue; complete reports.

Read `update_status` first: normalize the requested status, reject resolved
records and invalid transitions, check assignment, then mutate. Every check
comes before the assignment to status. Reopening is a separate operation.

The queue filters open records, then sorts by `(priority_rank, numeric_id)`.
Reports count all records, including resolved tickets, in one loop. Their
status and priority subtotals each equal the collection size, and absent
statuses and priorities retain zero counts.

Run this feature group's tests from the root:

```sh
python3 -m unittest engineer_b.tests.test_workflow -v
```

For your defence, explain why in_progress is excluded from this queue, why
T002 precedes T1000, which transitions are invalid, what reopening preserves,
and how an empty report works. Record only your real experiments and reviews.

See [source integration](../docs/source-integration.md) for how these actual
campus files are connected to Mordecai's project. Personal contribution and
peer review evidence still require genuine work by the collaborators.
