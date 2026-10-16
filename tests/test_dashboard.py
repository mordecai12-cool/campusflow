import unittest

from campusflow.dashboard import build_dashboard


class DashboardTests(unittest.TestCase):
    def test_dashboard_contains_summary_and_queue(self):
        tickets = [
            {
                "id": "T001",
                "title": "Network problem",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Broken laptop",
                "category": "Hardware",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Amina",
            },
            {
                "id": "T003",
                "title": "Portal issue",
                "category": "Software",
                "priority": "medium",
                "status": "resolved",
                "assigned_to": "David",
            },
        ]

        dashboard = build_dashboard(tickets)

        self.assertEqual(dashboard["total"], 3)
        self.assertEqual(
            dashboard["by_status"],
            {"open": 1, "in_progress": 1, "resolved": 1},
        )
        self.assertEqual(
            dashboard["by_priority"],
            {"critical": 1, "high": 1, "medium": 1, "low": 0},
        )
        self.assertEqual(
            dashboard["by_category"],
            {"Network": 1, "Hardware": 1, "Software": 1, "Other": 0},
        )
        self.assertEqual(dashboard["assigned"], 2)
        self.assertEqual(dashboard["unassigned"], 1)
        self.assertEqual(dashboard["resolution_rate"], 33.33333333333333)
        self.assertEqual([ticket["id"] for ticket in dashboard["work_queue"]], ["T001"])

    def test_empty_dashboard(self):
        dashboard = build_dashboard([])

        self.assertEqual(dashboard["total"], 0)
        self.assertEqual(
            dashboard["by_status"],
            {"open": 0, "in_progress": 0, "resolved": 0},
        )
        self.assertEqual(
            dashboard["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )
        self.assertEqual(
            dashboard["by_category"],
            {"Network": 0, "Hardware": 0, "Software": 0, "Other": 0},
        )
        self.assertEqual(dashboard["assigned"], 0)
        self.assertEqual(dashboard["unassigned"], 0)
        self.assertEqual(dashboard["resolution_rate"], 0.0)
        self.assertEqual(dashboard["work_queue"], [])

    def test_dashboard_does_not_mutate_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Printer issue",
                "category": "Hardware",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            }
        ]

        before = [ticket.copy() for ticket in tickets]

        dashboard = build_dashboard(tickets)
        dashboard["work_queue"][0]["title"] = "Changed"

        self.assertEqual(tickets, before)


if __name__ == "__main__":
    unittest.main()
