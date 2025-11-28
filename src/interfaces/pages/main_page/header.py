"""
Header component for the Main Page.
"""
import tkinter as tk
from typing import Callable

def create_header(
    parent: tk.Widget,
    username: str,
    on_logout: Callable[[], None]
) -> tk.Frame:
    """Create the header frame for the main page.

    Args:
        parent: The parent widget.
        username: The username to display.
        on_logout: The callback function for the logout button.

    Returns:
        The header frame.
    """
    header = tk.Frame(parent, bg="#2c3e50", height=70)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    # Title
    title_frame = tk.Frame(header, bg="#2c3e50")
    title_frame.pack(side=tk.LEFT, padx=20)

    tk.Label(
        title_frame,
        text="SafeHome Web Interface",
        font=("Arial", 18, "bold"),
        fg="#ffffff",
        bg="#2c3e50",
    ).pack()

    tk.Label(
        title_frame,
        text="Remote Access & Monitoring",
        font=("Arial", 10),
        fg="#bdc3c7",
        bg="#2c3e50",
    ).pack()

    # User info
    user_frame = tk.Frame(header, bg="#2c3e50")
    user_frame.pack(side=tk.RIGHT, padx=20)

    tk.Label(
        user_frame,
        text=f"👤 {username}",
        font=("Arial", 12),
        fg="#ffffff",
        bg="#2c3e50",
    ).pack()

    tk.Button(
        user_frame,
        text="Logout",
        font=("Arial", 9),
        command=on_logout,
        bg="#e74c3c",
        fg="#ffffff",
        relief=tk.FLAT,
        padx=10,
        pady=3,
    ).pack(pady=(5, 0))
    
    return header
