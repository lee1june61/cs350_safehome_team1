import tkinter as tk
from typing import Tuple

def create_status_display(parent: tk.Frame) -> Tuple[tk.Frame, tk.Label, tk.Label]:
    """Create system status display area.
    Returns: (status_frame, status_indicator_label, system_status_label)
    """
    status_frame = tk.LabelFrame(
        parent,
        text="System Status",
        font=("Arial", 14, "bold"),
        bg="#ffffff",
        relief=tk.RIDGE,
        borderwidth=2,
    )
    status_frame.pack(fill=tk.X, pady=(0, 20))

    indicator_frame = tk.Frame(status_frame, bg="#ffffff")
    indicator_frame.pack(pady=15)

    status_indicator = tk.Label(
        indicator_frame,
        text="⚫",
        font=("Arial", 48),
        bg="#ffffff",
    )
    status_indicator.pack(side=tk.LEFT, padx=20)

    status_text_frame = tk.Frame(indicator_frame, bg="#ffffff")
    status_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(
        status_text_frame,
        text="System:",
        font=("Arial", 11),
        bg="#ffffff",
    ).pack(anchor=tk.W)

    system_status_label = tk.Label(
        status_text_frame,
        text="DISARMED",
        font=("Arial", 16, "bold"),
        fg="#27ae60",
        bg="#ffffff",
    )
    system_status_label.pack(anchor=tk.W)
    return status_frame, status_indicator, system_status_label
