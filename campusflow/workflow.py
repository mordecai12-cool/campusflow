"""Compatibility record-based lifecycle API backed by Engineer B's source."""

from engineer_a.tickets import STATUSES
from engineer_b.workflow import (
    assign_ticket, reopen_ticket as _reopen_ticket, update_status as _update_status,
)


def update_status(ticket, new_status):
    """Update the supplied stored record through the shared lifecycle rules."""
    return _update_status([ticket], ticket["id"], new_status)


def reopen_ticket(ticket):
    """Reopen the supplied stored record through the shared lifecycle rules."""
    return _reopen_ticket([ticket], ticket["id"])
