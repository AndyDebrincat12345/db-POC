"""
Status Panel Component
Shows connection status and migration progress
"""

import tkinter as tk
from tkinter import ttk

class StatusPanel:
    """Status panel for showing connection and migration status"""
    
    def __init__(self, parent, bg_color="white"):
        self.parent = parent
        self.bg_color = bg_color
        self.create_widgets()
    
    def create_widgets(self):
        """Create status panel widgets"""
        # Main frame
        self.frame = tk.Frame(self.parent, bg=self.bg_color, relief="flat", bd=1)
        
        # Connection Status Frame
        self.connection_frame = tk.LabelFrame(
            self.frame,
            text="Connection Status",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 10, "bold")
        )
        self.connection_frame.pack(fill="x", padx=5, pady=5)
        
        # Connection status label
        self.connection_status = tk.Label(
            self.connection_frame,
            text="Not Connected",
            bg=self.bg_color,
            fg="red",
            font=("Arial", 9)
        )
        self.connection_status.pack(pady=5)
        
        # Tool Status Frame
        self.tool_frame = tk.LabelFrame(
            self.frame,
            text="Tool Status",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 10, "bold")
        )
        self.tool_frame.pack(fill="x", padx=5, pady=5)
        
        # Tool status labels
        self.tool_statuses = {}
        tools = ["Redgate", "Liquibase", "Bytebase"]
        
        for tool in tools:
            status_frame = tk.Frame(self.tool_frame, bg=self.bg_color)
            status_frame.pack(fill="x", pady=2)
            
            tool_label = tk.Label(
                status_frame,
                text=f"{tool}:",
                bg=self.bg_color,
                fg="black",
                font=("Arial", 9),
                width=10,
                anchor="w"
            )
            tool_label.pack(side="left")
            
            status_label = tk.Label(
                status_frame,
                text="Ready",
                bg=self.bg_color,
                fg="gray",
                font=("Arial", 9)
            )
            status_label.pack(side="left")
            
            self.tool_statuses[tool.lower()] = status_label
        
        # Progress Frame
        self.progress_frame = tk.LabelFrame(
            self.frame,
            text="Migration Progress",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 10, "bold")
        )
        self.progress_frame.pack(fill="x", padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        
        # Progress label
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Ready to migrate",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 9)
        )
        self.progress_label.pack(pady=2)
    
    def update_connection_status(self, connected, db_type=None):
        """Update connection status display"""
        if connected:
            self.connection_status.config(
                text=f"Connected to {db_type}" if db_type else "Connected",
                fg="green"
            )
        else:
            self.connection_status.config(
                text="Not Connected",
                fg="red"
            )
    
    def update_tool_status(self, tool, status, color="black"):
        """Update individual tool status"""
        tool_lower = tool.lower()
        if tool_lower in self.tool_statuses:
            self.tool_statuses[tool_lower].config(text=status, fg=color)
    
    def update_progress(self, value, text=None):
        """Update progress bar and label"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=text)
    
    def reset_progress(self):
        """Reset progress to initial state"""
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to migrate")
        
        # Reset tool statuses
        for tool_status in self.tool_statuses.values():
            tool_status.config(text="Ready", fg="gray")
    
    def get_frame(self):
        """Get the main frame for packing"""
        return self.frame
