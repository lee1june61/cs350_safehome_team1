"""
Verification UI component for the Security Page.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_verification_ui(
    parent: tk.Widget,
    verify_callback: Callable[[], None]
) -> Tuple[tk.StringVar, ttk.Entry, ttk.Button, ttk.Label]:
    """
    Creates the identity verification UI components.

    Args:
        parent: The parent widget.
        verify_callback: The callback function for the verify button.

    Returns:
        A tuple containing the string variable for the entry, the entry widget,
        the verify button, and the status label.
    """
    vf = ttk.LabelFrame(parent, text="Identity Confirmation", padding=10)
    vf.pack(fill='x', padx=30, pady=10)
    
    ttk.Label(vf, text="Phone or Address:").pack(side='left')
    val = tk.StringVar()
    entry = ttk.Entry(vf, textvariable=val, width=30)
    entry.pack(side='left', padx=5)
    verify_btn = ttk.Button(vf, text="Verify", command=verify_callback)
    verify_btn.pack(side='left')
    status_label = ttk.Label(vf, text="")
    status_label.pack(side='left', padx=10)
    
    return val, entry, verify_btn, status_label
