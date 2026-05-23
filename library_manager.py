"""
Capstone Project: Library Manager
A Campus Book Rental and Inventory System

Group: Kingsley, Chukwuemeka & Henry
Course: 10Alytics Python Fundamentals
Description: A command-line application that handles book inventory,
             borrow/return transactions, overdue fines, and reporting.

How to run:
    python library_manager.py
"""

from datetime import date, timedelta

# ============================================================
# DATA STORE — In-memory dictionaries (no database needed)
# ============================================================

# Each book: { book_id: { title, author, genre, total_copies, available_copies, checkout_count } }
inventory = {
    "B001": {"title": "Python Crash Course",      "author": "Eric Matthes",     "genre": "Programming", "total_copies": 5, "available_copies": 5, "checkout_count": 0},
    "B002": {"title": "Clean Code",               "author": "Robert C. Martin", "genre": "Programming", "total_copies": 3, "available_copies": 3, "checkout_count": 0},
    "B003": {"title": "The Data Science Handbook","author": "Field Cady",       "genre": "Data Science","total_copies": 4, "available_copies": 4, "checkout_count": 0},
    "B004": {"title": "Atomic Habits",            "author": "James Clear",      "genre": "Self-Help",   "total_copies": 6, "available_copies": 6, "checkout_count": 0},
    "B005": {"title": "Thinking Fast and Slow",   "author": "Daniel Kahneman",  "genre": "Psychology",  "total_copies": 2, "available_copies": 2, "checkout_count": 0},
}

# Active transactions: { transaction_id: { book_id, student_name, borrow_date, due_date } }
active_transactions = {}

# Completed transactions log
transaction_log = []

# Fine rate per overdue day
FINE_PER_DAY = 50.0   # e.g. ₦50/day
LOAN_DAYS    = 14     # 2-week loan period
transaction_counter = 1


# ============================================================
# MODULE A — INVENTORY MANAGEMENT
# ============================================================

def add_book():
    """Register a new book or increase copies of an existing one."""
    print("\n--- Add / Update Book ---")
    book_id = input("Enter Book ID (e.g. B006): ").strip().upper()

    if book_id in inventory:
        # Book exists — just add more copies
        try:
            extra = int(input(f"'{inventory[book_id]['title']}' already exists. How many copies to add? "))
            inventory[book_id]["total_copies"]     += extra
            inventory[book_id]["available_copies"] += extra
            print(f"Updated. Total copies now: {inventory[book_id]['total_copies']}")
        except ValueError:
            print("Invalid number. No changes made.")
    else:
        # New book entry
        title   = input("Title:  ").strip()
        author  = input("Author: ").strip()
        genre   = input("Genre:  ").strip()
        try:
            copies = int(input("Number of copies: "))
        except ValueError:
            print("Invalid number. Book not added.")
            return

        inventory[book_id] = {
            "title":             title,
            "author":            author,
            "genre":             genre,
            "total_copies":      copies,
            "available_copies":  copies,
            "checkout_count":    0,
        }
        print(f"Book '{title}' added successfully.")


def display_inventory():
    """List all books with formatted output."""
    print("\n" + "=" * 75)
    print(f"{'BOOK ID':<8} {'TITLE':<30} {'AUTHOR':<20} {'AVAIL':>5} {'TOTAL':>5}")
    print("=" * 75)

    if not inventory:
        print("No books in inventory.")
    else:
        for book_id, info in inventory.items():
            avail  = info["available_copies"]
            total  = info["total_copies"]
            status = f"{avail}/{total}"
            print(f"{book_id:<8} {info['title'][:29]:<30} {info['author'][:19]:<20} {avail:>5} {total:>5}")
    print("=" * 75)


def search_books():
    """Search by title, author, or genre."""
    print("\n--- Search Books ---")
    print("Search by: 1) Title  2) Author  3) Genre")
    choice = input("Enter choice (1/2/3): ").strip()

    field_map = {"1": "title", "2": "author", "3": "genre"}
    if choice not in field_map:
        print("Invalid choice.")
        return

    field   = field_map[choice]
    keyword = input(f"Enter {field} keyword: ").strip().lower()
    results = {
        bid: info for bid, info in inventory.items()
        if keyword in info[field].lower()
    }

    if not results:
        print(f"No books found matching '{keyword}' in {field}.")
    else:
        print(f"\nFound {len(results)} result(s):")
        print("-" * 60)
        for bid, info in results.items():
            print(f"  [{bid}] {info['title']} by {info['author']} | Genre: {info['genre']} | Available: {info['available_copies']}/{info['total_copies']}")


