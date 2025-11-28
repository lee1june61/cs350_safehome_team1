import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_system_status_section(parent_frame: tk.Widget) -> Tuple[tk.Frame, tk.Label]:
    """
    Creates the system status display section for the control panel.

    Args:
        parent_frame: The parent widget.

    Returns:
        A tuple containing the status frame and the system mode label.
    """
    status_frame = tk.LabelFrame(
        parent_frame,
        text="System Status",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        relief=tk.RIDGE,
        borderwidth=2,
    )
    status_frame.pack(fill=tk.X, pady=(0, 15))

    mode_container = tk.Frame(status_frame, bg="#ffffff")
    mode_container.pack(pady=10)

    tk.Label(
        mode_container,
        text="Current Mode:",
        font=("Arial", 10),
        bg="#ffffff",
    ).pack()

    system_mode_label = tk.Label(
        mode_container,
        text="HOME", # Default text, will be updated dynamically
        font=("Arial", 14, "bold"),
        fg="#27ae60", # Default color, will be updated dynamically
        bg="#ffffff",
    )
    system_mode_label.pack(pady=5)
    
    return status_frame, system_mode_label
