import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_zone_name_ui(parent_frame: ttk.Frame) -> tk.StringVar:
    """
    Creates the UI elements for the zone name input.

    Args:
        parent_frame: The parent ttk.Frame.

    Returns:
        A StringVar for the zone name input.
    """
    ttk.Label(parent_frame, text="Zone Name:").pack(anchor='w')
    name_var = tk.StringVar()
    ttk.Entry(parent_frame, textvariable=name_var, width=40).pack(pady=(5, 15))
    return name_var
