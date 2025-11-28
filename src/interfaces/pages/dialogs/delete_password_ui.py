import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_delete_password_ui(
    parent_frame: ttk.Frame,
    delete_command: Callable[[], None],
    cancel_command: Callable[[], None]
) -> tk.StringVar:
    """
    Creates the UI elements for deleting a camera password.

    Args:
        parent_frame: The parent ttk.Frame.
        delete_command: The command for the delete button.
        cancel_command: The command for the cancel button.

    Returns:
        A StringVar for the password input.
    """
    ttk.Label(parent_frame, text="Enter current password to delete:").pack(anchor='w')
    pw_var = tk.StringVar()
    ttk.Entry(parent_frame, textvariable=pw_var, show='*', width=30).pack(pady=(5, 15))
    
    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack()
    ttk.Button(btn_frame, text="Delete", command=delete_command, width=12).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Cancel", command=cancel_command, width=12).pack(side='left', padx=5)
    
    return pw_var
