import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# DB Connection

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# Run Liquibase

def run_liquibase():
    try:
        subprocess.run([
            r"C:\\Program Files\\liquibase\\liquibase.bat",
            "--defaultsFile=liquibase.properties",
            "update"
        ], cwd="liquibase", check=True)
        messagebox.showinfo("Success", "Liquibase migration completed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Reset DB

def reset_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        with open("sql/reset.sql", "r") as f:
            sql = f.read()
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
        for statement in statements:
            cursor.execute(statement)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Database reset successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View Table

def load_table_data(tree, table_name):
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Insert Handlers

def insert_user(username, email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def insert_location(location):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO locations (location_name) VALUES (%s)", (location,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Location added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def insert_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emails (email_address) VALUES (%s)", (email,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Email added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    root = tk.Tk()
    root.title("DB Migration POC GUI")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # --- Migrations Tab ---
    tab_migrations = ttk.Frame(notebook)
    ttk.Button(tab_migrations, text="Run Liquibase Migration", command=run_liquibase).pack(pady=10)
    notebook.add(tab_migrations, text="Migrations")

    # --- View Data Tab ---
    tab_view = ttk.Frame(notebook)
    table_selector = ttk.Combobox(tab_view, values=["users", "locations", "emails", "service_status"])
    table_selector.pack(pady=10)
    tree = ttk.Treeview(tab_view)
    tree.pack(expand=True, fill="both")
    ttk.Button(tab_view, text="Load Table", command=lambda: load_table_data(tree, table_selector.get())).pack(pady=5)
    notebook.add(tab_view, text="View Data")

    # --- Insert Data Tab ---
    tab_insert = ttk.Frame(notebook)

    def create_insert_section(parent, label, fields, submit_fn):
        frame = ttk.LabelFrame(parent, text=label)
        entries = []
        for f in fields:
            ttk.Label(frame, text=f).pack()
            e = ttk.Entry(frame)
            e.pack()
            entries.append(e)
        ttk.Button(frame, text="Submit", command=lambda: submit_fn(*[e.get() for e in entries])).pack(pady=5)
        frame.pack(pady=10, fill="x")

    create_insert_section(tab_insert, "Add User", ["Username", "Email"], insert_user)
    create_insert_section(tab_insert, "Add Location", ["Location Name"], insert_location)
    create_insert_section(tab_insert, "Add Email", ["Email Address"], insert_email)
    notebook.add(tab_insert, text="Insert Data")

    # --- Reset Tab ---
    tab_reset = ttk.Frame(notebook)
    ttk.Button(tab_reset, text="Reset Database", command=reset_database).pack(pady=20)
    notebook.add(tab_reset, text="Reset DB")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
