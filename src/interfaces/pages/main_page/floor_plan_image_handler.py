import tkinter as tk
from typing import Optional, Any
from pathlib import Path

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def find_floorplan_path() -> Optional[str]:
    """Find the floorplan.png file."""
    base_paths = [
        Path(__file__).parent.parent.parent.parent.parent /
        "virtual_device_v4" / "floorplan.png",
        Path("virtual_device_v4/floorplan.png"),
    ]
    for path in base_paths:
        if path.exists():
            return str(path.resolve())
    return None


class FloorPlanImageHandler:
    """Handles loading and drawing of the floor plan image."""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self._floorplan_image: Optional[ImageTk.PhotoImage] = None
        self._floorplan_path = find_floorplan_path()

    def draw_floor_plan(self, canvas_width: int, canvas_height: int) -> None:
        """Draw the floor plan - either from image or placeholder."""
        if self._load_floorplan_image(canvas_width, canvas_height):
            self._draw_floorplan_image()
        else:
            self._draw_placeholder_floor_plan()

    def _load_floorplan_image(self, canvas_width: int, canvas_height: int) -> bool:
        """Load the floorplan.png image."""
        if not HAS_PIL or not self._floorplan_path:
            return False
        
        try:
            pil_image = Image.open(self._floorplan_path)
            img_width, img_height = pil_image.size
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width, new_height = int(img_width * scale), int(img_height * scale)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self._floorplan_image = ImageTk.PhotoImage(pil_image)
            return True
        except Exception as e:
            print(f"Failed to load floorplan image: {e}")
            return False

    def _draw_floorplan_image(self) -> None:
        """Draw the loaded floorplan image on canvas."""
        if self._floorplan_image and self.canvas:
            self.canvas.create_image(400, 300, image=self._floorplan_image, anchor=tk.CENTER, tags='floorplan_bg')

    def _draw_placeholder_floor_plan(self) -> None:
        """Draw a placeholder floor plan."""
        rooms = [
            ("Living Room", 50, 50, 350, 250), ("Kitchen", 50, 270, 250, 450),
            ("Bedroom 1", 370, 50, 550, 250), ("Bedroom 2", 370, 270, 550, 450),
            ("Bathroom", 270, 270, 350, 350), ("Hallway", 270, 50, 350, 250),
        ]

        for name, x1, y1, x2, y2 in rooms:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ecf0f1", outline="#34495e", width=2, tags="floor_plan")
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(center_x, center_y, text=name, font=("Arial", 10, "bold"), fill="#7f8c8d", tags="floor_plan")
