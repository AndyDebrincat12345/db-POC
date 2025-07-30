# 🗄️ Multi-Database Support Guide

## Overview
The Database Migration POC now supports both **MySQL** and **Microsoft SQL Server** databases. You can easily switch between database types using the Settings tab in the GUI.

---

## 🆕 **New Features**

### **Database Type Selection**
- 🐬 **MySQL** - Traditional MySQL/MariaDB support
- 🏢 **Microsoft SQL Server** - Full SQL Server support with multiple authentication methods

### **Enhanced Settings Tab**
- ✅ Database type selection (Radio buttons)
- ✅ Dynamic form fields based on selected database
- ✅ SQL Server specific options (Driver selection, Windows Authentication)
- ✅ Connection testing with detailed feedback
- ✅ Real-time connection status display

---

## 📋 **Configuration Options**

### **MySQL Settings**
```
Database Type: MySQL
Host: localhost
Port: 3306
Database: your_database_name
Username: root
Password: your_password
```

### **SQL Server Settings - SQL Authentication**
```
Database Type: Microsoft SQL Server
Host: localhost (or server name)
Port: 1433
Database: your_database_name
Username: sa (or your SQL user)
Password: your_password
Driver: ODBC Driver 17 for SQL Server
Windows Authentication: ❌ (unchecked)
```

### **SQL Server Settings - Windows Authentication**
```
Database Type: Microsoft SQL Server
Host: localhost (or server name)
Port: 1433
Database: your_database_name
Username: (leave empty)
Password: (leave empty)
Driver: ODBC Driver 17 for SQL Server
Windows Authentication: ✅ (checked)
```

---

## 🔧 **Environment Variables**

Add to your `.env` file:

### For MySQL:
```bash
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=migration_poc
```

### For SQL Server:
```bash
DB_TYPE=sqlserver
DB_HOST=localhost
DB_PORT=1433
DB_USER=sa
DB_PASS=your_sqlserver_password
DB_NAME=migration_poc
```

---

## 🚀 **How to Use**

### **1. Database Type Selection**
1. Open the GUI application (`python gui.py`)
2. Navigate to the **⚙️ Settings** tab
3. Select your database type:
   - 🐬 **MySQL** for MySQL/MariaDB
   - 🏢 **Microsoft SQL Server** for SQL Server

### **2. Configure Connection**
1. Enter your database connection details
2. For SQL Server, choose appropriate driver
3. For Windows Authentication, check the trusted connection box
4. Click **🔗 Test Connection** to verify

### **3. Use the Application**
1. Once connected, all features work seamlessly:
   - **📊 Data Tab**: View and edit tables
   - **📈 Analysis Tab**: Schema analysis
   - **🚀 Migrations Tab**: Run migration tools

---

## 🛠️ **Prerequisites**

### **MySQL Requirements**
- ✅ MySQL Server 5.7+ or MariaDB 10.3+
- ✅ Python package: `mysql-connector-python` (already included)

### **SQL Server Requirements**
- ✅ Microsoft SQL Server 2012+ (Express, Standard, or Enterprise)
- ✅ ODBC Driver for SQL Server (recommended: ODBC Driver 17)
- ✅ Python package: `pyodbc` (already included)

### **Installing ODBC Driver for SQL Server**
Download from Microsoft:
- [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

## 🔍 **Database-Specific Features**

### **MySQL Features**
- ✅ Traditional MySQL syntax (`SHOW TABLES`, `DESCRIBE`)
- ✅ Information Schema queries for metadata
- ✅ Backtick table/column quoting
- ✅ `LIMIT` clause for result pagination

### **SQL Server Features**
- ✅ ANSI SQL syntax with Information Schema
- ✅ Bracket table/column quoting
- ✅ `TOP` clause for result pagination
- ✅ System tables for advanced metadata
- ✅ Windows Authentication support
- ✅ Multiple ODBC driver options

---

## 🧪 **Testing Connections**

Run the database connection test:
```bash
python test_database_connections.py
```

This will test both MySQL and SQL Server connections and provide detailed feedback.

---

## 🔧 **Troubleshooting**

### **Common MySQL Issues**
- ❌ **"Access denied"** → Check username/password
- ❌ **"Can't connect to server"** → Verify MySQL is running and host/port
- ❌ **"Unknown database"** → Ensure database exists

### **Common SQL Server Issues**
- ❌ **"Driver not found"** → Install ODBC Driver 17 for SQL Server
- ❌ **"Login failed"** → Check SQL Server authentication mode
- ❌ **"Server not found"** → Verify SQL Server is running and TCP/IP enabled
- ❌ **"Protocol error"** → Check firewall settings and SQL Server port

### **SQL Server Authentication Setup**
1. Enable **SQL Server and Windows Authentication Mode**
2. Enable **TCP/IP protocol** in SQL Server Configuration Manager
3. Restart SQL Server service
4. Create SQL Server login if using SQL Authentication

---

## 🎯 **Advanced Features**

### **Automatic Database Detection**
The application automatically:
- 🔄 Adjusts queries based on database type
- 🔄 Uses appropriate syntax for each database
- 🔄 Handles different data types and metadata formats
- 🔄 Provides database-specific error messages

### **Cross-Database Compatibility**
Migration scripts and analysis work across both database types:
- ✅ Table listing and analysis
- ✅ Data viewing and editing
- ✅ Schema analysis and reporting
- ✅ Migration tool integration

---

## 📊 **Feature Comparison**

| Feature | MySQL | SQL Server |
|---------|-------|------------|
| Connection Testing | ✅ | ✅ |
| Table Listing | ✅ | ✅ |
| Data Viewing | ✅ | ✅ |
| Data Editing | ✅ | ✅ |
| Schema Analysis | ✅ | ✅ |
| Windows Auth | ❌ | ✅ |
| Multiple Drivers | ❌ | ✅ |
| JSON Data Types | ✅ | Limited |

---

🎉 **Your database migration POC now supports enterprise-grade database platforms!**
