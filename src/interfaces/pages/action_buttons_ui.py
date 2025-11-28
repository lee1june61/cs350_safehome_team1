import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_action_buttons_section(parent_frame: ttk.Frame, enable_command: Callable[[], None], disable_command: Callable[[], None]) -> Tuple[ttk.Button, ttk.Button]:
    """
    Creates the UI section for camera action (enable/disable) buttons.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.
        enable_command: The command to execute for enabling the camera.
        disable_command: The command to execute for disabling the camera.

    Returns:
        A tuple containing the enable and disable buttons.
    """
    act_frame = ttk.LabelFrame(parent_frame, text="Actions", padding=8)
    act_frame.pack(fill='x', pady=5)
    
    _btn_en = ttk.Button(act_frame, text="Enable", command=enable_command, width=12)
    _btn_en.pack(pady=2)
    _btn_dis = ttk.Button(act_frame, text="Disable", command=disable_command, width=12)
    _btn_dis.pack(pady=2)
    
    return _btn_en, _btn_dis
