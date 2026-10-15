"""CampusFlow command-line helpdesk using only the Python standard library."""

import argparse
from pathlib import Path
import re

# Engineer A - Ticket management
from engineer_a.tickets import create_ticket, find_ticket, list_tickets

# Engineer B - Workflow and reports
from engineer_b.workflow import (
    assign_ticket,
    reopen_ticket,
    update_status,
    work_queue,
)
from engineer_b.reports import generate_report

# Engineer B - Search, filtering and quiz
from campusflow.search import filter_tickets, search_tickets
from campusflow.quiz import run_quiz

# Shared storage
from campusflow.storage import StorageError, load_tickets, save_tickets


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
0. Exit
"""


def display_ticket(ticket):
    print(f"\nTicket {ticket['id']}")
    for field, value in ticket.items():
        print(
            f"  {field}: "
            f"{value if value is not None else 'None (unassigned)'}"
        )


def display_collection(tickets, empty_message="No tickets found."):
    if not tickets:
        print(empty_message)

    for ticket in tickets:
        staff = ticket["assigned_to"] or "unassigned"
        print(
            f"{ticket['id']} | "
            f"{ticket['priority']} | "
            f"{ticket['status']} | "
            f"{ticket['title']} | "
            f"{staff}"
            elif choice == "1":
                title = input("Title: ")
                category = input(
                    "Category (Network/Hardware/Software/Other): "
                )
                urgency = input("Urgency (low/medium/high): ")
                affected_users = ask_count()

                ticket = create_ticket(
                    tickets,
                    title,
                    category,
                    urgency,
                    affected_users,
                )

                dirty = True
                print(
                    f"Created {ticket['id']} "
                    f"with {ticket['priority']} priority."
                )

            elif choice == "2":
                display_collection(list_tickets(tickets))

            elif choice == "3":
                ticket_id = input("Ticket ID: ")
                display_ticket(find_ticket(tickets, ticket_id))

            elif choice == "4":
                ticket_id = input("Ticket ID: ")
                staff_name = input("Staff name: ")

                ticket = assign_ticket(
                    tickets,
                    ticket_id,
                    staff_name,
                )

                dirty = True
                print(
                    f"Assigned {ticket['id']} "
                    f"to {ticket['assigned_to']}."
                )

            elif choice == "5":
                ticket_id = input("Ticket ID: ")
                new_status = input(
                    "New status (in_progress/resolved): "
                )

                ticket = update_status(
                    tickets,
                    ticket_id,
                    new_status,
                )

                dirty = True
                print(
                    f"Ticket {ticket['id']} "
                    f"is now {ticket['status']}."
                )

            elif choice == "6":
                ticket_id = input("Resolved ticket ID: ")

                ticket = reopen_ticket(
                    tickets,
                    ticket_id,
                )

                dirty = True
                print(
                    f"Reopened {ticket['id']}; "
                    f"status is open."
                )

            elif choice == "7":
                display_collection(
                    work_queue(tickets),
                    "No open tickets in the work queue.",
                )

            elif choice == "8":
                display_report(tickets)

            elif choice == "9":
                save_changes()
                dirty = False

            elif choice == "10":
                search_text = input(
                    "Enter a title or part of a title: "
                )

                results = search_tickets(
                    tickets,
                    search_text,
                )

                display_collection(
                    results,
                    "No matching tickets found.",
                )

            elif choice == "11":
                print(
                    "Leave a field empty to ignore that filter."
                )

                category = input(
                    "Category (Network/Hardware/Software/Other): "
                ).strip()

                status = input(
                    "Status (open/in_progress/resolved): "
                ).strip()

                priority = input(
                    "Priority (critical/high/medium/low): "
                ).strip()

                results = filter_tickets(
                    tickets,
                    category=category or None,
                    status=status or None,
                    priority=priority or None,
                )

                display_collection(
                    results,
                    "No tickets match those filters.",
                )

            elif choice == "12":
                run_quiz()

            else:
                print(
                    "Invalid choice. "
                    "Enter a number from 0 to 12."
                )

        except (EOFError, KeyboardInterrupt):
            print("\nInput ended.")

            if dirty:
                try:
                    save_changes()

                except StorageError as error:
                    print(
                        f"Error: {error} "
                        "Unsaved changes could not be stored."
                    )
                    return 1

            print("Goodbye.")
            return 0

        except ValueError as error:
            print(f"Error: {error}")
            # Failed saves keep dirty=True for retry.


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="CampusFlow campus helpdesk"
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help="JSON storage file",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a repeatable demo in temporary storage",
    )

    args = parser.parse_args(argv)

    if args.demo:
        from campusflow.demo import run_demo
        return run_demo()

    return run_menu(args.data)


if __name__ == "__main__":
    raise SystemExit(main())