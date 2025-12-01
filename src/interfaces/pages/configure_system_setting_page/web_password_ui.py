import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_web_password_section(parent_frame: ttk.Frame) -> Tuple[tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar]:
    """
    Creates the UI section for web login password configuration.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A tuple containing tk.StringVars for
        (current_pw1, new_pw1, confirm_pw1, current_pw2, new_pw2, confirm_pw2).
    """
    web_frame = ttk.LabelFrame(parent_frame, text="Web Login Passwords (8+ chars)", padding=10)
    web_frame.pack(fill='x', pady=5)
    web_frame.columnconfigure((0, 1, 2, 3), weight=1)
    
    web_pw1_current = tk.StringVar()
    web_pw1 = tk.StringVar()
    web_pw1_confirm = tk.StringVar()
    web_pw2_current = tk.StringVar()
    web_pw2 = tk.StringVar()
    web_pw2_confirm = tk.StringVar()

    ttk.Label(web_frame, text="Password 1").grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 2))
    ttk.Label(web_frame, text="Current:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw1_current, show='*', width=20).grid(row=1, column=1, pady=2, sticky='w')
    ttk.Label(web_frame, text="New:").grid(row=1, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw1, show='*', width=20).grid(row=1, column=3, pady=2, sticky='w')
    ttk.Label(web_frame, text="Confirm:").grid(row=2, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw1_confirm, show='*', width=20).grid(row=2, column=3, pady=2, sticky='w')

    ttk.Separator(web_frame, orient='horizontal').grid(row=3, column=0, columnspan=4, sticky='ew', pady=5)

    ttk.Label(web_frame, text="Password 2").grid(row=4, column=0, columnspan=4, sticky='w', pady=(5, 2))
    ttk.Label(web_frame, text="Current:").grid(row=5, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw2_current, show='*', width=20).grid(row=5, column=1, pady=2, sticky='w')
    ttk.Label(web_frame, text="New:").grid(row=5, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw2, show='*', width=20).grid(row=5, column=3, pady=2, sticky='w')
    ttk.Label(web_frame, text="Confirm:").grid(row=6, column=2, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw2_confirm, show='*', width=20).grid(row=6, column=3, pady=2, sticky='w')
    
    return (
        web_pw1_current, web_pw1, web_pw1_confirm,
        web_pw2_current, web_pw2, web_pw2_confirm
    )
