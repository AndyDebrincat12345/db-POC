# Database Migration Tool Comparison - EY POC

## Project Structure

This repository has been restructured into a clean, modular architecture:

```
db-POC/
├── main.py                 # Main entry point - run this to start the application
├── src/                    # Main source code directory
│   ├── gui/               # GUI components and interface
│   │   ├── main_window.py # Main GUI window and application logic
│   │   └── components/    # Reusable GUI components
│   │       ├── status_panel.py    # Connection and tool status display
│   │       └── output_panel.py    # Migration output and logging
│   ├── web/               # Web interface and API connections
│   │   └── connections.py # Bytebase API and web interface management
│   ├── database/          # Database connection management
│   │   └── connection.py  # MySQL and SQL Server connection handling
│   └── migrations/        # Migration tool executors
│       └── executors.py   # Bytebase, Liquibase, and Redgate execution logic
├── bytebase/              # Bytebase configuration and migrations
├── liquibase/             # Liquibase configuration and changelogs
├── redgate/               # Redgate configuration and scripts
└── requirements.txt       # Python dependencies
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

## Features

### Clean Architecture
- **Separation of Concerns**: GUI, web, database, and migration logic are separated
- **Modular Design**: Each component can be developed and tested independently
- **Professional Structure**: Industry-standard Python package organization

### GUI Components
- **Main Window**: Professional tkinter interface with tabbed layout
- **Status Panel**: Real-time connection and tool status display
- **Output Panel**: Comprehensive migration logging with color-coded messages
- **Configuration Tab**: Database connection and tool settings
- **Execution Tab**: Migration controls and real-time output
- **Analysis Tab**: Results comparison and recommendations

### Web Interfaces
- **BytebaseAPI**: Complete API client for Bytebase server interaction
- **WebInterfaceManager**: Automated web interface launching and management

### Database Support
- **MySQL**: Full connection support with mysql-connector-python
- **SQL Server**: ODBC connection support with pyodbc
- **Connection Testing**: Validate connections before migration execution

### Migration Tools
- **Bytebase**: API-based migration execution with Docker integration
- **Liquibase**: CLI-based execution with proper JDBC driver management
- **Redgate**: PowerShell-based deployment with schema comparison

## Usage

### 1. Configure Database Connection
- Select database type (MySQL/SQL Server)
- Enter connection parameters (host, port, database, username, password)
- Test connection to validate settings

### 2. Run Migrations
- **Individual Tools**: Run Redgate, Liquibase, or Bytebase separately
- **Comprehensive Comparison**: Run all tools sequentially for comparison
- **Real-time Output**: Monitor execution progress and results

### 3. Analyze Results
- Compare execution times and success rates
- Review detailed logs and error messages
- Generate recommendations based on results

## Development

### Adding New Features
1. **GUI Components**: Add to `src/gui/components/`
2. **Database Support**: Extend `src/database/connection.py`
3. **Migration Tools**: Add new executors to `src/migrations/`
4. **Web Interfaces**: Extend `src/web/connections.py`

### Code Organization
- **main.py**: Entry point with error handling
- **src/gui/**: All user interface components
- **src/web/**: Web-based tool interactions
- **src/database/**: Database connection management
- **src/migrations/**: Migration execution logic

## Benefits of New Structure

1. **Maintainability**: Clear separation makes code easier to maintain
2. **Testability**: Each module can be unit tested independently
3. **Scalability**: Easy to add new tools or database types
4. **Professional**: Industry-standard Python package structure
5. **Reusability**: Components can be reused in other projects

## Migration from Original Structure

The original monolithic `gui.py` file has been split into:
- **GUI Logic**: Moved to `src/gui/main_window.py` and components
- **Web Integration**: Extracted to `src/web/connections.py`
- **Database Logic**: Separated to `src/database/connection.py`
- **Migration Execution**: Organized in `src/migrations/executors.py`

This provides a much cleaner, more professional codebase that's easier to work with and extend.
