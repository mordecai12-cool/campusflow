"""Compatibility API for Mordecai's callers, backed by Engineer A's source."""

from engineer_a.tickets import (
    CATEGORIES,
    FIELDS,
    PRIORITIES,
    STATUSES,
    URGENCIES,
    _find_record,
    calculate_priority,
    create_ticket as _create_ticket,
    find_ticket,
    list_tickets,
    nonblank,
    normalize_choice,
    ticket_number,
    validate_affected_users,
    validate_records,
    add_note,
)
from engineer_b.workflow import assign_ticket as _assign_ticket

# Compatibility copies created by the legacy API.
_compat_created_records = {}


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket and synchronize its compatibility copy."""
    result = _assign_ticket(tickets, ticket_id, staff_name)

    for reference, _tickets in _compat_created_records.get(result["id"], []):
        if _tickets is tickets:
            reference["assigned_to"] = result["assigned_to"]

    return result.copy()


def create_ticket(*args):
    """Support both the original and shared API argument orders.

    Original:
        create_ticket(title, category, urgency, affected_users, tickets)

    Shared:
        create_ticket(tickets, title, category, urgency, affected_users)
    """
    if len(args) != 5:
        raise TypeError("create_ticket expects 5 arguments.")

    if isinstance(args[0], list):
        tickets, title, category, urgency, affected_users = args
    else:
        title, category, urgency, affected_users, tickets = args

    result = _create_ticket(
        tickets,
        title,
        category,
        urgency,
        affected_users,
    )

    returned = result.copy()
    _compat_created_records[result["id"]] = [(returned, tickets)]
    return returned

def validate_title(title):
    """Validate and return a trimmed title."""
    return nonblank(title, "Title")