import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi is not working",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": ""
            },
            {
                "id": "T002",
                "title": "Laptop screen damaged",
                "category": "Hardware",
                "priority": "medium",
                "status": "in_progress",
                "assigned_to": "Ada"
            },
            {
                "id": "T003",
                "title": "Printer is not working",
                "category": "Hardware",
                "priority": "critical",
                "status": "open",
                "assigned_to": ""
            }
        ]

    def test_search_is_case_insensitive(self):
        result = search_tickets(self.tickets, "WORKING")
        self.assertEqual([t["id"] for t in result], ["T001", "T003"])

    def test_search_returns_matching_title_only(self):
        result = search_tickets(self.tickets, "screen")
        self.assertEqual([t["id"] for t in result], ["T002"])

    def test_search_with_no_match_returns_empty_list(self):
        result = search_tickets(self.tickets, "printer jam")
        self.assertEqual(result, [])

    def test_empty_search_returns_empty_list(self):
        result = search_tickets(self.tickets, "   ")
        self.assertEqual(result, [])

    def test_search_does_not_change_original_tickets(self):
        original = [ticket.copy() for ticket in self.tickets]

        search_tickets(self.tickets, "working")

        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()
