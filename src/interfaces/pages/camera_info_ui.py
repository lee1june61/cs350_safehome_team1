import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_camera_info_section(parent_frame: ttk.Frame) -> ttk.Label:
    """
    Creates the UI section for displaying camera information.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A ttk.Label widget to display camera info.
    """
    info_frame = ttk.LabelFrame(parent_frame, text="Camera Info", padding=8)
    info_frame.pack(fill='x', pady=5)
    _info_label = ttk.Label(info_frame, text="")
    _info_label.pack(anchor='w')
    return _info_label
