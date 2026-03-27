import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime, timedelta
import os

FILE_NAME = "expenses.csv"

# ---------------- LOAD DATA ----------------
def load_data():
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame(columns=["Date", "Category", "Amount"])

    df = pd.read_csv(FILE_NAME, names=["Date", "Category", "Amount"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    return df


# ---------------- ADD EXPENSE ----------------
def add_expense():
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Enter valid date (YYYY-MM-DD) and amount")
        return

    with open(FILE_NAME, "a") as f:
        f.write(f"{date},{category},{amount}\n")

    output.delete(1.0, tk.END)
    output.insert(tk.END, "✅ Expense added successfully\n")


# ---------------- VIEW EXPENSES ----------------
def view_expenses():
    df = load_data()
    output.delete(1.0, tk.END)

    if df.empty:
        output.insert(tk.END, "No expenses found\n")
    else:
        output.insert(tk.END, df.to_string(index=False))


# ---------------- SUMMARY ----------------
def show_summary():
    df = load_data()
    output.delete(1.0, tk.END)

    if df.empty:
        output.insert(tk.END, "No expenses found\n")
        return

    today = datetime.today()
    week_start = today - timedelta(days=7)
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    last_month_end = month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    total = df["Amount"].sum()
    today_sum = df[df["Date"].dt.date == today.date()]["Amount"].sum()
    week_sum = df[df["Date"] >= week_start]["Amount"].sum()
    this_month = df[df["Date"] >= month_start]["Amount"].sum()
    last_month = df[
        (df["Date"] >= last_month_start) &
        (df["Date"] <= last_month_end)
    ]["Amount"].sum()
    year_sum = df[df["Date"] >= year_start]["Amount"].sum()

    output.insert(tk.END, f"""
💰 EXPENSE SUMMARY
────────────────────────────
Total Expense  : ₹{total:.2f}
Today          : ₹{today_sum:.2f}
Last 7 Days    : ₹{week_sum:.2f}
This Month     : ₹{this_month:.2f}
Last Month     : ₹{last_month:.2f}
This Year      : ₹{year_sum:.2f}

📊 MONTH COMPARISON
────────────────────────────
""")

    diff = this_month - last_month

    if diff > 0:
        output.insert(tk.END, f"You spent MORE than last month by ₹{diff:.2f} 📈")
    elif diff < 0:
        output.insert(tk.END, f"You spent LESS than last month by ₹{abs(diff):.2f} 📉")
    else:
        output.insert(tk.END, "You spent SAME as last month ➖")


# ---------------- UI DESIGN ----------------
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("900x550")
root.configure(bg="#f4f6f8")

# Header
tk.Label(
    root,
    text="Personal Expense Tracker",
    font=("Segoe UI", 20, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=10
).pack(fill="x")

# Main container
main_frame = tk.Frame(root, bg="#f4f6f8")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Left form card
form = tk.Frame(main_frame, bg="white", padx=20, pady=20, bd=1, relief="solid")
form.pack(side="left", fill="y", padx=10)

tk.Label(form, text="Add New Expense", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

tk.Label(form, text="Date (YYYY-MM-DD)", bg="white").pack(anchor="w")
date_entry = tk.Entry(form, width=25)
date_entry.pack(pady=5)

tk.Label(form, text="Category", bg="white").pack(anchor="w")
category_entry = tk.Entry(form, width=25)
category_entry.pack(pady=5)

tk.Label(form, text="Amount", bg="white").pack(anchor="w")
amount_entry = tk.Entry(form, width=25)
amount_entry.pack(pady=5)

tk.Button(form, text="Add Expense", bg="#27ae60", fg="white",
          width=20, command=add_expense).pack(pady=10)

tk.Button(form, text="View Expenses", bg="#2980b9", fg="white",
          width=20, command=view_expenses).pack(pady=5)

tk.Button(form, text="Show Summary", bg="#8e44ad", fg="white",
          width=20, command=show_summary).pack(pady=5)

# Right output card
output_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10, bd=1, relief="solid")
output_frame.pack(side="right", fill="both", expand=True)

tk.Label(output_frame, text="Output", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w")

scroll = tk.Scrollbar(output_frame)
scroll.pack(side="right", fill="y")

output = tk.Text(
    output_frame,
    height=20,
    font=("Consolas", 11),
    yscrollcommand=scroll.set,
    wrap="word"
)
output.pack(fill="both", expand=True)
scroll.config(command=output.yview)

root.mainloop()