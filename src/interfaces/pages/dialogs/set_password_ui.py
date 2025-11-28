import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional, Tuple, Callable

def create_set_password_ui(
    parent_frame: ttk.Frame,
    camera: Dict,
    set_command: Callable[[], None],
    cancel_command: Callable[[], None]
) -> Tuple[Optional[tk.StringVar], tk.StringVar, tk.StringVar]:
    """
    Creates the UI elements for setting a camera password.

    Args:
        parent_frame: The parent ttk.Frame.
        camera: The camera dictionary.
        set_command: The command for the set button.
        cancel_command: The command for the cancel button.

    Returns:
        A tuple of (old_var, new_var, confirm_var) StringVars.
    """
    old_var: Optional[tk.StringVar] = None
    if camera.get('has_password'):
        ttk.Label(parent_frame, text="Current Password:").pack(anchor='w')
        old_var = tk.StringVar()
        ttk.Entry(parent_frame, textvariable=old_var, show='*', width=30).pack(pady=(5, 10))
    
    ttk.Label(parent_frame, text="New Password (min 4 chars):").pack(anchor='w')
    new_var = tk.StringVar()
    ttk.Entry(parent_frame, textvariable=new_var, show='*', width=30).pack(pady=(5, 10))
    
    ttk.Label(parent_frame, text="Confirm Password:").pack(anchor='w')
    confirm_var = tk.StringVar()
    ttk.Entry(parent_frame, textvariable=confirm_var, show='*', width=30).pack(pady=(5, 15))
    
    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack()
    ttk.Button(btn_frame, text="Set", command=set_command, width=12).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Cancel", command=cancel_command, width=12).pack(side='left', padx=5)
    
    return old_var, new_var, confirm_var
