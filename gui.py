#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Database Migration POC GUI
Modern black, white, and yellow themed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import mysql.connector
import os
from dotenv import load_dotenv
import subprocess
import threading
import time
from datetime import datetime

load_dotenv()

class ProfessionalMigrationGUI:
    def __init__(self, root):
        self.root = root
        self.db_config = {
            'host': os.getenv("DB_HOST", "localhost"),
            'port': int(os.getenv("DB_PORT", 3306)),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASS"),
            'database': os.getenv("DB_NAME")
        }
        
        # Professional color scheme - Black, White, Yellow
        self.colors = {
            'primary_bg': '#1a1a1a',      # Dark black
            'secondary_bg': '#2d2d2d',    # Lighter black
            'accent': '#ffd700',          # Golden yellow
            'text_light': '#ffffff',      # White text
            'text_dark': '#000000',       # Black text
            'success': '#4CAF50',         # Green
            'error': '#f44336',           # Red
            'warning': '#ff9800',         # Orange
            'border': '#404040'           # Gray border
        }
        
        self.setup_styles()
        self.setup_main_window()
        self.create_interface()
    
    def add_mousewheel_support(self, canvas):
        """Add mouse wheel scrolling support to a canvas"""
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel events when entering/leaving the canvas
        canvas.bind('<Enter>', bind_mousewheel)
        canvas.bind('<Leave>', unbind_mousewheel)
    
    def setup_styles(self):
        """Configure professional styling"""
        style = ttk.Style()
        
        # Configure notebook (tabs)
        style.theme_use('clam')
        
        style.configure('Professional.TNotebook', 
                       background=self.colors['primary_bg'],
                       borderwidth=0)
        
        style.configure('Professional.TNotebook.Tab',
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_light'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Professional.TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['accent'])],
                 foreground=[('selected', self.colors['text_dark']),
                           ('active', self.colors['text_dark'])])
        
        # Configure frames
        style.configure('Professional.TFrame',
                       background=self.colors['primary_bg'])
        
        style.configure('Card.TFrame',
                       background=self.colors['secondary_bg'],
                       relief='flat',
                       borderwidth=1)
        
        # Configure labels
        style.configure('Heading.TLabel',
                       background=self.colors['primary_bg'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Professional.TLabel',
                       background=self.colors['primary_bg'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10))
        
        style.configure('Card.TLabel',
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10))
        
        # Configure buttons
        style.configure('Professional.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text_dark'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 10])
        
        style.map('Professional.TButton',
                 background=[('active', '#ffed4e'),
                           ('pressed', '#e6c200')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 10])
        
        style.configure('Danger.TButton',
                       background=self.colors['error'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[15, 10])
    
    def setup_main_window(self):
        """Configure main window"""
        self.root.title("Database Migration POC - Professional Interface")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['primary_bg'])
        
        # Add window control buttons
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure window has proper title bar controls (minimize, maximize, close)
        self.root.attributes('-topmost', False)  # Make sure window is not always on top
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1000, 600)
        
        # Enable window controls (minimize, maximize, close)
        self.root.resizable(True, True)
        
        # Ensure window has standard decorations (title bar with controls)
        self.root.overrideredirect(False)
        
        # Make sure window decorations are enabled
        self.root.overrideredirect(False)
    
    def create_interface(self):
        """Create the main interface"""
        # Status bar (create first so status_label exists)
        self.create_status_bar()
        
        # Header
        self.create_header()
        
        # Main content area
        self.create_main_content()
    
    def create_header(self):
        """Create professional header"""
        header_frame = tk.Frame(self.root, bg=self.colors['secondary_bg'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="Database Migration POC",
                              bg=self.colors['secondary_bg'],
                              fg=self.colors['accent'],
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(side='left', padx=20, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Liquibase vs Bytebase vs Redgate Comparison",
                                 bg=self.colors['secondary_bg'],
                                 fg=self.colors['text_light'],
                                 font=('Segoe UI', 12))
        subtitle_label.pack(side='left', padx=(0, 20), pady=20)
        
        # Connection status
        self.connection_status = tk.Label(header_frame,
                                         text="DISCONNECTED",
                                         bg=self.colors['secondary_bg'],
                                         fg=self.colors['error'],
                                         font=('Segoe UI', 10, 'bold'))
        self.connection_status.pack(side='right', padx=20, pady=20)
        
        # Test connection
        self.test_connection()
    
    def create_main_content(self):
        """Create main tabbed interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, style='Professional.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Professional.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_migrations_tab()
        self.create_console_tab()
        self.create_data_tab()
        self.create_analysis_tab()
        self.create_settings_tab()
    
    def create_migrations_tab(self):
        """Create professional migrations tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="Migrations")
        
        # Create scrollable frame
        canvas = tk.Canvas(tab_frame, bg=self.colors['primary_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Professional.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling support
        self.add_mousewheel_support(canvas)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Header
        header_label = ttk.Label(scrollable_frame, 
                                text="Migration Tool Comparison",
                                style='Heading.TLabel')
        header_label.pack(pady=(20, 30))
        
        # Migration cards container
        cards_frame = ttk.Frame(scrollable_frame, style='Professional.TFrame')
        cards_frame.pack(fill='x', padx=40)
        
        # Bytebase card
        self.create_migration_card(cards_frame, 
                                  "Bytebase", 
                                  "Incremental SQL Migrations",
                                  "5 files - Git-like incremental changes\nModern UI-driven workflow",
                                  self.colors['accent'],
                                  lambda: self.run_migration('bytebase'))
        
        # Liquibase card  
        self.create_migration_card(cards_frame,
                                  "Liquibase",
                                  "Enterprise XML Migrations", 
                                  "3 files - Enterprise batch releases\nDatabase-agnostic changesets",
                                  '#6a5acd',
                                  lambda: self.run_migration('liquibase'))
        
        # Redgate card
        self.create_migration_card(cards_frame,
                                  "Redgate", 
                                  "Traditional SQL Scripts",
                                  "2 files - DBA comprehensive scripts\nPure SQL approach",
                                  '#ff6b6b',
                                  lambda: self.run_migration('redgate'))
        
        # Action buttons
        actions_frame = ttk.Frame(scrollable_frame, style='Professional.TFrame')
        actions_frame.pack(fill='x', padx=40, pady=30)
        
        ttk.Button(actions_frame, 
                  text="Run All Tests (Automated)",
                  style='Professional.TButton',
                  command=self.run_automated_test).pack(side='left', padx=(0, 10))
        
        ttk.Button(actions_frame,
                  text="Reset Database", 
                  style='Danger.TButton',
                  command=self.reset_database).pack(side='left', padx=10)
        
        ttk.Button(actions_frame,
                  text="Quick Analysis",
                  style='Success.TButton', 
                  command=self.quick_analysis).pack(side='right')
    
    def create_migration_card(self, parent, title, subtitle, description, color, command):
        """Create a professional migration card"""
        # Card frame
        card = tk.Frame(parent, bg=self.colors['secondary_bg'], 
                       relief='flat', bd=1, highlightbackground=self.colors['border'],
                       highlightthickness=1)
        card.pack(fill='x', pady=10)
        
        # Card content
        content_frame = tk.Frame(card, bg=self.colors['secondary_bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with colored indicator
        title_frame = tk.Frame(content_frame, bg=self.colors['secondary_bg'])
        title_frame.pack(anchor='w', fill='x')
        
        # Colored circle indicator
        indicator_label = tk.Label(title_frame, text="●",
                                  bg=self.colors['secondary_bg'],
                                  fg=color, font=('Segoe UI', 20, 'bold'))
        indicator_label.pack(side='left', padx=(0, 10))
        
        # Title text
        title_label = tk.Label(title_frame, text=title,
                              bg=self.colors['secondary_bg'],
                              fg=color, font=('Segoe UI', 16, 'bold'))
        title_label.pack(side='left')
        
        # Subtitle
        subtitle_label = tk.Label(content_frame, text=subtitle,
                                 bg=self.colors['secondary_bg'],
                                 fg=self.colors['text_light'], 
                                 font=('Segoe UI', 12, 'bold'))
        subtitle_label.pack(anchor='w', pady=(5, 10))
        
        # Description
        desc_label = tk.Label(content_frame, text=description,
                             bg=self.colors['secondary_bg'],
                             fg=self.colors['text_light'],
                             font=('Segoe UI', 10),
                             justify='left')
        desc_label.pack(anchor='w', pady=(0, 15))
        
        # Button
        button_frame = tk.Frame(content_frame, bg=self.colors['secondary_bg'])
        button_frame.pack(fill='x')
        
        run_button = tk.Button(button_frame, text=f"Run {title} Migration",
                              bg=color, fg=self.colors['text_dark'],
                              font=('Segoe UI', 10, 'bold'),
                              border=0, padx=20, pady=8,
                              command=command)
        run_button.pack(side='left')
    
    def create_console_tab(self):
        """Create console/output log tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="Console")
        
        # Header
        header_label = ttk.Label(tab_frame, 
                                text="Console Output & Logs",
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
        # Console controls - at the top, always visible
        controls_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        controls_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        ttk.Button(controls_frame, text="Clear Console",
                  style='Danger.TButton',
                  command=self.clear_console).pack(side='left', padx=(0, 10))
        
        ttk.Button(controls_frame, text="Save Log",
                  style='Professional.TButton',
                  command=self.save_log).pack(side='left', padx=10)
        
        # Results area
        results_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     bg=self.colors['secondary_bg'],
                                                     fg=self.colors['text_light'],
                                                     font=('Consolas', 10),
                                                     insertbackground=self.colors['accent'])
        self.results_text.pack(fill='both', expand=True)
        
        # Add mouse wheel scrolling support to console
        def on_console_mousewheel(event):
            self.results_text.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_console_mousewheel(event):
            self.results_text.bind_all("<MouseWheel>", on_console_mousewheel)
        
        def unbind_console_mousewheel(event):
            self.results_text.unbind_all("<MouseWheel>")
        
        self.results_text.bind('<Enter>', bind_console_mousewheel)
        self.results_text.bind('<Leave>', unbind_console_mousewheel)
        
        # Initial message
        self.results_text.insert('1.0', "Ready to run migration comparisons...\n\n")
        self.results_text.insert('end', "Click 'Run All Tests' in the Migrations tab to begin automated testing.\n")
        self.results_text.insert('end', "Or run individual migrations to see detailed output.\n\n")
        self.results_text.insert('end', "Results will appear here with execution times, errors, and analysis.")
    
    def create_data_tab(self):
        """Create data viewing tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="Data View")
        
        # Header
        header_label = ttk.Label(tab_frame,
                                text="Database Tables and Data",
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
        # Controls frame
        controls_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Table selector
        ttk.Label(controls_frame, text="Select Table:",
                 style='Professional.TLabel').pack(side='left', padx=(0, 10))
        
        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(controls_frame, textvariable=self.table_var,
                                       state='readonly', width=30)
        self.table_combo.pack(side='left', padx=(0, 10))
        
        ttk.Button(controls_frame, text="Refresh Tables",
                  style='Professional.TButton',
                  command=self.refresh_tables).pack(side='left', padx=10)
        
        ttk.Button(controls_frame, text="Load Data", 
                  style='Success.TButton',
                  command=self.load_table_data).pack(side='left', padx=10)
        
        ttk.Button(controls_frame, text="Add Row",
                  style='Professional.TButton',
                  command=self.add_table_row).pack(side='left', padx=10)
        
        ttk.Button(controls_frame, text="Edit Row",
                  style='Professional.TButton',
                  command=self.edit_table_row).pack(side='left', padx=10)
        
        ttk.Button(controls_frame, text="Delete Row",
                  style='Danger.TButton',
                  command=self.delete_table_row).pack(side='left', padx=10)
        
        # Data display
        data_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        data_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for data
        self.data_tree = ttk.Treeview(data_frame)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient='vertical', command=self.data_tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient='horizontal', command=self.data_tree.xview)
        
        self.data_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and treeview
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        self.data_tree.pack(fill='both', expand=True)
        
        # Add mouse wheel scrolling support to data tree
        def on_tree_mousewheel(event):
            self.data_tree.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_tree_mousewheel(event):
            self.data_tree.bind_all("<MouseWheel>", on_tree_mousewheel)
        
        def unbind_tree_mousewheel(event):
            self.data_tree.unbind_all("<MouseWheel>")
        
        self.data_tree.bind('<Enter>', bind_tree_mousewheel)
        self.data_tree.bind('<Leave>', unbind_tree_mousewheel)
        
        # Initial table refresh
        self.refresh_tables()
    
    def create_analysis_tab(self):
        """Create analysis and insights tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="Analysis")
        
        # Header
        header_label = ttk.Label(tab_frame,
                                text="Database Schema Analysis & Performance Insights", 
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
        # Control buttons - at the top, always visible
        controls_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        controls_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        ttk.Button(controls_frame, text="Schema Analysis",
                  style='Professional.TButton',
                  command=self.analyze_database).pack(side='left', padx=(0, 10))
        
        ttk.Button(controls_frame, text="Migration Tools Info",
                  style='Success.TButton', 
                  command=self.show_migration_tools_info).pack(side='left', padx=10)
        
        # Analysis content
        analysis_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        analysis_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Analysis text area
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame,
                                                      bg=self.colors['secondary_bg'],
                                                      fg=self.colors['text_light'],
                                                      font=('Segoe UI', 10),
                                                      insertbackground=self.colors['accent'])
        self.analysis_text.pack(fill='both', expand=True)
        
        # Add mouse wheel scrolling support to analysis text
        def on_analysis_mousewheel(event):
            self.analysis_text.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_analysis_mousewheel(event):
            self.analysis_text.bind_all("<MouseWheel>", on_analysis_mousewheel)
        
        def unbind_analysis_mousewheel(event):
            self.analysis_text.unbind_all("<MouseWheel>")
        
        self.analysis_text.bind('<Enter>', bind_analysis_mousewheel)
        self.analysis_text.bind('<Leave>', unbind_analysis_mousewheel)
        
        # Initial content
        self.analysis_text.insert('1.0', "Database Schema Analysis & Migration Tools Information\n")
        self.analysis_text.insert('end', "="*65 + "\n\n")
        self.analysis_text.insert('end', "This tab provides detailed analysis and information:\n\n")
        self.analysis_text.insert('end', "Schema Analysis - Examine your database structure, tables, and relationships\n")
        self.analysis_text.insert('end', "   • Table details and record counts\n")
        self.analysis_text.insert('end', "   • Column information and data types\n")
        self.analysis_text.insert('end', "   • Database optimization recommendations\n\n")
        self.analysis_text.insert('end', "Migration Tools Info - Comprehensive comparison guide\n")
        self.analysis_text.insert('end', "   • Detailed comparison of Redgate, Bytebase, and Liquibase\n")
        self.analysis_text.insert('end', "   • Pros and cons of each approach\n")
        self.analysis_text.insert('end', "   • Testing recommendations and decision factors\n")
        self.analysis_text.insert('end', "   • File structures and implementation details\n\n")
        self.analysis_text.insert('end', "Select an option above to begin your analysis...\n")
    
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="Settings")
        
        # Header
        header_label = ttk.Label(tab_frame,
                                text="Configuration & Settings",
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
        # Settings content
        settings_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        settings_frame.pack(fill='both', padx=40, pady=20)
        
        # Database connection settings
        db_frame = ttk.LabelFrame(settings_frame, text="Database Connection")
        db_frame.pack(fill='x', pady=(0, 20))
        
        # Connection info
        info_text = f"""
Host: {self.db_config['host']}
Port: {self.db_config['port']}
Database: {self.db_config['database']}
User: {self.db_config['user']}
        """
        
        tk.Label(db_frame, text=info_text.strip(),
                bg=self.colors['primary_bg'], fg=self.colors['text_light'],
                font=('Consolas', 10), justify='left').pack(pady=10, padx=10, anchor='w')
        
        # Test connection button
        ttk.Button(db_frame, text="Test Connection",
                  style='Professional.TButton',
                  command=self.test_connection).pack(pady=10)
        
        # Migration paths
        paths_frame = ttk.LabelFrame(settings_frame, text="Migration Paths")
        paths_frame.pack(fill='x', pady=(0, 20))
        
        paths_info = """
Bytebase: bytebase/migrations/ (5 SQL files)
Liquibase: liquibase/changelog/ (3 XML files) 
Redgate: redgate/migrations/ (2 SQL files)
        """
        
        tk.Label(paths_frame, text=paths_info.strip(),
                bg=self.colors['primary_bg'], fg=self.colors['text_light'],
                font=('Segoe UI', 10), justify='left').pack(pady=10, padx=10, anchor='w')
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['secondary_bg'], height=30)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, 
                                    text="Ready",
                                    bg=self.colors['secondary_bg'],
                                    fg=self.colors['text_light'],
                                    font=('Segoe UI', 9))
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Time label
        self.time_label = tk.Label(self.status_bar,
                                  text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  bg=self.colors['secondary_bg'],
                                  fg=self.colors['text_light'],
                                  font=('Segoe UI', 9))
        self.time_label.pack(side='right', padx=10, pady=5)
        
        # Update time periodically
        self.update_time()
    
    def update_time(self):
        """Update time display"""
        self.time_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def get_connection(self):
        """Get database connection"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Connection failed: {err}")
            return None
    
    def test_connection(self):
        """Test database connection"""
        conn = self.get_connection()
        if conn:
            conn.close()
            self.connection_status.config(text="CONNECTED", fg=self.colors['success'])
            self.update_status("Database connection successful")
        else:
            self.connection_status.config(text="DISCONNECTED", fg=self.colors['error'])
            self.update_status("Database connection failed")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def run_migration(self, tool):
        """Run migration for specific tool"""
        self.update_status(f"Running {tool} migration...")
        
        # Run in separate thread to prevent GUI blocking
        def migrate():
            try:
                start_time = time.time()
                
                if tool == 'liquibase':
                    self.run_liquibase_migration()
                elif tool == 'bytebase':
                    self.run_folder_migration('bytebase/migrations', 'Bytebase')
                elif tool == 'redgate':
                    self.run_folder_migration('redgate/migrations', 'Redgate')
                
                execution_time = time.time() - start_time
                
                self.root.after(0, lambda: self.log_result(f"SUCCESS: {tool.capitalize()} migration completed in {execution_time:.2f}s"))
                self.root.after(0, lambda: self.update_status(f"{tool.capitalize()} migration completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"ERROR: {tool.capitalize()} migration failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status(f"{tool.capitalize()} migration failed"))
        
        threading.Thread(target=migrate, daemon=True).start()
    
    def run_liquibase_migration(self):
        """Run Liquibase migration"""
        liquibase_cmd = "liquibase.bat" if os.name == 'nt' else "liquibase"
        
        result = subprocess.run(
            [liquibase_cmd, "--defaultsFile=liquibase.properties", "update"],
            cwd="liquibase",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            raise Exception(result.stderr)
    
    def run_folder_migration(self, folder_path, tool_name):
        """Run SQL folder migration"""
        conn = self.get_connection()
        if not conn:
            raise Exception("Database connection failed")
        
        cursor = conn.cursor()
        
        try:
            files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
            
            for filename in files:
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "r", encoding='utf-8') as f:
                    sql = f.read()
                
                # Handle different delimiters (for stored procedures)
                if "DELIMITER" in sql:
                    # Split by delimiter changes and execute each part
                    parts = sql.split("DELIMITER")
                    current_delimiter = ";"
                    
                    for i, part in enumerate(parts):
                        if i == 0:
                            # First part uses default delimiter
                            statements = [stmt.strip() for stmt in part.split(";") if stmt.strip()]
                            for statement in statements:
                                if statement:
                                    cursor.execute(statement)
                                    # Consume all results to avoid "Unread result found" error
                                    try:
                                        cursor.fetchall()
                                    except:
                                        pass
                        else:
                            # Extract new delimiter and content
                            lines = part.strip().split('\n', 1)
                            if len(lines) >= 2:
                                new_delimiter = lines[0].strip()
                                content = lines[1] if len(lines) > 1 else ""
                                
                                if new_delimiter and content:
                                    if new_delimiter == ";":
                                        # Back to default delimiter
                                        statements = [stmt.strip() for stmt in content.split(";") if stmt.strip()]
                                        for statement in statements:
                                            if statement:
                                                cursor.execute(statement)
                                                # Consume all results
                                                try:
                                                    cursor.fetchall()
                                                except:
                                                    pass
                                    else:
                                        # Custom delimiter (like //)
                                        statements = [stmt.strip() for stmt in content.split(new_delimiter) if stmt.strip()]
                                        for statement in statements:
                                            if statement and not statement.startswith("DELIMITER"):
                                                cursor.execute(statement)
                                                # Consume all results
                                                try:
                                                    cursor.fetchall()
                                                except:
                                                    pass
                else:
                    # Standard SQL without delimiter changes
                    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
                    for statement in statements:
                        if statement:
                            cursor.execute(statement)
                            # Consume all results to avoid "Unread result found" error
                            try:
                                cursor.fetchall()
                            except:
                                pass
                
                conn.commit()
        
        finally:
            cursor.close()
            conn.close()
    
    def run_automated_test(self):
        """Run automated comparison test"""
        self.update_status("Running automated test...")
        self.log_result("AUTOMATED TEST: Starting automated migration tool comparison...\n")
        
        def run_test():
            try:
                # Run the migration tester script
                result = subprocess.run(
                    ["python", "migration_tester.py"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                self.root.after(0, lambda: self.log_result(result.stdout))
                if result.stderr:
                    self.root.after(0, lambda: self.log_result(f"\nErrors:\n{result.stderr}"))
                
                self.root.after(0, lambda: self.update_status("Automated test completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"ERROR: Automated test failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Automated test failed"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def reset_database(self):
        """Reset database"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the database? This will drop all tables and views."):
            self.update_status("Resetting database...")
            
            def reset():
                try:
                    conn = self.get_connection()
                    if not conn:
                        raise Exception("Database connection failed")
                    
                    cursor = conn.cursor()
                    
                    # Disable foreign key checks and autocommit
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                    cursor.execute("SET AUTOCOMMIT = 0")
                    
                    # First, drop all views (must be done before tables due to dependencies)
                    cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
                    views = cursor.fetchall()
                    for (view_name, table_type) in views:
                        try:
                            cursor.execute(f"DROP VIEW IF EXISTS `{view_name}`")
                            print(f"Dropped view: {view_name}")
                        except Exception as e:
                            print(f"Error dropping view {view_name}: {e}")
                    
                    # Then drop all tables
                    cursor.execute("SHOW TABLES")
                    all_objects = cursor.fetchall()
                    tables = [obj[0] for obj in all_objects]
                    
                    # Drop tables in multiple passes to handle foreign key dependencies
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        cursor.execute("SHOW TABLES")
                        remaining_tables = [table[0] for table in cursor.fetchall()]
                        
                        if not remaining_tables:
                            break
                            
                        for table_name in remaining_tables:
                            try:
                                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                                print(f"Dropped table: {table_name}")
                            except Exception as e:
                                print(f"Attempt {attempt+1}: Error dropping table {table_name}: {e}")
                    
                    # Re-enable foreign key checks
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                    cursor.execute("SET AUTOCOMMIT = 1")
                    conn.commit()
                    
                    # Verify database is completely clean
                    cursor.execute("SHOW TABLES")
                    remaining_tables = cursor.fetchall()
                    cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
                    remaining_views = cursor.fetchall()
                    
                    if remaining_tables or remaining_views:
                        raise Exception(f"Database reset incomplete - Tables: {remaining_tables}, Views: {remaining_views}")
                    
                    cursor.close()
                    conn.close()
                    
                    # Add a longer delay to ensure reset is complete
                    import time
                    time.sleep(1.0)
                    
                    self.root.after(0, lambda: self.log_result("DATABASE RESET: Database completely reset - all tables and views removed"))
                    self.root.after(0, lambda: self.update_status("Database reset completed"))
                    self.root.after(0, self.refresh_tables)
                    
                except Exception as e:
                    self.root.after(0, lambda: self.log_result(f"ERROR: Database reset failed: {str(e)}"))
                    self.root.after(0, lambda: self.update_status("Database reset failed"))
            
            threading.Thread(target=reset, daemon=True).start()
    
    def quick_analysis(self):
        """Quick database analysis"""
        self.update_status("Running quick analysis...")
        
        def analyze():
            try:
                conn = self.get_connection()
                if not conn:
                    raise Exception("Database connection failed")
                
                cursor = conn.cursor()
                
                # Get table count
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                analysis = f"QUICK ANALYSIS: Quick Analysis Results ({datetime.now().strftime('%H:%M:%S')})\n"
                analysis += "=" * 50 + "\n"
                analysis += f"Total tables: {len(tables)}\n\n"
                
                if tables:
                    analysis += "Tables found:\n"
                    for (table,) in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        analysis += f"  • {table}: {count} records\n"
                else:
                    analysis += "INFO: No tables found - run migrations first\n"
                
                cursor.close()
                conn.close()
                
                self.root.after(0, lambda: self.log_result(analysis))
                self.root.after(0, lambda: self.update_status("Quick analysis completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"ERROR: Analysis failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Analysis failed"))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def refresh_tables(self):
        """Refresh table list"""
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            self.table_combo['values'] = tables
            if tables:
                self.table_combo.set(tables[0])
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tables: {str(e)}")
    
    def load_table_data(self):
        """Load data for selected table"""
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first")
            return
        
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Clear existing data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
            
            # Get column names
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [row[0] for row in cursor.fetchall()]
            
            # Configure treeview columns
            self.data_tree['columns'] = columns
            self.data_tree['show'] = 'headings'
            
            for col in columns:
                self.data_tree.heading(col, text=col)
                self.data_tree.column(col, width=120)
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
            rows = cursor.fetchall()
            
            for row in rows:
                self.data_tree.insert('', 'end', values=row)
            
            cursor.close()
            conn.close()
            
            self.update_status(f"Loaded {len(rows)} records from {table_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table data: {str(e)}")
    
    def analyze_database(self):
        """Detailed database analysis"""
        self.analysis_text.delete('1.0', 'end')
        self.update_status("Running detailed analysis...")
        
        def analyze():
            try:
                conn = self.get_connection()
                if not conn:
                    raise Exception("Database connection failed")
                
                cursor = conn.cursor()
                
                analysis = f"DETAILED DATABASE ANALYSIS\n"
                analysis += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                analysis += "=" * 60 + "\n\n"
                
                # Get tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                analysis += f"SUMMARY\n"
                analysis += f"Total Tables: {len(tables)}\n\n"
                
                if tables:
                    analysis += f"TABLE DETAILS\n"
                    analysis += "-" * 40 + "\n"
                    
                    for (table,) in tables:
                        # Table info
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        
                        cursor.execute(f"DESCRIBE {table}")
                        columns = cursor.fetchall()
                        
                        analysis += f"\n{table.upper()}\n"
                        analysis += f"   Records: {count}\n"
                        analysis += f"   Columns: {len(columns)}\n"
                        
                        # Show column details
                        for col in columns[:5]:  # Show first 5 columns
                            analysis += f"   • {col[0]} ({col[1]})\n"
                        
                        if len(columns) > 5:
                            analysis += f"   ... and {len(columns) - 5} more columns\n"
                
                else:
                    analysis += "INFO: No tables found. Run migrations to create database schema.\n"
                
                analysis += f"\nRECOMMENDATIONS\n"
                analysis += "-" * 40 + "\n"
                
                if len(tables) > 0:
                    analysis += "• Database schema has been created successfully\n"
                    analysis += "• Consider running performance tests with larger datasets\n"
                    analysis += "• Review indexing strategy for production use\n"
                else:
                    analysis += "• Run migration tools to create database schema\n"
                    analysis += "• Start with Bytebase for incremental approach\n"
                    analysis += "• Compare execution times between tools\n"
                
                cursor.close()
                conn.close()
                
                self.root.after(0, lambda: self.analysis_text.insert('1.0', analysis))
                self.root.after(0, lambda: self.update_status("Detailed analysis completed"))
                
            except Exception as e:
                error_msg = f"ERROR: Analysis failed: {str(e)}"
                self.root.after(0, lambda: self.analysis_text.insert('1.0', error_msg))
                self.root.after(0, lambda: self.update_status("Analysis failed"))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def show_migration_tools_info(self):
        """Show comprehensive information about migration tools"""
        self.analysis_text.delete('1.0', 'end')
        
        info = f"DATABASE MIGRATION TOOLS COMPARISON\n"
        info += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += "=" * 70 + "\n\n"
        
        info += "OVERVIEW\n"
        info += "-" * 30 + "\n"
        info += "This POC compares three different approaches to database migrations:\n"
        info += "• Traditional SQL Scripts (Redgate style)\n"
        info += "• Modern Incremental Migrations (Bytebase style)\n"
        info += "• Enterprise XML Changesets (Liquibase)\n\n"
        
        info += "REDGATE APPROACH\n"
        info += "-" * 30 + "\n"
        info += "File Count: 2 SQL files\n"
        info += "Approach: Traditional DBA comprehensive scripts\n"
        info += "Structure:\n"
        info += "  • schema.sql - Complete database schema with all objects\n"
        info += "  • data.sql - Initial data population\n\n"
        info += "Characteristics:\n"
        info += "  + Pure SQL - no abstraction layer\n"
        info += "  + Complete control over SQL execution\n"
        info += "  + Supports complex stored procedures and functions\n"
        info += "  + Familiar to traditional DBAs\n"
        info += "  - No built-in rollback mechanisms\n"
        info += "  - Manual dependency management\n"
        info += "  - Harder to track individual changes\n\n"
        info += "Best For: Teams with strong SQL expertise, complex database logic\n\n"
        
        info += "BYTEBASE APPROACH\n"
        info += "-" * 30 + "\n"
        info += "File Count: 5 SQL files\n"
        info += "Approach: Git-like incremental changes\n"
        info += "Structure:\n"
        info += "  • 001_initial_schema.sql - Base tables\n"
        info += "  • 002_add_users.sql - User management\n"
        info += "  • 003_add_orders.sql - Order system\n"
        info += "  • 004_add_products.sql - Product catalog\n"
        info += "  • 005_add_relationships.sql - Foreign keys\n\n"
        info += "Characteristics:\n"
        info += "  + Incremental change tracking\n"
        info += "  + UI-driven workflow\n"
        info += "  + Built-in version control integration\n"
        info += "  + Automatic rollback capabilities\n"
        info += "  + Team collaboration features\n"
        info += "  - Learning curve for traditional DBAs\n"
        info += "  - May require workflow changes\n\n"
        info += "Best For: Development teams, CI/CD pipelines, collaborative environments\n\n"
        
        info += "LIQUIBASE APPROACH\n"
        info += "-" * 30 + "\n"
        info += "File Count: 3 XML files + properties\n"
        info += "Approach: Enterprise database-agnostic changesets\n"
        info += "Structure:\n"
        info += "  • db.changelog-master.xml - Main changelog\n"
        info += "  • create-tables.xml - Table definitions\n"
        info += "  • insert-data.xml - Data population\n"
        info += "  • liquibase.properties - Configuration\n\n"
        info += "Characteristics:\n"
        info += "  + Database-agnostic (MySQL, PostgreSQL, Oracle, etc.)\n"
        info += "  + Enterprise-grade rollback support\n"
        info += "  + Extensive change types and validations\n"
        info += "  + Integration with major IDEs and CI/CD\n"
        info += "  + Preconditions and context support\n"
        info += "  - XML can be verbose and complex\n"
        info += "  - Steeper learning curve\n"
        info += "  - Requires Liquibase knowledge\n\n"
        info += "Best For: Enterprise environments, multi-database support, complex deployment pipelines\n\n"
        
        info += "COMPARISON MATRIX\n"
        info += "-" * 30 + "\n"
        info += f"{'Aspect':<20} {'Redgate':<12} {'Bytebase':<12} {'Liquibase':<12}\n"
        info += f"{'Complexity':<20} {'Low':<12} {'Medium':<12} {'High':<12}\n"
        info += f"{'Learning Curve':<20} {'Minimal':<12} {'Moderate':<12} {'Steep':<12}\n"
        info += f"{'Rollback Support':<20} {'Manual':<12} {'Automatic':<12} {'Enterprise':<12}\n"
        info += f"{'Team Collaboration':<20} {'Basic':<12} {'Excellent':<12} {'Good':<12}\n"
        info += f"{'Database Support':<20} {'MySQL':<12} {'Multiple':<12} {'Universal':<12}\n"
        info += f"{'File Count':<20} {'2':<12} {'5':<12} {'3+config':<12}\n"
        info += f"{'Format':<20} {'Pure SQL':<12} {'SQL':<12} {'XML':<12}\n\n"
        
        info += "TESTING RECOMMENDATIONS\n"
        info += "-" * 30 + "\n"
        info += "1. Run each migration tool individually to compare execution times\n"
        info += "2. Use 'Reset Database' between tests for clean comparisons\n"
        info += "3. Check the Console tab for detailed execution logs\n"
        info += "4. Use 'Schema Analysis' to verify each tool creates the same structure\n"
        info += "5. Test rollback capabilities (where supported)\n\n"
        info += "WHAT TO LOOK FOR IN RESULTS\n"
        info += "-" * 30 + "\n"
        info += "• Execution speed differences\n"
        info += "• Error handling and recovery\n"
        info += "• Final database structure consistency\n"
        info += "• Ease of debugging from console output\n"
        info += "• Rollback and recovery capabilities\n\n"
        info += "DECISION FACTORS\n"
        info += "-" * 30 + "\n"
        info += "Choose Redgate if: You have strong SQL skills and simple deployment needs\n"
        info += "Choose Bytebase if: You want modern DevOps integration and team collaboration\n"
        info += "Choose Liquibase if: You need enterprise features and multi-database support\n"
        
        self.analysis_text.insert('1.0', info)
        self.update_status("Migration tools information displayed")
    
    def log_result(self, message):
        """Log result to console tab"""
        # Ensure there's a newline before new messages if console has content
        current_content = self.results_text.get('1.0', 'end-1c')
        if current_content and not current_content.endswith('\n'):
            self.results_text.insert('end', '\n')
        
        self.results_text.insert('end', f"{message}\n")
        self.results_text.see('end')
    
    def clear_console(self):
        """Clear console output"""
        self.results_text.delete('1.0', 'end')
        self.results_text.insert('1.0', "Console cleared.\n\n")
        self.update_status("Console cleared")
    
    def save_log(self):
        """Save console log to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get('1.0', 'end'))
                self.update_status(f"Log saved to {filename}")
                messagebox.showinfo("Success", f"Log saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save log: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.destroy()
    
    def add_table_row(self):
        """Add new row to selected table"""
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "Please select a table first")
            return
        
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Get column info
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            # Create input dialog
            self.create_row_input_dialog(table_name, columns, "Add")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get table structure: {str(e)}")
    
    def edit_table_row(self):
        """Edit selected row"""
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to edit")
            return
        
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "No table selected")
            return
        
        # Get row data
        item = self.data_tree.item(selected[0])
        row_values = item['values']
        
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Get column info
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            # Create edit dialog with current values
            self.create_row_input_dialog(table_name, columns, "Edit", row_values)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit row: {str(e)}")
    
    def delete_table_row(self):
        """Delete selected row"""
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to delete")
            return
        
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Warning", "No table selected")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this row?"):
            return
        
        # Get row data for WHERE clause (assuming first column is ID)
        item = self.data_tree.item(selected[0])
        row_values = item['values']
        
        try:
            conn = self.get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Get primary key column
            cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
            pk_info = cursor.fetchone()
            
            if pk_info:
                pk_column = pk_info[4]  # Column_name
                pk_value = row_values[0]  # Assuming first column is PK
                
                cursor.execute(f"DELETE FROM {table_name} WHERE {pk_column} = %s", (pk_value,))
                conn.commit()
                
                self.update_status(f"Row deleted from {table_name}")
                self.load_table_data()  # Refresh data
            else:
                messagebox.showwarning("Warning", "Cannot delete - no primary key found")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete row: {str(e)}")
    
    def create_row_input_dialog(self, table_name, columns, mode, current_values=None):
        """Create dialog for adding/editing rows"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{mode} Row - {table_name}")
        dialog.geometry("450x700")  # Made wider and taller
        dialog.configure(bg=self.colors['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"450x700+{x}+{y}")
        
        print(f"Creating dialog for {mode} in table {table_name}")  # Debug output
        
        # Header
        header_label = tk.Label(dialog, text=f"{mode} Row in {table_name}",
                               bg=self.colors['primary_bg'], fg=self.colors['accent'],
                               font=('Segoe UI', 14, 'bold'))
        header_label.pack(pady=20)
        
        # Main content frame (for scrollable area)
        content_frame = tk.Frame(dialog, bg=self.colors['primary_bg'])
        content_frame.pack(fill='both', expand=True, padx=0, pady=(0, 10))
        
        # Scrollable frame for fields (reduced height to make room for buttons)
        canvas = tk.Canvas(content_frame, bg=self.colors['primary_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['primary_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add mouse wheel scrolling support
        self.add_mousewheel_support(canvas)
        
        # Pack canvas with less height to leave room for buttons at bottom
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Create input fields
        entries = {}
        for i, col in enumerate(columns):
            col_name = col[0]
            col_type = col[1]
            is_nullable = col[2] == 'YES'
            col_default = col[4]
            is_auto_inc = 'auto_increment' in col[5].lower() if col[5] else False
            
            # Skip auto-increment fields in add mode
            if mode == "Add" and is_auto_inc:
                continue
            
            # Field frame
            field_frame = tk.Frame(scrollable_frame, bg=self.colors['primary_bg'])
            field_frame.pack(fill='x', pady=5, padx=10)
            
            # Label
            label_text = f"{col_name} ({col_type})"
            if not is_nullable:
                label_text += " *"
            
            tk.Label(field_frame, text=label_text,
                    bg=self.colors['primary_bg'], fg=self.colors['text_light'],
                    font=('Segoe UI', 10)).pack(anchor='w')
            
            # Entry
            entry = tk.Entry(field_frame, bg=self.colors['secondary_bg'],
                           fg=self.colors['text_light'], font=('Segoe UI', 10),
                           insertbackground=self.colors['accent'])
            entry.pack(fill='x', pady=(5, 0))
            
            # Set current value for edit mode
            if mode == "Edit" and current_values and i < len(current_values):
                entry.insert(0, str(current_values[i]) if current_values[i] is not None else "")
            
            entries[col_name] = entry
        
        # Fixed buttons at the bottom of the dialog (outside scrollable area)
        # Separator line
        separator = tk.Frame(dialog, height=2, bg=self.colors['border'])
        separator.pack(fill='x', padx=20, pady=(10, 0))
        
        # Buttons frame fixed at bottom - always visible, never scrolls
        button_frame = tk.Frame(dialog, bg='white', height=120)  # Fixed at bottom
        button_frame.pack(fill='x', pady=(10, 20), padx=20, side='bottom')
        button_frame.pack_propagate(False)  # Maintain fixed height
        
        def save_row():
            print(f"Save button clicked for {mode} in {table_name}")  # Debug output
            try:
                # Check if at least one field has data
                has_data = False
                for col_name, entry in entries.items():
                    if entry.get().strip():
                        has_data = True
                        break
                
                if not has_data:
                    print("No data entered, showing warning")  # Debug
                    messagebox.showwarning("Warning", "Please enter at least one field value")
                    return
                
                print("Data validation passed, proceeding with database operation")  # Debug
                conn = self.get_connection()
                if not conn:
                    print("Database connection failed")  # Debug
                    return
                
                cursor = conn.cursor()
                
                # Prepare data
                field_names = []
                field_values = []
                
                for col_name, entry in entries.items():
                    value = entry.get().strip()
                    if value or value == "0":  # Include if not empty or is zero
                        field_names.append(col_name)
                        field_values.append(value if value != "" else None)
                
                if mode == "Add":
                    # INSERT
                    placeholders = ", ".join(["%s"] * len(field_values))
                    sql = f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES ({placeholders})"
                    cursor.execute(sql, field_values)
                    success_msg = f"Row added to {table_name} successfully!"
                else:
                    # UPDATE - assuming first column is primary key
                    if current_values:
                        pk_column = columns[0][0]
                        pk_value = current_values[0]
                        
                        set_clause = ", ".join([f"{name} = %s" for name in field_names])
                        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = %s"
                        cursor.execute(sql, field_values + [pk_value])
                        success_msg = f"Row updated in {table_name} successfully!"
                
                conn.commit()
                cursor.close()
                conn.close()
                
                self.update_status(f"Row {mode.lower()}ed in {table_name}")
                self.load_table_data()  # Refresh data
                messagebox.showinfo("Success", success_msg)
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to {mode.lower()} row: {str(e)}")
        
        # Create highly visible buttons fixed at the bottom - always visible
        save_button = tk.Button(button_frame, text=f"{mode} Row",
                              bg='#00FF00', fg='black',  # Bright green background
                              font=('Segoe UI', 12, 'bold'), 
                              command=save_row,
                              width=20, height=2,
                              relief='raised', bd=3,
                              cursor='hand2',
                              activebackground='#32CD32',
                              activeforeground='black')
        save_button.pack(side='left', padx=(10, 5), pady=10, fill='both', expand=True)
        
        cancel_button = tk.Button(button_frame, text="Cancel",
                                bg='#FF4500', fg='white',  # Bright red/orange background
                                font=('Segoe UI', 12, 'bold'),
                                command=dialog.destroy,
                                width=20, height=2,
                                relief='raised', bd=3,
                                cursor='hand2',
                                activebackground='#FF6347',
                                activeforeground='white')
        cancel_button.pack(side='right', padx=(5, 10), pady=10, fill='both', expand=True)
        
        print(f"Buttons created and packed for {mode} dialog")  # Debug output
        print(f"Save button: {save_button}")  # Debug
        print(f"Cancel button: {cancel_button}")  # Debug
    
def main():
    root = tk.Tk()
    app = ProfessionalMigrationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
