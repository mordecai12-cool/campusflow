"""Engineer A feature tests. AI-authored; no individual contribution claimed."""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from campusflow.storage import load_tickets, save_tickets
from engineer_a.tickets import (
    calculate_priority, create_ticket, find_ticket, list_tickets, validate_records,
)


class PriorityTests(unittest.TestCase):
    def test_high_twelve_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_two_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_four_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_one_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_all_rule_boundaries(self):
        cases = (
            ("high", 9, "high"), ("high", 10, "critical"),
            ("low", 2, "low"), ("low", 3, "medium"),
            ("low", 9, "medium"), ("low", 10, "high"),
            ("medium", 1, "medium"), ("medium", 9, "medium"),
            ("medium", 10, "high"),
        )
        for urgency, count, expected in cases:
            with self.subTest(urgency=urgency, count=count):
                self.assertEqual(calculate_priority(urgency, count), expected)

    def test_case_variations_are_normalized(self):
        self.assertEqual(calculate_priority(" HIGH ", 10), "critical")


class TicketTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_creation_has_exact_fields_and_initial_state(self):
        ticket = create_ticket(self.tickets, " Wi-Fi down ", " nEtWoRk ", " HIGH ", 15)
        self.assertEqual(ticket, {
            "id": "T001", "title": "Wi-Fi down", "notes": [], "category": "Network",
            "urgency": "high", "affected_users": 15, "priority": "critical",
            "status": "open", "assigned_to": None,
        })
        self.assertEqual(self.tickets, [ticket])
        self.assertIsNot(self.tickets[0], ticket)

    def test_zero_rejected_without_consuming_id(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            create_ticket(self.tickets, "Issue", "Other", "low", 0)
        self.assertEqual(self.tickets, [])
        self.assertEqual(create_ticket(self.tickets, "Issue", "Other", "low", 1)["id"], "T001")

    def test_invalid_counts_leave_existing_state_unchanged(self):
        create_ticket(self.tickets, "Existing", "Other", "low", 1)
        before = deepcopy(self.tickets)
        for count in (-1, 0, 1.5, 1.0, "2", "hello", True, False, None):
            with self.subTest(count=count):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    create_ticket(self.tickets, "Issue", "Other", "high", count)
                self.assertEqual(self.tickets, before)

    def test_blank_titles_and_invalid_enums_preserve_state(self):
        for title, category, urgency in (
            ("", "Other", "low"), (" \t ", "Other", "low"),
            (None, "Other", "low"), ("Issue", "Wi-Fi", "low"),
            ("Issue", "Other", "urgent"), ("Issue", None, "low"),
        ):
            with self.subTest(title=title, category=category, urgency=urgency):
                with self.assertRaises(ValueError):
                    create_ticket(self.tickets, title, category, urgency, 1)
                self.assertEqual(self.tickets, [])

    def test_ids_use_highest_number_even_with_gaps_and_unsorted_records(self):
        create_ticket(self.tickets, "First", "Other", "low", 1)
        create_ticket(self.tickets, "Second", "Other", "low", 1)
        self.tickets[0]["id"] = "T1000"
        self.tickets.reverse()
        self.assertEqual(create_ticket(self.tickets, "Third", "Other", "low", 1)["id"], "T1001")

    def test_failed_creation_after_reload_preserves_next_id_and_records(self):
        create_ticket(self.tickets, "Existing", "Other", "low", 1)
        self.tickets[0]["id"] = "T999"
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(self.tickets, path)
            loaded = load_tickets(path)
            before = deepcopy(loaded)
            with self.assertRaisesRegex(ValueError, "Title"):
                create_ticket(loaded, " ", "Other", "low", 1)
            self.assertEqual(loaded, before)

            created = create_ticket(loaded, "After reload", "Other", "low", 1)
            self.assertEqual(created["id"], "T1000")
            self.assertEqual(loaded[0], before[0])
            self.assertEqual(len({ticket["id"] for ticket in loaded}), 2)
            save_tickets(loaded, path)
            self.assertEqual(load_tickets(path), loaded)

    def test_lookup_normalizes_id_and_returns_copy(self):
        create_ticket(self.tickets, "Issue", "Other", "low", 1)
        ticket = find_ticket(self.tickets, " t001 ")
        ticket["status"] = "resolved"
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_unknown_or_invalid_ids_are_helpful(self):
        for ticket_id in ("T999", "missing", "", None, "T000", "T0001"):
            with self.subTest(ticket_id=ticket_id):
                with self.assertRaises(ValueError):
                    find_ticket(self.tickets, ticket_id)

    def test_list_handles_empty_and_protects_stored_records(self):
        self.assertEqual(list_tickets(self.tickets), [])
        create_ticket(self.tickets, "Issue", "Other", "low", 1)
        result = list_tickets(self.tickets)
        result[0]["title"] = "Changed copy"
        result.append({})
        self.assertEqual(len(self.tickets), 1)
        self.assertEqual(self.tickets[0]["title"], "Issue")

    def test_valid_records_validate_without_mutating(self):
        create_ticket(self.tickets, "Issue", "Other", "low", 1)
        before = deepcopy(self.tickets)
        self.assertEqual(validate_records(self.tickets), before)
        self.assertEqual(self.tickets, before)
