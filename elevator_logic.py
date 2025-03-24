class ElevatorSystem:
    def __init__(self):
        # Define door service ranges
        self.doors = {
            'A': range(0, 6),     # Door A: Ground floor (0) to 5th floor
            'B': range(0, 9),     # Door B: Ground floor (0) to 8th floor
            'C': range(0, 11)     # Door C: Ground floor (0) to 10th floor
        }
        self.current_floor = 0    # Start at ground floor
        self.total_floors = 10    # Total floors in the building
    
    def assign_door(self, target_floor):
        """
        Assigns the appropriate door based on the target floor.
        Returns the assigned door or None if the floor is invalid.
        """
        if not isinstance(target_floor, int):
            return None
            
        if target_floor < 0 or target_floor > self.total_floors:
            return None
            
        # Find suitable doors for the requested floor
        suitable_doors = []
        for door, floor_range in self.doors.items():
            if target_floor in floor_range:
                suitable_doors.append(door)
        
        # Door assignment logic: use the most efficient door
        # For simplicity, we'll use the door that serves the fewest floors
        if suitable_doors:
            if target_floor <= 5:
                return 'A'  # Door A is optimal for floors 0-5
            elif target_floor <= 8:
                return 'B'  # Door B is optimal for floors 6-8
            else:
                return 'C'  # Door C is required for floors 9-10
        
        return None
    
    def move_to_floor(self, target_floor):
        """
        Simulates the elevator moving to the target floor.
        Returns a tuple of (success, door, message)
        """
        door = self.assign_door(target_floor)
        
        if door is None:
            return False, None, f"Invalid floor selection: {target_floor}"
        
        # Simulate elevator movement
        prev_floor = self.current_floor
        self.current_floor = target_floor
        
        direction = "up" if target_floor > prev_floor else "down" if target_floor < prev_floor else "staying on the same floor"
        
        floor_name = "Ground floor" if target_floor == 0 else f"{target_floor}{self.get_ordinal_suffix(target_floor)} floor"
        
        return True, door, f"Moving {direction} to {floor_name}. Please use Door {door}."
    
    def get_ordinal_suffix(self, num):
        """Returns the ordinal suffix for a number (1st, 2nd, 3rd, etc.)"""
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
        return suffix
    
    def get_floor_info(self):
        """Returns information about all floors and which doors serve them"""
        floor_info = []
        for floor in range(self.total_floors + 1):
            serving_doors = []
            for door, floor_range in self.doors.items():
                if floor in floor_range:
                    serving_doors.append(door)
            
            floor_name = "Ground floor" if floor == 0 else f"{floor}{self.get_ordinal_suffix(floor)} floor"
            floor_info.append((floor, floor_name, ", ".join(serving_doors)))
        
        return floor_info