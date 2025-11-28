import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_camera_list_right_panel_ui(
    parent_frame: ttk.Frame,
    on_select: Callable[[Any], None],
    view_command: Callable[[], None]
) -> Tuple[tk.Listbox, ttk.Label, ttk.Button]:
    """
    Creates the right panel UI for the camera list page, featuring a camera list, info, and view button.

    Args:
        parent_frame: The parent ttk.Frame.
        on_select: Callback for when an item in the listbox is selected.
        view_command: Command for the "View Camera" button.

    Returns:
        A tuple containing the Listbox, info Label, and View Camera Button.
    """
    right = ttk.Frame(parent_frame)
    right.grid(row=0, column=1, sticky='nsew')
    
    lf = ttk.LabelFrame(right, text="Cameras", padding=5)
    lf.pack(fill='both', expand=True)
    _list = tk.Listbox(lf, font=('Arial', 10), height=10)
    _list.pack(fill='both', expand=True)
    _list.bind('<<ListboxSelect>>', on_select)
    
    info = ttk.LabelFrame(right, text="Info", padding=5)
    info.pack(fill='x', pady=5)
    _info = ttk.Label(info, text="Select a camera")
    _info.pack()
    
    _btn = ttk.Button(right, text="View Camera", command=view_command, state='disabled')
    _btn.pack(pady=10)
    
    return _list, _info, _btn
