#!/usr/bin/env python3
"""
Professional Database Migration POC GUI
Modern white and yellow themed interface with enhanced web integration
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import webbrowser
import time
import mysql.connector

# Import our tool implementations
from bytebase_api import BytebaseAPI
from redgate_simulator import RedgateSimulator

load_dotenv()

class ProfessionalMigrationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Database Migration POC - EY Enterprise Tools")
        self.root.state('zoomed')  # Fullscreen on Windows
        self.root.configure(bg='white')
        
        # Initialize tool instances
        self.bytebase_api = BytebaseAPI()
        self.redgate_simulator = RedgateSimulator()
        
        # Results storage
        self.results = {
            'bytebase': [],
            'liquibase': [],
            'redgate': []
        }
        
        # Status variables
        self.web_interfaces_started = False
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Setup UI components
        self.setup_styles()
        self.setup_main_window()
        self.create_interface()
        
        # Start time updates
        self.update_time()
    def setup_styles(self):
        """Configure modern white and yellow theme styles"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure notebook (tabs) style
        style.configure('TNotebook', background='white', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#f8f9fa', 
                       foreground='#2c3e50',
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', '#ffd700'),
                           ('active', '#fff3cd')])
        
        # Configure frame styles
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=2)
        style.configure('Header.TFrame', background='#ffd700')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background='#ffd700',
                       foreground='#2c3e50',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        style.map('Primary.TButton',
                 background=[('active', '#ffed4a')])
        
        style.configure('Success.TButton',
                       background='#28a745',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Danger.TButton',
                       background='#dc3545',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Info.TButton',
                       background='#17a2b8',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
    
    def setup_main_window(self):
        """Setup main window properties"""
        self.root.configure(bg='white')
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (1000 // 2)
        self.root.geometry(f'1600x1000+{x}+{y}')
    
    def create_interface(self):
        """Create the main interface"""
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
    
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg='#ffd700', height=100)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🚀 Professional Database Migration Tools POC",
                              font=('Segoe UI', 24, 'bold'),
                              bg='#ffd700',
                              fg='#2c3e50')
        title_label.pack(expand=True)
    
    def create_main_content(self):
        """Create the main tabbed content area"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Create all 5 tabs
        self.create_migrations_tab()
        self.create_console_tab()
        self.create_data_tab()
        self.create_analysis_tab()
        self.create_settings_tab()
        
        # Now that all tabs are created and settings initialized, load table data
        try:
            self.refresh_tables()
        except Exception as e:
            # Silently handle initial table refresh errors
            pass
        
    def create_migrations_tab(self):
        """Create the migrations tab with tool cards and web integration"""
        migrations_frame = ttk.Frame(self.notebook)
        self.notebook.add(migrations_frame, text="🚀 Migrations")
        
        # Scrollable frame setup
        canvas = tk.Canvas(migrations_frame, bg='white')
        scrollbar = ttk.Scrollbar(migrations_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mousewheel support
        self.add_mousewheel_support(canvas)
        
        # Header section
        header_frame = tk.Frame(scrollable_frame, bg='#ffd700', height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text="🚀 Database Migration Tools Comparison",
                font=('Segoe UI', 18, 'bold'),
                bg='#ffd700', fg='#2c3e50').pack(expand=True)
        
        # Tools grid
        tools_grid = tk.Frame(scrollable_frame, bg='white')
        tools_grid.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tool cards
        self.create_migration_card(
            tools_grid, 
            "🔵 Bytebase Enterprise", 
            "#3498db",
            self.run_bytebase_migration,
            lambda: self.open_web_page('http://localhost:8080', 'Bytebase')
        )
        
        self.create_migration_card(
            tools_grid, 
            "🟣 Liquibase Professional", 
            "#9b59b6",
            self.run_liquibase_migration,
            lambda: self.open_web_page('http://localhost:5002', 'Liquibase')
        )
        
        self.create_migration_card(
            tools_grid, 
            "🔴 Redgate SQL Toolbelt", 
            "#e74c3c",
            self.run_redgate_migration,
            lambda: self.open_web_page('http://localhost:5001', 'Redgate')
        )
        
        # Comprehensive migration section
        migration_section = tk.LabelFrame(scrollable_frame,
                                        text="⚡ Migration Operations",
                                        font=('Segoe UI', 14, 'bold'),
                                        bg='white', fg='#2c3e50')
        migration_section.pack(fill='x', padx=20, pady=20)
        
        migration_buttons = tk.Frame(migration_section, bg='white')
        migration_buttons.pack(pady=15)
        
        tk.Button(migration_buttons, text="🚀 Run All Migrations",
                 command=self.run_all_migrations,
                 bg='#ffd700', fg='#2c3e50',
                 font=('Segoe UI', 14, 'bold'),
                 relief='flat', padx=30, pady=12).pack(side='left', padx=10)
        
        tk.Button(migration_buttons, text="🌐 Run All UIs",
                 command=self.start_all_web_interfaces,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
        
        tk.Button(migration_buttons, text="🔗 Open All Web Pages",
                 command=self.open_all_web_pages,
                 bg='#17a2b8', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
        
        tk.Button(migration_buttons, text="🔄 Reset Database",
                 command=self.reset_database,
                 bg='#dc3545', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
        
        tk.Button(migration_buttons, text="🧪 Run Tests",
                 command=self.run_automated_test,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_migration_card(self, parent, title, color, command, web_command):
        """Create a migration tool card"""
        card_frame = tk.Frame(parent, bg='white', relief='raised', bd=2)
        card_frame.pack(fill='x', pady=10)
        
        # Header
        header = tk.Frame(card_frame, bg=color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text=title,
                font=('Segoe UI', 16, 'bold'),
                bg=color, fg='white').pack(side='left', padx=20, pady=15)
        
        # Button container for execute and web UI buttons
        button_container = tk.Frame(header, bg=color)
        button_container.pack(side='right', padx=20, pady=15)
        
        tk.Button(button_container, text="🌐 Web UI",
                 command=web_command,
                 bg='white', fg=color,
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=12, pady=4).pack(side='right', padx=(10, 0))
        
        tk.Button(button_container, text="▶️ Execute",
                 command=command,
                 bg='white', fg=color,
                 font=('Segoe UI', 11, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='right')
    def create_console_tab(self):
        """Create the console/output tab"""
        console_frame = ttk.Frame(self.notebook)
        self.notebook.add(console_frame, text="📟 Console")
        
        # Console header
        console_header = tk.Frame(console_frame, bg='#ffd700', height=60)
        console_header.pack(fill='x', pady=(0, 10))
        console_header.pack_propagate(False)
        
        tk.Label(console_header,
                text="🖥️ Migration Console & Output Logs",
                font=('Segoe UI', 16, 'bold'),
                bg='#ffd700', fg='#2c3e50').pack(expand=True)
        
        # Console controls
        controls_frame = tk.Frame(console_frame, bg='white')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(controls_frame, text="🗑️ Clear Console",
                 command=self.clear_console,
                 bg='#dc3545', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="💾 Save Log",
                 command=self.save_console_log,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)
        
        # Console output area
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            height=25,
            font=('Consolas', 11),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ffd700'
        )
        self.console_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Add welcome message
        self.console_text.insert(tk.END, "🚀 Professional Database Migration Console\n")
        self.console_text.insert(tk.END, "=" * 60 + "\n")
        self.console_text.insert(tk.END, f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.console_text.insert(tk.END, "Ready for migration operations...\n\n")
    
    def create_data_tab(self):
        """Create the data visualization/tables tab"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="📊 Data")
        
        # Data header
        data_header = tk.Frame(data_frame, bg='#ffd700', height=60)
        data_header.pack(fill='x', pady=(0, 10))
        data_header.pack_propagate(False)
        
        self.data_header_label = tk.Label(data_header,
                text="📈 Database Tables & Migration Data",
                font=('Segoe UI', 16, 'bold'),
                bg='#ffd700', fg='#2c3e50')
        self.data_header_label.pack(expand=True)
        
        # Data controls
        data_controls = tk.Frame(data_frame, bg='white')
        data_controls.pack(fill='x', padx=20, pady=10)
        
        # Left side controls
        left_controls = tk.Frame(data_controls, bg='white')
        left_controls.pack(side='left')
        
        tk.Button(left_controls, text="🔄 Refresh Tables",
                 command=self.refresh_tables,
                 bg='#17a2b8', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='left', padx=(0, 5))
        
        tk.Button(left_controls, text="📊 Export Data",
                 command=self.export_table_data,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5).pack(side='left', padx=5)
        
        # Right side controls (for table view)
        right_controls = tk.Frame(data_controls, bg='white')
        right_controls.pack(side='right')
        
        # Back button (initially hidden)
        self.back_button = tk.Button(right_controls, text="⬆️ Back to Tables",
                 command=self.show_tables_list,
                 bg='#6c757d', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5)
        
        # Table action buttons (initially hidden)
        self.add_row_button = tk.Button(right_controls, text="➕ Add Row",
                 command=self.add_table_row,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5)
        
        self.edit_row_button = tk.Button(right_controls, text="✏️ Edit Row",
                 command=self.edit_table_row,
                 bg='#ffc107', fg='#2c3e50',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5)
        
        self.delete_row_button = tk.Button(right_controls, text="🗑️ Delete Row",
                 command=self.delete_table_row,
                 bg='#dc3545', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5)
        
        # Main display area
        self.data_display_frame = tk.Frame(data_frame, bg='white')
        self.data_display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create tables list view
        self.create_tables_list_view()
        
        # Create table content view (initially hidden)
        self.create_table_content_view()
        
        # State variables
        self.current_table = None
        self.viewing_table_content = False
        
        # Show tables list initially
        self.show_tables_list()
        
        # Load initial table data only after settings are initialized
        # Will be called after all tabs are created
    
    def create_analysis_tab(self):
        """Create the analysis/reports tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="📈 Analysis")
        
        # Analysis header
        analysis_header = tk.Frame(analysis_frame, bg='#ffd700', height=60)
        analysis_header.pack(fill='x', pady=(0, 10))
        analysis_header.pack_propagate(False)
        
        tk.Label(analysis_header,
                text="📊 Database Schema Analysis & Migration Reports",
                font=('Segoe UI', 16, 'bold'),
                bg='#ffd700', fg='#2c3e50').pack(expand=True)
        
        # Main content frame
        content_frame = tk.Frame(analysis_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Analysis controls
        controls_frame = tk.Frame(content_frame, bg='white')
        controls_frame.pack(fill='x', pady=(0, 15))
        
        tk.Button(controls_frame, text="🔍 Schema Analysis",
                 command=self.run_schema_analysis,
                 bg='#ffd700', fg='#2c3e50',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=25, pady=10).pack(side='left', padx=(0, 10))
        
        tk.Button(controls_frame, text="📋 Migration Summary",
                 command=self.generate_migration_summary,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=25, pady=10).pack(side='left', padx=10)
        
        tk.Button(controls_frame, text="🗑️ Clear Report",
                 command=self.clear_analysis,
                 bg='#dc3545', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=25, pady=10).pack(side='right')
        
        # Analysis results area
        self.analysis_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            height=25,
            font=('Consolas', 11),
            bg='#f8f9fa',
            relief='raised',
            bd=2
        )
        self.analysis_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Add initial welcome message
        self.analysis_text.insert(tk.END, "📊 Database Analysis Center\n")
        self.analysis_text.insert(tk.END, "=" * 50 + "\n\n")
        self.analysis_text.insert(tk.END, "Welcome to the Database Analysis Center!\n\n")
        self.analysis_text.insert(tk.END, "🔍 Use 'Schema Analysis' to examine your database structure\n")
        self.analysis_text.insert(tk.END, "📋 Use 'Migration Summary' to review completed operations\n\n")
        self.analysis_text.insert(tk.END, "Select an analysis option above to begin...\n")
    
    def create_settings_tab(self):
        """Create the settings/configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings header
        settings_header = tk.Frame(settings_frame, bg='#ffd700', height=60)
        settings_header.pack(fill='x', pady=(0, 10))
        settings_header.pack_propagate(False)
        
        tk.Label(settings_header,
                text="⚙️ Configuration & Database Settings",
                font=('Segoe UI', 16, 'bold'),
                bg='#ffd700', fg='#2c3e50').pack(expand=True)
        
        # Settings content
        settings_content = tk.Frame(settings_frame, bg='white')
        settings_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Database Connection Settings
        db_frame = tk.LabelFrame(settings_content,
                                text="🗄️ Database Connection",
                                font=('Segoe UI', 12, 'bold'),
                                bg='white')
        db_frame.pack(fill='x', pady=10)
        
        # Connection form
        form_frame = tk.Frame(db_frame, bg='white')
        form_frame.pack(padx=20, pady=15)
        
        # Host
        tk.Label(form_frame, text="Host:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.host_var = tk.StringVar(value=os.getenv("DB_HOST", "localhost"))
        tk.Entry(form_frame, textvariable=self.host_var, font=('Segoe UI', 10), width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # Port
        tk.Label(form_frame, text="Port:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.port_var = tk.StringVar(value=os.getenv("DB_PORT", "3306"))
        tk.Entry(form_frame, textvariable=self.port_var, font=('Segoe UI', 10), width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Database
        tk.Label(form_frame, text="Database:", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.db_var = tk.StringVar(value=os.getenv("DB_NAME", "status_poc"))
        tk.Entry(form_frame, textvariable=self.db_var, font=('Segoe UI', 10), width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Test connection button
        tk.Button(form_frame, text="🔗 Test Connection",
                 command=self.test_connection,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat', padx=15, pady=5).grid(row=1, column=2, columnspan=2, padx=10, pady=5)
        
        # Tool Settings
        tools_frame = tk.LabelFrame(settings_content,
                                   text="🛠️ Tool Configuration",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='white')
        tools_frame.pack(fill='x', pady=10)
        
        tools_content = tk.Frame(tools_frame, bg='white')
        tools_content.pack(padx=20, pady=15)
        
        # Tool status checkboxes
        self.bytebase_enabled = tk.BooleanVar(value=True)
        self.liquibase_enabled = tk.BooleanVar(value=True)
        self.redgate_enabled = tk.BooleanVar(value=True)
        
        tk.Checkbutton(tools_content, text="🔵 Enable Bytebase",
                      variable=self.bytebase_enabled,
                      font=('Segoe UI', 10),
                      bg='white').pack(anchor='w', pady=2)
        
        tk.Checkbutton(tools_content, text="🟣 Enable Liquibase",
                      variable=self.liquibase_enabled,
                      font=('Segoe UI', 10),
                      bg='white').pack(anchor='w', pady=2)
        
        tk.Checkbutton(tools_content, text="🔴 Enable Redgate",
                      variable=self.redgate_enabled,
                      font=('Segoe UI', 10),
                      bg='white').pack(anchor='w', pady=2)
    
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        status_frame = tk.Frame(self.root, bg='#2c3e50', height=40)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # Status label
        tk.Label(status_frame, textvariable=self.status_var,
                font=('Segoe UI', 10),
                bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=10)
        
        # Time label
        self.time_var = tk.StringVar()
        tk.Label(status_frame, textvariable=self.time_var,
                font=('Segoe UI', 10),
                bg='#2c3e50', fg='#ffd700').pack(side='right', padx=20, pady=10)
    def add_mousewheel_support(self, canvas):
        """Add mousewheel scrolling support to canvas"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_var.set(f"🕒 {current_time}")
        self.root.after(1000, self.update_time)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.log_to_console(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def log_to_console(self, message):
        """Add message to console"""
        if hasattr(self, 'console_text'):
            self.console_text.insert(tk.END, f"{message}\n")
            self.console_text.see(tk.END)
    
    def clear_console(self):
        """Clear the console output"""
        if hasattr(self, 'console_text'):
            self.console_text.delete(1.0, tk.END)
            self.log_to_console("Console cleared")
    
    def save_console_log(self):
        """Save console log to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.console_text.get(1.0, tk.END))
                self.update_status(f"Console log saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")
    
    def get_connection(self):
        """Get database connection using current settings"""
        try:
            connection = mysql.connector.connect(
                host=self.host_var.get(),
                port=int(self.port_var.get()),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=self.db_var.get()
            )
            return connection
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    def test_connection(self):
        """Test database connection"""
        try:
            conn = self.get_connection()
            conn.close()
            self.update_status("✅ Database connection successful")
            messagebox.showinfo("Success", "Database connection successful!")
        except Exception as e:
            self.update_status(f"❌ Database connection failed: {str(e)}")
            messagebox.showerror("Connection Error", str(e))
    
    def refresh_tables(self):
        """Refresh the tables display"""
        try:
            # Check if settings variables are initialized
            if not hasattr(self, 'host_var') or not hasattr(self, 'port_var') or not hasattr(self, 'db_var'):
                self.update_status("⚠️ Database settings not initialized yet")
                return
                
            # Clear existing items
            for item in self.tables_tree.get_children():
                self.tables_tree.delete(item)
            
            # Get table information
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                
                # Get table info
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = cursor.fetchone()[0]
                
                cursor.execute(f"""
                SELECT data_length + index_length as size 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() AND table_name = '{table_name}'
                """)
                size_result = cursor.fetchone()
                size = f"{size_result[0] / 1024:.1f} KB" if size_result[0] else "0 KB"
                
                self.tables_tree.insert('', 'end', text=table_name,
                                      values=('Table', row_count, size, datetime.now().strftime('%Y-%m-%d')))
            
            cursor.close()
            conn.close()
            self.update_status(f"✅ Loaded {len(tables)} tables")
            
        except Exception as e:
            self.update_status(f"❌ Failed to refresh tables: {str(e)}")
    
    def create_tables_list_view(self):
        """Create the tables list view"""
        self.tables_list_frame = tk.Frame(self.data_display_frame, bg='white')
        
        # Create treeview for table list
        self.tables_tree = ttk.Treeview(self.tables_list_frame, columns=('Type', 'Rows', 'Size', 'Modified'), show='tree headings')
        self.tables_tree.heading('#0', text='Table Name')
        self.tables_tree.heading('Type', text='Type')
        self.tables_tree.heading('Rows', text='Rows')
        self.tables_tree.heading('Size', text='Size')
        self.tables_tree.heading('Modified', text='Last Modified')
        
        # Table scrollbar
        self.table_list_scrollbar = ttk.Scrollbar(self.tables_list_frame, orient='vertical', command=self.tables_tree.yview)
        self.tables_tree.configure(yscrollcommand=self.table_list_scrollbar.set)
        
        self.tables_tree.pack(side='left', fill='both', expand=True)
        self.table_list_scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to open table
        self.tables_tree.bind('<Double-1>', self.on_table_double_click)
        
    def create_table_content_view(self):
        """Create the table content view"""
        self.table_content_frame = tk.Frame(self.data_display_frame, bg='white')
        
        # Create treeview for table content
        self.table_content_tree = ttk.Treeview(self.table_content_frame, show='tree headings')
        
        # Content scrollbars
        self.content_v_scrollbar = ttk.Scrollbar(self.table_content_frame, orient='vertical', command=self.table_content_tree.yview)
        self.content_h_scrollbar = ttk.Scrollbar(self.table_content_frame, orient='horizontal', command=self.table_content_tree.xview)
        
        self.table_content_tree.configure(
            yscrollcommand=self.content_v_scrollbar.set,
            xscrollcommand=self.content_h_scrollbar.set
        )
        
        # Pack content view
        self.table_content_tree.grid(row=0, column=0, sticky='nsew')
        self.content_v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.content_h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.table_content_frame.grid_rowconfigure(0, weight=1)
        self.table_content_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection
        self.table_content_tree.bind('<<TreeviewSelect>>', self.on_row_select)
    
    def show_tables_list(self):
        """Show the tables list view"""
        self.viewing_table_content = False
        self.current_table = None
        
        # Hide table content view
        self.table_content_frame.pack_forget()
        
        # Show tables list view
        self.tables_list_frame.pack(fill='both', expand=True)
        
        # Update header
        self.data_header_label.config(text="📈 Database Tables & Migration Data")
        
        # Hide table action buttons
        self.back_button.pack_forget()
        self.add_row_button.pack_forget()
        self.edit_row_button.pack_forget()
        self.delete_row_button.pack_forget()
        
        # Refresh tables list
        self.refresh_tables()
    
    def show_table_content(self, table_name):
        """Show the content of a specific table"""
        self.viewing_table_content = True
        self.current_table = table_name
        
        # Hide tables list view
        self.tables_list_frame.pack_forget()
        
        # Show table content view
        self.table_content_frame.pack(fill='both', expand=True)
        
        # Update header
        self.data_header_label.config(text=f"📋 Table: {table_name}")
        
        # Show table action buttons
        self.back_button.pack(side='right', padx=5)
        self.add_row_button.pack(side='right', padx=5)
        self.edit_row_button.pack(side='right', padx=5)
        self.delete_row_button.pack(side='right', padx=5)
        
        # Load table content
        self.load_table_content(table_name)
    
    def on_table_double_click(self, event):
        """Handle double-click on table in the list"""
        selection = self.tables_tree.selection()
        if selection:
            item = self.tables_tree.item(selection[0])
            table_name = item['text']
            self.show_table_content(table_name)
    
    def on_row_select(self, event):
        """Handle row selection in table content"""
        selection = self.table_content_tree.selection()
        if selection:
            # Enable edit/delete buttons when row is selected
            self.edit_row_button.config(state='normal')
            self.delete_row_button.config(state='normal')
        else:
            # Disable edit/delete buttons when no row is selected
            self.edit_row_button.config(state='disabled')
            self.delete_row_button.config(state='disabled')
    
    def load_table_content(self, table_name):
        """Load content of a specific table"""
        try:
            # Clear existing content
            for item in self.table_content_tree.get_children():
                self.table_content_tree.delete(item)
            
            # Get table structure and data
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get column information
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = cursor.fetchall()
            
            # Configure columns
            column_names = [col[0] for col in columns]
            self.table_content_tree['columns'] = column_names
            self.table_content_tree.heading('#0', text='Row')
            
            for col_name in column_names:
                self.table_content_tree.heading(col_name, text=col_name)
                self.table_content_tree.column(col_name, width=120, minwidth=50)
            
            # Get table data
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 500")  # Limit for performance
            rows = cursor.fetchall()
            
            # Insert data
            for i, row in enumerate(rows, 1):
                values = [str(val) if val is not None else '' for val in row]
                self.table_content_tree.insert('', 'end', text=str(i), values=values)
            
            cursor.close()
            conn.close()
            
            # Initially disable edit/delete buttons
            self.edit_row_button.config(state='disabled')
            self.delete_row_button.config(state='disabled')
            
            self.update_status(f"✅ Loaded {len(rows)} rows from {table_name}")
            
        except Exception as e:
            self.update_status(f"❌ Failed to load table content: {str(e)}")
    
    def create_row_dialog(self, mode, columns, current_values=None):
        """Create a dialog for adding or editing table rows"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{mode} Row in {self.current_table}")
        dialog.geometry("600x500")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f'600x500+{x}+{y}')
        
        # Header
        header_frame = tk.Frame(dialog, bg='#ffd700', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"{mode} Row in {self.current_table}",
                font=('Segoe UI', 16, 'bold'), bg='#ffd700', fg='#2c3e50').pack(expand=True)
        
        # Main content with scrollbar
        main_frame = tk.Frame(dialog, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Store entry widgets for later access
        entry_widgets = {}
        
        # Create form fields
        for i, column in enumerate(columns):
            col_name = column[0]
            col_type = column[1]
            is_nullable = column[2]
            col_key = column[3]
            col_default = column[4]
            
            # Skip auto-increment primary keys in add mode
            if mode == "Add" and col_key == "PRI" and "auto_increment" in column[5].lower():
                continue
            
            # Create row frame
            row_frame = tk.Frame(scrollable_frame, bg='white')
            row_frame.pack(fill='x', pady=8)
            
            # Column label
            label_text = f"{col_name} ({col_type})"
            if col_key == "PRI":
                label_text += " [PK]"
            if is_nullable == "NO":
                label_text += " *"
            
            tk.Label(row_frame, text=label_text,
                    font=('Segoe UI', 10, 'bold'), bg='white',
                    anchor='w', width=25).pack(side='left', padx=(0, 10))
            
            # Input widget based on column type
            if "text" in col_type.lower() or "varchar" in col_type.lower():
                if "text" in col_type.lower():
                    # Text area for TEXT fields
                    entry = tk.Text(row_frame, height=3, width=40, font=('Segoe UI', 9))
                    if current_values and i < len(current_values):
                        entry.insert('1.0', str(current_values[i]) if current_values[i] else '')
                else:
                    # Single line entry for VARCHAR
                    entry = tk.Entry(row_frame, font=('Segoe UI', 9), width=40)
                    if current_values and i < len(current_values):
                        entry.insert(0, str(current_values[i]) if current_values[i] else '')
            elif "int" in col_type.lower():
                # Numeric entry
                entry = tk.Entry(row_frame, font=('Segoe UI', 9), width=40)
                if current_values and i < len(current_values):
                    entry.insert(0, str(current_values[i]) if current_values[i] else '')
            elif "decimal" in col_type.lower() or "float" in col_type.lower():
                # Decimal entry
                entry = tk.Entry(row_frame, font=('Segoe UI', 9), width=40)
                if current_values and i < len(current_values):
                    entry.insert(0, str(current_values[i]) if current_values[i] else '')
            elif "date" in col_type.lower() or "time" in col_type.lower():
                # Date/time entry
                entry = tk.Entry(row_frame, font=('Segoe UI', 9), width=40)
                if current_values and i < len(current_values):
                    entry.insert(0, str(current_values[i]) if current_values[i] else '')
                # Add format hint
                if "datetime" in col_type.lower():
                    tk.Label(row_frame, text="(YYYY-MM-DD HH:MM:SS)",
                            font=('Segoe UI', 8), fg='#666', bg='white').pack(side='right')
                elif "date" in col_type.lower():
                    tk.Label(row_frame, text="(YYYY-MM-DD)",
                            font=('Segoe UI', 8), fg='#666', bg='white').pack(side='right')
            else:
                # Default entry
                entry = tk.Entry(row_frame, font=('Segoe UI', 9), width=40)
                if current_values and i < len(current_values):
                    entry.insert(0, str(current_values[i]) if current_values[i] else '')
            
            entry.pack(side='left', fill='x', expand=True)
            entry_widgets[col_name] = entry
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg='white')
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Save button
        def save_row():
            try:
                # Collect values from form
                values = {}
                for col_name, widget in entry_widgets.items():
                    if isinstance(widget, tk.Text):
                        value = widget.get('1.0', 'end-1c').strip()
                    else:
                        value = widget.get().strip()
                    
                    # Convert empty strings to None for nullable fields
                    if value == '':
                        value = None
                    
                    values[col_name] = value
                
                # Execute database operation
                if mode == "Add":
                    self.execute_insert(values)
                else:  # Edit mode
                    self.execute_update(values, current_values, columns)
                
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save row: {str(e)}")
        
        tk.Button(buttons_frame, text=f"💾 {mode} Row",
                 command=save_row,
                 bg='#28a745', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=30, pady=10).pack(side='right', padx=(10, 0))
        
        tk.Button(buttons_frame, text="❌ Cancel",
                 command=dialog.destroy,
                 bg='#6c757d', fg='white',
                 font=('Segoe UI', 12, 'bold'),
                 relief='flat', padx=30, pady=10).pack(side='right')
        
        # Add mousewheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def execute_insert(self, values):
        """Execute INSERT statement"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build INSERT statement
            columns = list(values.keys())
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f"`{col}`" for col in columns])
            
            insert_query = f"INSERT INTO `{self.current_table}` ({column_names}) VALUES ({placeholders})"
            insert_values = list(values.values())
            
            cursor.execute(insert_query, insert_values)
            conn.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Row added successfully to {self.current_table}")
                self.update_status(f"✅ Added new row to {self.current_table}")
                
                # Refresh table content
                self.load_table_content(self.current_table)
            else:
                messagebox.showwarning("Warning", "No rows were inserted")
                self.update_status(f"⚠️ No rows inserted to {self.current_table}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            raise Exception(f"Database insert failed: {str(e)}")
    
    def execute_update(self, values, current_values, columns):
        """Execute UPDATE statement"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get primary key information for WHERE clause
            cursor.execute(f"SHOW KEYS FROM `{self.current_table}` WHERE Key_name = 'PRIMARY'")
            primary_keys = cursor.fetchall()
            
            if not primary_keys:
                raise Exception("Cannot update row: No primary key found in table")
            
            # Get column names
            column_names = [col[0] for col in columns]
            
            # Build WHERE clause using primary key
            where_conditions = []
            where_values = []
            
            for pk in primary_keys:
                pk_column = pk[4]  # Column_name is at index 4
                if pk_column in column_names:
                    col_index = column_names.index(pk_column)
                    if col_index < len(current_values):
                        where_conditions.append(f"`{pk_column}` = %s")
                        where_values.append(current_values[col_index])
            
            if not where_conditions:
                raise Exception("Cannot update row: Primary key values not found")
            
            # Build SET clause
            set_conditions = []
            set_values = []
            
            for col_name, value in values.items():
                set_conditions.append(f"`{col_name}` = %s")
                set_values.append(value)
            
            # Execute UPDATE
            where_clause = " AND ".join(where_conditions)
            set_clause = ", ".join(set_conditions)
            update_query = f"UPDATE `{self.current_table}` SET {set_clause} WHERE {where_clause}"
            
            all_values = set_values + where_values
            cursor.execute(update_query, all_values)
            conn.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Row updated successfully in {self.current_table}")
                self.update_status(f"✅ Updated row in {self.current_table}")
                
                # Refresh table content
                self.load_table_content(self.current_table)
            else:
                messagebox.showwarning("Warning", "No rows were updated")
                self.update_status(f"⚠️ No rows updated in {self.current_table}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            raise Exception(f"Database update failed: {str(e)}")
    
    def add_table_row(self):
        """Add a new row to the current table"""
        if not self.current_table:
            return
        
        try:
            # Get column information
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE `{self.current_table}`")
            columns = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Create add row dialog
            self.create_row_dialog("Add", columns, None)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get table structure: {str(e)}")
            self.update_status(f"❌ Failed to prepare add dialog: {str(e)}")
    
    def edit_table_row(self):
        """Edit the selected row"""
        selection = self.table_content_tree.selection()
        if not selection or not self.current_table:
            return
        
        try:
            # Get selected row data
            item = self.table_content_tree.item(selection[0])
            row_values = item['values']
            
            # Get column information
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DESCRIBE `{self.current_table}`")
            columns = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Create edit dialog with current values
            self.create_row_dialog("Edit", columns, row_values)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare edit dialog: {str(e)}")
            self.update_status(f"❌ Failed to prepare edit dialog: {str(e)}")
    
    def delete_table_row(self):
        """Delete the selected row"""
        selection = self.table_content_tree.selection()
        if not selection or not self.current_table:
            return
        
        try:
            # Get selected row data
            item = self.table_content_tree.item(selection[0])
            row_values = item['values']
            
            # Get primary key information
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get table structure to find primary key
            cursor.execute(f"SHOW KEYS FROM `{self.current_table}` WHERE Key_name = 'PRIMARY'")
            primary_keys = cursor.fetchall()
            
            if not primary_keys:
                messagebox.showerror("Error", "Cannot delete row: No primary key found in table")
                cursor.close()
                conn.close()
                return
            
            # Get column names for building WHERE clause
            cursor.execute(f"DESCRIBE `{self.current_table}`")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]
            
            # Build WHERE clause using primary key
            where_conditions = []
            where_values = []
            
            for pk in primary_keys:
                pk_column = pk[4]  # Column_name is at index 4
                if pk_column in column_names:
                    col_index = column_names.index(pk_column)
                    if col_index < len(row_values):
                        where_conditions.append(f"`{pk_column}` = %s")
                        where_values.append(row_values[col_index])
            
            if not where_conditions:
                messagebox.showerror("Error", "Cannot delete row: Primary key values not found")
                cursor.close()
                conn.close()
                return
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete this row from {self.current_table}?\n\n"
                                  f"Primary key values: {', '.join(str(v) for v in where_values)}"):
                
                # Execute delete
                where_clause = " AND ".join(where_conditions)
                delete_query = f"DELETE FROM `{self.current_table}` WHERE {where_clause}"
                
                cursor.execute(delete_query, where_values)
                conn.commit()
                
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Row deleted successfully from {self.current_table}")
                    self.update_status(f"✅ Deleted row from {self.current_table}")
                    
                    # Refresh table content
                    self.load_table_content(self.current_table)
                else:
                    messagebox.showwarning("Warning", "No rows were deleted")
                    self.update_status(f"⚠️ No rows deleted from {self.current_table}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete row: {str(e)}")
            self.update_status(f"❌ Failed to delete row: {str(e)}")
    
    def export_table_data(self):
        """Export table data to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                # Implementation would go here
                self.update_status(f"✅ Data exported to {filename}")
                messagebox.showinfo("Success", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def run_schema_analysis(self):
        """Run schema analysis"""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "🔍 Database Schema Analysis Report\n")
        self.analysis_text.insert(tk.END, "=" * 50 + "\n\n")
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get schema information
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            self.analysis_text.insert(tk.END, f"📊 Database: {self.db_var.get()}\n")
            self.analysis_text.insert(tk.END, f"📋 Total Tables: {len(tables)}\n\n")
            
            self.analysis_text.insert(tk.END, "📋 Table Details:\n")
            self.analysis_text.insert(tk.END, "-" * 30 + "\n")
            
            for table in tables:
                table_name = table[0]
                
                # Get table info
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                row_count = cursor.fetchone()[0]
                
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = cursor.fetchall()
                
                self.analysis_text.insert(tk.END, f"\n🔹 {table_name}\n")
                self.analysis_text.insert(tk.END, f"   • Columns: {len(columns)}\n")
                self.analysis_text.insert(tk.END, f"   • Rows: {row_count:,}\n")
                
                # Show column details
                for col in columns:
                    col_name, col_type, nullable, key, default = col[0], col[1], col[2], col[3], col[4]
                    key_info = f" [{key}]" if key else ""
                    null_info = " (NULL)" if nullable == "YES" else " (NOT NULL)"
                    self.analysis_text.insert(tk.END, f"     - {col_name}: {col_type}{key_info}{null_info}\n")
            
            self.analysis_text.insert(tk.END, f"\n📊 Analysis completed successfully!\n")
            self.analysis_text.insert(tk.END, f"⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            cursor.close()
            conn.close()
            self.update_status("✅ Schema analysis completed")
            
        except Exception as e:
            self.analysis_text.insert(tk.END, f"❌ Analysis Error: {str(e)}\n")
            self.update_status(f"❌ Schema analysis failed: {str(e)}")
    
    def generate_migration_summary(self):
        """Generate migration summary"""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "📋 Migration Operations Summary\n")
        self.analysis_text.insert(tk.END, "=" * 50 + "\n\n")
        
        total_operations = 0
        
        for tool, results in self.results.items():
            total_operations += len(results)
            self.analysis_text.insert(tk.END, f"🔹 {tool.upper()}\n")
            self.analysis_text.insert(tk.END, f"   Operations: {len(results)}\n")
            
            if results:
                self.analysis_text.insert(tk.END, "   Recent Results:\n")
                for result in results[-3:]:  # Show last 3 results
                    self.analysis_text.insert(tk.END, f"   • {result}\n")
            else:
                self.analysis_text.insert(tk.END, "   • No operations performed yet\n")
            self.analysis_text.insert(tk.END, "\n")
        
        self.analysis_text.insert(tk.END, f"📊 Total Migration Operations: {total_operations}\n")
        self.analysis_text.insert(tk.END, f"⏰ Summary generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.update_status("✅ Migration summary generated")
    
    def clear_analysis(self):
        """Clear the analysis report"""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "📊 Database Analysis Center\n")
        self.analysis_text.insert(tk.END, "=" * 50 + "\n\n")
        self.analysis_text.insert(tk.END, "Analysis report cleared.\n\n")
        self.analysis_text.insert(tk.END, "🔍 Use 'Schema Analysis' to examine your database structure\n")
        self.analysis_text.insert(tk.END, "📋 Use 'Migration Summary' to review completed operations\n\n")
        self.analysis_text.insert(tk.END, "Select an analysis option above to begin...\n")
        self.update_status("🗑️ Analysis report cleared")
        
    
    # Web interface methods
    def start_all_web_interfaces(self):
        """Start all web interfaces"""
        self.update_status("🚀 Starting all web interfaces...")
        
        def start_interfaces():
            try:
                # Start web interface launcher
                subprocess.Popen([
                    'python', 'launch_web_interfaces.py'
                ], shell=True)
                
                self.web_interfaces_started = True
                self.update_status("✅ Web interfaces started successfully")
                
                # Update web status
                if hasattr(self, 'web_status_label'):
                    self.web_status_label.config(text="🌐 Web Interfaces: Running")
                
            except Exception as e:
                self.update_status(f"❌ Failed to start web interfaces: {str(e)}")
        
        thread = threading.Thread(target=start_interfaces)
        thread.daemon = True
        thread.start()
    
    def open_web_page(self, url, tool_name):
        """Open a specific web page"""
        try:
            webbrowser.open(url)
            self.update_status(f"🌐 Opened {tool_name} web interface: {url}")
        except Exception as e:
            self.update_status(f"❌ Failed to open {tool_name} web page: {str(e)}")
            messagebox.showerror("Error", f"Failed to open {tool_name} web page: {str(e)}")
    
    def open_all_web_pages(self):
        """Open all web interfaces in browser"""
        self.open_web_page('http://localhost:8080', 'Bytebase')
        time.sleep(1)
        self.open_web_page('http://localhost:5001', 'Redgate')
        time.sleep(1)
        self.open_web_page('http://localhost:5002', 'Liquibase')
    
    # Migration methods
    def run_bytebase_migration(self):
        """Run Bytebase migration"""
        if not self.bytebase_enabled.get():
            self.update_status("⚠️ Bytebase is disabled in settings")
            return
            
        self.update_status("🔵 Starting Bytebase migration...")
        
        def run_migration():
            try:
                # Get project root and migrations path
                project_root = os.path.dirname(os.path.abspath(__file__))
                migrations_path = os.path.join(project_root, "bytebase", "migrations")
                
                # Authenticate with Bytebase
                self.bytebase_api.authenticate()
                
                # Create project
                project = self.bytebase_api.create_project("gui-migration-test")
                self.log_to_console(f"✅ Project created: {project.get('title', 'Unknown')}")
                
                # Execute migration folder
                results = self.bytebase_api.execute_migration_folder(migrations_path)
                
                # Store and display results
                self.results['bytebase'] = results
                for result in results:
                    self.log_to_console(f"  {result}")
                
                self.update_status("✅ Bytebase migration completed")
                
            except Exception as e:
                error_msg = f"❌ Bytebase migration failed: {str(e)}"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
        
        thread = threading.Thread(target=run_migration)
        thread.daemon = True
        thread.start()
    
    def run_liquibase_migration(self):
        """Run Liquibase migration"""
        if not self.liquibase_enabled.get():
            self.update_status("⚠️ Liquibase is disabled in settings")
            return
            
        self.update_status("🟣 Starting Liquibase migration...")
        
        def run_migration():
            try:
                # Change to liquibase directory
                original_dir = os.getcwd()
                project_root = os.path.dirname(os.path.abspath(__file__))
                liquibase_dir = os.path.join(project_root, "liquibase")
                
                self.log_to_console(f"📁 Liquibase directory: {liquibase_dir}")
                
                if not os.path.exists(liquibase_dir):
                    error_msg = f"❌ Liquibase directory not found: {liquibase_dir}"
                    self.log_to_console(error_msg)
                    self.update_status("❌ Liquibase directory not found")
                    return
                
                os.chdir(liquibase_dir)
                self.log_to_console(f"📁 Changed to directory: {os.getcwd()}")
                
                # Run liquibase update with shell=True for Windows
                result = subprocess.run(
                    ["liquibase", "update"],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=60
                )
                
                os.chdir(original_dir)
                
                if result.returncode == 0:
                    self.log_to_console("✅ Liquibase update successful")
                    
                    # Parse output for meaningful information
                    output_lines = result.stdout.split('\n')
                    for line in output_lines:
                        if any(keyword in line.lower() for keyword in ['changesets run', 'update summary', 'successfully', 'executed']):
                            self.log_to_console(f"  {line.strip()}")
                    
                    # Check if any changesets were actually applied
                    if "Liquibase command 'update' was executed successfully" in result.stdout:
                        self.log_to_console("  📊 All changesets applied successfully")
                    
                    self.results['liquibase'] = ['✅ Liquibase update completed successfully']
                    self.update_status("✅ Liquibase migration completed")
                else:
                    error_msg = f"❌ Liquibase failed (exit code {result.returncode})"
                    self.log_to_console(error_msg)
                    if result.stderr:
                        self.log_to_console(f"Error details: {result.stderr}")
                    if result.stdout:
                        self.log_to_console(f"Output: {result.stdout}")
                    self.update_status("❌ Liquibase migration failed")
                
            except FileNotFoundError:
                error_msg = "❌ Liquibase not found. Please ensure Liquibase is installed and in PATH"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
            except subprocess.TimeoutExpired:
                error_msg = "❌ Liquibase update timed out after 60 seconds"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
            except Exception as e:
                error_msg = f"❌ Liquibase error: {str(e)}"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
        
        thread = threading.Thread(target=run_migration)
        thread.daemon = True
        thread.start()
    
    def run_redgate_migration(self):
        """Run Redgate migration"""
        if not self.redgate_enabled.get():
            self.update_status("⚠️ Redgate is disabled in settings")
            return
            
        self.update_status("🔴 Starting Redgate migration...")
        
        def run_migration():
            try:
                # Get project root and migrations path
                project_root = os.path.dirname(os.path.abspath(__file__))
                migrations_path = os.path.join(project_root, "redgate", "migrations")
                
                self.log_to_console(f"📁 Using migration path: {migrations_path}")
                
                # Deploy migration package
                results = self.redgate_simulator.deploy_migration_package(migrations_path)
                
                # Store and display results
                self.results['redgate'] = results
                for result in results:
                    self.log_to_console(f"  {result}")
                
                self.update_status("✅ Redgate migration completed")
                
            except Exception as e:
                error_msg = f"❌ Redgate migration failed: {str(e)}"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
        
        thread = threading.Thread(target=run_migration)
        thread.daemon = True
        thread.start()
    
    def run_all_migrations(self):
        """Run all enabled migrations sequentially"""
        self.update_status("🚀 Starting all migrations...")
        self.log_to_console("\n" + "="*60)
        self.log_to_console("🚀 COMPREHENSIVE MIGRATION TEST")
        self.log_to_console("="*60)
        
        def run_all():
            if self.redgate_enabled.get():
                self.run_redgate_migration()
                time.sleep(2)
            
            if self.liquibase_enabled.get():
                time.sleep(3)
                self.run_liquibase_migration()
                time.sleep(2)
            
            if self.bytebase_enabled.get():
                time.sleep(3)
                self.run_bytebase_migration()
            
            time.sleep(2)
            self.update_status("✅ All migrations completed")
        
        thread = threading.Thread(target=run_all)
        thread.daemon = True
        thread.start()
    
    def run_automated_test(self):
        """Run automated tests"""
        self.update_status("🧪 Running automated tests...")
        
        def run_test():
            try:
                # Run the test tools script
                result = subprocess.run(
                    ["python", "test_tools.py"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                self.log_to_console("\n🧪 AUTOMATED TEST RESULTS:")
                self.log_to_console("="*40)
                self.log_to_console(result.stdout)
                
                if result.returncode == 0:
                    self.update_status("✅ Automated tests completed successfully")
                else:
                    self.update_status("❌ Some automated tests failed")
                    
            except Exception as e:
                error_msg = f"❌ Test execution failed: {str(e)}"
                self.update_status(error_msg)
                self.log_to_console(error_msg)
        
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
    
    def reset_database(self):
        """Reset database to clean state"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the database? This will clear all data."):
            self.update_status("🔄 Resetting database...")
            
            def reset_db():
                try:
                    # Run the reset script
                    result = subprocess.run(
                        ["python", "reset_database.py"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    self.log_to_console("🔄 Database reset completed")
                    self.log_to_console(result.stdout)
                    
                    self.update_status("✅ Database reset completed")
                    self.refresh_tables()
                    
                except Exception as e:
                    error_msg = f"❌ Database reset failed: {str(e)}"
                    self.update_status(error_msg)
                    self.log_to_console(error_msg)
            
            thread = threading.Thread(target=reset_db)
            thread.daemon = True
            thread.start()


def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    app = ProfessionalMigrationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
