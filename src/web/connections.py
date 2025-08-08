"""
Web Connection Module for Database Migration Tools
Handles all web-based interactions including Bytebase API and web interface management
"""

import requests
import webbrowser
import subprocess
import time
from datetime import datetime

class BytebaseAPI:
    """Bytebase API client for migration management"""
    
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def check_connection(self):
        """Check if Bytebase server is accessible"""
        try:
            response = requests.get(f"{self.base_url}/v1/actuator/health", 
                                  headers=self.headers, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def create_migration_issue(self, sql_file, database="status_poc"):
        """Create a migration issue in Bytebase"""
        try:
            # Read SQL file content
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Create migration issue payload
            payload = {
                "type": "DATABASE_SCHEMA_UPDATE",
                "title": f"Migration: {sql_file}",
                "description": f"Database migration from file: {sql_file}",
                "sql": sql_content,
                "database": database
            }
            
            # Send request to Bytebase API
            response = requests.post(f"{self.base_url}/v1/issues", 
                                   json=payload, headers=self.headers, timeout=30)
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"Migration issue created for {sql_file}"}
            else:
                return {"success": False, "message": f"Failed to create issue: {response.status_code}"}
                
        except FileNotFoundError:
            return {"success": False, "message": f"SQL file not found: {sql_file}"}
        except Exception as e:
            return {"success": False, "message": f"Error creating migration: {str(e)}"}


class WebInterfaceManager:
    """Manages web interfaces for different migration tools"""
    
    def __init__(self):
        self.running_interfaces = {}
    
    def open_web_page(self, url, tool_name):
        """Open web page in default browser"""
        try:
            webbrowser.open(url)
            return {"success": True, "message": f"Opened {tool_name} web interface"}
        except Exception as e:
            return {"success": False, "message": f"Failed to open {tool_name}: {str(e)}"}
    
    def start_bytebase_interface(self):
        """Start Bytebase web interface (Docker container)"""
        try:
            # Check if Bytebase is already running
            check_cmd = "docker ps --filter name=bytebase --format '{{.Names}}'"
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            
            if "bytebase" in result.stdout:
                return {"success": True, "message": "Bytebase is already running"}
            
            # Start Bytebase container
            start_cmd = """
            docker run --name bytebase \\
              --restart always \\
              --publish 8080:8080 \\
              --health-cmd "curl --fail http://localhost:8080/healthz || exit 1" \\
              --health-interval 5m \\
              --health-timeout 60s \\
              --volume ~/.bytebase/data:/var/opt/bytebase \\
              bytebase/bytebase:latest \\
              --data /var/opt/bytebase \\
              --port 8080
            """
            
            # Run in background
            process = subprocess.Popen(start_cmd, shell=True)
            self.running_interfaces['bytebase'] = process
            
            # Wait a moment for startup
            time.sleep(3)
            
            return {"success": True, "message": "Bytebase interface started"}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to start Bytebase: {str(e)}"}
    
    def start_liquibase_interface(self):
        """Start Liquibase web interface (simulated)"""
        # Note: Liquibase doesn't have a built-in web UI, so this is a placeholder
        return {"success": True, "message": "Liquibase CLI-based (no web interface)"}
    
    def start_redgate_interface(self):
        """Start Redgate web interface (simulated)"""
        # Note: Redgate tools are typically desktop-based, so this is a placeholder
        return {"success": True, "message": "Redgate desktop tools (no web interface)"}
    
    def start_all_interfaces(self):
        """Start all available web interfaces"""
        results = []
        
        # Start Bytebase
        result = self.start_bytebase_interface()
        results.append(f"Bytebase: {result['message']}")
        
        # Note for other tools
        results.append("Liquibase: CLI-based tool (no web interface)")
        results.append("Redgate: Desktop-based tools (no web interface)")
        
        return results
    
    def open_all_web_pages(self):
        """Open all available web interfaces"""
        results = []
        
        # Open Bytebase
        result = self.open_web_page('http://localhost:8081', 'Bytebase')
        results.append(f"Bytebase: {result['message']}")
        
        # Note for other tools
        results.append("Liquibase: No web interface available")
        results.append("Redgate: No web interface available")
        
        return results
    
    def stop_all_interfaces(self):
        """Stop all running web interfaces"""
        results = []
        
        try:
            # Stop Bytebase container
            stop_cmd = "docker stop bytebase"
            subprocess.run(stop_cmd, shell=True, capture_output=True)
            results.append("Bytebase: Stopped")
        except Exception as e:
            results.append(f"Bytebase: Error stopping - {str(e)}")
        
        # Clear running interfaces
        self.running_interfaces.clear()
        
        return results
