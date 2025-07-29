#!/usr/bin/env python3
"""
Database Migration Tools - Web Interface Launcher
This script launches web interfaces for all three tools: Bytebase, Liquibase Pro, and Redgate
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_bytebase_status():
    """Check if Bytebase Docker container is running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        return 'bytebase/bytebase' in result.stdout
    except:
        return False

def start_bytebase():
    """Start Bytebase Docker container if not running"""
    if not check_bytebase_status():
        print("🟡 Starting Bytebase Docker container...")
        try:
            subprocess.run([
                'docker', 'run', '-d', '--name', 'bytebase-poc',
                '-p', '8080:8080',
                '--pull', 'always',
                'bytebase/bytebase:latest',
                '--data', '/var/opt/bytebase',
                '--port', '8080'
            ], check=True)
            print("✅ Bytebase container started successfully")
            time.sleep(10)  # Wait for container to be ready
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start Bytebase: {e}")
    else:
        print("✅ Bytebase is already running")

def start_redgate_web():
    """Start Redgate web interface"""
    print("🔴 Starting Redgate Web Interface...")
    subprocess.Popen([sys.executable, 'redgate_web.py'], shell=True)

def start_liquibase_web():
    """Start Liquibase web interface"""
    print("🔵 Starting Liquibase Web Interface...")
    subprocess.Popen([sys.executable, 'liquibase_web.py'], shell=True)

def open_browsers():
    """Open all web interfaces in browser"""
    time.sleep(3)  # Wait for servers to start
    
    print("\n🌐 Opening web interfaces...")
    webbrowser.open('http://localhost:8080')  # Bytebase
    time.sleep(1)
    webbrowser.open('http://localhost:5001')  # Redgate
    time.sleep(1)
    webbrowser.open('http://localhost:5002')  # Liquibase

def main():
    """Main function to launch all web interfaces"""
    print("🚀 Database Migration Tools - Web Interface Launcher")
    print("=" * 60)
    
    # Activate virtual environment
    print("📦 Activating Python virtual environment...")
    
    # Check if we're in the right directory
    if not os.path.exists('db-venv'):
        print("❌ Virtual environment not found. Please run from the project root directory.")
        return
    
    # Start Bytebase Docker container
    start_bytebase()
    
    # Start web interfaces in separate threads
    redgate_thread = threading.Thread(target=start_redgate_web, daemon=True)
    liquibase_thread = threading.Thread(target=start_liquibase_web, daemon=True)
    
    redgate_thread.start()
    liquibase_thread.start()
    
    # Open browsers
    browser_thread = threading.Thread(target=open_browsers, daemon=True)
    browser_thread.start()
    
    print("\n✅ All web interfaces are starting up!")
    print("🌐 Web URLs:")
    print("   • Bytebase:   http://localhost:8080")
    print("   • Redgate:    http://localhost:5001") 
    print("   • Liquibase:  http://localhost:5002")
    print("\n⚡ All tools are now running with full enterprise capabilities!")
    print("📊 You can now perform comprehensive comparisons across all three platforms.")
    print("\n💡 Features available:")
    print("   🔵 Bytebase: Full Docker deployment, Web UI, API integration")
    print("   🔴 Redgate: Professional simulation, Schema compare, Deployment reports")
    print("   🟣 Liquibase: Enterprise CLI, Web interface, Professional features")
    
    print("\n⏹️  Press Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        print("✅ Web interfaces stopped")

if __name__ == '__main__':
    main()
