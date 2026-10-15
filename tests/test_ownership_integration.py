"""Verify both projects' APIs operate on one shared persisted collection."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from campusflow.reports import generate_report, get_queue
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import assign_ticket, update_status
from engineer_a.tickets import create_ticket as create_owned_ticket
from engineer_b.reports import generate_report as generate_owned_report
from engineer_b.workflow import reopen_ticket, update_status as update_owned_status


class OwnershipIntegrationTests(unittest.TestCase):
    def test_both_apis_share_lifecycle_reports_and_persistence(self):
        tickets = []
        created = create_owned_ticket(tickets, "Wi-Fi", "Network", "high", 12)
        assign_ticket(tickets, created["id"], "Staff")
        update_owned_status(tickets, created["id"], "in_progress")
        update_status(tickets[0], "resolved")
        self.assertEqual(find_ticket(tickets, created["id"])["status"], "resolved")
        self.assertEqual(get_queue(tickets), [])
        self.assertEqual(generate_report(tickets), generate_owned_report(tickets))
        self.assertEqual(generate_report(tickets)["by_status"]["resolved"], 1)

        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(tickets, path)
            loaded = load_tickets(path)
            self.assertEqual(loaded, tickets)
            reopened = reopen_ticket(loaded, created["id"])
            self.assertEqual(reopened["assigned_to"], "Staff")
            self.assertEqual([ticket["id"] for ticket in get_queue(loaded)], ["T001"])
            second = create_ticket("Laptop", "Hardware", "low", 1, loaded)
            self.assertEqual(second["id"], "T002")
            save_tickets(loaded, path)
            self.assertEqual(load_tickets(path), loaded)
