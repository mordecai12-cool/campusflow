"""End-to-end CLI tests in isolated temporary directories. AI-authored."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from campusflow.storage import load_tickets
from main import run_menu


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tickets.json"

    def run_menu(self, input_text, *extra_args):
        return subprocess.run(
            [sys.executable, str(ROOT / "main.py"), "--data", str(self.path), *extra_args],
            input=input_text, capture_output=True, text=True,
            cwd=self.directory.name, timeout=10, check=False,
        )

    def test_exit_is_clean_and_read_only_session_creates_no_data(self):
        result = self.run_menu("0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CAMPUSFLOW", result.stdout)
        self.assertIn("Goodbye", result.stdout)
        self.assertFalse(self.path.exists())

    def test_clone_launcher_runs_from_another_directory(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "run.py"), "--data", str(self.path)],
            input="0\n", capture_output=True, text=True,
            cwd=self.directory.name, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CAMPUSFLOW", result.stdout)
        self.assertIn("Goodbye", result.stdout)
        self.assertFalse(self.path.exists())

    def test_invalid_choices_loop_until_exit(self):
        result = self.run_menu("hello\n13\n-1\n\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Invalid choice."), 4)
        self.assertIn("Goodbye", result.stdout)

    def test_end_of_input_exits_without_traceback(self):
        result = self.run_menu("")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Goodbye", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_search_and_filter_use_loaded_tickets(self):
        inputs = (
            "1\nWi-Fi down\nNetwork\nhigh\n12\n"
            "10\nWi-Fi\n1\n0\n"
            "11\nNetwork\nopen\ncritical\n"
            "0\n"
        )
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)

        ticket_line = "T001 | critical | open | Wi-Fi down | unassigned"
        self.assertEqual(result.stdout.count(ticket_line), 2)

    def test_search_retries_after_no_match_and_returns_to_menu(self):
        inputs = (
            "1\nWi-Fi down\nNetwork\nhigh\n12\n"
            "10\nno-ticket-matches-this\nNetwork\n1\n0\n"
        )
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No tickets matched 'no-ticket-matches-this'", result.stdout)
        self.assertIn("Found 1 matching ticket(s)", result.stdout)
        self.assertIn("Ticket T001", result.stdout)
        self.assertIn("Goodbye.", result.stdout)

    def test_search_shows_multiple_results_and_allows_selection(self):
        inputs = (
            "1\nWi-Fi down\nNetwork\nhigh\n12\n"
            "1\nWi-Fi slow\nNetwork\nmedium\n3\n"
            "10\nWi-Fi\n2\n0\n0\n"
        )
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Found 2 matching ticket(s)", result.stdout)
        self.assertIn("1. T001", result.stdout)
        self.assertIn("2. T002", result.stdout)
        self.assertIn("Ticket T002", result.stdout)
        self.assertIn("Goodbye.", result.stdout)

    def test_search_invalid_selection_can_be_corrected(self):
        inputs = (
            "1\nWi-Fi down\nNetwork\nhigh\n12\n"
            "10\nWi-Fi\n99\n1\n0\n0\n"
        )
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Invalid selection.", result.stdout)
        self.assertIn("Ticket T001", result.stdout)
        self.assertIn("Goodbye.", result.stdout)

    def test_search_zero_returns_to_main_menu(self):
        result = self.run_menu("10\n0\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("10. Search Tickets", result.stdout)
        self.assertIn("Goodbye.", result.stdout)

    def test_quiz_menu_option_runs_quiz(self):
        output = StringIO()
        with (
            patch("builtins.input", side_effect=["12", "0"]),
            patch("main.run_quiz") as quiz,
            redirect_stdout(output),
        ):
            status = run_menu(self.path)

        self.assertEqual(status, 0)
        quiz.assert_called_once_with()
        self.assertIn("12. Engineering Understanding Check", output.getvalue())

    def test_empty_views_reports_and_unknown_id(self):
        result = self.run_menu("2\n7\n8\n3\nT999\n0\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No tickets found.", result.stdout)
        self.assertIn("No open tickets", result.stdout)
        self.assertIn("Total tickets: 0", result.stdout)
        self.assertIn("Unknown ticket ID", result.stdout)

    def test_full_menu_flow_and_restart(self):
        inputs = (
            "1\n Wi-Fi down \n nEtWoRk \n HIGH \n12\n"
            "1\nLaptop\nHardware\nlow\n1\n"
            "5\nT002\nin_progress\n"
            "4\nt001\n Demo Staff \n"
            "5\nT001\nin_progress\n5\nT001\nresolved\n"
            "4\nT001\nAnother Staff\n"
            "3\nT001\n2\n7\n8\n6\nT001\n9\n0\n"
        )
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)
        for text in ("Created T001 with critical priority", "Created T002 with low priority",
                     "Assign the ticket", "Reopen the resolved ticket", "Total tickets: 2",
                     "Reopened T001", "assigned_to: Demo Staff", "Saved 2 ticket(s)"):
            self.assertIn(text, result.stdout)
        tickets = load_tickets(self.path)
        self.assertEqual(tickets[0]["status"], "open")
        self.assertEqual(tickets[0]["assigned_to"], "Demo Staff")
        self.assertIsNone(tickets[1]["assigned_to"])
        restart = self.run_menu("2\n1\nAfter restart\nOther\nmedium\n1\n0\n")
        self.assertEqual(restart.returncode, 0, restart.stderr)
        self.assertIn("Loaded 2 ticket(s)", restart.stdout)
        self.assertIn("Created T003", restart.stdout)
        self.assertEqual([t["id"] for t in load_tickets(self.path)], ["T001", "T002", "T003"])

    def test_invalid_counts_are_rejected_without_consuming_id(self):
        inputs = ""
        for count in ("0", "-1", "1.5", "True", "text", "1_000"):
            inputs += f"1\nIssue\nOther\nlow\n{count}\n"
        inputs += "1\nValid\nOther\nlow\n1\n0\n"
        result = self.run_menu(inputs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Created T001"), 1)
        self.assertNotIn("Created T002", result.stdout)
        self.assertEqual(len(load_tickets(self.path)), 1)

    def test_eof_during_unfinished_creation_preserves_completed_ticket(self):
        result = self.run_menu("1\nFirst\nOther\nlow\n1\n1\nIncomplete\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        tickets = load_tickets(self.path)
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["title"], "First")

    def test_corrupted_startup_stops_without_overwriting(self):
        self.path.write_text("{broken", encoding="utf-8")
        before = self.path.read_bytes()
        result = self.run_menu("9\n0\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Startup stopped to protect your data", result.stdout)
        self.assertNotIn("Enter choice", result.stdout)
        self.assertEqual(self.path.read_bytes(), before)

    def test_failed_save_is_reported_and_damaged_file_is_preserved(self):
        answers = iter(["1", "Issue", "Other", "low", "1", "9", "0"])
        def next_input(prompt):
            answer = next(answers, None)
            if answer is None:
                raise EOFError
            if answer == "9":
                self.path.write_text("{damaged after startup", encoding="utf-8")
            return answer
        output = StringIO()
        with patch("builtins.input", side_effect=next_input), redirect_stdout(output):
            status = run_menu(self.path)
        self.assertEqual(status, 1)
        self.assertIn("Cannot save", output.getvalue())
        self.assertIn("Unsaved changes could not be stored", output.getvalue())
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{damaged after startup")

    def test_keyboard_interrupt_saves_completed_changes(self):
        answers = ["1", "Issue", "Other", "low", "1", KeyboardInterrupt()]
        output = StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            status = run_menu(self.path)
        self.assertEqual(status, 0)
        self.assertEqual(len(load_tickets(self.path)), 1)

    def test_demo_completes_without_writing_runtime_data(self):
        result = self.run_menu("", "--demo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Demo assertions passed", result.stdout)
        self.assertIn("Numeric tie-break: T002, T010, T1000", result.stdout)
        self.assertIn("Created after reload: T005", result.stdout)
        self.assertFalse(self.path.exists())
