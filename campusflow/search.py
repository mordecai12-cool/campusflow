def search_tickets(tickets, search_text):
    """Find tickets containing the search text anywhere in their details."""
    search_text = str(search_text or "").strip().casefold()

    if not search_text:
        return []

    matches = []

    for ticket in tickets:
        # Searching the complete record includes IDs, titles, notes, category,
        # urgency, affected users, priority, status, assigned staff and other
        # fields, including values stored inside lists or dictionaries.
        if search_text in str(ticket).casefold():
            matches.append(ticket)

    return matches


def filter_tickets(tickets, category=None, status=None, priority=None):
    """Return tickets matching every filter that the user supplies."""
    category = category.strip().casefold() if category and category.strip() else None
    status = status.strip().casefold() if status and status.strip() else None
    priority = priority.strip().casefold() if priority and priority.strip() else None

    filtered = []

    for ticket in tickets:
        if category and str(ticket.get("category") or "").casefold() != category:
            continue

        if status and str(ticket.get("status") or "").casefold() != status:
            continue

        if priority and str(ticket.get("priority") or "").casefold() != priority:
            continue

        filtered.append(ticket)

    return filtered
