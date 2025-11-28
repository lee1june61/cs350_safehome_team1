import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_sensor_list_ui(parent_frame: ttk.Frame) -> tk.Listbox:
    """
    Creates the UI elements for the sensor listbox.

    Args:
        parent_frame: The parent ttk.Frame.

    Returns:
        A Listbox for selecting sensors.
    """
    ttk.Label(parent_frame, text="Select Sensors:").pack(anchor='w')
    
    list_frame = ttk.Frame(parent_frame)
    list_frame.pack(fill='both', expand=True, pady=(5, 15))
    scrollbar = ttk.Scrollbar(list_frame)
    scrollbar.pack(side='right', fill='y')
    listbox = tk.Listbox(list_frame, selectmode='multiple', 
                                   yscrollcommand=scrollbar.set, height=10)
    listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=listbox.yview)
    
    return listbox
