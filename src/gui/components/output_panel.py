"""
Output Panel Component
Shows migration execution results and logs
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class OutputPanel:
    """Output panel for showing migration results and logs"""
    
    def __init__(self, parent, bg_color="white"):
        self.parent = parent
        self.bg_color = bg_color
        self.create_widgets()
    
    def create_widgets(self):
        """Create output panel widgets"""
        # Main frame
        self.frame = tk.Frame(self.parent, bg=self.bg_color)
        
        # Header frame
        self.header_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        # Title
        self.title_label = tk.Label(
            self.header_frame,
            text="Migration Output",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(side="left")
        
        # Clear button
        self.clear_button = tk.Button(
            self.header_frame,
            text="Clear",
            command=self.clear_output,
            bg="#f0f0f0",
            fg="black",
            font=("Arial", 9),
            relief="raised",
            bd=1
        )
        self.clear_button.pack(side="right", padx=5)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            bg="white",
            fg="black",
            font=("Courier New", 9),
            relief="solid",
            bd=1
        )
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure text tags for different message types
        self.output_text.tag_configure("success", foreground="green")
        self.output_text.tag_configure("error", foreground="red")
        self.output_text.tag_configure("warning", foreground="orange")
        self.output_text.tag_configure("info", foreground="blue")
        self.output_text.tag_configure("header", foreground="black", font=("Courier New", 9, "bold"))
    
    def add_message(self, message, msg_type="normal"):
        """Add a message to the output panel"""
        self.output_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "header":
            # For headers, don't add timestamp
            self.output_text.insert(tk.END, f"{message}\n", msg_type)
        else:
            self.output_text.insert(tk.END, f"[{timestamp}] {message}\n", msg_type)
        
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)  # Auto-scroll to bottom
    
    def add_tool_header(self, tool_name):
        """Add a tool execution header"""
        separator = "=" * 50
        self.add_message(f"\n{separator}", "header")
        self.add_message(f"EXECUTING {tool_name.upper()} MIGRATION", "header")
        self.add_message(f"{separator}", "header")
    
    def add_tool_results(self, tool_name, results):
        """Add results from a migration tool"""
        if not results:
            return
        
        for result in results:
            # Determine message type based on content
            if "✓" in result or "Successfully" in result:
                msg_type = "success"
            elif "❌" in result or "Failed" in result or "Error" in result:
                msg_type = "error"
            elif "⚠️" in result or "Warning" in result:
                msg_type = "warning"
            else:
                msg_type = "normal"
            
            self.add_message(result, msg_type)
    
    def add_summary(self, tool_results, execution_times):
        """Add execution summary"""
        self.add_message("\n" + "="*50, "header")
        self.add_message("MIGRATION SUMMARY", "header")
        self.add_message("="*50, "header")
        
        total_time = 0
        
        for tool, results in tool_results.items():
            # Determine overall status
            success_count = sum(1 for r in results if "✓" in r)
            error_count = sum(1 for r in results if "❌" in r)
            
            if error_count > 0:
                status = "FAILED"
                status_type = "error"
            elif success_count > 0:
                status = "SUCCESS"
                status_type = "success"
            else:
                status = "NO CHANGES"
                status_type = "info"
            
            # Get execution time
            exec_time = execution_times.get(tool, 0)
            total_time += exec_time
            
            self.add_message(f"{tool.upper()}: {status} ({exec_time:.1f}s)", status_type)
        
        self.add_message(f"\nTotal execution time: {total_time:.1f}s", "info")
        self.add_message("="*50 + "\n", "header")
    
    def clear_output(self):
        """Clear all output"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # Add initial message
        self.add_message("Migration output will appear here...", "info")
    
    def get_frame(self):
        """Get the main frame for packing"""
        return self.frame
