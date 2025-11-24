"""UI helper functions."""

import tkinter as tk
from typing import Tuple, List


def create_labeled_frame(parent: tk.Widget, text: str, **kwargs) -> tk.LabelFrame:
    """Create a labeled frame with consistent styling."""
    return tk.LabelFrame(parent, text=text, **kwargs)


def create_button(parent: tk.Widget, text: str, command, **kwargs) -> tk.Button:
    """Create a button with consistent styling."""
    return tk.Button(parent, text=text, command=command, **kwargs)


def create_keypad(parent: tk.Widget, callback) -> tk.Frame:
    """Create numeric keypad.

    Args:
        parent: Parent widget
        callback: Function to call with button value

    Returns:
        Frame containing keypad
    """
    keypad = tk.Frame(parent, bg="white")

    buttons = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["C", "0", "✓"]]

    for row in buttons:
        row_frame = tk.Frame(keypad, bg="white")
        row_frame.pack()

        for btn_text in row:
            if btn_text == "C":
                bg_color = "#f44336"
            elif btn_text == "✓":
                bg_color = "#4CAF50"
            else:
                bg_color = "#e0e0e0"

            btn = tk.Button(
                row_frame,
                text=btn_text,
                font=("Arial", 18, "bold"),
                width=4,
                height=2,
                bg=bg_color,
                command=lambda x=btn_text: callback(x),
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    return keypad


def center_window(window: tk.Tk, width: int, height: int):
    """Center window on screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
