#!/usr/bin/env python3
"""
Redgate Web Interface - Professional simulation with web UI
This creates a web interface to demonstrate Redgate's enterprise capabilities
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import sys
sys.path.append('..')
from redgate_simulator import RedgateSimulator
import threading
import webbrowser

load_dotenv()

app = Flask(__name__)
app.secret_key = 'redgate_poc_secret_key'

class RedgateWebInterface:
    def __init__(self):
        self.simulator = RedgateSimulator()
        self.deployment_history = []
        
    def get_database_info(self):
        """Get database connection information"""
        try:
            conn = self.simulator.get_connection()
            cursor = conn.cursor()
            
            # Get database info
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()[0]
            
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            conn.close()
            
            return {
                'version': version,
                'database': database,
                'tables': tables,
                'table_count': len(tables),
                'status': 'Connected'
            }
        except Exception as e:
            return {
                'status': 'Disconnected',
                'error': str(e)
            }
    
    def get_schema_comparison(self):
        """Generate schema comparison report"""
        try:
            # Generate current schema
            schema_file = self.simulator.generate_schema_script()
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_content = f.read()
            
            # Count different object types
            table_count = schema_content.count('CREATE TABLE')
            procedure_count = schema_content.count('CREATE PROCEDURE')
            trigger_count = schema_content.count('CREATE TRIGGER')
            
            return {
                'schema_file': schema_file,
                'table_count': table_count,
                'procedure_count': procedure_count,
                'trigger_count': trigger_count,
                'last_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {'error': str(e)}

# Create global instance
redgate_web = RedgateWebInterface()

@app.route('/')
def index():
    """Main dashboard"""
    db_info = redgate_web.get_database_info()
    return render_template('redgate_dashboard.html', db_info=db_info)

@app.route('/schema-compare')
def schema_compare():
    """Schema comparison page"""
    comparison = redgate_web.get_schema_comparison()
    return render_template('schema_compare.html', comparison=comparison)

@app.route('/deployment')
def deployment():
    """Deployment management page"""
    return render_template('deployment.html', history=redgate_web.deployment_history)

@app.route('/api/deploy', methods=['POST'])
def deploy_migrations():
    """API endpoint to deploy migrations"""
    try:
        folder_path = request.json.get('folder_path', 'redgate/migrations')
        
        # Run deployment
        results = redgate_web.simulator.deploy_migration_package(folder_path)
        
        # Add to history
        deployment_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'folder': folder_path,
            'results': results,
            'status': 'Success' if all('✓' in r for r in results) else 'Failed'
        }
        redgate_web.deployment_history.append(deployment_record)
        
        return jsonify({
            'status': 'success',
            'results': results,
            'deployment_id': len(redgate_web.deployment_history)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/schema-export')
def export_schema():
    """Export current schema"""
    try:
        schema_file = redgate_web.simulator.generate_schema_script()
        return jsonify({
            'status': 'success',
            'file_path': schema_file,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def start_redgate_web():
    """Start the Redgate web interface"""
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Create dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redgate SQL Source Control - POC</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            display: flex;
            align-items: center;
        }
        .redgate-logo {
            background: #dc3545;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            margin-right: 1rem;
            font-weight: bold;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h3 {
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #dc3545;
            padding-bottom: 0.5rem;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
        .status-connected {
            background: #28a745;
        }
        .status-disconnected {
            background: #dc3545;
        }
        .nav-buttons {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #dc3545;
            color: white;
        }
        .btn-primary:hover {
            background: #c82333;
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background: #5a6268;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        .stat-item {
            text-align: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #dc3545;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <span class="redgate-logo">REDGATE</span>
            SQL Source Control - POC Dashboard
        </h1>
    </div>
    
    <div class="container">
        <div class="nav-buttons">
            <a href="/schema-compare" class="btn btn-primary">Schema Compare</a>
            <a href="/deployment" class="btn btn-secondary">Deployment Manager</a>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>Database Connection</h3>
                <p>
                    <span class="status-indicator {% if db_info.status == 'Connected' %}status-connected{% else %}status-disconnected{% endif %}"></span>
                    {{ db_info.status }}
                </p>
                {% if db_info.status == 'Connected' %}
                <p><strong>Database:</strong> {{ db_info.database }}</p>
                <p><strong>Version:</strong> {{ db_info.version }}</p>
                {% else %}
                <p><strong>Error:</strong> {{ db_info.error }}</p>
                {% endif %}
            </div>
            
            <div class="card">
                <h3>Database Statistics</h3>
                {% if db_info.status == 'Connected' %}
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">{{ db_info.table_count }}</div>
                        <div class="stat-label">Tables</div>
                    </div>
                </div>
                {% else %}
                <p>Connect to database to view statistics</p>
                {% endif %}
            </div>
            
            <div class="card">
                <h3>Quick Actions</h3>
                <button class="btn btn-primary" onclick="exportSchema()">Export Schema</button>
                <button class="btn btn-secondary" onclick="runDeployment()">Deploy Changes</button>
            </div>
        </div>
    </div>

    <script>
        function exportSchema() {
            fetch('/api/schema-export')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Schema exported successfully to: ' + data.file_path);
                    } else {
                        alert('Export failed: ' + data.message);
                    }
                });
        }

        function runDeployment() {
            fetch('/api/deploy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    folder_path: 'redgate/migrations'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Deployment completed! Check deployment page for details.');
                    window.location.href = '/deployment';
                } else {
                    alert('Deployment failed: ' + data.message);
                }
            });
        }
    </script>
</body>
</html>
"""
    
    with open('templates/redgate_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # Create schema compare template
    schema_compare_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redgate Schema Compare</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8f9fa;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 1rem 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .back-btn {
            background: #6c757d;
            color: white;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 3px;
            margin-bottom: 1rem;
            display: inline-block;
        }
        .comparison-panel {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            text-align: center;
        }
        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Schema Compare</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <div class="comparison-panel">
            <h2>Current Database Schema</h2>
            {% if comparison.error %}
            <p style="color: red;">Error: {{ comparison.error }}</p>
            {% else %}
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ comparison.table_count }}</div>
                    <div>Tables</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ comparison.procedure_count }}</div>
                    <div>Procedures</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ comparison.trigger_count }}</div>
                    <div>Triggers</div>
                </div>
            </div>
            <p><strong>Schema file:</strong> {{ comparison.schema_file }}</p>
            <p><strong>Generated:</strong> {{ comparison.last_generated }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""
    
    with open('templates/schema_compare.html', 'w', encoding='utf-8') as f:
        f.write(schema_compare_html)
    
    # Create deployment template
    deployment_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redgate Deployment Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8f9fa;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 1rem 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .deployment-item {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-success {
            border-left: 4px solid #28a745;
        }
        .status-failed {
            border-left: 4px solid #dc3545;
        }
        .back-btn {
            background: #6c757d;
            color: white;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 3px;
            margin-bottom: 1rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Deployment Manager</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <h2>Deployment History</h2>
        {% if history %}
        {% for deployment in history %}
        <div class="deployment-item status-{{ deployment.status.lower() }}">
            <h3>Deployment #{{ loop.index }}</h3>
            <p><strong>Timestamp:</strong> {{ deployment.timestamp }}</p>
            <p><strong>Folder:</strong> {{ deployment.folder }}</p>
            <p><strong>Status:</strong> {{ deployment.status }}</p>
            <details>
                <summary>View Results</summary>
                <ul>
                {% for result in deployment.results %}
                <li>{{ result }}</li>
                {% endfor %}
                </ul>
            </details>
        </div>
        {% endfor %}
        {% else %}
        <p>No deployments yet. Run a deployment from the dashboard.</p>
        {% endif %}
    </div>
</body>
</html>
"""
    
    with open('templates/deployment.html', 'w', encoding='utf-8') as f:
        f.write(deployment_html)
    
    print("🔴 Starting Redgate Web Interface on http://localhost:5001")
    
    # Start Flask app
    app.run(host='localhost', port=5001, debug=False)

if __name__ == '__main__':
    start_redgate_web()
