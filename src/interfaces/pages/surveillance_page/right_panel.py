"""
Right panel for the Surveillance Page, with buttons and camera list.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

def create_right_panel(
    parent: tk.Widget,
    navigate_callback: Callable[[str], None],
    on_list_double_click: Callable
) -> Tuple[tk.Listbox]:
    """
    Creates the right panel with navigation buttons and a camera list.
    """
    right = ttk.Frame(parent)
    right.grid(row=0, column=1, sticky='nsew')
    
    tk.Button(right, text="Pick a Camera", font=('Arial', 12), bg='#2196F3', fg='white',
             height=2, command=lambda: navigate_callback('camera_list')).pack(fill='x', pady=5)
    tk.Button(right, text="All Cameras", font=('Arial', 12), bg='#4CAF50', fg='white',
             height=2, command=lambda: navigate_callback('thumbnail_view')).pack(fill='x', pady=5)
    
    lf = ttk.LabelFrame(right, text="Cameras", padding=5)
    lf.pack(fill='both', expand=True, pady=10)
    
    listbox = tk.Listbox(lf, font=('Arial', 10))
    listbox.pack(fill='both', expand=True)
    listbox.bind('<Double-Button-1>', on_list_double_click)
    
    ttk.Label(right, text="Double-click to view", foreground='gray').pack()
    
    return listbox
