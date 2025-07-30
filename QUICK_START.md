# 🚀 Quick Start Guide - Database Migration POC

## ⚡ **Instant Launch Options**

### **Option 1: Easy Launch (Recommended)**
Double-click one of these files:
- `launch_gui.bat` - Windows Batch file
- `launch_gui.ps1` - PowerShell script (if execution policy allows)

### **Option 2: Command Line**
```bash
# Method 1: Using virtual environment directly
.\db-venv\Scripts\python.exe gui.py

# Method 2: Activate virtual environment first
.\db-venv\Scripts\Activate.ps1
python gui.py
```

### **Option 3: PowerShell**
```powershell
# Navigate to project directory
cd "C:\Users\XH782WN\OneDrive - EY\Documents\db-POC"

# Run with virtual environment
.\db-venv\Scripts\python.exe gui.py
```

---

## 🔧 **If You Encounter Issues**

### **"ModuleNotFoundError: No module named 'pyodbc'"**
**Solution:** Always use the virtual environment Python:
```bash
.\db-venv\Scripts\python.exe gui.py
```
**Instead of:** `python gui.py`

### **Virtual Environment Issues**
**Reinstall dependencies:**
```bash
.\db-venv\Scripts\pip.exe install -r requirements.txt
```

### **ODBC Driver Issues (SQL Server)**
**Download and install:**
- [Microsoft ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

## 🎯 **What You'll See**

Once the GUI launches, you'll have:
- **⚙️ Settings Tab**: Configure MySQL or SQL Server connections
- **🚀 Migrations Tab**: Run migration tools (Bytebase, Liquibase, Redgate)
- **📊 Data Tab**: View and edit database tables
- **📈 Analysis Tab**: Schema analysis and reports
- **📟 Console Tab**: View operation logs

---

## 🗄️ **Database Setup**

### **MySQL Example:**
1. Go to Settings tab
2. Select "🐬 MySQL" 
3. Configure: Host, Port (3306), Database, Username, Password
4. Click "🔗 Test Connection"

### **SQL Server Example:**
1. Go to Settings tab
2. Select "🏢 Microsoft SQL Server"
3. Configure: Host, Port (1433), Database, Authentication
4. Choose Windows Auth or SQL Server Auth
5. Click "🔗 Test Connection"

---

## ✅ **Quick Verification**

After launch, verify everything works:
1. ✅ GUI opens without errors
2. ✅ Go to Settings tab
3. ✅ Select database type (MySQL/SQL Server)
4. ✅ Test database connection
5. ✅ Go to Data tab and refresh tables

---

**🎉 You're ready to use the Database Migration POC!**
