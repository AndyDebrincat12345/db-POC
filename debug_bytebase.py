#!/usr/bin/env python3
"""
Debug script for Bytebase migration issue
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def debug_migration():
    print("Starting Bytebase migration debug...")
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )
    
    cursor = conn.cursor()
    
    try:
        # Reset database first
        print("Resetting database...")
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        for (table,) in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
        conn.commit()
        print("Database reset completed")
        
        # Get migration files
        folder_path = 'bytebase/migrations'
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.sql')])
        print(f"Found migration files: {files}")
        
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            print(f"\nProcessing {filename}...")
            
            # Check existing tables before processing
            cursor.execute('SHOW TABLES')
            existing_tables = [table[0] for table in cursor.fetchall()]
            print(f"Existing tables before {filename}: {existing_tables}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            print(f"File content length: {len(sql)} characters")
            
            # Split into statements using the same logic as GUI
            statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
            print(f"Found {len(statements)} statements")
            
            for i, statement in enumerate(statements):
                if statement:
                    try:
                        print(f"  Executing statement {i+1}: {statement[:80].replace('\n', ' ')}...")
                        cursor.execute(statement)
                        # Consume all results
                        try:
                            cursor.fetchall()
                        except:
                            pass
                        print(f"  Statement {i+1}: OK")
                    except Exception as e:
                        print(f"  Statement {i+1}: FAILED - {e}")
                        print(f"  Full statement: {statement}")
                        raise e
            
            conn.commit()
            print(f"✅ {filename} completed successfully")
    
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    debug_migration()
