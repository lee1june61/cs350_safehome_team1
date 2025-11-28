"""
Left panel for the Surveillance Page, containing the floor plan.
"""
import tkinter as tk
from tkinter import ttk
from ...components.floor_plan import FloorPlan
from typing import Callable

def create_left_panel(
    parent: tk.Widget,
    on_device_click: Callable[[str, str], None]
) -> FloorPlan:
    """
    Creates the left panel with the floor plan.
    """
    left = ttk.LabelFrame(parent, text="Floor Plan - Click camera", padding=5)
    left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    floorplan = FloorPlan(left, 400, 320, show_sensors=False) # Only show cameras
    floorplan.set_on_click(on_device_click)
    floorplan.create().pack()
    
    return floorplan
