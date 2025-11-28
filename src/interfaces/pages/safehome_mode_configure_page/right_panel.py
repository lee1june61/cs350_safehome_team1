"""
Right panel for the SafeHomeModeConfigurePage, containing mode selection,
sensor list, and action buttons.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple, List

MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST']
MODE_DESCRIPTIONS = {
    'HOME': 'At home - perimeter sensors only',
    'AWAY': 'Away from home - all sensors active',
    'OVERNIGHT': 'Overnight travel - all except motion',
    'EXTENDED': 'Extended travel - all sensors active',
    'GUEST': 'Guest at home - same as HOME'
}

def create_right_panel(
    parent: tk.Widget,
    mode_var: tk.StringVar,
    load_mode_callback: Callable,
    save_mode_callback: Callable,
    reset_mode_callback: Callable,
    select_all_callback: Callable,
    clear_all_callback: Callable,
) -> Tuple[ttk.Label, tk.Listbox]:
    """
    Creates the right panel with mode configuration controls.
    """
    right = ttk.Frame(parent)
    right.grid(row=0, column=1, sticky='nsew')
    
    # Mode selection
    mode_frame = ttk.LabelFrame(right, text="Select Mode to Configure", padding=5)
    mode_frame.pack(fill='x')
    
    for mode in MODES:
        rb = ttk.Radiobutton(mode_frame, text=mode, variable=mode_var, 
                              value=mode, command=load_mode_callback)
        rb.pack(anchor='w', pady=1)
    
    # Mode description
    mode_desc_label = ttk.Label(mode_frame, text="", font=('Arial', 8), foreground='#666')
    mode_desc_label.pack(anchor='w', pady=(5, 0))
    
    # Sensor list for current mode
    sensor_frame = ttk.LabelFrame(right, text="Sensors in Mode", padding=5)
    sensor_frame.pack(fill='both', expand=True, pady=5)
    
    sensor_listbox = tk.Listbox(sensor_frame, height=6, font=('Arial', 9))
    sensor_listbox.pack(fill='both', expand=True)
    
    # Buttons
    btn_frame = ttk.Frame(right)
    btn_frame.pack(fill='x', pady=5)
    
    ttk.Button(btn_frame, text="Save Mode", command=save_mode_callback, width=12).pack(side='left', padx=2)
    ttk.Button(btn_frame, text="Reset Mode", command=reset_mode_callback, width=12).pack(side='left', padx=2)
    
    # Quick actions
    quick_frame = ttk.LabelFrame(right, text="Quick Actions", padding=5)
    quick_frame.pack(fill='x', pady=5)
    
    ttk.Button(quick_frame, text="Select All", command=select_all_callback, width=12).pack(side='left', padx=2)
    ttk.Button(quick_frame, text="Clear All", command=clear_all_callback, width=12).pack(side='left', padx=2)
    
    return mode_desc_label, sensor_listbox
