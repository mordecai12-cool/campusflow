from campusflow.workflow import get_work_queue
from campusflow.search import search_tickets, filter_tickets
from campusflow.reports import generate_reports
from campusflow.quiz import run_quiz


def create_sample_tickets():
    """Create temporary tickets for testing the CLI."""
    return [
        {
            "id": "T001",
            "title": "Projector not working",
            "category": "Equipment",
            "priority": "high",
            "status": "open",
            "assigned_to": "Amina",
        },
        {
            "id": "T002",
            "title": "Library internet problem",
            "category": "Network",
            "priority": "critical",
            "status": "open",
            "assigned_to": "David",
        },
        {
            "id": "T003",
            "title": "Student portal issue",
            "category": "Software",
            "priority": "medium",
            "status": "in_progress",
            "assigned_to": "Grace",
        },
        {
            "id": "T004",
            "title": "Broken classroom chair",
            "category": "Equipment",
            "priority": "low",
            "status": "resolved",
            "assigned_to": "Amina",
        },
    ]


def display_tickets(tickets):
    """Display the important details of each ticket."""
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        print("-" * 40)
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket.get('assigned_to') or 'Unassigned'}")

    print("-" * 40)


def show_reports(tickets):
    """Display ticket totals and report breakdowns."""
    report = generate_reports(tickets)

    print("\n===== TICKET REPORTS =====")
    print(f"Total tickets: {report['total']}")
    print(f"Resolved tickets: {report['resolved']}")
    print(f"Unresolved tickets: {report['unresolved']}")
    print(
        f"Resolution percentage: "
        f"{report['resolution_percentage']:.2f}%"
    )

    print("\nCounts by status:")
    for status, count in report["status_breakdown"].items():
        print(f"  {status}: {count}")

    print("\nCounts by priority:")
    for priority, count in report["priority_breakdown"].items():
        print(f"  {priority}: {count}")

    print("\nCounts by category:")
    for category, count in report["category_breakdown"].items():
        print(f"  {category}: {count}")


def search_menu(tickets):
    """Ask for a title and display matching tickets."""
    text = input("Enter a title or part of a title: ")
    results = search_tickets(tickets, text)
    display_tickets(results)


def filter_menu(tickets):
    """Filter tickets using any combination of criteria."""
    print("Leave a field empty to ignore that filter.")
    category = input("Category: ").strip()
    status = input("Status (open/in_progress/resolved): ").strip()
    priority = input("Priority (critical/high/medium/low): ").strip()

    results = filter_tickets(
        tickets,
        category=category or None,
        status=status or None,
        priority=priority or None,
    )

    display_tickets(results)


def main():
    tickets = create_sample_tickets()

    while True:
        print("\n====================================")
        print("       CAMPUSFLOW HELPDESK")
        print("====================================")
        print("1. View All Tickets")
        print("2. View Open Work Queue")
        print("3. Search Tickets")
        print("4. Filter Tickets")
        print("5. View Reports")
        print("6. Engineering Understanding Check")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_tickets(tickets)

        elif choice == "2":
            display_tickets(get_work_queue(tickets))

        elif choice == "3":
            search_menu(tickets)

        elif choice == "4":
            filter_menu(tickets)

        elif choice == "5":
            show_reports(tickets)

        elif choice == "6":
            run_quiz()

        elif choice == "7":
            print("Thank you for using CampusFlow. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
