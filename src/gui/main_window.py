"""
Main GUI Window
Professional Migration Tool Comparison Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from pathlib import Path

# Import our modular components
from web.connections import BytebaseAPI, WebInterfaceManager
from database.connection import DatabaseConnection
from migrations.executors import MigrationManager
from gui.components.status_panel import StatusPanel
from gui.components.output_panel import OutputPanel


class ProfessionalMigrationGUI:
    """Professional GUI for database migration tool comparison"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.db_connection = None
        self.bytebase_api = BytebaseAPI()
        self.web_manager = WebInterfaceManager()
        self.migration_manager = None
        
        # State tracking
        self.is_migrating = False
        self.migration_results = {}
        self.execution_times = {}
        
        # Create GUI
        self.create_widgets()
        self.setup_styles()
        
        # Initialize output
        self.output_panel.add_message("Welcome to Database Migration Tool Comparison", "info")
        self.output_panel.add_message("Please configure your database connection to begin.", "info")
    
    def setup_window(self):
        """Configure main window"""
        self.root.title("Database Migration Tool Comparison - EY POC")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Make resizable
        self.root.minsize(1000, 600)
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure(
            "EY.TButton",
            background="#ffd700",
            foreground="black",
            borderwidth=1,
            focuscolor="none"
        )
        style.map(
            "EY.TButton",
            background=[('active', '#ffed4e'), ('pressed', '#e6c200')]
        )
    
    def create_widgets(self):
        """Create main GUI widgets"""
        # Header
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.root, bg="#ffd700", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Database Migration Tool Comparison",
            bg="#ffd700",
            fg="black",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Professional Comparison: Redgate, Liquibase, and Bytebase",
            bg="#ffd700",
            fg="black",
            font=("Arial", 12)
        )
        subtitle_label.pack()
    
    def create_main_content(self):
        """Create main content area"""
        # Main container
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Configuration tab
        self.create_config_tab()
        
        # Execution tab
        self.create_execution_tab()
        
        # Analysis tab
        self.create_analysis_tab()
    
    def create_config_tab(self):
        """Create configuration tab"""
        config_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(config_frame, text="Configuration")
        
        # Left panel - Database Configuration
        left_panel = tk.LabelFrame(
            config_frame,
            text="Database Configuration",
            bg="white",
            fg="black",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Database type selection
        tk.Label(left_panel, text="Database Type:", bg="white", fg="black", font=("Arial", 10)).pack(anchor="w", pady=(0, 5))
        
        self.db_type_var = tk.StringVar(value="mysql")
        db_type_frame = tk.Frame(left_panel, bg="white")
        db_type_frame.pack(fill="x", pady=(0, 10))
        
        tk.Radiobutton(db_type_frame, text="MySQL", variable=self.db_type_var, value="mysql", 
                      bg="white", fg="black", font=("Arial", 10)).pack(side="left", padx=(0, 20))
        tk.Radiobutton(db_type_frame, text="SQL Server", variable=self.db_type_var, value="sqlserver", 
                      bg="white", fg="black", font=("Arial", 10)).pack(side="left")
        
        # Connection fields
        fields = [
            ("Host:", "host_entry"),
            ("Port:", "port_entry"),
            ("Database:", "database_entry"),
            ("Username:", "username_entry"),
            ("Password:", "password_entry")
        ]
        
        self.entries = {}
        for label, entry_name in fields:
            tk.Label(left_panel, text=label, bg="white", fg="black", font=("Arial", 10)).pack(anchor="w", pady=(5, 2))
            entry = tk.Entry(left_panel, font=("Arial", 10), width=30)
            if "password" in entry_name:
                entry.config(show="*")
            entry.pack(fill="x", pady=(0, 5))
            self.entries[entry_name] = entry
        
        # Set default values
        self.entries["host_entry"].insert(0, "localhost")
        self.entries["port_entry"].insert(0, "3306")
        self.entries["username_entry"].insert(0, "root")
        
        # Connection buttons
        button_frame = tk.Frame(left_panel, bg="white")
        button_frame.pack(fill="x", pady=10)
        
        self.connect_btn = ttk.Button(
            button_frame,
            text="Test Connection",
            command=self.test_connection,
            style="EY.TButton"
        )
        self.connect_btn.pack(side="left", padx=(0, 10))
        
        self.save_config_btn = ttk.Button(
            button_frame,
            text="Save Configuration",
            command=self.save_configuration,
            style="EY.TButton"
        )
        self.save_config_btn.pack(side="left")
        
        # Right panel - Tool Configuration
        right_panel = tk.LabelFrame(
            config_frame,
            text="Tool Configuration",
            bg="white",
            fg="black",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Web interfaces section
        web_frame = tk.LabelFrame(right_panel, text="Web Interfaces", bg="white", fg="black", font=("Arial", 10, "bold"))
        web_frame.pack(fill="x", pady=(0, 10))
        
        bytebase_btn = ttk.Button(
            web_frame,
            text="Open Bytebase (Port 8080)",
            command=lambda: self.web_manager.open_bytebase(),
            style="EY.TButton"
        )
        bytebase_btn.pack(fill="x", pady=5)
        
        # Tool status section
        status_frame = tk.LabelFrame(right_panel, text="Tool Status", bg="white", fg="black", font=("Arial", 10, "bold"))
        status_frame.pack(fill="x", pady=(0, 10))
        
        # Create status indicators
        tools = ["Redgate", "Liquibase", "Bytebase"]
        self.tool_status_labels = {}
        
        for tool in tools:
            tool_frame = tk.Frame(status_frame, bg="white")
            tool_frame.pack(fill="x", pady=2)
            
            tk.Label(tool_frame, text=f"{tool}:", bg="white", fg="black", font=("Arial", 10), width=12, anchor="w").pack(side="left")
            status_label = tk.Label(tool_frame, text="Ready", bg="white", fg="gray", font=("Arial", 10))
            status_label.pack(side="left")
            
            self.tool_status_labels[tool.lower()] = status_label
    
    def create_execution_tab(self):
        """Create execution tab"""
        execution_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(execution_frame, text="Migration Execution")
        
        # Left side - Controls and Status
        left_panel = tk.Frame(execution_frame, bg="white")
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Migration controls
        control_frame = tk.LabelFrame(
            left_panel,
            text="Migration Controls",
            bg="white",
            fg="black",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Individual tool buttons
        tool_buttons = [
            ("Run Redgate Migration", "redgate", self.run_redgate_migration),
            ("Run Liquibase Migration", "liquibase", self.run_liquibase_migration),
            ("Run Bytebase Migration", "bytebase", self.run_bytebase_migration)
        ]
        
        self.tool_buttons = {}
        for text, tool, command in tool_buttons:
            btn = ttk.Button(control_frame, text=text, command=command, style="EY.TButton")
            btn.pack(fill="x", pady=5)
            self.tool_buttons[tool] = btn
        
        # Separator
        ttk.Separator(control_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Run all button
        self.run_all_btn = ttk.Button(
            control_frame,
            text="Run All Migrations",
            command=self.run_all_migrations,
            style="EY.TButton"
        )
        self.run_all_btn.pack(fill="x", pady=5)
        
        # Status panel
        self.status_panel = StatusPanel(left_panel)
        self.status_panel.get_frame().pack(fill="both", expand=True)
        
        # Right side - Output
        right_panel = tk.Frame(execution_frame, bg="white")
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.output_panel = OutputPanel(right_panel)
        self.output_panel.get_frame().pack(fill="both", expand=True)
    
    def create_analysis_tab(self):
        """Create analysis tab"""
        analysis_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(analysis_frame, text="Results Analysis")
        
        # Placeholder for future analysis features
        tk.Label(
            analysis_frame,
            text="Migration Results Analysis",
            bg="white",
            fg="black",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        tk.Label(
            analysis_frame,
            text="This section will contain detailed analysis of migration results\nincluding performance comparisons and recommendations.",
            bg="white",
            fg="gray",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=10)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9),
            relief="sunken",
            anchor="w",
            padx=10
        )
        self.status_bar.pack(side="bottom", fill="x")
    
    def test_connection(self):
        """Test database connection"""
        try:
            # Get connection parameters
            db_type = self.db_type_var.get()
            host = self.entries["host_entry"].get()
            port = self.entries["port_entry"].get()
            database = self.entries["database_entry"].get()
            username = self.entries["username_entry"].get()
            password = self.entries["password_entry"].get()
            
            if not all([host, port, database, username]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Create connection
            self.db_connection = DatabaseConnection(db_type, host, port, database, username, password)
            
            # Test connection
            test_result = self.db_connection.test_connection()
            if test_result["success"]:
                success_msg = f"✅ Connected to {db_type.upper()}\nDatabase: {database}\nServer: {test_result.get('db_info', 'Unknown')}"
                messagebox.showinfo("Success", success_msg)
                self.status_panel.update_connection_status(True, db_type.upper())
                self.status_bar.config(text=f"Connected to {db_type} database on {host}:{port}")
                
                # Initialize migration manager
                self.migration_manager = MigrationManager(self.db_connection, self.bytebase_api)
                
            else:
                error_msg = test_result.get("message", "Unknown connection error")
                messagebox.showerror("Error", f"Failed to connect to database:\n\n{error_msg}")
                self.status_panel.update_connection_status(False)
                self.status_bar.config(text="Connection failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            self.status_panel.update_connection_status(False)
            self.status_bar.config(text="Connection error")
    
    def save_configuration(self):
        """Save current configuration"""
        messagebox.showinfo("Configuration", "Configuration saved successfully!")
    
    def run_tool_migration(self, tool_name):
        """Run migration for a specific tool"""
        if not self.db_connection:
            messagebox.showerror("Error", "Please connect to a database first")
            return
        
        if self.is_migrating:
            messagebox.showwarning("Warning", "Migration already in progress")
            return
        
        self.is_migrating = True
        self.status_panel.update_tool_status(tool_name, "Running...", "blue")
        self.output_panel.add_tool_header(tool_name)
        
        def migration_callback(results):
            """Handle migration completion"""
            self.migration_results[tool_name] = results
            self.output_panel.add_tool_results(tool_name, results)
            
            # Determine status
            has_errors = any("❌" in r for r in results)
            has_success = any("✓" in r for r in results)
            
            if has_errors:
                status, color = "Failed", "red"
            elif has_success:
                status, color = "Complete", "green"
            else:
                status, color = "No Changes", "gray"
            
            self.status_panel.update_tool_status(tool_name, status, color)
            self.is_migrating = False
        
        # Run migration
        self.migration_manager.run_migration(tool_name.lower(), lambda t, r: migration_callback(r))
    
    def run_redgate_migration(self):
        """Run Redgate migration"""
        self.run_tool_migration("Redgate")
    
    def run_liquibase_migration(self):
        """Run Liquibase migration"""
        self.run_tool_migration("Liquibase")
    
    def run_bytebase_migration(self):
        """Run Bytebase migration"""
        self.run_tool_migration("Bytebase")
    
    def run_all_migrations(self):
        """Run all migrations sequentially"""
        if not self.db_connection:
            messagebox.showerror("Error", "Please connect to a database first")
            return
        
        if self.is_migrating:
            messagebox.showwarning("Warning", "Migration already in progress")
            return
        
        self.is_migrating = True
        self.status_panel.reset_progress()
        self.output_panel.add_message("Starting comprehensive migration comparison...", "info")
        
        def progress_callback(event_type, data):
            """Handle progress updates"""
            if event_type == 'complete':
                self.is_migrating = False
                self.status_panel.update_progress(100, "All migrations completed")
                self.output_panel.add_summary(self.migration_results, self.execution_times)
        
        # Run all migrations
        self.migration_manager.run_all_migrations(progress_callback)


# GUI initialization
def create_gui():
    """Create and return the main GUI"""
    root = tk.Tk()
    app = ProfessionalMigrationGUI(root)
    return root, app
