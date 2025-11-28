import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_control_panel_password_section(parent_frame: ttk.Frame) -> Tuple[tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar]:
    """
    Creates the UI section for control panel password configuration.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A tuple containing tk.StringVars for (master_pw, master_pw_confirm, guest_pw, guest_pw_confirm).
    """
    panel_frame = ttk.LabelFrame(parent_frame, text="Control Panel Passwords (4 digits)", padding=10)
    panel_frame.pack(fill='x', pady=5)
    
    master_pw = tk.StringVar()
    master_pw_confirm = tk.StringVar()
    guest_pw = tk.StringVar()
    guest_pw_confirm = tk.StringVar()
    
    ttk.Label(panel_frame, text="Master Password:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=master_pw, show='*', width=15).grid(row=0, column=1, pady=2)
    ttk.Label(panel_frame, text="Confirm:").grid(row=0, column=2, sticky='e', padx=5)
    ttk.Entry(panel_frame, textvariable=master_pw_confirm, show='*', width=15).grid(row=0, column=3, pady=2)
    
    ttk.Label(panel_frame, text="Guest Password:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=guest_pw, show='*', width=15).grid(row=1, column=1, pady=2)
    ttk.Label(panel_frame, text="Confirm:").grid(row=1, column=2, sticky='e', padx=5)
    ttk.Entry(panel_frame, textvariable=guest_pw_confirm, show='*', width=15).grid(row=1, column=3, pady=2)
    ttk.Label(panel_frame, text="(Guest password can be empty)", font=('Arial', 8)).grid(row=2, column=0, columnspan=4)
    
    return master_pw, master_pw_confirm, guest_pw, guest_pw_confirm
