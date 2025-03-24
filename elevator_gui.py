import tkinter as tk
from tkinter import ttk, messagebox
import time
from elevator_logic import ElevatorSystem

class ElevatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JKUAT Towers Elevator System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.elevator = ElevatorSystem()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="JKUAT Towers Elevator System",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#1a5276"
        )
        title_label.pack(pady=10)
        
        # Information frame
        info_frame = tk.Frame(main_frame, bg="#f0f0f0")
        info_frame.pack(fill=tk.X, pady=10)
        
        # Door information
        door_info_label = tk.Label(
            info_frame,
            text="Door Information:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            anchor="w"
        )
        door_info_label.pack(fill=tk.X)
        
        door_info = [
            "Door A serves Ground floor to 5th floor",
            "Door B serves Ground floor to 8th floor",
            "Door C serves Ground floor to 10th floor"
        ]
        
        for info in door_info:
            label = tk.Label(
                info_frame,
                text=f"• {info}",
                font=("Arial", 11),
                bg="#f0f0f0",
                anchor="w",
                padx=20
            )
            label.pack(fill=tk.X)
        
        # Current status frame
        status_frame = tk.Frame(main_frame, bg="#e8f4f8", relief=tk.RIDGE, bd=2)
        status_frame.pack(fill=tk.X, pady=15)
        
        self.status_label = tk.Label(
            status_frame,
            text="Current Floor: Ground Floor",
            font=("Arial", 12),
            bg="#e8f4f8",
            pady=10
        )
        self.status_label.pack()
        
        self.door_label = tk.Label(
            status_frame,
            text="Please select a floor",
            font=("Arial", 12),
            bg="#e8f4f8",
            pady=5
        )
        self.door_label.pack()
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg="#f0f0f0")
        controls_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Left side - Floor buttons
        floor_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        floor_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)
        
        floor_label = tk.Label(
            floor_frame,
            text="Select Floor:",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        floor_label.pack(anchor="w", pady=5)
        
        # Create floor buttons in grid layout
        button_frame = tk.Frame(floor_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons for floor 10 down to ground (0)
        row, col = 0, 0
        max_cols = 3
        
        self.floor_buttons = []
        for floor in range(10, -1, -1):
            floor_text = "G" if floor == 0 else str(floor)
            btn = tk.Button(
                button_frame,
                text=floor_text,
                width=6,
                height=2,
                font=("Arial", 14, "bold"),
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                command=lambda f=floor: self.request_floor(f)
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.floor_buttons.append(btn)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid
        for i in range(4):  # 4 rows needed for 11 buttons with 3 columns
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(max_cols):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Right side - Visual representation
        visual_frame = tk.Frame(controls_frame, bg="#e8f4f8", relief=tk.RIDGE, bd=2)
        visual_frame.pack(side=tk.RIGHT, padx=20, fill=tk.BOTH, expand=True)
        
        visual_label = tk.Label(
            visual_frame,
            text="Building Floors",
            font=("Arial", 12, "bold"),
            bg="#e8f4f8"
        )
        visual_label.pack(pady=10)
        
        # Create visual representation of floors and doors with a scrollbar
        canvas_frame = tk.Frame(visual_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a scrollbar for the floors canvas
        scrollbar = tk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas with scrollbar
        floors_canvas = tk.Canvas(
            canvas_frame, 
            bg="white", 
            bd=0, 
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        floors_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar
        scrollbar.config(command=floors_canvas.yview)
        
        # Draw floors
        floor_height = 30
        canvas_width = 350
        total_height = (11 * floor_height) + 50  # 11 floors (0-10) + padding
        
        # Set the canvas scroll region
        floors_canvas.config(scrollregion=(0, 0, canvas_width, total_height))
        
        # Draw building
        self.floor_rects = []
        door_info = self.elevator.get_floor_info()
        
        # Calculate the top position for the 10th floor
        top_y = 20  # Starting position from top
        
        for floor_num, floor_name, doors in door_info:
            # Place floors from top (10th) to bottom (G)
            y_pos = top_y + ((10 - floor_num) * floor_height)
            
            rect = floors_canvas.create_rectangle(
                50, y_pos, canvas_width - 50, y_pos + floor_height,
                fill="#d5dbdb", outline="black"
            )
            self.floor_rects.append(rect)
            
            # Floor label
            floors_canvas.create_text(
                30, y_pos + floor_height/2,
                text=f"{floor_num}" if floor_num > 0 else "G",
                font=("Arial", 10, "bold")
            )
            
            # Door indicators
            door_text = f"Doors: {doors}"
            floors_canvas.create_text(
                canvas_width - 100, y_pos + floor_height/2,
                text=door_text,
                font=("Arial", 9)
            )
            
            # Floor name
            floors_canvas.create_text(
                120, y_pos + floor_height/2,
                text=floor_name,
                font=("Arial", 9)
            )
        
        # Elevator indicator - start at Ground floor (bottom)
        ground_y = top_y + (10 * floor_height)  # Position for ground floor
        self.elevator_indicator = floors_canvas.create_rectangle(
            70, ground_y, 100, ground_y + floor_height,
            fill="#3498db", outline="black"
        )
        
        # Status bar at bottom
        status_bar = tk.Frame(self.root, bg="#1a5276", height=25)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        status_text = tk.Label(
            status_bar,
            text="© JKUAT Towers Elevator System | Computer Science Project",
            fg="white",
            bg="#1a5276",
            font=("Arial", 9)
        )
        status_text.pack(side=tk.RIGHT, padx=10)
        
        # Store canvas for animation
        self.floors_canvas = floors_canvas
        self.top_y = top_y
        self.floor_height = floor_height
        
    def request_floor(self, floor):
        # Get current floor before movement
        prev_floor = self.elevator.current_floor
        
        # Call the elevator logic
        success, door, message = self.elevator.move_to_floor(floor)
        
        if success:
            # Update status
            floor_name = "Ground Floor" if floor == 0 else f"{floor}{self.elevator.get_ordinal_suffix(floor)} Floor"
            self.status_label.config(text=f"Current Floor: {floor_name}")
            self.door_label.config(text=f"Use Door {door}")
            
            # Animate elevator movement
            self.animate_elevator(prev_floor, floor)
            
            # Highlight the assigned door
            self.highlight_door(door)
        else:
            messagebox.showerror("Error", message)
    
    def animate_elevator(self, from_floor, to_floor):
        """Animate elevator movement between floors"""
        steps = 20  # Animation smoothness
        
        # Calculate positions using the new coordinate system
        start_y = self.top_y + ((10 - from_floor) * self.floor_height)
        end_y = self.top_y + ((10 - to_floor) * self.floor_height)
        distance = end_y - start_y
        step_size = distance / steps
        
        def move_step(step):
            if step < steps:
                # Move indicator
                self.floors_canvas.move(self.elevator_indicator, 0, step_size)
                # Schedule next step
                self.root.after(50, lambda: move_step(step + 1))
        
        # Start animation
        move_step(0)
    
    def highlight_door(self, door):
        """Highlight the assigned door in the UI"""
        # Reset all button colors
        for btn in self.floor_buttons:
            btn.config(bg="#3498db")
        
        # Change door label with highlight color based on door
        door_colors = {"A": "#27ae60", "B": "#f39c12", "C": "#e74c3c"}
        self.door_label.config(
            text=f"Use Door {door}",
            fg=door_colors.get(door, "black"),
            font=("Arial", 14, "bold")
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorGUI(root)
    root.mainloop()