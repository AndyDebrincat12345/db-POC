#!/usr/bin/env python3
"""
Database reset utility for the POC
This handles cleaning up tables between test runs
"""

import os
import sqlite3
import tempfile

def reset_simulation_database():
    """Reset the simulation database by removing any existing simulation files"""
    try:
        # For our POC, we'll simulate database resets by clearing any temp simulation data
        temp_dir = tempfile.gettempdir()
        simulation_files = []
        
        # Look for simulation state files
        for filename in os.listdir(temp_dir):
            if filename.startswith('migration_sim_') or filename.startswith('redgate_sim_'):
                filepath = os.path.join(temp_dir, filename)
                try:
                    os.remove(filepath)
                    simulation_files.append(filename)
                except OSError:
                    pass
        
        # Create fresh simulation database
        simulation_db_path = os.path.join(temp_dir, 'migration_sim_db.sqlite')
        if os.path.exists(simulation_db_path):
            os.remove(simulation_db_path)
        
        # Create a fresh SQLite database for simulation
        conn = sqlite3.connect(simulation_db_path)
        cursor = conn.cursor()
        
        # Create a simple metadata table for tracking migrations
        cursor.execute('''
        CREATE TABLE migration_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            migration_file TEXT NOT NULL,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'SUCCESS'
        )
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database reset completed")
        print(f"   Cleared {len(simulation_files)} simulation files")
        print(f"   Created fresh simulation database at: {simulation_db_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        return False

def get_simulation_db_path():
    """Get the path to the simulation database"""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, 'migration_sim_db.sqlite')

def check_table_exists(table_name):
    """Check if a table exists in the simulation database"""
    try:
        db_path = get_simulation_db_path()
        if not os.path.exists(db_path):
            return False
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
        """, (table_name,))
        
        exists = cursor.fetchone() is not None
        conn.close()
        
        return exists
        
    except Exception:
        return False

if __name__ == "__main__":
    reset_simulation_database()
