import mysql.connector
 
# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="status_poc"
)
 
cursor = conn.cursor()
 
# Fetch all services
cursor.execute("SELECT id, service_name, status, last_checked FROM service_status")
 
rows = cursor.fetchall()
 
print("Service Statuses:")
for row in rows:
    print(row)
 
cursor.close()
conn.close()