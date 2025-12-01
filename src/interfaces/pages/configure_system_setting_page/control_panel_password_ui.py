import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_control_panel_password_section(parent_frame: ttk.Frame) -> Tuple[tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar]:
    """
    Creates the UI section for control panel password configuration.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A tuple containing tk.StringVars for
        (master_current, master_new, master_confirm, guest_current, guest_new, guest_confirm).
    """
    panel_frame = ttk.LabelFrame(parent_frame, text="Control Panel Passwords (4 digits)", padding=10)
    panel_frame.pack(fill='x', pady=5)
    panel_frame.columnconfigure((0, 1, 2, 3), weight=1)
    
    master_pw_current = tk.StringVar()
    master_pw = tk.StringVar()
    master_pw_confirm = tk.StringVar()
    guest_pw_current = tk.StringVar()
    guest_pw = tk.StringVar()
    guest_pw_confirm = tk.StringVar()
    
    ttk.Label(panel_frame, text="Master Password").grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 2))
    ttk.Label(panel_frame, text="Current:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=master_pw_current, show='*', width=15).grid(row=1, column=1, pady=2, sticky='w')
    ttk.Label(panel_frame, text="New:").grid(row=1, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=master_pw, show='*', width=15).grid(row=1, column=3, pady=2, sticky='w')
    ttk.Label(panel_frame, text="Confirm:").grid(row=2, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=master_pw_confirm, show='*', width=15).grid(row=2, column=3, pady=2, sticky='w')
    
    ttk.Separator(panel_frame, orient='horizontal').grid(row=3, column=0, columnspan=4, sticky='ew', pady=5)
    
    ttk.Label(panel_frame, text="Guest Password").grid(row=4, column=0, columnspan=4, sticky='w', pady=(5, 2))
    ttk.Label(panel_frame, text="Current:").grid(row=5, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=guest_pw_current, show='*', width=15).grid(row=5, column=1, pady=2, sticky='w')
    ttk.Label(panel_frame, text="New:").grid(row=5, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=guest_pw, show='*', width=15).grid(row=5, column=3, pady=2, sticky='w')
    ttk.Label(panel_frame, text="Confirm:").grid(row=6, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(panel_frame, textvariable=guest_pw_confirm, show='*', width=15).grid(row=6, column=3, pady=2, sticky='w')
    ttk.Label(panel_frame, text="(Guest password can be empty)", font=('Arial', 8)).grid(row=7, column=0, columnspan=4)
    
    return (
        master_pw_current, master_pw, master_pw_confirm,
        guest_pw_current, guest_pw, guest_pw_confirm
    )
