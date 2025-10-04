#!/usr/bin/env python3
"""
Personal Expense Tracker - CLI
Save file as: expense_tracker.py
Run: python3 expense_tracker.py
"""
import json
import os
import uuid
from datetime import datetime

DATA_FILE = "expenses.json"
DATE_FORMAT = "%Y-%m-%d"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id():
    return uuid.uuid4().hex


def parse_date(s):
    try:
        return datetime.strptime(s, DATE_FORMAT).date()
    except Exception:
        return None


def print_table(rows, headers):
    # compute column widths
    widths = []
    for i, h in enumerate(headers):
        maxw = len(h)
        for r in rows:
            v = str(r[i])
            if len(v) > maxw:
                maxw = len(v)
        widths.append(maxw)
    # header
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(header_line)
    print(sep)
    for r in rows:
        print(" | ".join(str(r[i]).ljust(widths[i]) for i in range(len(headers))))


def add_expense(data):
    print("\n-- Add Expense --")
    # amount
    while True:
        amt = input("Amount: ").strip()
        try:
            amount = float(amt)
            if amount <= 0:
                raise ValueError
            break
        except Exception:
            print("Please enter a positive number (e.g., 250.50).")
    # date
    while True:
        d = input(f"Date ({DATE_FORMAT}) [leave blank = today]: ").strip()
        if not d:
            date = datetime.today().date()
            break
        parsed = parse_date(d)
        if parsed:
            date = parsed
            break
        print("Date must be in YYYY-MM-DD format.")
    category = input("Category (optional, e.g., Food, Travel): ").strip() or "Uncategorized"
    note = input("Note (optional): ").strip()
    expense = {
        "id": generate_id(),
        "amount": round(amount, 2),
        "date": date.strftime(DATE_FORMAT),
        "category": category,
        "note": note,
        "created_at": datetime.now().isoformat(),
    }
    data.append(expense)
    save_data(data)
    print("Expense added successfully.")


def list_expenses_rows(data, filtered):
    rows = []
    for e in filtered:
        rows.append([e["id"][:8], e["date"], f"{e['amount']:.2f}", e.get("category", ""), e.get("note", "")])
    return rows


def view_expenses(data):
    print("\n-- View Expenses --")
    if not data:
        print("No expenses found.")
        return
    cat = input("Filter by category (leave blank to skip): ").strip()
    drange = input("Filter by date range (YYYY-MM-DD to YYYY-MM-DD) leave blank to skip: ").strip()
    start = end = None
    if drange:
        parts = [p.strip() for p in drange.split("to")]
        if len(parts) == 2:
            start = parse_date(parts[0])
            end = parse_date(parts[1])
            if not start or not end:
                print("Invalid date range — ignoring date filter.")
                start = end = None
        else:
            print("Invalid date range format — ignoring date filter.")
    filtered = []
    for e in data:
        if cat and e.get("category", "").lower() != cat.lower():
            continue
        if start and end:
            ed = parse_date(e["date"])
            if not (start <= ed <= end):
                continue
        filtered.append(e)
    filtered.sort(key=lambda x: x["date"])
    rows = list_expenses_rows(data, filtered)
    headers = ["ID", "Date", "Amount", "Category", "Note"]
    if rows:
        print_table(rows, headers)
        total = sum(e["amount"] for e in filtered)
        print(f"\nTotal (shown): {total:.2f}")
    else:
        print("No expenses match the filters.")


def find_expense_by_shortid(data, shortid):
    # return first match where id startswith shortid
    for e in data:
        if e["id"].startswith(shortid):
            return e
    return None


def update_expense(data):
    print("\n-- Update Expense --")
    if not data:
        print("No expenses found.")
        return
    view_expenses(data)
    sid = input("Enter ID (first 8 characters) of expense to update (leave blank to cancel): ").strip()
    if not sid:
        print("Cancelled.")
        return
    exp = find_expense_by_shortid(data, sid)
    if not exp:
        print("Expense not found.")
        return
    print("Press Enter to keep current value.")
    # amount
    while True:
        amt = input(f"Amount [{exp['amount']}]: ").strip()
        if not amt:
            break
        try:
            a = float(amt)
            if a <= 0:
                raise ValueError
            exp["amount"] = round(a, 2)
            break
        except Exception:
            print("Enter a positive number.")
    # date
    while True:
        d = input(f"Date [{exp['date']}]: ").strip()
        if not d:
            break
        parsed = parse_date(d)
        if parsed:
            exp["date"] = parsed.strftime(DATE_FORMAT)
            break
        print("Date must be YYYY-MM-DD.")
    cat = input(f"Category [{exp.get('category','')}]: ").strip()
    if cat:
        exp["category"] = cat
    note = input(f"Note [{exp.get('note','')}]: ").strip()
    if note:
        exp["note"] = note
    exp["updated_at"] = datetime.now().isoformat()
    save_data(data)
    print("Expense updated.")


def delete_expense(data):
    print("\n-- Delete Expense --")
    if not data:
        print("No expenses found.")
        return
    view_expenses(data)
    sid = input("Enter ID (first 8 chars) of expense to delete (leave blank to cancel): ").strip()
    if not sid:
        print("Cancelled.")
        return
    exp = find_expense_by_shortid(data, sid)
    if not exp:
        print("Expense not found.")
        return
    confirm = input(f"Delete expense {sid} [{exp['amount']} on {exp['date']}] ? (y/N): ").strip().lower()
    if confirm == "y":
        data.remove(exp)
        save_data(data)
        print("Expense deleted.")
    else:
        print("Cancelled.")


def show_summary(data):
    print("\n-- Summary Report --")
    if not data:
        print("No expenses found.")
        return
    total = sum(e["amount"] for e in data)
    by_cat = {}
    by_month = {}
    for e in data:
        cat = e.get("category", "Uncategorized")
        by_cat[cat] = by_cat.get(cat, 0) + e["amount"]
        month = e["date"][:7]  # YYYY-MM
        by_month[month] = by_month.get(month, 0) + e["amount"]
    print(f"Total spent: {total:.2f}\n")
    print("By category:")
    rows = [[k, f"{v:.2f}"] for k, v in sorted(by_cat.items(), key=lambda x: -x[1])]
    print_table(rows, ["Category", "Amount"])
    print("\nBy month:")
    rows = [[k, f"{v:.2f}"] for k, v in sorted(by_month.items(), key=lambda x: x[0])]
    print_table(rows, ["Month", "Amount"])


def main_menu():
    data = load_data()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1) Add expense")
        print("2) View expenses")
        print("3) Update expense")
        print("4) Delete expense")
        print("5) Summary report")
        print("6) Exit")
        choice = input("Choose (1-6): ").strip()
        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_expenses(data)
        elif choice == "3":
            update_expense(data)
        elif choice == "4":
            delete_expense(data)
        elif choice == "5":
            show_summary(data)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 1-6.")


if __name__ == "__main__":
    main_menu()
