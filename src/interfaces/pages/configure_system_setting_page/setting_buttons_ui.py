import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_buttons_section(parent_frame: ttk.Frame, save_command: Callable, reset_command: Callable) -> ttk.Label:
    """
    Creates the UI section for save and reset buttons, and the status message.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.
        save_command: The command to execute when the "Save All Settings" button is pressed.
        reset_command: The command to execute when the "Reset to Defaults" button is pressed.

    Returns:
        A ttk.Label widget for displaying status messages.
    """
    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack(pady=15)
    ttk.Button(btn_frame, text="Save All Settings", command=save_command, width=20).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Reset to Defaults", command=reset_command, width=20).pack(side='left', padx=5)
    
    status_label = ttk.Label(parent_frame, text="", font=('Arial', 10))
    status_label.pack(pady=5)
    
    return status_label
