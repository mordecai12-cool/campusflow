"""Engineer B feature group: queue and ticket reports."""

from engineer_a.tickets import CATEGORIES, PRIORITIES, STATUSES


def generate_report(tickets):
    """Count statuses and priorities in one pass over ticket records."""
    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}

    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }


def generate_detailed_report(tickets):
    """Return status, priority, category, assignment and resolution analytics."""
    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}
    by_category = {category: 0 for category in CATEGORIES}

    assigned = 0
    resolved = 0

    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1
        by_category[ticket["category"]] += 1

        if ticket["assigned_to"] is None:
            continue

        assigned += 1
        if ticket["status"] == "resolved":
            resolved += 1

    total = len(tickets)
    unassigned = total - assigned
    resolution_rate = (resolved / total * 100) if total else 0.0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "assigned": assigned,
        "unassigned": unassigned,
        "resolution_rate": resolution_rate,
    }
