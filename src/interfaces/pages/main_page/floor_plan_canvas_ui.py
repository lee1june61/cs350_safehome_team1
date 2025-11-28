import tkinter as tk
from typing import Callable, Optional

def create_floor_plan_canvas_section(parent_frame: tk.Widget, on_canvas_click: Callable) -> tk.Canvas:
    """
    Creates the canvas section for the floor plan.

    Args:
        parent_frame: The parent widget.
        on_canvas_click: The callback function for canvas clicks.

    Returns:
        The tk.Canvas widget for the floor plan.
    """
    canvas_frame = tk.Frame(parent_frame, bg="#ffffff")
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    floor_plan_canvas = tk.Canvas(
        canvas_frame,
        width=800,
        height=600,
        bg="#f5f5f5",
        highlightthickness=1,
        highlightbackground="#bdc3c7",
    )
    floor_plan_canvas.pack(fill=tk.BOTH, expand=True)
    floor_plan_canvas.bind("<Button-1>", on_canvas_click)
    
    return floor_plan_canvas
