"""Engineer B feature tests. AI-authored; no individual contribution claimed."""

from copy import deepcopy
import unittest

from engineer_b.reports import generate_report
from engineer_a.tickets import create_ticket
from engineer_b.workflow import assign_ticket, reopen_ticket, update_status, work_queue


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Issue", "Other", "low", 1)

    def test_unassigned_ticket_cannot_start_and_state_is_preserved(self):
        before = deepcopy(self.tickets)
        with self.assertRaisesRegex(ValueError, "Assign"):
            update_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets, before)

    def test_assigned_ticket_follows_full_lifecycle(self):
        assigned = assign_ticket(self.tickets, " t001 ", "  Demo Staff  ")
        self.assertEqual(assigned["assigned_to"], "Demo Staff")
        self.assertEqual(update_status(self.tickets, "T001", "IN_PROGRESS")["status"], "in_progress")
        self.assertEqual(update_status(self.tickets, "T001", " resolved ")["status"], "resolved")

    def test_reopened_ticket_completes_second_lifecycle_with_assignment(self):
        assign_ticket(self.tickets, "T001", "Staff")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        reopened = reopen_ticket(self.tickets, "T001")
        self.assertEqual(reopened["assigned_to"], "Staff")
        before = deepcopy(self.tickets)
        for status in ("resolved", "open"):
            with self.subTest(status=status), self.assertRaises(ValueError):
                update_status(self.tickets, "T001", status)
            self.assertEqual(self.tickets, before)

        update_status(self.tickets, "T001", "in_progress")
        resolved = update_status(self.tickets, "T001", "resolved")
        self.assertEqual(resolved["assigned_to"], "Staff")
        self.assertEqual(resolved["status"], "resolved")
        self.assertEqual(work_queue(self.tickets), [])
        self.assertEqual(generate_report(self.tickets), {
            "total": 1,
            "by_status": {"open": 0, "in_progress": 0, "resolved": 1},
            "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 1},
        })

    def test_invalid_transitions_preserve_state(self):
        assign_ticket(self.tickets, "T001", "Staff")
        for status in ("open", "resolved", "closed", None):
            with self.subTest(status=status):
                before = deepcopy(self.tickets)
                with self.assertRaises(ValueError):
                    update_status(self.tickets, "T001", status)
                self.assertEqual(self.tickets, before)
        update_status(self.tickets, "T001", "in_progress")
        for status in ("open", "in_progress"):
            before = deepcopy(self.tickets)
            with self.assertRaises(ValueError):
                update_status(self.tickets, "T001", status)
            self.assertEqual(self.tickets, before)

    def test_blank_staff_and_unknown_id_do_not_mutate(self):
        for identifier, name in (("T001", " "), ("T001", None), ("T999", "Staff")):
            with self.subTest(identifier=identifier, name=name):
                before = deepcopy(self.tickets)
                with self.assertRaises(ValueError):
                    assign_ticket(self.tickets, identifier, name)
                self.assertEqual(self.tickets, before)

    def test_resolved_protected_until_explicit_reopen(self):
        assign_ticket(self.tickets, "T001", "Staff")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        before = deepcopy(self.tickets)
        with self.assertRaisesRegex(ValueError, "Reopen"):
            assign_ticket(self.tickets, "T001", "Replacement")
        for status in ("open", "in_progress", "resolved"):
            with self.assertRaisesRegex(ValueError, "reopen"):
                update_status(self.tickets, "T001", status)
        self.assertEqual(self.tickets, before)
        reopened = reopen_ticket(self.tickets, "T001")
        self.assertEqual(reopened["status"], "open")
        self.assertEqual(reopened["assigned_to"], "Staff")
        self.assertEqual(assign_ticket(self.tickets, "T001", "Replacement")["assigned_to"], "Replacement")

    def test_reopen_requires_resolved_ticket(self):
        before = deepcopy(self.tickets)
        for identifier in ("T001", "T999"):
            with self.assertRaises(ValueError):
                reopen_ticket(self.tickets, identifier)
            self.assertEqual(self.tickets, before)
        assign_ticket(self.tickets, "T001", "Staff")
        update_status(self.tickets, "T001", "in_progress")
        with self.assertRaises(ValueError):
            reopen_ticket(self.tickets, "T001")
        self.assertEqual(self.tickets[0]["status"], "in_progress")

    def test_mutator_results_are_independent_copies(self):
        result = assign_ticket(self.tickets, "T001", "Staff")
        result["assigned_to"] = "Changed"
        result = update_status(self.tickets, "T001", "in_progress")
        result["status"] = "resolved"
        self.assertEqual(self.tickets[0]["assigned_to"], "Staff")
        self.assertEqual(self.tickets[0]["status"], "in_progress")


