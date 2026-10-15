# Data structures and function contracts

These are the implemented contracts for the AI-assisted integration branch.
They document how the application works. Both engineers must review and record
actual agreement; this document does not claim agreement before implementation.

## Responsibilities

Working role map from the conversation: Engineer A is Mordecai
(`mordecai12-cool`); Engineer B is Michael (`miikese`). A owns creation,
validation and priority with matching tests. B owns assignment, lifecycle,
queue and reports with matching tests. Persistence and CLI are shared.
The integration branch also fixes A-module validation issues; A must review
those changes. The repository keeps the suggested campusflow package layout.

## The five contract questions

| Question | Implemented decision |
| --- | --- |
| Where is the collection stored and passed? | run_menu in main.py owns a list of ticket dictionaries, loaded once. Functions receive the list explicitly; update_status/reopen_ticket receive a stored record from that list. There is no mutable module-global collection. |
| How is invalid input signalled and displayed? | Operations raise ValueError before mutation. StorageError subclasses ValueError. The CLI catches errors, prints Error and keeps the menu available; a load error stops startup. |
| What do creation, assignment and updates return? | A shallow copy of the affected ticket dictionary after success. Query/list/queue results are copies. The shared internal lookup returns a mutable stored record for workflow use. |
| Who owns JSON loading/saving? | campusflow/storage.py exports load_tickets(path) and save_tickets(tickets, path). main.py calls them at startup, explicit save and exit. They accept string or pathlib.Path paths. |
| How do we test without interactive input? | Business functions have no input calls. Unit tests call them directly; CLI tests use subprocess input or mocked input; persistence tests use temporary directories. |

## Record schema

Exactly eight fields: id, title, category, urgency, affected_users, priority,
status and assigned_to. Fields are scalar values, so shallow copies suffice.
Title and staff are trimmed nonblank strings; unassigned staff is None.
Categories: Network, Hardware, Software, Other. Urgency: low, medium, high.
Priority: critical, high, medium, low. Status: open, in_progress, resolved.
Affected users is a positive integer, with bool rejected explicitly.
IDs are T001 onward, with at least three digits. Creation allocates the
highest stored numeric suffix plus one; validation failures do not consume IDs.

## Public contracts

```python
# Engineer A: campusflow/tickets.py
calculate_priority(urgency, affected_users) -> str
validate_title(title) -> str  # trimmed title; invalid input raises ValueError
create_ticket(title, category, urgency, affected_users, tickets) -> dict
find_ticket(tickets, ticket_id) -> dict
list_tickets(tickets) -> list
validate_records(tickets) -> list  # same validated collection; no mutation

# Engineer B: campusflow/workflow.py
assign_ticket(tickets, ticket_id, staff_name) -> dict
update_status(ticket, new_status) -> dict
reopen_ticket(ticket) -> dict

# Engineer B: campusflow/reports.py
get_queue(tickets) -> list
generate_report(tickets) -> dict  # total, by_status, by_priority

# Shared: campusflow/storage.py
load_tickets(path) -> list
save_tickets(tickets, path) -> None
```

create_ticket keeps the earlier argument order. tickets.assign_ticket remains
a compatibility wrapper; the assignment implementation lives in workflow.
The CLI uses _find_record internally for workflow mutation. Public find_ticket
returns a copy and must not be used to mutate a stored record.
Errors now consistently raise ValueError rather than returning error strings.
validate_title now returns the trimmed title rather than valid/invalid strings.
These changes are documented for both partners to review.

## Lifecycle and persistence rules

Only open -> in_progress (when assigned), in_progress -> resolved, and explicit
reopening resolved -> open are allowed. Reopening retains assignment.
Assignment is allowed while open/in_progress and rejected while resolved.
Queue filters only open and sorts priority then numeric ID. Reports count all
records once and retain zero-valued categories in both breakdowns.

JSON must be an array of normalized, valid, unique records. Validate exact
fields, types, priority consistency and assignment for progressed/resolved
records; reject duplicate object keys. Missing files start empty. Corruption
stops loading and prevents saving over the damaged file, including damage
introduced after startup. Safe saves validate, serialize UTF-8 JSON, create
parent directories, write/fsync a temporary sibling and use os.replace.
Default storage is project-root/data/tickets.json. This is single-process;
there is no locking or reconciliation of concurrent valid writes.

## Actual agreement record — pending

Each partner should add their own approval or requested changes here, with
actual date, account and commit/PR reference. No signatures, peer approvals
or prior discussions are invented by the assistant.

| Fellow | Agreement status | Evidence to supply |
| --- | --- | --- |
| Mordecai / mordecai12-cool | Pending | Review all five contracts above; record accepted decisions or concrete changes, actual date and PR/commit reference. |
| Michael / miikese | Pending | Review all five contracts above; record accepted decisions or concrete changes, actual date and PR/commit reference. |

The guide requires discussion before implementing features. A later review
can document current agreement, but must not be backdated as an earlier
discussion. The assistant asked for the fellows' actual decisions in chat;
no response has been received at the time of this update.

## Combining the actual campus source with this repository

The engineer_a and engineer_b folders are copied from Michael's local campus
working tree with matching tests. main.py directly imports those modules;
storage uses Engineer A's validation. The older campusflow public API is
retained through adapters: creation keeps the list-last signature and
record-based status/reopen calls wrap the supplied record in a one-item list.
Both APIs therefore operate on the same dictionary records without duplicate
business implementations. Reports and queue use Engineer B's functions.
The mixed-API integration test verifies lifecycle, reports and JSON reload.
See source-integration.md for provenance and copied-file hashes.

## Proposed refactor for partner review

Ticket creation delegates ID calculation to _next_ticket_id after title,
category, urgency and affected-user validation. It still appends only after
all checks pass. The helper reads the highest stored numeric ID and holds no
allocation state, so failed creation after reload does not consume an ID.

Workflow normalizes the target and finds the stored ticket, then delegates
all lifecycle and assignment prerequisites to _validate_transition before
mutating status. Reopening remains a separate explicit operation. Both public
interfaces retain their existing behavior. The two new regression scenarios
passed before the refactor, and all 97 tests passed after it.
These are implemented choices for review, not a signed human agreement.
