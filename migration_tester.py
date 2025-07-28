#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Migration Tool Comparison Script
This script helps test and compare Liquibase, Bytebase, and Redgate migration tools.
"""

import os
import sys
import time
import mysql.connector
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'database': os.getenv("DB_NAME")
}

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_step(text):
    """Print a formatted step"""
    print(f"\n[*] {text}")

def print_result(text):
    """Print a formatted result"""
    print(f"[+] {text}")

def print_error(text):
    """Print a formatted error"""
    print(f"[-] {text}")

def get_db_connection():
    """Get database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print_error(f"Database connection failed: {err}")
        return None

def reset_database():
    """Reset database to clean state"""
    print_step("Resetting database...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Drop all views first
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        for (view_name, table_type) in views:
            cursor.execute(f"DROP VIEW IF EXISTS `{view_name}`")
        
        # Drop all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        
        print_result("Database reset completed")
        return True
        
    except Exception as e:
        print_error(f"Database reset failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def count_tables():
    """Count tables in database"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    count = len(tables)
    
    cursor.close()
    conn.close()
    return count

def run_liquibase_migration():
    """Run Liquibase migration"""
    print_step("Running Liquibase migration...")
    
    start_time = time.time()
    
    try:
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
            table_count = count_tables()
            print_result(f"Liquibase migration completed in {execution_time:.2f}s - {table_count} tables created")
            return True, execution_time
        else:
            print_error(f"Liquibase migration failed: {result.stderr}")
            return False, execution_time
            
    except Exception as e:
        execution_time = time.time() - start_time
        print_error(f"Liquibase migration error: {e}")
        return False, execution_time

def run_folder_migration(folder_path, tool_name):
    """Run SQL folder migration (for Bytebase and Redgate)"""
    print_step(f"Running {tool_name} migration...")
    
    start_time = time.time()
    
    try:
        conn = get_db_connection()
        if not conn:
            return False, 0
        
        cursor = conn.cursor()
        
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
        
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding='utf-8') as f:
                sql = f.read()
            
            # Handle different delimiters (for stored procedures)
            if "DELIMITER" in sql:
                # Split by delimiter changes and execute each part
                parts = sql.split("DELIMITER")
                current_delimiter = ";"
                
                for i, part in enumerate(parts):
                    if i == 0:
                        # First part uses default delimiter
                        statements = [stmt.strip() for stmt in part.split(";") if stmt.strip()]
                        for statement in statements:
                            if statement:
                                cursor.execute(statement)
                                # Consume all results to avoid "Unread result found" error
                                try:
                                    cursor.fetchall()
                                except:
                                    pass
                    else:
                        # Extract new delimiter and content
                        lines = part.strip().split('\n', 1)
                        if len(lines) >= 2:
                            new_delimiter = lines[0].strip()
                            content = lines[1] if len(lines) > 1 else ""
                            
                            if new_delimiter and content:
                                if new_delimiter == ";":
                                    # Back to default delimiter
                                    statements = [stmt.strip() for stmt in content.split(";") if stmt.strip()]
                                    for statement in statements:
                                        if statement:
                                            cursor.execute(statement)
                                            # Consume all results
                                            try:
                                                cursor.fetchall()
                                            except:
                                                pass
                                else:
                                    # Custom delimiter (like //)
                                    statements = [stmt.strip() for stmt in content.split(new_delimiter) if stmt.strip()]
                                    for statement in statements:
                                        if statement and not statement.startswith("DELIMITER"):
                                            cursor.execute(statement)
                                            # Consume all results
                                            try:
                                                cursor.fetchall()
                                            except:
                                                pass
            else:
                # Standard SQL without delimiter changes
                statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
                for statement in statements:
                    if statement:
                        cursor.execute(statement)
                        # Consume results to avoid "Unread result found" error
                        try:
                            cursor.fetchall()
                        except:
                            pass
            
            conn.commit()
        
        cursor.close()
        conn.close()
        
        execution_time = time.time() - start_time
        table_count = count_tables()
        print_result(f"{tool_name} migration completed in {execution_time:.2f}s - {table_count} tables created")
        return True, execution_time
        
    except Exception as e:
        execution_time = time.time() - start_time
        print_error(f"{tool_name} migration failed: {e}")
        return False, execution_time

def analyze_results(results):
    """Analyze and display comparison results"""
    print_header("MIGRATION TOOL COMPARISON RESULTS")
    
    print(f"{'Tool':<12} {'Status':<12} {'Time (s)':<10} {'Tables':<8}")
    print("-" * 50)
    
    for tool, success, exec_time, tables in results:
        status = "[+] SUCCESS" if success else "[-] FAILED"
        print(f"{tool:<12} {status:<12} {exec_time:<10.2f} {tables:<8}")
    
    # Find fastest successful migration
    successful_results = [(tool, exec_time) for tool, success, exec_time, tables in results if success]
    
    if successful_results:
        fastest = min(successful_results, key=lambda x: x[1])
        slowest = max(successful_results, key=lambda x: x[1])
        
        print(f"\n[*] PERFORMANCE SUMMARY")
        print(f"[+] Fastest: {fastest[0]} ({fastest[1]:.2f}s)")
        print(f"[+] Slowest: {slowest[0]} ({slowest[1]:.2f}s)")
        
        if len(successful_results) > 1:
            speed_ratio = slowest[1] / fastest[1]
            print(f"[*] Speed difference: {speed_ratio:.1f}x")

def main():
    """Main comparison function"""
    print_header("DATABASE MIGRATION TOOL COMPARISON")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test each migration tool
    tools = [
        ("Redgate", "redgate/migrations"),
        ("Bytebase", "bytebase/migrations"),
        ("Liquibase", None)  # Special case for Liquibase
    ]
    
    for tool_name, folder_path in tools:
        # Reset database before each test
        if not reset_database():
            print_error(f"Failed to reset database for {tool_name}")
            continue
        
        # Small delay to ensure reset is complete
        time.sleep(1.0)
        
        # Run migration
        if tool_name == "Liquibase":
            success, exec_time = run_liquibase_migration()
        else:
            success, exec_time = run_folder_migration(folder_path, tool_name)
        
        # Count final tables
        final_tables = count_tables() if success else 0
        results.append((tool_name, success, exec_time, final_tables))
    
    # Analyze and display results
    analyze_results(results)
    
    print_header("COMPARISON COMPLETE")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
