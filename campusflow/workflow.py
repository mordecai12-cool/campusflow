"""Compatibility record-based lifecycle API backed by Engineer B's source."""

from engineer_b.workflow import (
    assign_ticket as _assign_ticket,
    reopen_ticket as _reopen_ticket,
    update_status as _update_status,
)
from campusflow.tickets import _compat_created_records


def _single_record_tickets(ticket):
    """Provide the compatibility API with the supplied record."""
    return [ticket]


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket while keeping compatibility record references synchronized."""
    result = _assign_ticket(tickets, ticket_id, staff_name)

    for reference, stored_tickets in _compat_created_records.get(result["id"], []):
        if stored_tickets is tickets:
            reference["assigned_to"] = result["assigned_to"]

    return result.copy()


def update_status(ticket, new_status):
    """Update the real stored record and synchronize the compatibility copy."""
    records = _compat_created_records.get(ticket["id"], [])

    for reference, tickets in records:
        if reference is ticket:
            result = _update_status(tickets, ticket["id"], new_status)
            reference["status"] = result["status"]
            reference["assigned_to"] = result["assigned_to"]
            return result.copy()

    result = _update_status(_single_record_tickets(ticket), ticket["id"], new_status)
    ticket["status"] = result["status"]
    ticket["assigned_to"] = result["assigned_to"]
    return result.copy()


def reopen_ticket(ticket):
    """Reopen the real stored record and synchronize the compatibility copy."""
    records = _compat_created_records.get(ticket["id"], [])

    for reference, tickets in records:
        if reference is ticket:
            result = _reopen_ticket(tickets, ticket["id"])
            reference["status"] = result["status"]
            reference["assigned_to"] = result["assigned_to"]
            return result.copy()

    result = _reopen_ticket(_single_record_tickets(ticket), ticket["id"])
    ticket["status"] = result["status"]
    ticket["assigned_to"] = result["assigned_to"]
    return result.copy()
