import tkinter as tk
from typing import Callable, Optional

def create_header(parent: tk.Frame, username: str) -> tk.Frame:
    """Create header with title and user info."""
    header = tk.Frame(parent, bg="#2c3e50", height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    tk.Label(
        header,
        text="SafeHome Control Panel",
        font=("Arial", 18, "bold"),
        fg="#ffffff",
        bg="#2c3e50",
    ).pack(side=tk.LEFT, padx=20, pady=15)

    user_frame = tk.Frame(header, bg="#2c3e50")
    user_frame.pack(side=tk.RIGHT, padx=20)

    tk.Label(
        user_frame,
        text=f"User: {username}",
        font=("Arial", 11),
        fg="#ffffff",
        bg="#2c3e50",
    ).pack()
    return header
