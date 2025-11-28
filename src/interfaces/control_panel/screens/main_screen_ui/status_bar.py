import tkinter as tk
from typing import Callable

def create_status_bar(parent: tk.Frame, on_logout: Callable[[], None]) -> tuple[tk.Frame, tk.Label]:
    """Create status bar at bottom.
    Returns: (status_bar_frame, status_message_label)
    """
    status_bar = tk.Frame(parent, bg="#ecf0f1", height=30)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    status_bar.pack_propagate(False)

    status_label = tk.Label(
        status_bar,
        text="Ready",
        font=("Arial", 9),
        bg="#ecf0f1",
        anchor=tk.W,
    )
    status_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    tk.Button(
        status_bar,
        text="Logout",
        font=("Arial", 9),
        command=on_logout,
        relief=tk.FLAT,
        bg="#ecf0f1",
    ).pack(side=tk.RIGHT, padx=10)
    return status_bar, status_label
