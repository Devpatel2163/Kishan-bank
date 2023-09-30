import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create or connect to a SQLite database
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

# Create a table to store customer information
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                gender TEXT,
                password TEXT,
                balance REAL
                )''')
conn.commit()

# Function to create a new customer record during registration
def create_customer_record(name, gender, password, balance):
    cursor.execute("INSERT INTO customers (name, gender, password, balance) VALUES (?, ?, ?, ?)",
                   (name, gender, password, balance))
    conn.commit()

# Function to handle registration button click
def register():
    global entry_name, entry_gender, entry_password, entry_balance
    name = entry_name.get()
    gender = entry_gender.get()
    password = entry_password.get()
    balance = entry_balance.get()

    create_customer_record(name, gender, password, balance)
    messagebox.showinfo("Success", "Registration successful!")
    register_screen.destroy()

# Function to handle login button click
def login():
    global entry_username, entry_login_password
    name = entry_username.get()
    password = entry_login_password.get()

    if name == "" or password == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    cursor.execute("SELECT password FROM customers WHERE name=?", (name,))
    stored_password = cursor.fetchone()

    if not stored_password:
        messagebox.showerror("Error", "User not found.")
    elif password == stored_password[0]:
        login_screen.destroy()
        messagebox.showinfo("Success", "Login successful!")
        open_account_dashboard(name)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to open the account dashboard
def open_account_dashboard(name):
    dashboard_screen = tk.Tk()
    dashboard_screen.title("Account Dashboard")

    cursor.execute("SELECT * FROM customers WHERE name=?", (name,))
    customer_data = cursor.fetchone()

    label_welcome = tk.Label(dashboard_screen, text=f"Welcome, {name}!", font=("Helvetica", 14, "bold"))
    label_welcome.grid(row=0, column=0, columnspan=2, pady=10)

    label_info = tk.Label(dashboard_screen, text=f"Name: {customer_data[1]}\nGender: {customer_data[2]}\nBalance: {customer_data[4]}", font=("Helvetica", 12))
    label_info.grid(row=1, column=0, columnspan=2, pady=10)

    # Function to show personal information
    def show_personal_info():
        messagebox.showinfo("Personal Information", f"Name: {customer_data[1]}\nGender: {customer_data[2]}\nBalance: {customer_data[4]}")

    # Function to handle deposit button click
    def deposit():
        deposit_screen = tk.Toplevel(dashboard_screen)
        deposit_screen.title("Deposit")

        def deposit_amount():
            try:
                amount = float(entry_deposit.get())
                new_balance = customer_data[4] + amount
                cursor.execute("UPDATE customers SET balance=? WHERE name=?", (new_balance, name))
                conn.commit()
                messagebox.showinfo("Deposit", f"Deposit successful. Your new balance is: {new_balance}")
                dashboard_screen.destroy()
                open_account_dashboard(name)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

        label_deposit = tk.Label(deposit_screen, text="Enter deposit amount:")
        label_deposit.grid(row=0, column=0, pady=5)
        entry_deposit = tk.Entry(deposit_screen)
        entry_deposit.grid(row=0, column=1, pady=5)
        btn_deposit = tk.Button(deposit_screen, text="Deposit", command=deposit_amount)
        btn_deposit.grid(row=1, column=0, columnspan=2, pady=5)

    # Function to handle withdraw button click
    def withdraw():
        withdraw_screen = tk.Toplevel(dashboard_screen)
        withdraw_screen.title("Withdraw")

        def withdraw_amount():
            try:
                amount = float(entry_withdraw.get())
                if amount > customer_data[4]:
                    messagebox.showerror("Error", "Insufficient balance.")
                else:
                    new_balance = customer_data[4] - amount
                    cursor.execute("UPDATE customers SET balance=? WHERE name=?", (new_balance, name))
                    conn.commit()
                    messagebox.showinfo("Withdraw", f"Withdrawal successful. Your new balance is: {new_balance}")
                    dashboard_screen.destroy()
                    open_account_dashboard(name)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

        label_withdraw = tk.Label(withdraw_screen, text="Enter withdrawal amount:")
        label_withdraw.grid(row=0, column=0, pady=5)
        entry_withdraw = tk.Entry(withdraw_screen)
        entry_withdraw.grid(row=0, column=1, pady=5)
        btn_withdraw = tk.Button(withdraw_screen, text="Withdraw", command=withdraw_amount)
        btn_withdraw.grid(row=1, column=0, columnspan=2, pady=5)

    # Add buttons for personal info, deposit, and withdraw
    btn_personal_info = tk.Button(dashboard_screen, text="Personal Information", command=show_personal_info)
    btn_personal_info.grid(row=2, column=0, columnspan=2, pady=5)

    btn_deposit = tk.Button(dashboard_screen, text="Deposit", command=deposit)
    btn_deposit.grid(row=3, column=0, pady=5)

    btn_withdraw = tk.Button(dashboard_screen, text="Withdraw", command=withdraw)
    btn_withdraw.grid(row=3, column=1, pady=5)

# Create the main application window
root = tk.Tk()
root.title("Kishan Bank")

# Function to handle "Register" button click
def open_register_screen():
    global register_screen, entry_name, entry_gender, entry_password, entry_balance
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")

    label_name = tk.Label(register_screen, text="Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(register_screen)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    label_gender = tk.Label(register_screen, text="Gender:")
    label_gender.grid(row=1, column=0, padx=5, pady=5)
    entry_gender = tk.Entry(register_screen)
    entry_gender.grid(row=1, column=1, padx=5, pady=5)

    label_password = tk.Label(register_screen, text="Password:")
    label_password.grid(row=2, column=0, padx=5, pady=5)
    entry_password = tk.Entry(register_screen, show="*")
    entry_password.grid(row=2, column=1, padx=5, pady=5)

    label_balance = tk.Label(register_screen, text="Balance:")
    label_balance.grid(row=3, column=0, padx=5, pady=5)
    entry_balance = tk.Entry(register_screen)
    entry_balance.grid(row=3, column=1, padx=5, pady=5)

    btn_submit = tk.Button(register_screen, text="Submit", command=register)
    btn_submit.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Function to handle "Login" button click
def open_login_screen():
    global login_screen, entry_username, entry_login_password
    login_screen = tk.Toplevel(root)
    login_screen.title("Login")

    label_username = tk.Label(login_screen, text="Username:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(login_screen)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_login_password = tk.Label(login_screen, text="Password:")
    label_login_password.grid(row=1, column=0, padx=5, pady=5)
    entry_login_password = tk.Entry(login_screen, show="*")
    entry_login_password.grid(row=1, column=1, padx=5, pady=5)

    btn_login_submit = tk.Button(login_screen, text="Login", command=login)
    btn_login_submit.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# Add labels and buttons for the main screen
label_welcome = tk.Label(root, text="jb Bank", font=("Helvetica", 18, "bold"))
label_welcome.grid(row=0, column=0, columnspan=2, pady=20)

btn_register = tk.Button(root, text="Register", font=("Helvetica", 12), command=open_register_screen)
btn_register.grid(row=1, column=0, padx=10, pady=10)

btn_login = tk.Button(root, text="Login", font=("Helvetica", 12), command=open_login_screen)
btn_login.grid(row=1, column=1, padx=10, pady=10)

# Close the database connection when the application is closed
root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

root.mainloop()
