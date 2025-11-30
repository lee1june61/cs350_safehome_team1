"""
Right panel for the SafetyZonePage, containing zone list and controls.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_right_panel(parent: tk.Widget, callbacks: dict) -> Tuple[tk.Listbox, ttk.Label]:
    """
    Creates the right panel with zone list, status, and management buttons.
    """
    right = ttk.Frame(parent)
    right.grid(row=0, column=1, sticky='nsew')
    
    # Zone list
    zone_frame = ttk.LabelFrame(right, text="Safety Zones", padding=5)
    zone_frame.pack(fill='both', expand=True)
    
    zone_list = tk.Listbox(zone_frame, height=8, font=('Arial', 10), selectmode='single')
    zone_list.pack(fill='both', expand=True)
    zone_list.bind('<<ListboxSelect>>', callbacks['on_zone_select'])
    
    status_label = ttk.Label(zone_frame, text="", font=('Arial', 9))
    status_label.pack(pady=3)
    
    # Arm/Disarm buttons
    arm_frame = ttk.Frame(right)
    arm_frame.pack(fill='x', pady=5)
    ttk.Button(arm_frame, text="🔴 Arm Zone", command=callbacks['arm_zone'], width=14).pack(side='left', padx=2)
    ttk.Button(arm_frame, text="⚪ Disarm Zone", command=callbacks['disarm_zone'], width=14).pack(side='left', padx=2)
    
    # Zone management buttons
    manage_frame = ttk.LabelFrame(right, text="Manage Zones", padding=5)
    manage_frame.pack(fill='x', pady=5)
    
    btn_row1 = ttk.Frame(manage_frame)
    btn_row1.pack(fill='x', pady=2)
    ttk.Button(btn_row1, text="Create Zone", command=callbacks['create_zone'], width=12).pack(side='left', padx=2)
    ttk.Button(btn_row1, text="Delete Zone", command=callbacks['delete_zone'], width=12).pack(side='left', padx=2)
    
    btn_row2 = ttk.Frame(manage_frame)
    btn_row2.pack(fill='x', pady=2)
    ttk.Button(btn_row2, text="Edit Zone", command=callbacks['edit_sensors'], width=12).pack(side='left', padx=2)
    
    # Help text
    help_text = (
        "• Select a zone, then click or drag on the floor plan to add sensors\n"
        "• Use the popup dialog's Finish button to save sensor changes\n"
        "• Green = Armed, Orange = Selected"
    )
    ttk.Label(right, text=help_text, font=('Arial', 8), foreground='#666').pack(pady=5)
    
    return zone_list, status_label