# ============================================================
# MODULE B — ORDER PROCESSING (CHECKOUT & RETURN)
# ============================================================

def checkout_book():
    """Verify availability and check out a book to a student."""
    global transaction_counter

    print("\n--- Checkout Book ---")
    display_inventory()

    book_id      = input("Enter Book ID to checkout: ").strip().upper()
    student_name = input("Student name: ").strip()

    # Validate book exists
    if book_id not in inventory:
        print(f"Book ID '{book_id}' not found in inventory.")
        return

    book = inventory[book_id]

    # Check availability
    if book["available_copies"] <= 0:
        print(f"Sorry, '{book['title']}' has no available copies right now.")
        return

    # Process checkout
    borrow_date = date.today()
    due_date    = borrow_date + timedelta(days=LOAN_DAYS)

    txn_id = f"TXN{transaction_counter:04d}"
    transaction_counter += 1

    active_transactions[txn_id] = {
        "book_id":      book_id,
        "student_name": student_name,
        "borrow_date":  borrow_date,
        "due_date":     due_date,
    }

    # Update inventory
    inventory[book_id]["available_copies"] -= 1
    inventory[book_id]["checkout_count"]   += 1

    print(f"\n✔ Checkout successful!")
    print(f"  Transaction ID : {txn_id}")
    print(f"  Book           : {book['title']}")
    print(f"  Student        : {student_name}")
    print(f"  Borrow Date    : {borrow_date}")
    print(f"  Due Date       : {due_date}")


def return_book():
    """Return a book, calculate overdue fines if applicable."""
    print("\n--- Return Book ---")

    if not active_transactions:
        print("No active transactions at the moment.")
        return

    # Show active transactions
    print("\nActive Transactions:")
    print("-" * 65)
    for txn_id, txn in active_transactions.items():
        book_title = inventory[txn["book_id"]]["title"]
        print(f"  {txn_id} | {book_title:<30} | {txn['student_name']:<20} | Due: {txn['due_date']}")
    print("-" * 65)

    txn_id = input("Enter Transaction ID to return: ").strip().upper()

    if txn_id not in active_transactions:
        print(f"Transaction '{txn_id}' not found.")
        return

    txn         = active_transactions[txn_id]
    return_date = date.today()
    due_date    = txn["due_date"]
    book_id     = txn["book_id"]
    book_title  = inventory[book_id]["title"]

    # Calculate overdue fine
    overdue_days = (return_date - due_date).days
    fine = 0.0

    if overdue_days > 0:
        fine = overdue_days * FINE_PER_DAY
        print(f"\n⚠ Book is {overdue_days} day(s) overdue.")
        print(f"  Fine: ₦{fine:,.2f} (₦{FINE_PER_DAY}/day × {overdue_days} days)")
    else:
        days_early = abs(overdue_days)
        print(f"\n✔ Book returned on time ({days_early} day(s) early). No fine.")

    # Update inventory
    inventory[book_id]["available_copies"] += 1

    # Log the transaction
    transaction_log.append({
        "txn_id":       txn_id,
        "book_id":      book_id,
        "book_title":   book_title,
        "student_name": txn["student_name"],
        "borrow_date":  txn["borrow_date"],
        "due_date":     due_date,
        "return_date":  return_date,
        "overdue_days": max(overdue_days, 0),
        "fine":         fine,
    })

    # Remove from active
    del active_transactions[txn_id]

    print(f"  '{book_title}' returned successfully by {txn['student_name']}.")


# ============================================================
# MODULE C — REPORTING
# ============================================================

