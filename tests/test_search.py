import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi is not working",
                "notes": "Connection drops in the library",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
                "priority": "high",
                "status": "open",
                "assigned_to": ""
            },
            {
                "id": "T002",
                "title": "Laptop screen damaged",
                "notes": "Screen flickers after startup",
                "category": "Hardware",
                "urgency": "medium",
                "affected_users": 1,
                "priority": "medium",
                "status": "in_progress",
                "assigned_to": "Ada"
            },
            {
                "id": "T003",
                "title": "Printer is not working",
                "notes": "Printer jams frequently",
                "category": "Hardware",
                "urgency": "high",
                "affected_users": 5,
                "priority": "critical",
                "status": "open",
                "assigned_to": ""
            }
        ]

    def test_search_is_case_insensitive(self):
        result = search_tickets(self.tickets, "WORKING")
        self.assertEqual([t["id"] for t in result], ["T001", "T003"])

    def test_search_matches_partial_title(self):
        result = search_tickets(self.tickets, "screen")
        self.assertEqual([t["id"] for t in result], ["T002"])

    def test_search_matches_ticket_id(self):
        result = search_tickets(self.tickets, "t00")
        self.assertEqual([t["id"] for t in result], ["T001", "T002", "T003"])

    def test_search_matches_category(self):
        result = search_tickets(self.tickets, "network")
        self.assertEqual([t["id"] for t in result], ["T001"])

    def test_search_matches_notes(self):
        result = search_tickets(self.tickets, "library")
        self.assertEqual([t["id"] for t in result], ["T001"])

    def test_search_matches_assigned_staff(self):
        result = search_tickets(self.tickets, "ada")
        self.assertEqual([t["id"] for t in result], ["T002"])

    def test_search_matches_status_and_numeric_fields(self):
        self.assertEqual(
            [t["id"] for t in search_tickets(self.tickets, "in_progress")],
            ["T002"]
        )
        self.assertEqual(
            [t["id"] for t in search_tickets(self.tickets, "12")],
            ["T001"]
        )

    def test_search_with_no_match_returns_empty_list(self):
        self.assertEqual(search_tickets(self.tickets, "printer jam that does not exist"), [])

    def test_empty_search_returns_empty_list(self):
        self.assertEqual(search_tickets(self.tickets, "   "), [])
        self.assertEqual(search_tickets(self.tickets, None), [])

    def test_search_does_not_change_original_tickets(self):
        original = [ticket.copy() for ticket in self.tickets]
        search_tickets(self.tickets, "working")
        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()
