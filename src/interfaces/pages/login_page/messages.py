"""
Message display component for the LoginPage.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple

def create_message_display(parent: tk.Widget) -> Tuple[ttk.Label, Optional[ttk.Label]]:
    """
    Creates the message display labels for status and info.
    """
    status_msg = ttk.Label(parent, text="", foreground='red')
    status_msg.pack(pady=5)
    
    return status_msg, None
