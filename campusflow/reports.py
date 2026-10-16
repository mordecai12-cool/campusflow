"""Compatibility queue and report API backed by Engineer B's source."""

from engineer_b.reports import generate_detailed_report, generate_report
from engineer_b.workflow import work_queue


def get_queue(tickets):
    """Return the shared open queue using the original public function name."""
    return work_queue(tickets)
