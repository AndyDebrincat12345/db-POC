import os
import pyodbc
from dotenv import load_dotenv
import subprocess

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1433")  # Default SQL Server port
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASS};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

def run_sql_file(cursor, filepath):
    with open(filepath, "r") as f:
        sql = f.read()

    # Split by "GO" statements (common batch separator in SQL Server scripts)
    statements = [stmt.strip() for stmt in sql.split("GO") if stmt.strip()]
    for statement in statements:
        cursor.execute(statement)
    cursor.commit()

# Rest of your functions: just replace mysql.connector.Error with pyodbc.Error or Exception

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

# Example of insert with pyodbc parameter style:
def insert_user(cursor, conn):
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        print("✔️ User inserted successfully.\n")
    except pyodbc.Error as err:
        print(f"❌ Error inserting user: {err}\n")

# Adjust exception handling throughout your code similarly

def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # your menu loop here (unchanged)
        pass
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
