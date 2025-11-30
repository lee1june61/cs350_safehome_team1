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
    mode_change_callback: Callable[[str], None],
    edit_mode_callback: Callable[[], None],
) -> ttk.Label:
    """
    Creates the right panel with mode configuration controls.
    """
    right = ttk.Frame(parent)
    right.grid(row=0, column=1, sticky='nsew')

    # Mode selection
    mode_frame = ttk.LabelFrame(right, text="Select Mode to Configure", padding=5)
    mode_frame.pack(fill='x')

    for mode in MODES:
        rb = ttk.Radiobutton(
            mode_frame,
            text=mode,
            variable=mode_var,
            value=mode,
            command=lambda m=mode: mode_change_callback(m),
        )
        rb.pack(anchor='w', pady=1)

    ttk.Button(
        mode_frame,
        text="Edit Mode",
        command=edit_mode_callback,
        width=14,
    ).pack(anchor='center', pady=(6, 0))

    mode_desc_label = ttk.Label(mode_frame, text="", font=('Arial', 8), foreground='#666')
    mode_desc_label.pack(anchor='w', pady=(5, 0))

    # Placeholder frame to keep layout consistent
    ttk.Label(
        right,
        text="Use 'Edit Mode' to adjust sensor assignments.\nChanges are shown in the popup.",
        foreground="#777",
        padding=10,
        anchor="center",
        justify="center",
    ).pack(fill="both", expand=True, pady=20)

    return mode_desc_label
