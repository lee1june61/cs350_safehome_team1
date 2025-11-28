import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_web_password_section(parent_frame: ttk.Frame) -> Tuple[tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar]:
    """
    Creates the UI section for web login password configuration.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A tuple containing tk.StringVars for (web_pw1, web_pw1_confirm, web_pw2, web_pw2_confirm).
    """
    web_frame = ttk.LabelFrame(parent_frame, text="Web Login Passwords (8+ chars)", padding=10)
    web_frame.pack(fill='x', pady=5)
    
    web_pw1 = tk.StringVar()
    web_pw1_confirm = tk.StringVar()
    web_pw2 = tk.StringVar()
    web_pw2_confirm = tk.StringVar()
    
    ttk.Label(web_frame, text="Password 1:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw1, show='*', width=20).grid(row=0, column=1, pady=2)
    ttk.Label(web_frame, text="Confirm:").grid(row=0, column=2, sticky='e', padx=5)
    ttk.Entry(web_frame, textvariable=web_pw1_confirm, show='*', width=20).grid(row=0, column=3, pady=2)
    
    ttk.Label(web_frame, text="Password 2:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(web_frame, textvariable=web_pw2, show='*', width=20).grid(row=1, column=1, pady=2)
    ttk.Label(web_frame, text="Confirm:").grid(row=1, column=2, sticky='e', padx=5)
    ttk.Entry(web_frame, textvariable=web_pw2_confirm, show='*', width=20).grid(row=1, column=3, pady=2)
    
    return web_pw1, web_pw1_confirm, web_pw2, web_pw2_confirm
