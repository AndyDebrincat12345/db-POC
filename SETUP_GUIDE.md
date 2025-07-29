# Complete Setup Guide for Database Migration Tools POC

## Prerequisites
- Python 3.8+
- MySQL 8.0+
- Docker Desktop (for Bytebase)
- Administrative privileges

## Step 1: Install Required Dependencies

```powershell
# Navigate to project directory
cd "c:\Users\XH782WN\OneDrive - EY\Documents\db-POC"

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Set Up Bytebase (Full Implementation)

### 2.1 Start Bytebase Server
```powershell
# Start Docker Desktop first
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait for Docker to start (about 1-2 minutes), then run:
docker run -d --name bytebase-poc --restart always --publish 8080:8080 --volume "c:\Users\XH782WN\OneDrive - EY\Documents\db-POC\bytebase-data:/var/opt/bytebase" bytebase/bytebase:2.11.1 --data /var/opt/bytebase --port 8080
```

### 2.2 Configure Bytebase
1. Open browser and go to: http://localhost:8080
2. Create admin account (email: admin@example.com, password: admin123)
3. Create a new project: "POC Database"
4. Add database instance:
   - Host: localhost
   - Port: 3306
   - Username: root
   - Password: eyroot
   - Database: status_poc

### 2.3 Test Bytebase API
```powershell
python bytebase_api.py
```

## Step 3: Verify Liquibase (Already Working)

```powershell
# Test Liquibase installation
liquibase --version

# Test migration (from liquibase directory)
cd liquibase
liquibase update
cd ..
```

## Step 4: Set Up Redgate Simulation

The Redgate simulator uses MySQL native tools to replicate Redgate's workflow:

```powershell
# Test Redgate simulator
python redgate_simulator.py
```

## Step 5: Test Complete Setup

```powershell
# Run the updated GUI with proper tool implementations
python gui.py
```

## Expected Behavior

### Bytebase
- Uses REST API calls to create migration issues
- Manages migrations through web interface
- Provides GitOps workflow integration

### Liquibase
- Uses CLI tool for migration execution
- Handles XML changesets and dependencies
- Provides cross-database compatibility

### Redgate (Simulated)
- Uses mysqldump for schema comparison
- Generates deployment reports
- Simulates enterprise deployment workflow

## Troubleshooting

### Bytebase Issues
- **"Server not running"**: Ensure Docker Desktop is started and container is running
- **"Authentication failed"**: Check if you've completed the initial setup at http://localhost:8080
- **"Cannot connect"**: Verify port 8080 is not blocked by firewall

### Liquibase Issues
- **"Command not found"**: Ensure Liquibase is properly installed and in PATH
- **"Connection failed"**: Check database credentials in liquibase.properties

### Redgate Issues
- **"mysqldump not found"**: Ensure MySQL client tools are installed and in PATH
- **"Permission denied"**: Check database user permissions

## Verification Checklist

- [ ] Bytebase web interface accessible at http://localhost:8080
- [ ] Bytebase API test passes (python bytebase_api.py)
- [ ] Liquibase version check works (liquibase --version)
- [ ] Redgate simulator test passes (python redgate_simulator.py)
- [ ] GUI launches without errors (python gui.py)
- [ ] All three migration tools execute successfully in GUI

## Next Steps

1. Complete the setup using this guide
2. Run comprehensive tests using the updated GUI
3. Document results in the LaTeX report
4. Compare the actual tool implementations vs simulations
