import os
import subprocess
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

def run_sql_scripts_from_folder(cursor, conn, folder_path):
    sql_files = sorted(f for f in os.listdir(folder_path) if f.endswith(".sql"))
    for filename in sql_files:
        file_path = os.path.join(folder_path, filename)
        print(f"Running migration {filename}...")
        with open(file_path, "r", encoding="utf-8") as f:
            sql = f.read()
            try:
                cursor.execute(sql, multi=True)  # multi=True for multiple statements in one file
                conn.commit()
                print(f"✔ Executed {filename}")
            except mysql.connector.Error as err:
                print(f"❌ Error executing {filename}: {err}")
                conn.rollback()

def run_liquibase_migrations():
    print("Running Liquibase migrations...")
    # Liquibase command assumes liquibase.properties is in liquibase folder
    try:
        result = subprocess.run(
            ["liquibase", "--defaultsFile=liquibase/liquibase.properties", "update"],
            cwd="liquibase",
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print("✔ Liquibase migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Liquibase migration error:\n{e.stderr}")

def run_migrations():
    while True:
        print("\nSelect migration tool to run:")
        print("1. Liquibase")
        print("2. Redgate")
        print("3. Bytebase")
        print("4. Skip migrations")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            run_liquibase_migrations()
            break
        elif choice == "2":
            run_sql_scripts_from_folder(cursor, conn, "redgate/migrations")
            break
        elif choice == "3":
            run_sql_scripts_from_folder(cursor, conn, "bytebase/migrations")
            break
        elif choice == "4":
            print("Skipping migrations...")
            break
        else:
            print("Invalid choice. Please try again.")

def check_service_status():
    cursor.execute("SELECT id, status, updated_at FROM service_status ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    print("\nService Statuses:")
    for row in rows:
        print(f"ID: {row[0]}, Status: {row[1]}, Updated At: {row[2]}")
    print()

def insert_service_status():
    status = input("Enter new service status (e.g. UP, DOWN): ").strip()
    cursor.execute("INSERT INTO service_status (status) VALUES (%s)", (status,))
    conn.commit()
    print("✔️ Status inserted successfully.\n")

def view_users():
    cursor.execute("SELECT id, username, email, created_at FROM users")
    rows = cursor.fetchall()
    print("\nUsers:")
    for row in rows:
        print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, Created At: {row[3]}")
    print()

def insert_user():
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        print("✔️ User inserted successfully.\n")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}\n")

def main_menu():
    while True:
        print("=== Status POC CLI ===")
        print("1. Check Service Status")
        print("2. Insert Service Status")
        print("3. View Users")
        print("4. Insert User")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            check_service_status()
        elif choice == "2":
            insert_service_status()
        elif choice == "3":
            view_users()
        elif choice == "4":
            insert_user()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice. Try again.\n")

    print("👋 Exiting. Goodbye!")

if __name__ == "__main__":
    try:
        run_migrations()
        main_menu()
    finally:
        cursor.close()
        conn.close()
