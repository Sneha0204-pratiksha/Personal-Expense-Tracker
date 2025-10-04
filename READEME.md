Personal Expense Tracker

A simple **CLI-based Personal Expense Tracker** built in **Python** for the **Evaao Internship Assignment**.

---

## 🚀 Features

### ✅ Must-Have
- ➕ Add expense (amount, date, note)
- 👀 View expenses
- ✏️ Update expense
- ❌ Delete expense
- 💾 Save data to local JSON file (`expenses.json`)
- ⚙️ Basic validation and error handling

### 🌟 Good-to-Have (Implemented)
- 🗂 Add Categories (Food, Travel, Bills, etc.)
- 📊 Summary Reports (total spent, by category, by month)
- 🔍 Filter by category or date range
- 🖥️ Simple and interactive Command-Line Interface (CLI)

---

## 🧠 Design & Assumptions

- Each expense is stored as a JSON object with:
  - Unique ID (auto-generated)
  - Amount
  - Date (`YYYY-MM-DD` format)
  - Category
  - Note
- All expenses are saved persistently in a local file `expenses.json`.
- If date is not provided, it defaults to today’s date.
- IDs are shortened to the first 8 characters for easier reference in updates/deletions.

---

## ⚙️ Requirements

- Python **3.6 or above**
- No external libraries required (only standard library)

---

## 🏃 How to Run

1. **Download or clone** this repository:
   ```bash
   https://github.com/Sneha0204-pratiksha/Personal-Expense-Tracker.git
