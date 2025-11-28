"""
Login form component for the LoginPage.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_login_form(
    parent: tk.Widget,
    login_callback: Callable,
    user_var: tk.StringVar,
    pw1_var: tk.StringVar,
    pw2_var: tk.StringVar
) -> ttk.Button:
    """
    Creates the login form with User ID and password inputs.
    """
    f = ttk.LabelFrame(parent, text="Credentials", padding=15)
    f.pack(padx=20, pady=10)
    
    ttk.Label(f, text="User ID:").grid(row=0, column=0, sticky='e', pady=5)
    ttk.Entry(f, textvariable=user_var, width=25).grid(row=0, column=1, pady=5)
    
    ttk.Label(f, text="Password 1:").grid(row=1, column=0, sticky='e', pady=5)
    ttk.Entry(f, textvariable=pw1_var, show='*', width=25).grid(row=1, column=1, pady=5)
    
    ttk.Label(f, text="Password 2:").grid(row=2, column=0, sticky='e', pady=5)
    e = ttk.Entry(f, textvariable=pw2_var, show='*', width=25)
    e.grid(row=2, column=1, pady=5)
    e.bind('<Return>', lambda x: login_callback())
    
    login_btn = ttk.Button(f, text="Login", command=login_callback, width=15)
    login_btn.grid(row=3, column=0, columnspan=2, pady=15)
    
    return login_btn
