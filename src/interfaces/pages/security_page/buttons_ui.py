"""
Buttons UI component for the Security Page.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List

def create_buttons_ui(
    parent: tk.Widget,
    navigate_callback: Callable[[str], None]
) -> List[tk.Button]:
    """
    Creates the main function buttons for the security page.

    Args:
        parent: The parent widget.
        navigate_callback: The callback function for navigation.

    Returns:
        A list of the created button widgets.
    """
    bf = ttk.Frame(parent)
    bf.pack(expand=True, fill='both', padx=30, pady=10)
    bf.columnconfigure(0, weight=1)
    
    buttons = []
    items = [
        ("Safety Zone", 'safety_zone'),
        ("Set SafeHome Mode", 'safehome_mode'),
        ("View Intrusion Log", 'view_log'),
        ("Redefine Security Modes", 'safehome_mode_configure')
    ]
    
    for i, (txt, page) in enumerate(items):
        b = tk.Button(
            bf,
            text=txt,
            font=('Arial', 14),
            bg='#607D8B',
            fg='white',
            height=2,
            state='disabled',
            command=lambda p=page: navigate_callback(p)
        )
        b.grid(row=i, column=0, sticky='ew', pady=8, padx=20)
        buttons.append(b)
        
    return buttons
