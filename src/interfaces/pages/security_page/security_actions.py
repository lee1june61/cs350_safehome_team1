"""Helper utilities for building security action buttons."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, List


ACTION_ITEMS = [
    ("Safety Zone", "safety_zone"),
    ("Set SafeHome Mode", "safehome_mode"),
    ("View Intrusion Log", "view_log"),
    ("Redefine Security Modes", "safehome_mode_configure"),
]


def create_security_actions(parent: tk.Widget, navigate_cb: Callable[[str], None]) -> List[tk.Button]:
    """Create action buttons and return the button list."""
    frame = ttk.Frame(parent)
    frame.pack(expand=True, fill="both", padx=30, pady=10)
    frame.columnconfigure(0, weight=1)

    buttons: List[tk.Button] = []
    for row, (label, page_name) in enumerate(ACTION_ITEMS):
        btn = tk.Button(
            frame,
            text=label,
            font=("Arial", 14),
            bg="#607D8B",
            fg="white",
            height=2,
            state="disabled",
            command=lambda p=page_name: navigate_cb(p),
        )
        btn.grid(row=row, column=0, sticky="ew", pady=8, padx=20)
        buttons.append(btn)
    return buttons





