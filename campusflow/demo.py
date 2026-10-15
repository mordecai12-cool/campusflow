"""Repeatable technical demonstration; no invented collaboration evidence."""

from pathlib import Path
from tempfile import TemporaryDirectory

from engineer_b.reports import generate_report
from .storage import load_tickets, save_tickets
from engineer_a.tickets import calculate_priority, create_ticket, find_ticket
from engineer_b.workflow import assign_ticket, reopen_ticket, update_status, work_queue


def run_demo():
    tickets = []
    print("CampusFlow demonstration — temporary data, no changes to your saved tickets")
    for title, category, urgency, count in (
        ("Campus Wi-Fi is down", "Network", "high", 12),
        ("Broken laptops", "Hardware", "high", 2),
        ("Development environment issue", "Software", "low", 4),
        ("Learning platform question", "Other", "low", 1),
    ):
        ticket = create_ticket(tickets, title, category, urgency, count)
        print(f"Created {ticket['id']}: {urgency} + {count} → {ticket['priority']}")
    for count in (9, 10):
        print(f"Boundary: high + {count} → {calculate_priority('high', count)}")
    before = len(tickets)
    try:
        create_ticket(tickets, "Invalid count", "Other", "low", 0)
    except ValueError as error:
        print(f"Rejected zero users: {error}")
    assert len(tickets) == before
    print(f"Ticket count unchanged: {len(tickets)}")
    try:
        update_status(tickets, "T002", "in_progress")
    except ValueError as error:
        print(f"Rejected unassigned transition: {error}")
    assert find_ticket(tickets, "T002")["status"] == "open"
    print("T002 remains open.")
    assign_ticket(tickets, "T001", "Demo Staff")
    print(f"Assigned ticket: {find_ticket(tickets, 'T001')}")
    for status in ("in_progress", "resolved"):
        update_status(tickets, "T001", status)
        print(f"T001 → {status}")
    try:
        assign_ticket(tickets, "T001", "Another Staff")
    except ValueError as error:
        print(f"Resolved edit rejected: {error}")
    print("Open queue:")
    for ticket in work_queue(tickets):
        print(f"  {ticket['id']}: {ticket['priority']}")
    ties = []
    for identifier in ("T1000", "T010", "T002"):
        create_ticket(ties, "Numeric queue example", "Other", "high", 2)
        ties[-1]["id"] = identifier
    print("Numeric tie-break:", ", ".join(t["id"] for t in work_queue(ties)))
    report = generate_report(tickets)
    print("Report:", report)
    assert sum(report["by_status"].values()) == report["total"]
    assert sum(report["by_priority"].values()) == report["total"]
    with TemporaryDirectory(prefix="campusflow-demo-") as directory:
        path = Path(directory) / "tickets.json"
        save_tickets(tickets, path)
        loaded = load_tickets(path)
        assert loaded == tickets
        print(f"JSON restart reload: {len(loaded)} tickets preserved, including assignment and status.")
        new_ticket = create_ticket(loaded, "After restart", "Software", "medium", 1)
        assert new_ticket["id"] == "T005"
        print(f"Created after reload: {new_ticket['id']} (unique)")
        reopen_ticket(loaded, "T001")
        print("Explicit reopening: T001 → open; staff assignment retained.")
    print("Demo assertions passed. Run unittest separately for automated test evidence.")
    return 0
