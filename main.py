import os
import mysql.connector
from dotenv import load_dotenv
import subprocess

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def run_sql_file(cursor, filepath):
    with open(filepath, "r") as f:
        sql = f.read()
    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
    for statement in statements:
        cursor.execute(statement)

def run_liquibase_migrations():
    print("Running Liquibase migrations (via CLI)...")

    liquibase_executable = r"C:\Program Files\liquibase\liquibase.bat"  # adjust as needed

    subprocess.run(
        [
            liquibase_executable,
            "--defaultsFile=liquibase.properties",
            "update"
        ],
        cwd="liquibase",
        check=True
    )


def run_migration_folder(cursor, folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        print(f"Running migration {filename} ...")
        try:
            run_sql_file(cursor, filepath)
            print("✔️ Success")
        except mysql.connector.Error as err:
            print(f"❌ Error running {filename}: {err}")
            break

def reset_database(cursor):
    reset_sql_path = os.path.join("sql", "reset.sql")
    print("Resetting database...")
    try:
        run_sql_file(cursor, reset_sql_path)
        print("✔️ Database reset successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error resetting database: {err}")

def check_service_status(cursor):
    try:
        cursor.execute("SELECT id, status, updated_at FROM service_status ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        print("\nService Statuses:")
        for row in rows:
            print(f"ID: {row[0]}, Status: {row[1]}, Updated At: {row[2]}")
        print()
    except mysql.connector.Error as err:
        print(f"❌ Error fetching service status: {err}\n")

def insert_service_status(cursor, conn):
    status = input("Enter new service status (e.g. UP, DOWN): ").strip()
    try:
        cursor.execute("INSERT INTO service_status (status) VALUES (%s)", (status,))
        conn.commit()
        print("✔️ Status inserted successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting status: {err}\n")

def view_table(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\n{table_name.capitalize()}:")
        for row in rows:
            print(row)
        print()
    except mysql.connector.Error as err:
        print(f"❌ Error viewing table '{table_name}': {err}\n")

def insert_user(cursor, conn):
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        print("✔️ User inserted successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting user: {err}\n")

def insert_location(cursor, conn):
    location_name = input("Enter location name: ").strip()
    try:
        cursor.execute("INSERT INTO locations (location_name) VALUES (%s)", (location_name,))
        conn.commit()
        print("✔️ Location inserted successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting location: {err}\n")

def insert_email(cursor, conn):
    email_address = input("Enter email address: ").strip()
    try:
        cursor.execute("INSERT INTO emails (email_address) VALUES (%s)", (email_address,))
        conn.commit()
        print("✔️ Email inserted successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting email: {err}\n")
def migrations_menu(cursor, conn):
    while True:
        print("\n--- Migrations Menu ---")
        print("1. Run Liquibase migrations (users)")
        print("2. Run Redgate migrations (locations)")
        print("3. Run Bytebase migrations (emails)")
        print("4. Back")
        choice = input("Select an option (1-4): ").strip()
        if choice == "1":
            run_liquibase_migrations()
        elif choice == "2":
            run_migration_folder(cursor, os.path.join("redgate", "migrations"))
            conn.commit()
        elif choice == "3":
            run_migration_folder(cursor, os.path.join("bytebase", "migrations"))
            conn.commit()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice. Try again.")

def view_menu(cursor):
    while True:
        print("\n--- View Data Menu ---")
        print("1. View Service Status")
        print("2. View Users")
        print("3. View Locations")
        print("4. View Emails")
        print("5. Back")
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            check_service_status(cursor)
        elif choice == "2":
            view_table(cursor, "users")
        elif choice == "3":
            view_table(cursor, "locations")
        elif choice == "4":
            view_table(cursor, "emails")
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice. Try again.")

def insert_menu(cursor, conn):
    while True:
        print("\n--- Insert Data Menu ---")
        print("1. Insert Service Status")
        print("2. Insert User")
        print("3. Insert Location")
        print("4. Insert Email")
        print("5. Back")
        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            insert_service_status(cursor, conn)
        elif choice == "2":
            insert_user(cursor, conn)
        elif choice == "3":
            insert_location(cursor, conn)
        elif choice == "4":
            insert_email(cursor, conn)
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice. Try again.")

def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        while True:
            print("\n=== DB Migration POC ===")
            print("1. Migrations")
            print("2. View Data")
            print("3. Insert Data")
            print("4. Reset Database")
            print("5. Exit")
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                migrations_menu(cursor, conn)
            elif choice == "2":
                view_menu(cursor)
            elif choice == "3":
                insert_menu(cursor, conn)
            elif choice == "4":
                reset_database(cursor)
                conn.commit()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Try again.")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