class QueueAndReportTests(unittest.TestCase):
    def make_report_tickets(self):
        tickets = []
        cases = (
            ("low", 1, "open"),
            ("high", 10, "open"),
            ("low", 2, "in_progress"),
            ("high", 12, "resolved"),
            ("high", 2, "in_progress"),
            ("low", 1, "open"),
        )
        for index, (urgency, count, status) in enumerate(cases, start=1):
            ticket = create_ticket(tickets, f"Issue {index}", "Other", urgency, count)
            if status != "open":
                assign_ticket(tickets, ticket["id"], "Staff")
                update_status(tickets, ticket["id"], "in_progress")
                if status == "resolved":
                    update_status(tickets, ticket["id"], "resolved")
        return tickets

    def test_queue_orders_all_priorities_and_numeric_ids(self):
        tickets = []
        cases = (("T1000", "high", 2), ("T010", "high", 2),
                 ("T003", "low", 1), ("T004", "high", 10),
                 ("T005", "low", 3), ("T002", "high", 2))
        for identifier, urgency, count in cases:
            create_ticket(tickets, "Issue", "Other", urgency, count)
            tickets[-1]["id"] = identifier
        before = deepcopy(tickets)
        queue = work_queue(tickets)
        self.assertEqual([t["id"] for t in queue], ["T004", "T002", "T010", "T1000", "T005", "T003"])
        self.assertEqual(tickets, before)
        queue[0]["title"] = "Changed copy"
        self.assertEqual(tickets, before)

    def test_queue_excludes_in_progress_and_resolved(self):
        tickets = []
        for _ in range(3):
            create_ticket(tickets, "Issue", "Other", "high", 10)
        for identifier in ("T001", "T002"):
            assign_ticket(tickets, identifier, "Staff")
            update_status(tickets, identifier, "in_progress")
        update_status(tickets, "T002", "resolved")
        self.assertEqual([t["id"] for t in work_queue(tickets)], ["T003"])

    def test_empty_queue_and_report(self):
        self.assertEqual(work_queue([]), [])
        self.assertEqual(generate_report([]), {
            "total": 0,
            "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
            "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        })

    def test_report_counts_all_statuses_and_priorities(self):
        tickets = []
        for urgency, count in (("high", 12), ("high", 2), ("low", 4), ("low", 1)):
            create_ticket(tickets, "Issue", "Other", urgency, count)
        assign_ticket(tickets, "T001", "Staff")
        update_status(tickets, "T001", "in_progress")
        assign_ticket(tickets, "T002", "Staff")
        update_status(tickets, "T002", "in_progress")
        update_status(tickets, "T002", "resolved")
        report = generate_report(tickets)
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["by_status"], {"open": 2, "in_progress": 1, "resolved": 1})
        self.assertEqual(report["by_priority"], {"critical": 1, "high": 1, "medium": 1, "low": 1})
        self.assertEqual(sum(report["by_status"].values()), report["total"])
        self.assertEqual(sum(report["by_priority"].values()), report["total"])

    def test_report_counts_repeated_statuses_and_priorities(self):
        report = generate_report(self.make_report_tickets())
        self.assertEqual(report, {
            "total": 6,
            "by_status": {"open": 3, "in_progress": 2, "resolved": 1},
            "by_priority": {"critical": 2, "high": 1, "medium": 0, "low": 3},
        })
        self.assertEqual(sum(report["by_status"].values()), report["total"])
        self.assertEqual(sum(report["by_priority"].values()), report["total"])

    def test_report_preserves_records_order_and_independent_counts(self):
        tickets = self.make_report_tickets()
        tickets.reverse()
        before = deepcopy(tickets)
        report = generate_report(tickets)
        expected_report = deepcopy(report)
        self.assertEqual(tickets, before)

        report["total"] = 999
        report["by_status"]["open"] = 999
        report["by_priority"]["critical"] = 999
        self.assertEqual(tickets, before)
        self.assertEqual(generate_report(tickets), expected_report)
        self.assertEqual(tickets, before)
