def search_tickets(tickets, search_text):
    """Find tickets whose titles contain the search text, ignoring case."""
    search_text = search_text.strip().casefold()

    if not search_text:
        return []

    matches = []

    for ticket in tickets:
        title = ticket.get("title", "")

        if search_text in title.casefold():
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
