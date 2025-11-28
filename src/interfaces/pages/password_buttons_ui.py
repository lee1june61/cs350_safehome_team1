import tkinter as tk
from tkinter import ttk
from typing import Callable

def create_password_buttons_section(parent_frame: ttk.Frame, set_pw_command: Callable[[], None], del_pw_command: Callable[[], None]) -> None:
    """
    Creates the UI section for camera password management buttons.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.
        set_pw_command: The command to execute for setting the password.
        del_pw_command: The command to execute for deleting the password.
    """
    pw_frame = ttk.LabelFrame(parent_frame, text="Password", padding=8)
    pw_frame.pack(fill='x', pady=5)
    ttk.Button(pw_frame, text="Set Password", command=set_pw_command, width=12).pack(pady=2)
    ttk.Button(pw_frame, text="Delete Password", command=del_pw_command, width=12).pack(pady=2)
