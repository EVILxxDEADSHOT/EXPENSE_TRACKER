import mysql.connector
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import messagebox

# Define Colors
BG_COLOR = "#161616"
TEXT_COLOR = "white"
BUTTON_COLOR = "#D32F2F"
ENTRY_COLOR = "#1E1E1E"

# Database Setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="expense_tracker"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(255),
        amount DECIMAL(10, 2),
        category VARCHAR(255),
        account ENUM('Saving', 'Current'),
        note TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(255),
        amount DECIMAL(10, 2),
        category VARCHAR(255),
        account ENUM('Saving', 'Current'),
        note TEXT
    )
""")
conn.commit()

def save_income():
    cursor.execute("INSERT INTO income (date, amount, category, account, note) VALUES (%s, %s, %s, %s, %s)",
                   (date_entry.get(), amount_entry.get(), category_var.get(), account_var.get(), note_entry.get()))
    conn.commit()
    update_totals()
    clear_entries()
    show_popup("Income added successfully!")

def save_expense():
    cursor.execute("INSERT INTO expense (date, amount, category, account, note) VALUES (%s, %s, %s, %s, %s)",
                   (date_entry.get(), amount_entry.get(), category_var.get(), account_var.get(), note_entry.get()))
    conn.commit()
    update_totals()
    clear_entries()
    show_popup("Expense added successfully!")

def fetch_entries():
    selected_date = history_date_entry.get()
    for row in table.get_children():
        table.delete(row)

    cursor.execute("SELECT date, amount, category, account, note, 'Income' FROM income WHERE date = %s", (selected_date,))
    income_data = cursor.fetchall()

    cursor.execute("SELECT date, amount, category, account, note, 'Expense' FROM expense WHERE date = %s", (selected_date,))
    expense_data = cursor.fetchall()

    for entry in income_data + expense_data:
        table.insert("", "end", values=entry)

def update_totals():
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income.set(cursor.fetchone()[0] or 0)
    cursor.execute("SELECT SUM(amount) FROM expense")
    total_expense.set(cursor.fetchone()[0] or 0)

def clear_entries():
    date_entry.set_date('')
    amount_entry.delete(0, tk.END)
    category_var.set('')
    account_var.set('')
    note_entry.delete(0, tk.END)

def show_popup(message):
    messagebox.showinfo("Success", message)

# Initialize Window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("450x750")
root.configure(bg=BG_COLOR)

# Income & Expense Selection Frame
frame_top = tk.Frame(root, bg=BG_COLOR)
frame_top.pack(pady=10)

income_btn = tk.Button(frame_top, text="Income", font=("Arial", 12), fg=TEXT_COLOR, bg=BG_COLOR,
                        activebackground=BG_COLOR, activeforeground=BUTTON_COLOR, command=lambda: save_button.config(command=save_income),
                        relief="solid", bd=1, width=10)
income_btn.grid(row=0, column=0, padx=10)

expense_btn = tk.Button(frame_top, text="Expense", font=("Arial", 12), fg=TEXT_COLOR, bg=BG_COLOR,
                         activebackground=BG_COLOR, activeforeground=BUTTON_COLOR, command=lambda: save_button.config(command=save_expense),
                         relief="solid", bd=1, width=10)
expense_btn.grid(row=0, column=1, padx=10)

# Entry Form Frame
frame_form = tk.Frame(root, bg=BG_COLOR)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Date", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0, sticky="w")
date_entry = DateEntry(frame_form, width=17, background=ENTRY_COLOR, foreground=TEXT_COLOR, borderwidth=2)
date_entry.grid(row=0, column=1, padx=10)

tk.Label(frame_form, text="Amount", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(frame_form, bg=ENTRY_COLOR, fg=TEXT_COLOR)
amount_entry.grid(row=1, column=1, padx=10)

tk.Label(frame_form, text="Category", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=2, column=0, sticky="w")
categories = ["Food", "Health", "Education", "Loan", "Basic Needs"]
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame_form, textvariable=category_var, values=categories, state="readonly")
category_dropdown.grid(row=2, column=1, padx=10)

tk.Label(frame_form, text="Account", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=3, column=0, sticky="w")
account_var = tk.StringVar()
saving_radio = tk.Radiobutton(frame_form, text="Saving", variable=account_var, value="Saving", fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
saving_radio.grid(row=3, column=1, sticky="w")
current_radio = tk.Radiobutton(frame_form, text="Current", variable=account_var, value="Current", fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BG_COLOR)
current_radio.grid(row=3, column=1, padx=80)

tk.Label(frame_form, text="Description", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=4, column=0, sticky="w")
note_entry = tk.Entry(frame_form, bg=ENTRY_COLOR, fg=TEXT_COLOR)
note_entry.grid(row=4, column=1, padx=10)

save_button = tk.Button(root, text="ADD", bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Arial", 12), width=15)
save_button.pack(pady=10)

# Total Income & Expense Display
total_income = tk.IntVar()
total_expense = tk.IntVar()
update_totals()

totals_frame = tk.Frame(root, bg=BG_COLOR)
totals_frame.pack(pady=10)

tk.Label(totals_frame, text="Total Income:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0)
tk.Label(totals_frame, textvariable=total_income, fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=1)

tk.Label(totals_frame, text="Total Expense:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=1, column=0)
tk.Label(totals_frame, textvariable=total_expense, fg=TEXT_COLOR, bg=BG_COLOR).grid(row=1, column=1)

# History Section
history_frame = tk.Frame(root, bg=BG_COLOR)
history_frame.pack(pady=10)

tk.Label(history_frame, text="View Entries For:", fg=TEXT_COLOR, bg=BG_COLOR).grid(row=0, column=0)
history_date_entry = DateEntry(history_frame, width=12, background=ENTRY_COLOR, foreground=TEXT_COLOR, borderwidth=2)
history_date_entry.grid(row=0, column=1, padx=10)
tk.Button(history_frame, text="Show Entries", bg=BUTTON_COLOR, fg=TEXT_COLOR, command=fetch_entries).grid(row=0, column=2, padx=5)

# Table to Display Entries
table_frame = tk.Frame(root, bg=BG_COLOR)
table_frame.pack(pady=10)

columns = ("Date", "Amount", "Category", "Account", "Note", "Type")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=75)
table.pack()

root.mainloop()
