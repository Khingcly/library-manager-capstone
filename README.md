# Library Manager — Campus Book Rental and Inventory System

**Capstone Project | 10Alytics Python Fundamentals**  
**Group:** Kingsley, Chukwuemeka & Henry  
**Tools:** Python (core only — no external libraries)

---

## Project Overview

Library Manager is a command-line application that automates the day-to-day operations of a campus library. It handles book inventories, tracks borrow/return transactions, calculates overdue fines, and generates essential reports — all from the terminal.

---

## Problem Statement

Many campus libraries still rely on manual processes to track collections, leading to:
- Inefficient record keeping and misplaced entries
- No real-time visibility into book availability
- Difficulty tracking overdue returns and collecting fines
- Time-consuming manual reporting

Library Manager solves all of this with a simple, menu-driven CLI system.

---

## Features

### A. Inventory Management
- Add new books or increase copies of existing ones
- View full inventory with availability status and visual stock bar
- Search by title, author, or genre

### B. Order Processing
- Checkout: verifies availability, records student name, sets due date (14-day loan)
- Return: validates the transaction, calculates overdue fines (₦50/day)
- All transactions are tracked with unique IDs (e.g. TXN0001)

### C. Reporting
- Real-time inventory report with visual availability bars
- Popular books ranked by checkout frequency
- Transaction summary: active loans, overdue books, estimated fines, completed returns

---

## How to Run

No installation required — just Python 3.

```bash
python library_manager.py
```

You will see a menu like this:

```
==================================================
     LIBRARY MANAGER — Campus Book System
==================================================
  INVENTORY
    1. Add / Update Book
    2. View All Books
    3. Search Books

  TRANSACTIONS
    4. Checkout Book
    5. Return Book

  REPORTS
    6. Inventory Report
    7. Popular Books
    8. Transaction Summary

    0. Exit
==================================================
```

---

## Python Concepts Used

| Concept | Where Used |
|---------|-----------|
| Dictionaries | `inventory`, `active_transactions`, `transaction_log` |
| Functions | Each feature is its own function |
| Loops (`for`) | Displaying inventory, reports |
| Conditionals (`if/else`) | Availability checks, overdue calculation |
| `datetime` module | Borrow date, due date, overdue days |
| String formatting | Formatted table output, progress bars |
| `input()` | All user interactions |
| Global variables | `transaction_counter`, data stores |

---

## Sample Output

```
✔ Checkout successful!
  Transaction ID : TXN0001
  Book           : Python Crash Course
  Student        : Kingsley Andy
  Borrow Date    : 2026-05-23
  Due Date       : 2026-06-06

[B001] Python Crash Course     [████░] 4/5
[B002] Clean Code              [███]   3/3
```

---

## Authors

**Kingsley Andy, Chukwuemeka & Henry**  
10Alytics | Python Fundamentals Capstone
