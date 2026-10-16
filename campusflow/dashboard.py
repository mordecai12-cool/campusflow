"""Student dashboard built from Engineer B's ticket reporting features."""

from engineer_b.reports import generate_detailed_report
from engineer_b.workflow import work_queue


def build_dashboard(tickets):
    """Return dashboard analytics and the current open work queue."""
    report = generate_detailed_report(tickets)

    return {
        "total": report["total"],
        "by_status": report["by_status"],
        "by_priority": report["by_priority"],
        "by_category": report["by_category"],
        "assigned": report["assigned"],
        "unassigned": report["unassigned"],
        "resolution_rate": report["resolution_rate"],
        "work_queue": work_queue(tickets),
    }
