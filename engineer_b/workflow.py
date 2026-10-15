"""Engineer B feature group: assignment, strict workflow and open queue.

AI-authored implementation; this is not evidence of a fellow's independent work.
"""

from engineer_a.tickets import (
    PRIORITIES, STATUSES, _find_record, nonblank, normalize_choice, ticket_number,
)


def assign_ticket(tickets, ticket_id, staff_name):
    staff_name = nonblank(staff_name, "Staff name")
    ticket = _find_record(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise ValueError("Resolved tickets cannot be reassigned. Reopen the resolved ticket first.")
    ticket["assigned_to"] = staff_name
    return ticket.copy()


def _validate_transition(ticket, new_status):
    """Check a normalized target status before the stored record is changed."""
    current = ticket["status"]
    if current == "resolved":
        raise ValueError("Resolved tickets cannot be modified. Use the explicit reopen command.")
    allowed = {"open": "in_progress", "in_progress": "resolved"}
    if allowed.get(current) != new_status:
        raise ValueError(f"Invalid transition: {current} → {new_status}. Follow open → in_progress → resolved.")
    if new_status == "in_progress" and ticket["assigned_to"] is None:
        raise ValueError("Assign the ticket to a staff member before starting work.")


def update_status(tickets, ticket_id, new_status):
    new_status = normalize_choice(new_status, STATUSES, "Status")
    ticket = _find_record(tickets, ticket_id)
    _validate_transition(ticket, new_status)
    ticket["status"] = new_status
    return ticket.copy()


def reopen_ticket(tickets, ticket_id):
    ticket = _find_record(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise ValueError("Only a resolved ticket can be reopened.")
    ticket["status"] = "open"
    return ticket.copy()


def work_queue(tickets):
    """Only open tickets, sorted by priority then the numeric ticket ID."""
    ranks = {priority: rank for rank, priority in enumerate(PRIORITIES)}
    ordered = sorted(
        (ticket for ticket in tickets if ticket["status"] == "open"),
        key=lambda ticket: (ranks[ticket["priority"]], ticket_number(ticket["id"])),
    )
    return [ticket.copy() for ticket in ordered]

