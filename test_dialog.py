#!/usr/bin/env python3
"""
Test script to verify the Add Row dialog functionality
"""

import tkinter as tk
from tkinter import messagebox

def test_dialog():
    """Test the dialog with buttons"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Colors for testing
    colors = {
        'primary_bg': '#1a1a1a',
        'secondary_bg': '#2d2d2d',
        'accent': '#ffd700',
        'text_light': '#ffffff',
        'text_dark': '#000000',
        'border': '#404040'
    }
    
    # Create test dialog
    dialog = tk.Toplevel(root)
    dialog.title("Test Add Row Dialog")
    dialog.geometry("400x600")
    dialog.configure(bg=colors['primary_bg'])
    
    # Header
    header_label = tk.Label(dialog, text="Test Add Row Dialog",
                           bg=colors['primary_bg'], fg=colors['accent'],
                           font=('Segoe UI', 14, 'bold'))
    header_label.pack(pady=20)
    
    # Sample input field
    field_frame = tk.Frame(dialog, bg=colors['primary_bg'])
    field_frame.pack(fill='x', pady=10, padx=20)
    
    tk.Label(field_frame, text="Sample Field:",
            bg=colors['primary_bg'], fg=colors['text_light'],
            font=('Segoe UI', 10)).pack(anchor='w')
    
    test_entry = tk.Entry(field_frame, bg=colors['secondary_bg'],
                         fg=colors['text_light'], font=('Segoe UI', 10))
    test_entry.pack(fill='x', pady=(5, 0))
    
    # Separator line
    separator = tk.Frame(dialog, height=2, bg=colors['border'])
    separator.pack(fill='x', padx=20, pady=(10, 0))
    
    # Buttons frame with enhanced visibility
    button_frame = tk.Frame(dialog, bg=colors['primary_bg'], height=80)
    button_frame.pack(fill='x', pady=(20, 20), padx=20)
    button_frame.pack_propagate(False)  # Maintain fixed height
    
    def test_save():
        value = test_entry.get()
        if value:
            messagebox.showinfo("Success", f"Value entered: {value}")
            dialog.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter a value")
    
    # Create buttons with enhanced styling for better visibility
    save_button = tk.Button(button_frame, text="Add Row",
                          bg=colors['accent'], fg=colors['text_dark'],
                          font=('Segoe UI', 12, 'bold'), 
                          command=test_save,
                          width=15, height=2,
                          relief='raised', bd=3,
                          cursor='hand2',
                          activebackground='#ffed4e',
                          activeforeground=colors['text_dark'])
    save_button.pack(side='left', padx=(0, 15), pady=10)
    
    cancel_button = tk.Button(button_frame, text="Cancel",
                            bg='#808080', fg='white',
                            font=('Segoe UI', 12, 'bold'),
                            command=dialog.destroy,
                            width=15, height=2,
                            relief='raised', bd=3,
                            cursor='hand2',
                            activebackground='#696969',
                            activeforeground='white')
    cancel_button.pack(side='right', padx=(15, 0), pady=10)
    
    # Center dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
    y = (dialog.winfo_screenheight() // 2) - (600 // 2)
    dialog.geometry(f"400x600+{x}+{y}")
    
    dialog.focus_set()
    dialog.wait_window()

if __name__ == "__main__":
    test_dialog()
