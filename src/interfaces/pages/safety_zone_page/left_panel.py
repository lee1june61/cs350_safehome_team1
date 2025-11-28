"""
Left panel for the SafetyZonePage, containing the floor plan.
"""
import tkinter as tk
from tkinter import ttk
from ...components.floor_plan import FloorPlan
from typing import Callable, Tuple

def create_left_panel(
    parent: tk.Widget,
    on_sensor_selected: Callable,
    on_device_click: Callable
) -> Tuple[FloorPlan, ttk.Label]:
    """
    Creates the left panel with the floor plan and selection info.
    """
    left = ttk.LabelFrame(parent, text="Floor Plan - Click sensors to select", padding=5)
    left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    floorplan = FloorPlan(left, 420, 280, show_cameras=False, show_sensors=True)
    floorplan.create().pack(fill='both', expand=True)
    floorplan.set_on_sensor_click(on_sensor_selected)
    floorplan.set_on_click(on_device_click)
    
    sel_info = ttk.Label(left, text="Selected sensors: None", font=('Arial', 9))
    sel_info.pack(pady=(5, 0))
    
    return floorplan, sel_info
