#!/usr/bin/env python3
"""
Database Migration Tool Comparison Script
This script helps test and compare Liquibase, Bytebase, and Redgate migration tools.
"""

import os
import sys
import time
import mysql.connector
from dotenv import load_dotenv
import subprocess
import json
from datetime import datetime

load_dotenv()

class MigrationTester:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'port': int(os.getenv("DB_PORT", 3306)),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASS"),
            'database': os.getenv("DB_NAME")
        }
        self.results = {
            'bytebase': {'execution_time': 0, 'errors': [], 'success': False},
            'liquibase': {'execution_time': 0, 'errors': [], 'success': False},
            'redgate': {'execution_time': 0, 'errors': [], 'success': False}
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
                print(f"Statement: {statement[:100]}...")
                raise
    
    def test_bytebase_migrations(self):
        """Test Bytebase SQL migrations"""
        print("\n🔵 Testing Bytebase Migrations...")
        start_time = time.time()
        
        try:
            conn = self.get_connection()
            if not conn:
                raise Exception("Failed to connect to database")
            
            cursor = conn.cursor()
            
            migration_folder = "bytebase/migrations"
            files = sorted([f for f in os.listdir(migration_folder) if f.endswith(".sql")])
            
            for filename in files:
                filepath = os.path.join(migration_folder, filename)
                print(f"  📄 Running {filename}...")
                try:
                    self.run_sql_file(cursor, filepath)
                    conn.commit()
                    print(f"  ✅ {filename} completed successfully")
                except Exception as err:
                    self.results['bytebase']['errors'].append(f"{filename}: {str(err)}")
                    print(f"  ❌ {filename} failed: {err}")
                    conn.rollback()
                    break
            
            cursor.close()
            conn.close()
            
            if not self.results['bytebase']['errors']:
                self.results['bytebase']['success'] = True
                
        except Exception as err:
            self.results['bytebase']['errors'].append(str(err))
        
        self.results['bytebase']['execution_time'] = time.time() - start_time
        print(f"🔵 Bytebase completed in {self.results['bytebase']['execution_time']:.2f}s")
    
    def test_liquibase_migrations(self):
        """Test Liquibase XML migrations"""
        print("\n🟡 Testing Liquibase Migrations...")
        start_time = time.time()
        
        try:
            # Check if Liquibase is available
            liquibase_cmd = self._get_liquibase_command()
            
            result = subprocess.run(
                [liquibase_cmd, "--defaultsFile=liquibase.properties", "update"],
                cwd="liquibase",
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.results['liquibase']['success'] = True
                print("  ✅ Liquibase migrations completed successfully")
            else:
                self.results['liquibase']['errors'].append(result.stderr)
                print(f"  ❌ Liquibase failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.results['liquibase']['errors'].append("Liquibase command timed out")
            print("  ❌ Liquibase command timed out")
        except FileNotFoundError:
            self.results['liquibase']['errors'].append("Liquibase executable not found")
            print("  ❌ Liquibase executable not found")
        except Exception as err:
            self.results['liquibase']['errors'].append(str(err))
            print(f"  ❌ Liquibase error: {err}")
        
        self.results['liquibase']['execution_time'] = time.time() - start_time
        print(f"🟡 Liquibase completed in {self.results['liquibase']['execution_time']:.2f}s")
    
    def test_redgate_migrations(self):
        """Test Redgate SQL migrations"""
        print("\n🔴 Testing Redgate Migrations...")
        start_time = time.time()
        
        try:
            conn = self.get_connection()
            if not conn:
                raise Exception("Failed to connect to database")
            
            cursor = conn.cursor()
            
            migration_folder = "redgate/migrations"
            files = sorted([f for f in os.listdir(migration_folder) if f.endswith(".sql")])
            
            for filename in files:
                filepath = os.path.join(migration_folder, filename)
                print(f"  📄 Running {filename}...")
                try:
                    self.run_sql_file(cursor, filepath)
                    conn.commit()
                    print(f"  ✅ {filename} completed successfully")
                except Exception as err:
                    self.results['redgate']['errors'].append(f"{filename}: {str(err)}")
                    print(f"  ❌ {filename} failed: {err}")
                    conn.rollback()
                    break
            
            cursor.close()
            conn.close()
            
            if not self.results['redgate']['errors']:
                self.results['redgate']['success'] = True
                
        except Exception as err:
            self.results['redgate']['errors'].append(str(err))
        
        self.results['redgate']['execution_time'] = time.time() - start_time
        print(f"🔴 Redgate completed in {self.results['redgate']['execution_time']:.2f}s")
    
    def _get_liquibase_command(self):
        """Get the appropriate Liquibase command for the platform"""
        if os.name == 'nt':  # Windows
            return "liquibase.bat"
        else:  # Linux/Mac
            return "liquibase"
    
    def analyze_database_state(self):
        """Analyze the final database state after all migrations"""
        print("\n📊 Analyzing Database State...")
        
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Get table count
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"  📋 Total tables created: {len(tables)}")
            
            # Analyze specific tables
            test_tables = ['users', 'users_comprehensive', 'users_redgate', 'products', 'categories']
            
            for table in test_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"  📊 {table}: {count} records")
                except mysql.connector.Error:
                    print(f"  ❌ Table {table} not found")
            
            cursor.close()
            conn.close()
            
        except Exception as err:
            print(f"  ❌ Analysis failed: {err}")
    
    def generate_report(self):
        """Generate a comprehensive comparison report"""
        print("\n" + "="*60)
        print("📋 MIGRATION TOOL COMPARISON REPORT")
        print("="*60)
        
        for tool, result in self.results.items():
            print(f"\n{tool.upper()}:")
            print(f"  ✅ Success: {'Yes' if result['success'] else 'No'}")
            print(f"  ⏱️  Execution Time: {result['execution_time']:.2f}s")
            print(f"  ❌ Errors: {len(result['errors'])}")
            
            if result['errors']:
                print("  Error Details:")
                for i, error in enumerate(result['errors'][:3], 1):
                    print(f"    {i}. {error[:100]}...")
        
        # Determine winner
        successful_tools = [tool for tool, result in self.results.items() if result['success']]
        
        if successful_tools:
            fastest = min(successful_tools, key=lambda x: self.results[x]['execution_time'])
            print(f"\n🏆 Fastest Successful Tool: {fastest.upper()}")
        
        print(f"\n📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def run_all_tests(self):
        """Run all migration tests"""
        print("🚀 Starting Database Migration Tool Comparison")
        print("Testing: Bytebase, Liquibase, and Redgate")
        
        # Reset database first
        self.reset_database()
        
        # Run tests
        self.test_bytebase_migrations()
        self.test_liquibase_migrations()
        self.test_redgate_migrations()
        
        # Analyze results
        self.analyze_database_state()
        self.generate_report()
    
    def reset_database(self):
        """Reset database to clean state"""
        print("\n🔄 Resetting database...")
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Drop all tables to start fresh
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for (table,) in tables:
                cursor.execute(f"DROP TABLE {table}")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()
            
            cursor.close()
            conn.close()
            print("  ✅ Database reset completed")
            
        except Exception as err:
            print(f"  ❌ Database reset failed: {err}")

if __name__ == "__main__":
    tester = MigrationTester()
    tester.run_all_tests()
