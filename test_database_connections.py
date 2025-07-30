#!/usr/bin/env python3
"""
Test script for database connection functionality
Tests both MySQL and SQL Server connections
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL connection"""
    print("🐬 Testing MySQL Connection...")
    try:
        import mysql.connector
        
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "test")
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        print(f"✅ MySQL connection successful: {version}")
        return True
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        return False

def test_sqlserver_connection():
    """Test SQL Server connection"""
    print("🏢 Testing SQL Server Connection...")
    try:
        import pyodbc
        
        # Test connection string for SQL Server
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "1433")
        database = os.getenv("DB_NAME", "master")
        username = os.getenv("DB_USER", "sa")
        password = os.getenv("DB_PASS", "")
        
        connection_string = f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={host},{port};
        DATABASE={database};
        UID={username};
        PWD={password};
        """
        
        connection = pyodbc.connect(connection_string.strip())
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        # Extract version info
        version_info = version.split('\n')[0] if '\n' in version else version[:50] + "..."
        print(f"✅ SQL Server connection successful: {version_info}")
        return True
        
    except Exception as e:
        print(f"❌ SQL Server connection failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🧪 Database Connection Test Suite")
    print("=" * 50)
    
    mysql_ok = test_mysql_connection()
    print()
    sqlserver_ok = test_sqlserver_connection()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   MySQL: {'✅ PASS' if mysql_ok else '❌ FAIL'}")
    print(f"   SQL Server: {'✅ PASS' if sqlserver_ok else '❌ FAIL'}")
    
    if mysql_ok or sqlserver_ok:
        print("\n🎉 At least one database connection is working!")
        print("💡 Update your .env file with the working database settings.")
    else:
        print("\n⚠️  No database connections are working.")
        print("💡 Please check your database settings and ensure:")
        print("   • Database servers are running")
        print("   • Credentials are correct in .env file")
        print("   • Network connectivity is available")
        print("   • Required drivers are installed (ODBC Driver for SQL Server)")

if __name__ == "__main__":
    main()
