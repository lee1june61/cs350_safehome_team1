"""
Message display component for the LoginPage.
"""
import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_message_display(parent: tk.Widget) -> Tuple[ttk.Label, ttk.Label]:
    """
    Creates the message display labels for status and info.
    """
    status_msg = ttk.Label(parent, text="", foreground='red')
    status_msg.pack(pady=5)
    
    info_msg = ttk.Label(parent, text="Default: admin / password / password", foreground='gray')
    info_msg.pack()
    
    return status_msg, info_msg
