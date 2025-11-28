"""
Floor Plan component for the Main Page.
"""
import tkinter as tk
from typing import Callable, Optional
from ... import utils

from .floor_plan_legend_ui import create_floor_plan_legend_section
from .floor_plan_canvas_ui import create_floor_plan_canvas_section
from .floor_plan_instructions_ui import create_floor_plan_instructions_section
from .floor_plan_image_handler import FloorPlanImageHandler


class FloorPlan:
    """
    Manages the floor plan display, including loading the image and drawing placeholders.
    """
    def __init__(self, parent: tk.Widget, on_canvas_click: Callable):
        self.parent = parent
        self.on_canvas_click = on_canvas_click
        self.floor_plan_canvas: Optional[tk.Canvas] = None
        self._image_handler: Optional[FloorPlanImageHandler] = None

    def create_panel(self, parent: tk.Widget) -> tk.LabelFrame:
        """Create the floor plan panel."""
        panel = tk.LabelFrame(
            parent,
            text="🏠 House Floor Plan - Click devices to control",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            relief=tk.RIDGE,
            borderwidth=2,
        )

        create_floor_plan_legend_section(panel)

        self.floor_plan_canvas = create_floor_plan_canvas_section(panel, self.on_canvas_click)
        self._image_handler = FloorPlanImageHandler(self, self.floor_plan_canvas)
        self._image_handler.draw_floor_plan(800, 600) # Pass canvas dimensions

        create_floor_plan_instructions_section(panel)
        return panel

