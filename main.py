"""
JKUAT Towers Elevator System
----------------------------
This program simulates an elevator system for the JKUAT towers in Nairobi.

- Door A serves ground floor up to 5th floor
- Door B serves ground floor up to 8th floor
- Door C serves ground floor up to 10th floor

Run this script to launch the application.
"""

import tkinter as tk
from elevator_gui import ElevatorGUI

def main():
    # Initialize the main window
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap("elevator_icon.ico")
    except:
        pass  # Continue without icon if not found
        
    # Create the application
    app = ElevatorGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()