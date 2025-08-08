#!/usr/bin/env python3
"""
Professional Database Migration Tools POC - Main Entry Point
EY Enterprise Tools Comparison

This is the main entry point for the Professional Database Migration Tools POC.
Run this file to start the application.
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the application"""
    try:
        # Import the main GUI class
        from gui.main_window import ProfessionalMigrationGUI
        
        # Create and configure the root window
        root = tk.Tk()
        root.title("Professional Database Migration POC - EY Enterprise Tools")
        
        # Initialize the main application
        app = ProfessionalMigrationGUI(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all required modules are installed and the project structure is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
