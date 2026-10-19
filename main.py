"""CampusFlow command-line helpdesk using only the Python standard library."""

import argparse
from pathlib import Path
import re

from engineer_a.tickets import create_ticket, find_ticket, list_tickets, add_note
from engineer_b.workflow import assign_ticket, reopen_ticket, update_status, work_queue
from engineer_b.reports import generate_report
from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.search import filter_tickets, search_tickets
from campusflow.quiz import run_quiz


DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "tickets.json"
MENU = """
==================================
           CAMPUSFLOW
    Campus Helpdesk Management
==================================
1. Create Ticket
2. List All Tickets
3. View Ticket Details
4. Assign Ticket
5. Update Ticket Status
6. Reopen Resolved Ticket
7. View Work Queue
8. Generate Reports
9. Save Tickets
10. Search Tickets
11. Filter Tickets
12. Engineering Understanding Check
13. Add Note to Ticket
0. Exit
"""


def display_ticket(ticket):
    print(f"\nTicket {ticket['id']}")
    for field, value in ticket.items():
        print(f"  {field}: {value if value is not None else 'None (unassigned)'}")


def display_collection(tickets, empty_message="No tickets found."):
    if not tickets:
        print(empty_message)
    for ticket in tickets:
        staff = ticket["assigned_to"] or "unassigned"
        print(f"{ticket['id']} | {ticket['priority']} | {ticket['status']} | {ticket['title']} | {staff}")


def display_report(tickets):
    report = generate_report(tickets)
    print(f"Total tickets: {report['total']}")
    for group in ("by_status", "by_priority"):
        for label, count in report[group].items():
            print(f"  {label}: {count}")


def ask_count():
    raw = input("Affected users (positive integer): ").strip()
    if not re.fullmatch(r"[0-9]+", raw):
        raise ValueError("Affected users must be a positive integer; text and decimals are not allowed.")
    return int(raw)


def search_menu(tickets):
    """Search all ticket details, let the user choose a result, or return."""
    while True:
        search_text = input(
            "Enter text to search (or 0 to return to the main menu): "
        ).strip()

        if search_text == "0":
            return

        if not search_text:
            print("Please enter a search term, or enter 0 to return to the main menu.")
            continue

        results = search_tickets(tickets, search_text)

        if not results:
            print(f"No tickets matched '{search_text}'. Try another search or enter 0 to return.")
            continue

        print(f"Found {len(results)} matching ticket(s):")
        for number, ticket in enumerate(results, start=1):
            staff = ticket.get("assigned_to") or "unassigned"
            print(
                f"{number}. {ticket.get('id', 'Unknown ID')} | "
                f"{ticket.get('priority', 'unknown')} | "
                f"{ticket.get('status', 'unknown')} | "
                f"{ticket.get('title', '')} | {staff}"
            )

        while True:
            selection = input(
                "Enter a result number to view details, press Enter to search again, "
                "or enter 0 to return to the main menu: "
            ).strip()

            if selection == "0":
                return

            if selection == "":
                break

            if selection.isdigit() and 1 <= int(selection) <= len(results):
                display_ticket(results[int(selection) - 1])
                break

            print(
                f"Invalid selection. Enter a number from 1 to {len(results)}, "
                "press Enter to search again, or enter 0 to return to the main menu."
            )


def run_menu(data_path):
    try:
        tickets = load_tickets(data_path)
    except StorageError as error:
        print(f"Error: {error}")
        print("Startup stopped to protect your data. Restore a valid backup or choose another --data path.")
        return 1
    print(f"Loaded {len(tickets)} ticket(s). Storage: {data_path}")
    dirty = False

    def save_changes():
        save_tickets(tickets, data_path)
        print(f"Saved {len(tickets)} ticket(s) to {data_path}.")

    while True:
        print(MENU)
        try:
            choice = input("Enter choice: ").strip()
            if choice == "0":
                if dirty:
                    save_changes()
                print("Goodbye.")
                return 0
            if choice == "1":
                title = input("Title: ")
                category = input("Category (Network/Hardware/Software/Other): ")
                urgency = input("Urgency (low/medium/high): ")
                affected_users = ask_count()
                ticket = create_ticket(tickets, title, category, urgency, affected_users)
                dirty = True
                print(f"Created {ticket['id']} with {ticket['priority']} priority.")
            elif choice == "2":
                display_collection(list_tickets(tickets))
            elif choice == "3":
                display_ticket(find_ticket(tickets, input("Ticket ID: ")))
            elif choice == "4":
                ticket_id = input("Ticket ID: ")
                staff_name = input("Staff name: ")
                ticket = assign_ticket(tickets, ticket_id, staff_name)
                dirty = True
                print(f"Assigned {ticket['id']} to {ticket['assigned_to']}.")
            elif choice == "5":
                ticket_id = input("Ticket ID: ")
                new_status = input("New status (in_progress/resolved): ")
                ticket = update_status(tickets, ticket_id, new_status)
                dirty = True
                print(f"Ticket {ticket['id']} is now {ticket['status']}.")
            elif choice == "6":
                ticket = reopen_ticket(tickets, input("Resolved ticket ID: "))
                dirty = True
                print(f"Reopened {ticket['id']}; status is open.")
            elif choice == "7":
                display_collection(work_queue(tickets), "No open tickets in the work queue.")
            elif choice == "8":
                display_report(tickets)
            elif choice == "9":
                save_changes()
                dirty = False
            elif choice == "10":
                search_menu(tickets)
            elif choice == "11":
                print("Leave a field empty to ignore that filter.")
                category = input("Category (Network/Hardware/Software/Other): ").strip()
                status = input("Status (open/in_progress/resolved): ").strip()
                priority = input("Priority (critical/high/medium/low): ").strip()
                results = filter_tickets(
                    tickets,
                    category=category or None,
                    status=status or None,
                    priority=priority or None,
                )
                display_collection(results, "No tickets match those filters.")
            elif choice == "12":
                run_quiz()
            elif choice == "13":
                ticket_id = input("Ticket ID: ").strip()
                author = input("Your name: ").strip()
                message = input("Note (5-300 characters): ").strip()
                note = add_note(tickets, ticket_id, author, message)
                dirty = True
                print(f"Note {note['note_id']} added to ticket {ticket_id}.")
            else:
                print("Invalid choice. Enter a number from 0 to 13.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended.")
            if dirty:
                try:
                    save_changes()
                except StorageError as error:
                    print(f"Error: {error} Unsaved changes could not be stored.")
                    return 1
            print("Goodbye.")
            return 0
        except ValueError as error:
            print(f"Error: {error}")
            # Failed saves keep dirty=True and the menu available for retry.


def main(argv=None):
    parser = argparse.ArgumentParser(description="CampusFlow campus helpdesk")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="JSON storage file")
    parser.add_argument("--demo", action="store_true", help="Run a repeatable demo in temporary storage")
    args = parser.parse_args(argv)
    if args.demo:
        from campusflow.demo import run_demo
        return run_demo()
    return run_menu(args.data)


if __name__ == "__main__":
    raise SystemExit(main())