def report_inventory():
    """Real-time inventory report showing stock levels."""
    print("\n" + "=" * 75)
    print("  REAL-TIME INVENTORY REPORT")
    print("=" * 75)

    total_books     = sum(b["total_copies"] for b in inventory.values())
    available_books = sum(b["available_copies"] for b in inventory.values())
    checked_out     = total_books - available_books

    print(f"  Total Books in System : {total_books}")
    print(f"  Currently Available   : {available_books}")
    print(f"  Currently Checked Out : {checked_out}")
    print("-" * 75)

    for book_id, info in inventory.items():
        avail = info["available_copies"]
        total = info["total_copies"]
        bar   = "█" * avail + "░" * (total - avail)
        print(f"  [{book_id}] {info['title'][:28]:<28} [{bar}] {avail}/{total}")

    print("=" * 75)


def report_popular_books():
    """Show books ranked by checkout frequency."""
    print("\n" + "=" * 60)
    print("  POPULAR BOOKS REPORT (by checkout count)")
    print("=" * 60)

    sorted_books = sorted(
        inventory.items(),
        key=lambda x: x[1]["checkout_count"],
        reverse=True
    )

    if all(info["checkout_count"] == 0 for _, info in sorted_books):
        print("  No checkouts recorded yet.")
    else:
        rank = 1
        for book_id, info in sorted_books:
            if info["checkout_count"] > 0:
                print(f"  #{rank:<3} {info['title'][:30]:<30} — {info['checkout_count']} checkout(s)")
                rank += 1

    print("=" * 60)


def report_transaction_summary():
    """End-of-day report: totals, fines, overdue books."""
    print("\n" + "=" * 70)
    print("  TRANSACTION SUMMARY REPORT")
    print("=" * 70)

    # Active (still out)
    print(f"\n  Active Transactions   : {len(active_transactions)}")
    overdue_active = [
        txn for txn in active_transactions.values()
        if date.today() > txn["due_date"]
    ]
    print(f"  Overdue (not returned): {len(overdue_active)}")

    if overdue_active:
        print("\n  Overdue Books:")
        print("  " + "-" * 60)
        for txn in overdue_active:
            days_over  = (date.today() - txn["due_date"]).days
            est_fine   = days_over * FINE_PER_DAY
            book_title = inventory[txn["book_id"]]["title"]
            print(f"    {book_title[:28]:<28} | {txn['student_name']:<18} | {days_over}d overdue | Est. fine: ₦{est_fine:,.2f}")

    # Completed
    print(f"\n  Completed Returns     : {len(transaction_log)}")
    total_fines = sum(t["fine"] for t in transaction_log)
    print(f"  Total Fines Collected : ₦{total_fines:,.2f}")

    if transaction_log:
        print("\n  Return Log:")
        print("  " + "-" * 65)
        for t in transaction_log:
            fine_str = f"₦{t['fine']:,.2f}" if t["fine"] > 0 else "No fine"
            print(f"    {t['txn_id']} | {t['book_title'][:25]:<25} | {t['student_name']:<18} | {fine_str}")

    print("=" * 70)


# ============================================================
# MAIN MENU — CLI Entry Point
# ============================================================

def main_menu():
    print("\n" + "=" * 50)
    print("     LIBRARY MANAGER — Campus Book System")
    print("=" * 50)
    print("  INVENTORY")
    print("    1. Add / Update Book")
    print("    2. View All Books")
    print("    3. Search Books")
    print("\n  TRANSACTIONS")
    print("    4. Checkout Book")
    print("    5. Return Book")
    print("\n  REPORTS")
    print("    6. Inventory Report")
    print("    7. Popular Books")
    print("    8. Transaction Summary")
    print("\n    0. Exit")
    print("=" * 50)


def run():
    """Main application loop."""
    print("\nWelcome to Library Manager!")
    print(f"Loan period: {LOAN_DAYS} days | Fine rate: ₦{FINE_PER_DAY}/overdue day")

    while True:
        main_menu()
        choice = input("\nEnter your choice: ").strip()

        if   choice == "1": add_book()
        elif choice == "2": display_inventory()
        elif choice == "3": search_books()
        elif choice == "4": checkout_book()
        elif choice == "5": return_book()
        elif choice == "6": report_inventory()
        elif choice == "7": report_popular_books()
        elif choice == "8": report_transaction_summary()
        elif choice == "0":
            print("\nGoodbye! Library session ended.")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

        input("\nPress Enter to continue...")


# ============================================================
if __name__ == "__main__":
    run()
