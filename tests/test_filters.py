import unittest

from campusflow.search import filter_tickets


class TestFilterTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "category": "Hardware",
                "status": "open",
                "priority": "high"
            },
            {
                "id": "T002",
                "category": "Hardware",
                "status": "resolved",
                "priority": "high"
            },
            {
                "id": "T003",
                "category": "Network",
                "status": "open",
                "priority": "high"
            },
            {
                "id": "T004",
                "category": "Hardware",
                "status": "open",
                "priority": "low"
            }
        ]

    def test_combined_filters_use_and_logic(self):
        result = filter_tickets(
            self.tickets,
            category="Hardware",
            status="open",
            priority="high"
        )
        self.assertEqual([t["id"] for t in result], ["T001"])

    def test_category_filter(self):
        result = filter_tickets(self.tickets, category="Network")
        self.assertEqual([t["id"] for t in result], ["T003"])

    def test_status_filter(self):
        result = filter_tickets(self.tickets, status="resolved")
        self.assertEqual([t["id"] for t in result], ["T002"])

    def test_priority_filter(self):
        result = filter_tickets(self.tickets, priority="low")
        self.assertEqual([t["id"] for t in result], ["T004"])

    def test_no_filters_returns_all_tickets(self):
        result = filter_tickets(self.tickets)
        self.assertEqual(
            [t["id"] for t in result],
            ["T001", "T002", "T003", "T004"]
        )


    def test_filters_are_case_insensitive(self):
        result = filter_tickets(self.tickets, category="hardware", status="OPEN", priority="HIGH")
        self.assertEqual([t["id"] for t in result], ["T001"])

    def test_filter_values_ignore_surrounding_whitespace(self):
        result = filter_tickets(self.tickets, category=" Hardware ", status=" open ", priority=" high ")
        self.assertEqual([t["id"] for t in result], ["T001"])


if __name__ == "__main__":
    unittest.main()
