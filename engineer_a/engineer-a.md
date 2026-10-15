# Engineer A feature group

AI-authored code and tests, organized for study and review. This document does
not claim that a fellow personally implemented them.

Application: `engineer_a/tickets.py`. Tests: `engineer_a/tests/test_tickets.py`.

The shared `main.py` imports these functions and passes its ticket collection.
Engineer B uses this module's ticket helpers; `campusflow/storage.py` uses its
record validation. All groups work on the same list passed by the caller.

Responsibilities: validate input; normalize allowed choices; apply ordered
priority rules; allocate IDs after validation; create the eight-field record;
list/view copies; validate persisted records for shared integration.

Read `calculate_priority` first. Rule order matters when both high urgency
and ten users match. Next follow `create_ticket`: it validates before looking
up the next ID or appending, so a rejected operation cannot consume an ID.
`max` over numeric suffixes handles unsorted loaded records and gaps.

Run this feature group's tests from the root:

```sh
python3 -m unittest engineer_a.tests.test_tickets -v
```

For your defence, explain why `True` is rejected as a count, how T1000 is
allocated, what prevents blank titles, and why query results are copies.
Run your own unfamiliar-topic experiments and record your genuine findings.
Do not submit AI-authored tests as proof of independent human implementation.
