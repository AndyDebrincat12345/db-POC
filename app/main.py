from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()
cursor.execute("SELECT id, service_name, status, last_checked FROM service_status")
rows = cursor.fetchall()

print("Service Statuses:")
for row in rows:
    print(row)

cursor.close()
conn.close()
