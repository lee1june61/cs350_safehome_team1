import tkinter as tk
from typing import Callable

def create_styled_button(
    parent: tk.Frame,
    text: str,
    command: Callable[[], None],
    bg_color: str,
) -> tk.Button:
    """Create a styled button."""
    return tk.Button(
        parent,
        text=text,
        font=("Arial", 12, "bold"),
        bg=bg_color,
        fg="#ffffff",
        width=12,
        height=2,
        relief=tk.RAISED,
        borderwidth=3,
        command=command,
        cursor="hand2",
    )
