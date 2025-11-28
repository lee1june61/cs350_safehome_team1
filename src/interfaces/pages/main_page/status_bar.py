"""
Status Bar component for the Main Page.
"""
import tkinter as tk

def create_status_bar(parent: tk.Frame) -> (tk.Frame, tk.Label):
    """Create the status bar at the bottom of the main page.

    Args:
        parent: The parent widget.

    Returns:
        A tuple containing the status bar frame and the status label.
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
    status_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH)

    # Connection indicator
    tk.Label(
        status_bar,
        text="🟢 Connected",
        font=("Arial", 9),
        bg="#ecf0f1",
        fg="#27ae60",
    ).pack(side=tk.RIGHT, padx=10)
    
    return status_bar, status_label
