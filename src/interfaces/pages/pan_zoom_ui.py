import tkinter as tk
from tkinter import ttk
from typing import Callable

def create_pan_zoom_section(parent_frame: ttk.Frame, pan_command: Callable[[str], None], zoom_command: Callable[[str], None]) -> None:
    """
    Creates the UI section for pan and zoom controls.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.
        pan_command: The command to execute for pan actions.
        zoom_command: The command to execute for zoom actions.
    """
    ptz_frame = ttk.LabelFrame(parent_frame, text="Pan/Zoom", padding=8)
    ptz_frame.pack(fill='x', pady=5)
    
    pf = ttk.Frame(ptz_frame)
    pf.pack()
    ttk.Button(pf, text="◄ L", command=lambda: pan_command('L'), width=6).pack(side='left', padx=2)
    ttk.Button(pf, text="R ►", command=lambda: pan_command('R'), width=6).pack(side='left', padx=2)
    
    zf = ttk.Frame(ptz_frame)
    zf.pack(pady=5)
    ttk.Button(zf, text="+ In", command=lambda: zoom_command('in'), width=6).pack(side='left', padx=2)
    ttk.Button(zf, text="- Out", command=lambda: zoom_command('out'), width=6).pack(side='left', padx=2)
