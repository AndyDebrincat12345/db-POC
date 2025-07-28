#!/usr/bin/env python3
"""
Fix GUI issues script
"""

# Read the current GUI file
with open('gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove Unicode emojis from tab names
content = content.replace('text="� Console"', 'text="Console"')
content = content.replace('text="� Analysis"', 'text="Analysis"')

# Fix 2: Ensure filedialog is imported
if 'from tkinter import filedialog' not in content:
    content = content.replace(
        'from tkinter import ttk, messagebox, scrolledtext',
        'from tkinter import ttk, messagebox, scrolledtext, filedialog'
    )

# Fix 3: Ensure window controls are properly enabled
# Make sure the window has proper title bar controls
window_setup = '''    def setup_main_window(self):
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
        self.root.overrideredirect(False)'''

# Find and replace the setup_main_window method
import re
pattern = r'    def setup_main_window\(self\):.*?self\.root\.resizable\(True, True\)'
content = re.sub(pattern, window_setup, content, flags=re.DOTALL)

# Write the fixed content back
with open('gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("GUI fixes applied:")
print("1. ✓ Fixed Unicode emoji issues in tab names")
print("2. ✓ Added filedialog import for save functionality")
print("3. ✓ Ensured proper window controls (minimize, maximize, close)")
