"""
Device Renderer for the Main Page Floor Plan.
"""
import tkinter as tk
from typing import Dict

class DeviceRenderer:
    """
    Manages rendering device icons on the floor plan canvas.
    """
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.device_items: Dict[str, Dict] = {}

    def add_device_icon(
        self,
        device_type: str,
        device_id: str,
        x: int,
        y: int,
        armed: bool = False,
    ) -> None:
        """Add a device icon to the floor plan canvas."""
        symbols = {
            "window_door_sensor": "🟥", "motion_sensor": "🟦",
            "camera": "📹", "alarm": "🔔",
        }
        colors = {
            "window_door_sensor": "#e74c3c" if armed else "#bdc3c7",
            "motion_sensor": "#3498db" if armed else "#bdc3c7",
            "camera": "#9b59b6" if armed else "#bdc3c7",
            "alarm": "#e67e22" if armed else "#bdc3c7",
        }

        symbol = symbols.get(device_type, "⚫")
        color = colors.get(device_type, "#95a5a6")

        circle_id = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color, outline="#2c3e50", width=2, tags=("device", f"device_{device_id}"))
        text_id = self.canvas.create_text(x, y, text=symbol, font=("Arial", 14), tags=("device", f"device_{device_id}"))
        label_id = self.canvas.create_text(x, y + 25, text=device_id, font=("Arial", 8), fill="#2c3e50", tags=("device", f"device_{device_id}"))

        self.device_items[device_id] = {
            "type": device_type, "armed": armed, "circle": circle_id,
            "text": text_id, "label": label_id,
        }

    def get_device_at(self, x: int, y: int) -> (str, str):
        """Find a device at the given coordinates."""
        items = self.canvas.find_overlapping(x - 5, y - 5, x + 5, y + 5)
        for item in items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("device_"):
                    device_id = tag.replace("device_", "")
                    if device_id in self.device_items:
                        return self.device_items[device_id]["type"], device_id
        return None, None
