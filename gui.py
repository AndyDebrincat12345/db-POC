#!/usr/bin/env python3
"""
Professional Database Migration POC GUI
Modern black, white, and yellow themed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1000, 600)
    
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
                                         text="🔴 Disconnected",
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
        self.create_comparison_tab()
        self.create_data_tab()
        self.create_analysis_tab()
        self.create_settings_tab()
    
    def create_migrations_tab(self):
        """Create professional migrations tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="🛠️ Migrations")
        
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
                                  "🔵 Bytebase", 
                                  "Incremental SQL Migrations",
                                  "5 files - Git-like incremental changes\nModern UI-driven workflow",
                                  self.colors['accent'],
                                  lambda: self.run_migration('bytebase'))
        
        # Liquibase card  
        self.create_migration_card(cards_frame,
                                  "🟡 Liquibase",
                                  "Enterprise XML Migrations", 
                                  "3 files - Enterprise batch releases\nDatabase-agnostic changesets",
                                  '#ffa500',
                                  lambda: self.run_migration('liquibase'))
        
        # Redgate card
        self.create_migration_card(cards_frame,
                                  "🔴 Redgate", 
                                  "Traditional SQL Scripts",
                                  "2 files - DBA comprehensive scripts\nPure SQL approach",
                                  '#ff6b6b',
                                  lambda: self.run_migration('redgate'))
        
        # Action buttons
        actions_frame = ttk.Frame(scrollable_frame, style='Professional.TFrame')
        actions_frame.pack(fill='x', padx=40, pady=30)
        
        ttk.Button(actions_frame, 
                  text="🤖 Run All Tests (Automated)",
                  style='Professional.TButton',
                  command=self.run_automated_test).pack(side='left', padx=(0, 10))
        
        ttk.Button(actions_frame,
                  text="🔄 Reset Database", 
                  style='Danger.TButton',
                  command=self.reset_database).pack(side='left', padx=10)
        
        ttk.Button(actions_frame,
                  text="📊 Quick Analysis",
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
        
        # Title
        title_label = tk.Label(content_frame, text=title,
                              bg=self.colors['secondary_bg'],
                              fg=color, font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor='w')
        
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
        
        run_button = tk.Button(button_frame, text=f"Run {title.split()[1]} Migration",
                              bg=color, fg=self.colors['text_dark'],
                              font=('Segoe UI', 10, 'bold'),
                              border=0, padx=20, pady=8,
                              command=command)
        run_button.pack(side='left')
    
    def create_comparison_tab(self):
        """Create comparison results tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="📊 Comparison")
        
        # Header
        header_label = ttk.Label(tab_frame, 
                                text="Migration Tool Comparison Results",
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
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
        
        # Initial message
        self.results_text.insert('1.0', "🚀 Ready to run migration comparisons...\n\n")
        self.results_text.insert('end', "Click 'Run All Tests' in the Migrations tab to begin automated testing.\n")
        self.results_text.insert('end', "Or run individual migrations to see detailed output.\n\n")
        self.results_text.insert('end', "Results will appear here with execution times, errors, and analysis.")
    
    def create_data_tab(self):
        """Create data viewing tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="👁️ Data View")
        
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
        
        ttk.Button(controls_frame, text="🔄 Refresh Tables",
                  style='Professional.TButton',
                  command=self.refresh_tables).pack(side='left', padx=10)
        
        ttk.Button(controls_frame, text="📋 Load Data", 
                  style='Success.TButton',
                  command=self.load_table_data).pack(side='left', padx=10)
        
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
        
        # Initial table refresh
        self.refresh_tables()
    
    def create_analysis_tab(self):
        """Create analysis and insights tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="🔍 Analysis")
        
        # Header
        header_label = ttk.Label(tab_frame,
                                text="Database Analysis & Insights", 
                                style='Heading.TLabel')
        header_label.pack(pady=20)
        
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
        
        # Control buttons
        controls_frame = ttk.Frame(tab_frame, style='Professional.TFrame')
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(controls_frame, text="🔍 Analyze Current State",
                  style='Professional.TButton',
                  command=self.analyze_database).pack(side='left', padx=(0, 10))
        
        ttk.Button(controls_frame, text="📈 Performance Report",
                  style='Success.TButton', 
                  command=self.performance_report).pack(side='left', padx=10)
    
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        tab_frame = ttk.Frame(self.notebook, style='Professional.TFrame')
        self.notebook.add(tab_frame, text="⚙️ Settings")
        
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
        ttk.Button(db_frame, text="🔌 Test Connection",
                  style='Professional.TButton',
                  command=self.test_connection).pack(pady=10)
        
        # Migration paths
        paths_frame = ttk.LabelFrame(settings_frame, text="Migration Paths")
        paths_frame.pack(fill='x', pady=(0, 20))
        
        paths_info = """
