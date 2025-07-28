#!/usr/bin/env python3
"""
Interactive Database Migration Testing Interface
Updated to work with comprehensive migration test structure
"""

import os
import mysql.connector
from dotenv import load_dotenv
import subprocess
import time
from datetime import datetime

load_dotenv()

class InteractiveMigrationTester:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'port': int(os.getenv("DB_PORT", 3306)),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASS"),
            'database': os.getenv("DB_NAME")
        }
    
    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"❌ Database connection failed: {err}")
            return None

    def run_sql_file(self, cursor, filepath):
        """Execute SQL file with proper statement splitting"""
        with open(filepath, "r") as f:
            sql = f.read()
        
        # Split by semicolon for MySQL
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
        
        for statement in statements:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                print(f"❌ Error executing statement: {err}")
                print(f"Statement preview: {statement[:100]}...")
                raise

    def run_liquibase_migrations(self):
        """Run Liquibase migrations via CLI"""
        print("🟡 Running Liquibase migrations...")
        start_time = time.time()
        
        try:
            # Determine correct command for platform
            liquibase_cmd = "liquibase.bat" if os.name == 'nt' else "liquibase"
            
            result = subprocess.run(
                [liquibase_cmd, "--defaultsFile=liquibase.properties", "update"],
                cwd="liquibase",
                capture_output=True,
                text=True,
                timeout=120
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Liquibase completed successfully in {execution_time:.2f}s")
                if result.stdout:
                    print("📝 Output:", result.stdout[-200:])  # Show last 200 chars
            else:
                print(f"❌ Liquibase failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Liquibase command timed out")
        except FileNotFoundError:
            print("❌ Liquibase executable not found. Please install Liquibase CLI.")
        except Exception as err:
            print(f"❌ Liquibase error: {err}")

    def run_migration_folder(self, cursor, conn, folder_path, tool_name):
        """Run SQL migrations from a folder"""
        print(f"📁 Running {tool_name} migrations from {folder_path}...")
        start_time = time.time()
        
        try:
            if not os.path.exists(folder_path):
                print(f"❌ Migration folder not found: {folder_path}")
                return
            
            files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
            
            if not files:
                print(f"❌ No SQL files found in {folder_path}")
                return
            
            print(f"📋 Found {len(files)} migration files")
            
            for filename in files:
                filepath = os.path.join(folder_path, filename)
                print(f"  📄 Running {filename}...")
                try:
                    self.run_sql_file(cursor, filepath)
                    conn.commit()
                    print(f"  ✅ {filename} completed successfully")
                except mysql.connector.Error as err:
                    print(f"  ❌ {filename} failed: {err}")
                    conn.rollback()
                    return
            
            execution_time = time.time() - start_time
            print(f"✅ {tool_name} migrations completed in {execution_time:.2f}s")
            
        except Exception as err:
            print(f"❌ Error running {tool_name} migrations: {err}")

    def reset_database(self, cursor, conn):
        """Reset database to clean state"""
        print("🔄 Resetting database...")
        try:
            # Drop all tables to start fresh
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"  🗑️  Dropping {len(tables)} existing tables...")
                for (table,) in tables:
                    cursor.execute(f"DROP TABLE {table}")
                    print(f"  ❌ Dropped table: {table}")
            else:
                print("  ℹ️  No tables to drop")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()
            print("  ✅ Database reset completed")
            
        except mysql.connector.Error as err:
            print(f"  ❌ Database reset failed: {err}")

    def analyze_database_state(self, cursor):
        """Analyze current database state"""
        print("\n📊 Current Database State:")
        try:
            # Get table count
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"  📋 Total tables: {len(tables)}")
            
            if not tables:
                print("  ℹ️  No tables found in database")
                return
            
            # Show table names
            table_names = [table[0] for table in tables]
            print(f"  📝 Tables: {', '.join(table_names)}")
            
            # Count records in key tables
            key_tables = ['users', 'users_comprehensive', 'users_redgate', 'products', 'categories', 'roles', 'permissions']
            
            for table in key_tables:
                if table in table_names:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        print(f"  📊 {table}: {count} records")
                    except mysql.connector.Error as err:
                        print(f"  ❌ Error reading {table}: {err}")
            
        except mysql.connector.Error as err:
            print(f"  ❌ Database analysis failed: {err}")

    def view_table_data(self, cursor, table_name, limit=10):
        """View data from a specific table"""
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"  ℹ️  Table '{table_name}' is empty")
                return
            
            # Get column names
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [row[0] for row in cursor.fetchall()]
            
            print(f"\n📋 {table_name.capitalize()} (showing up to {limit} records):")
            print("  " + " | ".join(f"{col:15}" for col in columns))
            print("  " + "-" * (len(columns) * 17))
            
            for row in rows:
                formatted_row = []
                for item in row:
                    if item is None:
                        formatted_row.append("NULL")
                    elif isinstance(item, str) and len(item) > 15:
                        formatted_row.append(item[:12] + "...")
                    else:
                        formatted_row.append(str(item))
                print("  " + " | ".join(f"{item:15}" for item in formatted_row))
            
        except mysql.connector.Error as err:
            print(f"  ❌ Error viewing table '{table_name}': {err}")

    def insert_test_user(self, cursor, conn):
        """Insert a test user into the appropriate users table"""
        print("\n👤 Insert Test User")
        username = input("  Enter username: ").strip()
        email = input("  Enter email: ").strip()
        first_name = input("  Enter first name (optional): ").strip() or None
        last_name = input("  Enter last name (optional): ").strip() or None
        
        # Try to insert into the most comprehensive users table available
        tables_to_try = ['users_comprehensive', 'users_redgate', 'users']
        
        for table in tables_to_try:
            try:
                cursor.execute("SHOW TABLES LIKE %s", (table,))
                if cursor.fetchone():
                    if table == 'users_comprehensive':
                        cursor.execute(
                            "INSERT INTO users_comprehensive (username, email, first_name, last_name) VALUES (%s, %s, %s, %s)",
                            (username, email, first_name, last_name)
                        )
                    elif table == 'users_redgate':
                        cursor.execute(
                            "INSERT INTO users_redgate (username, email, first_name, last_name) VALUES (%s, %s, %s, %s)",
                            (username, email, first_name, last_name)
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO users (username, email) VALUES (%s, %s)",
                            (username, email)
                        )
                    
                    conn.commit()
                    print(f"  ✅ User added to {table}")
                    return
                    
            except mysql.connector.Error as err:
                print(f"  ❌ Error inserting into {table}: {err}")
                continue
        
        print("  ❌ No suitable users table found")

    def migrations_menu(self):
        """Interactive migrations menu"""
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            while True:
                print("\n" + "="*50)
                print("🛠️  MIGRATIONS MENU")
                print("="*50)
                print("1. 🔵 Run Bytebase migrations (5 SQL files)")
                print("2. 🟡 Run Liquibase migrations (3 XML files)")
                print("3. 🔴 Run Redgate migrations (2 SQL files)")
                print("4. 🤖 Run automated comparison test")
                print("5. 🔄 Reset database")
                print("6. 📊 Analyze database state")
                print("7. ⬅️  Back to main menu")
                
                choice = input("\nSelect option (1-7): ").strip()
                
                if choice == "1":
                    self.run_migration_folder(cursor, conn, "bytebase/migrations", "Bytebase")
                elif choice == "2":
                    self.run_liquibase_migrations()
                elif choice == "3":
                    self.run_migration_folder(cursor, conn, "redgate/migrations", "Redgate")
                elif choice == "4":
                    print("🤖 Running automated comparison...")
                    os.system("python migration_tester.py")
                elif choice == "5":
                    self.reset_database(cursor, conn)
                elif choice == "6":
                    self.analyze_database_state(cursor)
                elif choice == "7":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
        
        finally:
            cursor.close()
            conn.close()

    def view_menu(self):
        """Interactive view data menu"""
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            while True:
                print("\n" + "="*50)
                print("👁️  VIEW DATA MENU")
                print("="*50)
                
                # Get available tables
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                if not tables:
                    print("ℹ️  No tables found. Run migrations first.")
                    input("Press Enter to continue...")
                    break
                
                print("Available tables:")
                for i, table in enumerate(tables, 1):
                    print(f"{i:2}. 📋 {table}")
                
                print(f"{len(tables)+1:2}. 📊 Database overview")
                print(f"{len(tables)+2:2}. ⬅️  Back to main menu")
                
                try:
                    choice = int(input(f"\nSelect table (1-{len(tables)+2}): ").strip())
                    
                    if 1 <= choice <= len(tables):
                        table_name = tables[choice-1]
                        limit = input(f"Enter limit (default 10): ").strip() or "10"
                        self.view_table_data(cursor, table_name, int(limit))
                        input("\nPress Enter to continue...")
                    elif choice == len(tables)+1:
                        self.analyze_database_state(cursor)
                        input("\nPress Enter to continue...")
                    elif choice == len(tables)+2:
                        break
                    else:
                        print("❌ Invalid choice.")
                        
                except ValueError:
                    print("❌ Please enter a valid number.")
        
        finally:
            cursor.close()
            conn.close()

    def insert_menu(self):
        """Interactive insert data menu"""
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        try:
            while True:
                print("\n" + "="*50)
                print("➕ INSERT DATA MENU")
                print("="*50)
                print("1. 👤 Insert test user")
                print("2. 🏢 Insert test category")
                print("3. 📦 Insert test product")
                print("4. ⬅️  Back to main menu")
                
                choice = input("\nSelect option (1-4): ").strip()
                
                if choice == "1":
                    self.insert_test_user(cursor, conn)
                elif choice == "2":
                    print("🏢 Insert test category - Feature coming soon")
                elif choice == "3":
                    print("📦 Insert test product - Feature coming soon")
                elif choice == "4":
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
        
        finally:
            cursor.close()
            conn.close()

    def main_menu(self):
        """Main interactive menu"""
        print("🚀 Database Migration POC - Interactive Testing Interface")
        print("Updated for comprehensive migration comparison")
        
        while True:
            print("\n" + "="*60)
            print("🎯 MAIN MENU")
            print("="*60)
            print("1. 🛠️  Migrations - Run and compare migration tools")
            print("2. 👁️  View Data - Inspect database tables and records")
            print("3. ➕ Insert Data - Add test data to tables")
            print("4. 📋 Show Migration Info - Display file structure")
            print("5. 🎨 Launch GUI - Open graphical interface")
            print("6. 🚪 Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self.migrations_menu()
            elif choice == "2":
                self.view_menu()
            elif choice == "3":
                self.insert_menu()
            elif choice == "4":
                self.show_migration_info()
            elif choice == "5":
                print("🎨 Launching GUI...")
                try:
                    os.system("python gui.py")
                except Exception as err:
                    print(f"❌ Failed to launch GUI: {err}")
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def show_migration_info(self):
        """Display migration file structure and info"""
        print("\n" + "="*60)
        print("📋 MIGRATION STRUCTURE OVERVIEW")
        print("="*60)
        
        migration_info = {
            "🔵 Bytebase (Incremental SQL)": {
                "path": "bytebase/migrations",
                "description": "5 files - Git-like incremental changes",
                "files": [
                    "001-create-users-comprehensive.sql",
                    "002-create-roles-permissions.sql", 
                    "003-create-products-system.sql",
                    "004-alter-tables-add-features.sql",
                    "005-seed-sample-data.sql"
                ]
            },
            "🟡 Liquibase (Enterprise XML)": {
                "path": "liquibase/changelog",
                "description": "3 files - Enterprise batch releases",
                "files": [
                    "001-create-users-comprehensive.xml",
                    "002-create-roles-permissions.xml",
                    "003-alter-tables-inventory.xml"
                ]
            },
            "🔴 Redgate (Traditional SQL)": {
                "path": "redgate/migrations", 
                "description": "2 files - DBA comprehensive scripts",
                "files": [
                    "001-create-users-comprehensive.sql",
                    "002-create-audit-performance.sql"
                ]
            }
        }
        
        for tool, info in migration_info.items():
            print(f"\n{tool}")
            print(f"  📁 Path: {info['path']}")
            print(f"  📝 {info['description']}")
            print(f"  📄 Files:")
            for file in info['files']:
                filepath = os.path.join(info['path'], file)
                exists = "✅" if os.path.exists(filepath) else "❌"
                print(f"    {exists} {file}")
        
        print(f"\n🎯 Purpose: Each tool tests different workflow patterns")
        print(f"   • Bytebase: Agile/continuous deployment")
        print(f"   • Liquibase: Enterprise/scheduled releases") 
        print(f"   • Redgate: Traditional DBA approach")
        
        input("\nPress Enter to continue...")

def main():
    tester = InteractiveMigrationTester()
    tester.main_menu()

if __name__ == "__main__":
    main()
def main():
    tester = InteractiveMigrationTester()
    tester.main_menu()

if __name__ == "__main__":
    main()
