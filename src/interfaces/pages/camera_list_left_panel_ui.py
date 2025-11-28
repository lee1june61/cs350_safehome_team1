import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple
from ..components.floor_plan import FloorPlan

def create_camera_list_left_panel_ui(parent_frame: ttk.Frame, on_map_click: Callable[[str, str], None]) -> FloorPlan:
    """
    Creates the left panel UI for the camera list page, featuring a floor plan.

    Args:
        parent_frame: The parent ttk.Frame.
        on_map_click: Callback for when a camera is clicked on the floor plan.

    Returns:
        The FloorPlan instance used in the left panel.
    """
    left = ttk.LabelFrame(parent_frame, text="Click camera on map", padding=5)
    left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    floorplan = FloorPlan(left, on_map_click) # FloorPlan now handles its own dimensions
    fp_canvas = floorplan.create_panel(left) # Use create_panel from the FloorPlan class
    fp_canvas.pack(fill='both', expand=True)
    return floorplan
