"""
RoomRenderer - Room drawing logic for floor plan

Single Responsibility: Draw rooms on canvas.
"""
import tkinter as tk
from typing import List, Dict


# Default room layout
DEFAULT_ROOMS = [
    {'name': 'Living Room', 'bounds': (30, 30, 180, 140)},
    {'name': 'Kitchen', 'bounds': (190, 30, 280, 100)},
    {'name': 'Bedroom', 'bounds': (30, 150, 140, 230)},
    {'name': 'Bathroom', 'bounds': (150, 150, 220, 200)},
    {'name': 'Entrance', 'bounds': (290, 30, 370, 80)},
]


class RoomRenderer:
    """Handles room rendering on floor plan canvas"""
    
    @staticmethod
    def draw_rooms(canvas: tk.Canvas, rooms: List[Dict] = None) -> None:
        """Draw all room outlines on canvas"""
        if rooms is None:
            rooms = DEFAULT_ROOMS
        
        for room in rooms:
            RoomRenderer.draw_room(canvas, room)
    
    @staticmethod
    def draw_room(canvas: tk.Canvas, room: Dict) -> None:
        """Draw a single room"""
        x1, y1, x2, y2 = room['bounds']
        
        # Draw rectangle
        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='white', outline='#424242', width=2
        )
        
        # Draw label
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        canvas.create_text(
            cx, cy, text=room['name'],
            font=('Arial', 8), fill='#757575'
        )
    
    @staticmethod
    def get_room_at_point(rooms: List[Dict], x: int, y: int) -> Dict:
        """Get room containing a point"""
        for room in rooms:
            x1, y1, x2, y2 = room['bounds']
            if x1 <= x <= x2 and y1 <= y <= y2:
                return room
        return None
