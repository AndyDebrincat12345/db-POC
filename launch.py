#!/usr/bin/env python3
"""
Master Database Migration Tools Launcher
Simple launcher to start all enterprise web interfaces
"""

import os
import subprocess
import sys

def main():
    """Launch all database migration web interfaces"""
    print("🚀 Database Migration Tools - Enterprise POC")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('db-venv'):
        print("❌ Virtual environment not found. Please run from the project root directory.")
        return
    
    # Change to web directory and launch
    try:
        os.chdir('web')
        
        # Activate virtual environment and launch
        if os.name == 'nt':  # Windows
            subprocess.run([
                '..\\db-venv\\Scripts\\python.exe', 
                'launch_web_interfaces.py'
            ])
        else:  # Unix/Linux/Mac
            subprocess.run([
                '../db-venv/bin/python', 
                'launch_web_interfaces.py'
            ])
            
    except Exception as e:
        print(f"❌ Failed to launch: {e}")
        print("💡 Try running: cd web && python launch_web_interfaces.py")

if __name__ == '__main__':
    main()
