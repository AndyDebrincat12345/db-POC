#!/usr/bin/env python3
"""
Liquibase Web Interface - Professional web UI for Liquibase Pro features
This creates a comprehensive web interface for Liquibase enterprise capabilities
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
import threading
import webbrowser
import glob

load_dotenv()

app = Flask(__name__)
app.secret_key = 'liquibase_poc_secret_key'

class LiquibaseWebInterface:
    def __init__(self):
        self.liquibase_path = os.path.abspath('../liquibase')
        self.changelog_path = os.path.join(self.liquibase_path, 'changelog')
        self.execution_history = []
        
    def run_liquibase_command(self, command_args):
        """Execute Liquibase CLI command"""
        try:
            # Change to liquibase directory
            original_dir = os.getcwd()
            os.chdir(self.liquibase_path)
            
            # Run liquibase command
            cmd = ['liquibase'] + command_args
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            os.chdir(original_dir)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            os.chdir(original_dir)
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_status(self):
        """Get Liquibase status and connection info"""
        result = self.run_liquibase_command(['status', '--verbose'])
        
        # Get changelog files
        changelog_files = []
        if os.path.exists(self.changelog_path):
            changelog_files = [f for f in os.listdir(self.changelog_path) if f.endswith('.xml')]
        
        return {
            'command_result': result,
            'changelog_files': changelog_files,
            'changelog_count': len(changelog_files)
        }
    
    def get_history(self):
        """Get Liquibase deployment history"""
        result = self.run_liquibase_command(['history'])
        return result
    
    def run_update(self):
        """Run Liquibase update"""
        result = self.run_liquibase_command(['update'])
        
        # Add to execution history
        history_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'command': 'update',
            'success': result['success'],
            'output': result.get('stdout', '') + result.get('stderr', '')
        }
        self.execution_history.append(history_record)
        
        return result
    
    def run_rollback(self, tag_or_count):
        """Run Liquibase rollback"""
        if tag_or_count.isdigit():
            command_args = ['rollback-count', tag_or_count]
        else:
            command_args = ['rollback', tag_or_count]
            
        result = self.run_liquibase_command(command_args)
        
        # Add to execution history
        history_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'command': f'rollback {tag_or_count}',
            'success': result['success'],
            'output': result.get('stdout', '') + result.get('stderr', '')
        }
        self.execution_history.append(history_record)
        
        return result
    
    def validate_changelog(self):
        """Validate changelog files"""
        result = self.run_liquibase_command(['validate'])
        return result
    
    def generate_docs(self):
        """Generate Liquibase documentation"""
        result = self.run_liquibase_command(['db-doc', 'docs'])
        return result

# Create global instance
liquibase_web = LiquibaseWebInterface()

@app.route('/')
def index():
    """Main dashboard"""
    status = liquibase_web.get_status()
    return render_template('liquibase_dashboard.html', status=status)

@app.route('/changelog')
def changelog():
    """Changelog management page"""
    changelog_files = []
    if os.path.exists(liquibase_web.changelog_path):
        for file in os.listdir(liquibase_web.changelog_path):
            if file.endswith('.xml'):
                file_path = os.path.join(liquibase_web.changelog_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                changelog_files.append({
                    'name': file,
                    'path': file_path,
                    'size': len(content),
                    'preview': content[:200] + '...' if len(content) > 200 else content
                })
    
    return render_template('changelog_manager.html', changelog_files=changelog_files)

@app.route('/history')
def history():
    """Execution history page"""
    db_history = liquibase_web.get_history()
    return render_template('liquibase_history.html', 
                         execution_history=liquibase_web.execution_history,
                         db_history=db_history)

@app.route('/api/update', methods=['POST'])
def api_update():
    """API endpoint to run update"""
    result = liquibase_web.run_update()
    return jsonify(result)

@app.route('/api/rollback', methods=['POST'])
def api_rollback():
    """API endpoint to run rollback"""
    tag_or_count = request.json.get('target', '1')
    result = liquibase_web.run_rollback(tag_or_count)
    return jsonify(result)

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """API endpoint to validate changelog"""
    result = liquibase_web.validate_changelog()
    return jsonify(result)

@app.route('/api/generate-docs', methods=['POST'])
def api_generate_docs():
    """API endpoint to generate documentation"""
    result = liquibase_web.generate_docs()
    return jsonify(result)

def start_liquibase_web():
    """Start the Liquibase web interface"""
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liquibase Pro - POC Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: #333;
        }
        .header {
            background: #1e293b;
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            display: flex;
            align-items: center;
        }
        .liquibase-logo {
            background: #4f46e5;
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
            color: #1e293b;
            border-bottom: 2px solid #4f46e5;
            padding-bottom: 0.5rem;
        }
        .nav-buttons {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
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
            background: #4f46e5;
            color: white;
        }
        .btn-primary:hover {
            background: #3730a3;
        }
        .btn-success {
            background: #059669;
            color: white;
        }
        .btn-success:hover {
            background: #047857;
        }
        .btn-warning {
            background: #d97706;
            color: white;
        }
        .btn-warning:hover {
            background: #b45309;
        }
        .btn-secondary {
            background: #6b7280;
            color: white;
        }
        .btn-secondary:hover {
            background: #4b5563;
        }
        .status-box {
            background: #f3f4f6;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .status-success {
            border-left: 4px solid #059669;
        }
        .status-error {
            border-left: 4px solid #dc2626;
        }
        .code-output {
            background: #1f2937;
            color: #e5e7eb;
            padding: 1rem;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <span class="liquibase-logo">LIQUIBASE</span>
            Pro - POC Dashboard
        </h1>
    </div>
    
    <div class="container">
        <div class="nav-buttons">
            <a href="/changelog" class="btn btn-primary">Changelog Manager</a>
            <a href="/history" class="btn btn-secondary">History</a>
            <button class="btn btn-success" onclick="runUpdate()">Update Database</button>
            <button class="btn btn-warning" onclick="validateChangelog()">Validate</button>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>Connection Status</h3>
                {% if status.command_result.success %}
                <div class="status-box status-success">
                    <strong>✓ Connected</strong>
                    <p>Liquibase is ready to execute migrations</p>
                </div>
                {% else %}
                <div class="status-box status-error">
                    <strong>✗ Connection Error</strong>
                    <p>{{ status.command_result.get('stderr', 'Unknown error') }}</p>
                </div>
                {% endif %}
            </div>
            
            <div class="card">
                <h3>Changelog Information</h3>
                <p><strong>Files:</strong> {{ status.changelog_count }}</p>
                {% if status.changelog_files %}
                <ul>
                {% for file in status.changelog_files %}
                <li>{{ file }}</li>
                {% endfor %}
                </ul>
                {% else %}
                <p>No changelog files found</p>
                {% endif %}
            </div>
            
            <div class="card">
                <h3>Quick Actions</h3>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <button class="btn btn-success" onclick="runUpdate()">Deploy Changes</button>
                    <button class="btn btn-warning" onclick="rollbackOne()">Rollback (1)</button>
                    <button class="btn btn-primary" onclick="generateDocs()">Generate Docs</button>
                </div>
            </div>
        </div>
        
        {% if status.command_result.stdout or status.command_result.stderr %}
        <div class="card">
            <h3>Last Command Output</h3>
            <div class="code-output">{{ status.command_result.stdout }}{{ status.command_result.stderr }}</div>
        </div>
        {% endif %}
    </div>

    <script>
        function runUpdate() {
            if (confirm('Deploy all pending changes to the database?')) {
                showLoading('Deploying changes...');
                fetch('/api/update', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                })
                .then(response => response.json())
                .then(data => {
                    hideLoading();
                    if (data.success) {
                        alert('✓ Update completed successfully!');
                        location.reload();
                    } else {
                        alert('✗ Update failed: ' + (data.stderr || data.error || 'Unknown error'));
                    }
                });
            }
        }

        function validateChangelog() {
            showLoading('Validating changelog...');
            fetch('/api/validate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success) {
                    alert('✓ Changelog validation passed!');
                } else {
                    alert('✗ Validation failed: ' + (data.stderr || data.error || 'Unknown error'));
                }
            });
        }

        function rollbackOne() {
            if (confirm('Rollback the last migration?')) {
                showLoading('Rolling back...');
                fetch('/api/rollback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: '1'})
                })
                .then(response => response.json())
                .then(data => {
                    hideLoading();
                    if (data.success) {
                        alert('✓ Rollback completed!');
                        location.reload();
                    } else {
                        alert('✗ Rollback failed: ' + (data.stderr || data.error || 'Unknown error'));
                    }
                });
            }
        }

        function generateDocs() {
            showLoading('Generating documentation...');
            fetch('/api/generate-docs', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success) {
                    alert('✓ Documentation generated successfully!');
                } else {
                    alert('✗ Documentation generation failed: ' + (data.stderr || data.error || 'Unknown error'));
                }
            });
        }

        function showLoading(message) {
            // Simple loading indication
            document.body.style.cursor = 'wait';
        }

        function hideLoading() {
            document.body.style.cursor = 'default';
        }
    </script>
</body>
</html>
"""
    
    with open('templates/liquibase_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # Create changelog manager template
    changelog_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liquibase Changelog Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8fafc;
        }
        .header {
            background: #1e293b;
            color: white;
            padding: 1rem 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .back-btn {
            background: #6b7280;
            color: white;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 3px;
            margin-bottom: 1rem;
            display: inline-block;
        }
        .changelog-item {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4f46e5;
        }
        .changelog-preview {
            background: #f3f4f6;
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Changelog Manager</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <h2>Changelog Files</h2>
        {% if changelog_files %}
        {% for file in changelog_files %}
        <div class="changelog-item">
            <h3>{{ file.name }}</h3>
            <p><strong>Size:</strong> {{ file.size }} characters</p>
            <p><strong>Path:</strong> {{ file.path }}</p>
            <details>
                <summary>Preview</summary>
                <div class="changelog-preview">{{ file.preview }}</div>
            </details>
        </div>
        {% endfor %}
        {% else %}
        <p>No changelog files found in the changelog directory.</p>
        {% endif %}
    </div>
</body>
</html>
"""
    
    with open('templates/changelog_manager.html', 'w', encoding='utf-8') as f:
        f.write(changelog_html)
    
    # Create history template
    history_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liquibase History</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8fafc;
        }
        .header {
            background: #1e293b;
            color: white;
            padding: 1rem 2rem;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .history-item {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-success {
            border-left: 4px solid #059669;
        }
        .status-failed {
            border-left: 4px solid #dc2626;
        }
        .back-btn {
            background: #6b7280;
            color: white;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 3px;
            margin-bottom: 1rem;
            display: inline-block;
        }
        .code-output {
            background: #1f2937;
            color: #e5e7eb;
            padding: 1rem;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Execution History</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <h2>Recent Executions</h2>
        {% if execution_history %}
        {% for item in execution_history %}
        <div class="history-item {% if item.success %}status-success{% else %}status-failed{% endif %}">
            <h3>{{ item.command }}</h3>
            <p><strong>Timestamp:</strong> {{ item.timestamp }}</p>
            <p><strong>Status:</strong> {% if item.success %}Success{% else %}Failed{% endif %}</p>
            {% if item.output %}
            <details>
                <summary>View Output</summary>
                <div class="code-output">{{ item.output }}</div>
            </details>
            {% endif %}
        </div>
        {% endfor %}
        {% else %}
        <p>No executions yet. Run some commands from the dashboard.</p>
        {% endif %}
        
        {% if db_history.success %}
        <h2>Database History</h2>
        <div class="history-item">
            <h3>Liquibase Database History</h3>
            <div class="code-output">{{ db_history.stdout }}</div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""
    
    with open('templates/liquibase_history.html', 'w', encoding='utf-8') as f:
        f.write(history_html)
    
    print("🔵 Starting Liquibase Web Interface on http://localhost:5002")
    
    # Start Flask app
    app.run(host='localhost', port=5002, debug=False)

if __name__ == '__main__':
    start_liquibase_web()
