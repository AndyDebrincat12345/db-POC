# DB Migration POC

## Overview

This project is a **Proof of Concept (POC)** demonstrating how to manage database migrations and perform basic CRUD operations using Python. It supports both **MySQL** and **Microsoft SQL Server**, and allows executing SQL migration script **RedGate** and **Bytebase**, integrating **Liquibase CLI**, and interacting with the database via an interactive command-line menu.

---

## Features

* Connect to either **MySQL** or **Microsoft SQL Server Manager** using `.env` configuration.
* Execute SQL migration scripts from organized folders (e.g., Redgate, Bytebase).
* Run **Liquibase** migrations via subprocess.
* Reset the database using a predefined reset SQL script.
* View and insert data into key tables: `service_status`, `users`, `locations`, and `emails`.
* Secure credentials via environment variables.
* Correctly handle SQL script batch execution:

  * `;` splitting for MySQL
  * `GO` splitting for SQL Server
* Simple interactive CLI for:

  * Running migrations
  * Viewing data
  * Inserting data
  * Resetting the DB

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AndyDebrincat12345/db-POC.git
cd db-POC
```


### 2. Set Up a Virtual Environment

#### On Windows:

```bash
python -m venv db-venv
db-venv\Scripts\activate
```

#### On macOS / Linux:

```bash
python3 -m venv db-venv
source db-venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install python-dotenv mysql-connector-python pyodbc
```

Only install the connector(s) relevant to your database engine.

* For **SQL Server**, make sure **Microsoft ODBC Driver 18** (or later) is installed:
  [Download here](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

## Environment Configuration

Create a `.env` file in the root of the project with:

```ini
DB_HOST=your_db_host_or_ip
DB_PORT=3306           # Use 1433 for SQL Server
DB_USER=your_username
DB_PASS=your_password
DB_NAME=your_database_name
```

---

## Liquibase Integration (Optional)

To use Liquibase:

1. Install Liquibase CLI: [https://www.liquibase.org/download](https://www.liquibase.org/download)
2. Configure a `liquibase.properties` file in your project root.
3. Update the script to point to your `liquibase` executable (e.g., `liquibase.bat` on Windows).

---

## Usage

Run the script:

```bash
python main.py
```
or for Microsoft SQL Server Manager

```bash
python main_microsoft.py
```

Choose from the following menu options:

* Migrations – Run Liquibase or folder-based migrations.
* View Data – Query and display table contents.
* Insert Data – Add new rows via CLI prompts.
* Reset Database – Execute a full database reset script.
* Exit – Close the application.

---

## Database-Specific Notes

| Aspect            | MySQL                    | SQL Server (ODBC) |
| ----------------- | ------------------------ | ----------------- |
| Script delimiter  | `;`                      | `GO`              |
| Param placeholder | `%s`                     | `?`               |
| Driver used       | `mysql-connector-python` | `pyodbc`          |

---

## Troubleshooting

* Git conflicts: Commit or stash local changes before pulling.
* DB connection errors: Check `.env`, network, user privileges, drivers.
* ODBC issues: Confirm installed ODBC driver and connection string.
* SQL script failures: Verify syntax compatibility with selected DBMS.

---
## License

This project is the property of **EY (Ernst & Young)** and was developed through an internship program.  
It is provided **as-is** for demonstration and educational purposes.

**This code and all related materials may not be copied, reused, or redistributed without prior written permission from EY.**

For full license details, please refer to the [LICENSE](LICENSE) file.
---

## Contact

For questions, improvements, or contributions, please contact the project developer:  
**Graham Pellegrini** – [grahammalta@gmail.com](mailto:grahammalta@gmail.com)

>Note: Other developers add your contact here if you want buq
