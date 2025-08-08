"""
Database Connection Module
Handles database connections for MySQL and SQL Server
"""

import os
import mysql.connector
import pyodbc
from typing import Optional, Dict, Any

class DatabaseConnection:
    """Database connection manager for multiple database types"""
    
    def __init__(self, db_type=None, host=None, port=None, database=None, username=None, password=None, **kwargs):
        """Initialize database connection with optional parameters"""
        self.connection = None
        self.db_type = db_type
        self.connection_params = {}
        
        # If parameters provided, attempt connection
        if db_type and host and database:
            if db_type == "mysql":
                port = int(port) if port else 3306
                username = username or "root"
                password = password or ""
                self.connect_mysql(host, port, username, password, database)
            elif db_type == "sqlserver":
                driver = kwargs.get('driver', 'ODBC Driver 17 for SQL Server')
                trusted_connection = kwargs.get('trusted_connection', True)
                port = port or "1433"
                self.connect_sqlserver(host, port, database, driver, username, password, trusted_connection)
    
    def connect_mysql(self, host: str, port: int, user: str, password: str, database: str):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            self.db_type = "mysql"
            self.connection_params = {
                'host': host,
                'port': port,
                'user': user,
                'database': database
            }
            return {"success": True, "message": "Connected to MySQL successfully"}
        except Exception as e:
            return {"success": False, "message": f"MySQL connection failed: {str(e)}"}
    
    def connect_sqlserver(self, host: str, port: str, database: str, driver: str, 
                         username: str = None, password: str = None, trusted_connection: bool = True):
        """Connect to SQL Server database"""
        try:
            # Handle different SQL Server connection formats
            if "\\" in host:
                # Named instance format
                if "," in host:
                    server = host
                else:
                    server = f"{host},14766"  # Dynamic port
            else:
                server = f"{host},{port}"
            
            if trusted_connection:
                # Windows Authentication
                connection_string = f"""
                DRIVER={{{driver}}};
                SERVER={server};
                DATABASE={database};
                Trusted_Connection=yes;
                """
            else:
                # SQL Server Authentication
                connection_string = f"""
                DRIVER={{{driver}}};
                SERVER={server};
                DATABASE={database};
                UID={username};
                PWD={password};
                """
            
            self.connection = pyodbc.connect(connection_string.strip())
            self.db_type = "sqlserver"
            self.connection_params = {
                'host': host,
                'port': port,
                'database': database,
                'driver': driver,
                'trusted_connection': trusted_connection
            }
            return {"success": True, "message": "Connected to SQL Server successfully"}
            
        except Exception as e:
            # Try alternative connection formats
            alternate_servers = [
                f"{host.split(',')[0]}",  # Just the host
                f"{host.split(',')[0]},1433",  # Standard port
                ".\\SQLEXPRESS",  # Named pipes
                "(local)\\SQLEXPRESS"  # Local format
            ]
            
            for alt_server in alternate_servers:
                try:
                    if trusted_connection:
                        alt_connection_string = f"""
                        DRIVER={{{driver}}};
                        SERVER={alt_server};
                        DATABASE={database};
                        Trusted_Connection=yes;
                        """
                    else:
                        alt_connection_string = f"""
                        DRIVER={{{driver}}};
                        SERVER={alt_server};
                        DATABASE={database};
                        UID={username};
                        PWD={password};
                        """
                    
                    self.connection = pyodbc.connect(alt_connection_string.strip())
                    self.db_type = "sqlserver"
                    self.connection_params = {
                        'host': alt_server,
                        'port': port,
                        'database': database,
                        'driver': driver,
                        'trusted_connection': trusted_connection
                    }
                    return {"success": True, "message": f"Connected to SQL Server successfully (using {alt_server})"}
                    
                except Exception:
                    continue
            
            return {"success": False, "message": f"SQL Server connection failed: {str(e)}"}
    
    def test_connection(self):
        """Test the current database connection"""
        try:
            if not self.connection:
                return {"success": False, "message": "No active connection"}
            
            cursor = self.connection.cursor()
            
            if self.db_type == "mysql":
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                db_info = f"MySQL {version}"
            elif self.db_type == "sqlserver":
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                db_info = version.split('\n')[0] if '\n' in version else version[:50] + "..."
            
            cursor.close()
            
            return {
                "success": True, 
                "message": "Connection test successful",
                "db_info": db_info,
                "db_type": self.db_type.upper(),
                "database": self.connection_params.get('database', 'Unknown')
            }
            
        except Exception as e:
            return {"success": False, "message": f"Connection test failed: {str(e)}"}
    
    def get_tables(self):
        """Get list of tables in the database"""
        try:
            if not self.connection:
                return {"success": False, "message": "No active connection"}
            
            cursor = self.connection.cursor()
            tables = []
            
            if self.db_type == "mysql":
                cursor.execute("SHOW TABLES")
                table_results = cursor.fetchall()
                
                for table_row in table_results:
                    table_name = table_row[0]
                    
                    # Get table info
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    row_count = cursor.fetchone()[0]
                    
                    tables.append({
                        'name': table_name,
                        'type': 'TABLE',
                        'rows': row_count,
                        'size': 'N/A',
                        'modified': 'N/A'
                    })
                    
            elif self.db_type == "sqlserver":
                cursor.execute("""
                    SELECT TABLE_NAME, TABLE_TYPE 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                table_results = cursor.fetchall()
                
                for table_name, table_type in table_results:
                    # Get row count
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
                        row_count = cursor.fetchone()[0]
                    except:
                        row_count = 0
                    
                    tables.append({
                        'name': table_name,
                        'type': table_type,
                        'rows': row_count,
                        'size': 'N/A',
                        'modified': 'N/A'
                    })
            
            cursor.close()
            return {"success": True, "tables": tables}
            
        except Exception as e:
            return {"success": False, "message": f"Failed to get tables: {str(e)}"}
    
    def execute_query(self, query: str):
        """Execute a SQL query"""
        try:
            if not self.connection:
                return {"success": False, "message": "No active connection"}
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # If it's a SELECT query, fetch results
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                
                return {
                    "success": True,
                    "results": results,
                    "columns": columns
                }
            else:
                # For INSERT, UPDATE, DELETE
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                
                return {
                    "success": True,
                    "message": f"Query executed successfully. {affected_rows} rows affected."
                }
                
        except Exception as e:
            return {"success": False, "message": f"Query execution failed: {str(e)}"}
    
    def close(self):
        """Close the database connection"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                self.db_type = None
                self.connection_params = {}
            return {"success": True, "message": "Connection closed successfully"}
        except Exception as e:
            return {"success": False, "message": f"Error closing connection: {str(e)}"}
    
    def is_connected(self):
        """Check if database is currently connected"""
        return self.connection is not None