🔵 Bytebase: bytebase/migrations/ (5 SQL files)
🟡 Liquibase: liquibase/changelog/ (3 XML files) 
🔴 Redgate: redgate/migrations/ (2 SQL files)
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
            self.connection_status.config(text="🟢 Connected", fg=self.colors['success'])
            self.update_status("Database connection successful")
        else:
            self.connection_status.config(text="🔴 Disconnected", fg=self.colors['error'])
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
                
                self.root.after(0, lambda: self.log_result(f"✅ {tool.capitalize()} migration completed in {execution_time:.2f}s"))
                self.root.after(0, lambda: self.update_status(f"{tool.capitalize()} migration completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"❌ {tool.capitalize()} migration failed: {str(e)}"))
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
                with open(filepath, "r") as f:
                    sql = f.read()
                
                statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
                
                for statement in statements:
                    cursor.execute(statement)
                
                conn.commit()
        
        finally:
            cursor.close()
            conn.close()
    
    def run_automated_test(self):
        """Run automated comparison test"""
        self.update_status("Running automated test...")
        self.log_result("🤖 Starting automated migration tool comparison...\n")
        
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
                self.root.after(0, lambda: self.log_result(f"❌ Automated test failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Automated test failed"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def reset_database(self):
        """Reset database"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the database? This will drop all tables."):
            self.update_status("Resetting database...")
            
            def reset():
                try:
                    conn = self.get_connection()
                    if not conn:
                        raise Exception("Database connection failed")
                    
                    cursor = conn.cursor()
                    
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    
                    for (table,) in tables:
                        cursor.execute(f"DROP TABLE {table}")
                    
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                    conn.commit()
                    
                    cursor.close()
                    conn.close()
                    
                    self.root.after(0, lambda: self.log_result("🔄 Database reset completed"))
                    self.root.after(0, lambda: self.update_status("Database reset completed"))
                    self.root.after(0, self.refresh_tables)
                    
                except Exception as e:
                    self.root.after(0, lambda: self.log_result(f"❌ Database reset failed: {str(e)}"))
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
                
                analysis = f"📊 Quick Analysis Results ({datetime.now().strftime('%H:%M:%S')})\n"
                analysis += "=" * 50 + "\n"
                analysis += f"📋 Total tables: {len(tables)}\n\n"
                
                if tables:
                    analysis += "📝 Tables found:\n"
                    for (table,) in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        analysis += f"  • {table}: {count} records\n"
                else:
                    analysis += "ℹ️  No tables found - run migrations first\n"
                
                cursor.close()
                conn.close()
                
                self.root.after(0, lambda: self.log_result(analysis))
                self.root.after(0, lambda: self.update_status("Quick analysis completed"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"❌ Analysis failed: {str(e)}"))
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
                
                analysis = f"🔍 Detailed Database Analysis\n"
                analysis += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                analysis += "=" * 60 + "\n\n"
                
                # Get tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                analysis += f"📊 SUMMARY\n"
                analysis += f"Total Tables: {len(tables)}\n\n"
                
                if tables:
                    analysis += f"📋 TABLE DETAILS\n"
                    analysis += "-" * 40 + "\n"
                    
                    for (table,) in tables:
                        # Table info
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        
                        cursor.execute(f"DESCRIBE {table}")
                        columns = cursor.fetchall()
                        
                        analysis += f"\n🗂️  {table.upper()}\n"
                        analysis += f"   Records: {count}\n"
                        analysis += f"   Columns: {len(columns)}\n"
                        
                        # Show column details
                        for col in columns[:5]:  # Show first 5 columns
                            analysis += f"   • {col[0]} ({col[1]})\n"
                        
                        if len(columns) > 5:
                            analysis += f"   ... and {len(columns) - 5} more columns\n"
                
                else:
                    analysis += "ℹ️  No tables found. Run migrations to create database schema.\n"
                
                analysis += f"\n📈 RECOMMENDATIONS\n"
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
                error_msg = f"❌ Analysis failed: {str(e)}"
                self.root.after(0, lambda: self.analysis_text.insert('1.0', error_msg))
                self.root.after(0, lambda: self.update_status("Analysis failed"))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def performance_report(self):
        """Generate performance report"""
        self.analysis_text.delete('1.0', 'end')
        self.analysis_text.insert('1.0', "📈 Generating performance report...\n\n")
        self.analysis_text.insert('end', "This feature analyzes migration performance metrics.\n")
        self.analysis_text.insert('end', "Run the automated test first to generate performance data.\n\n")
        self.analysis_text.insert('end', "Performance metrics include:\n")
        self.analysis_text.insert('end', "• Execution time comparison\n")
        self.analysis_text.insert('end', "• Error handling analysis\n") 
        self.analysis_text.insert('end', "• Resource usage patterns\n")
        self.analysis_text.insert('end', "• Scalability assessment\n")
    
    def log_result(self, message):
        """Log result to comparison tab"""
        self.results_text.insert('end', f"{message}\n")
        self.results_text.see('end')

def main():
    root = tk.Tk()
    app = ProfessionalMigrationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
