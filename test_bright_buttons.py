#!/usr/bin/env python3
"""
Simple test for bright button visibility
"""

import tkinter as tk
from tkinter import messagebox

def test_bright_buttons():
    """Test bright buttons to ensure they're visible"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create test dialog
    dialog = tk.Toplevel(root)
    dialog.title("Button Visibility Test")
    dialog.geometry("450x300")
    dialog.configure(bg='#1a1a1a')  # Dark background
    
    # Header
    header_label = tk.Label(dialog, text="Button Visibility Test",
                           bg='#1a1a1a', fg='#ffd700',
                           font=('Segoe UI', 16, 'bold'))
    header_label.pack(pady=30)
    
    # Info label
    info_label = tk.Label(dialog, text="Can you see both buttons below clearly?",
                         bg='#1a1a1a', fg='white',
                         font=('Segoe UI', 12))
    info_label.pack(pady=20)
    
    # Button frame with white background
    button_frame = tk.Frame(dialog, bg='white', height=150)
    button_frame.pack(fill='x', pady=20, padx=20)
    button_frame.pack_propagate(False)
    
    def test_save():
        messagebox.showinfo("Success", "Save button clicked!")
    
    def test_cancel():
        messagebox.showinfo("Success", "Cancel button clicked!")
        dialog.destroy()
    
    # Bright green save button
    save_button = tk.Button(button_frame, text="✅ Save Test",
                          bg='#00FF00', fg='black',
                          font=('Segoe UI', 14, 'bold'), 
                          command=test_save,
                          width=18, height=3,
                          relief='raised', bd=5,
                          cursor='hand2',
                          activebackground='#32CD32',
                          activeforeground='black',
                          highlightbackground='#FFFF00',
                          highlightcolor='#FFFF00',
                          highlightthickness=3)
    save_button.pack(side='top', pady=(15, 10), fill='x')
    
    # Bright red cancel button
    cancel_button = tk.Button(button_frame, text="❌ Cancel Test",
                            bg='#FF4500', fg='white',
                            font=('Segoe UI', 14, 'bold'),
                            command=test_cancel,
                            width=18, height=3,
                            relief='raised', bd=5,
                            cursor='hand2',
                            activebackground='#FF6347',
                            activeforeground='white',
                            highlightbackground='#FFFF00',
                            highlightcolor='#FFFF00',
                            highlightthickness=3)
    cancel_button.pack(side='top', pady=(10, 15), fill='x')
    
    # Center dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
    y = (dialog.winfo_screenheight() // 2) - (300 // 2)
    dialog.geometry(f"450x300+{x}+{y}")
    
    dialog.focus_set()
    dialog.wait_window()

if __name__ == "__main__":
    test_bright_buttons()
