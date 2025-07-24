from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables
load_dotenv()

# Establish DB connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

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
        main_menu()
    finally:
        cursor.close()
        conn.close()
