import tkinter as tk
from tkinter import ttk
from typing import Callable

def create_action_buttons_ui(parent_frame: ttk.Frame, mode: str, save_command: Callable[[], None], cancel_command: Callable[[], None]) -> None:
    """
    Creates the UI elements for the action buttons (Create/Update, Cancel).

    Args:
        parent_frame: The parent ttk.Frame.
        mode: The dialog mode ('create' or 'update').
        save_command: The command for the save/update button.
        cancel_command: The command for the cancel button.
    """
    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack()
    ttk.Button(btn_frame, text='Create' if mode == 'create' else 'Update', 
              command=save_command, width=12).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Cancel", command=cancel_command, width=12).pack(side='left', padx=5)
