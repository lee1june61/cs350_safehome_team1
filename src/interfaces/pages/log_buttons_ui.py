import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_log_buttons_section(parent_frame: ttk.Frame, load_command: Callable[[], None], clear_command: Callable[[], None]) -> ttk.Label:
    """
    Creates the UI section for log refresh and clear buttons, and the status message.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.
        load_command: The command to execute for refreshing the log.
        clear_command: The command to execute for clearing the log display.

    Returns:
        A ttk.Label widget for displaying status messages.
    """
    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack(fill='x', pady=10)
    
    ttk.Button(btn_frame, text="Refresh", command=load_command, width=12).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Clear Log", command=clear_command, width=12).pack(side='left', padx=5)
    
    status_label = ttk.Label(parent_frame, text="", font=('Arial', 9))
    status_label.pack()
    
    return status_label
