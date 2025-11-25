"""Booting screen view."""

import tkinter as tk
from .base_screen import BaseScreen
from ..config.ui_config import UIConfig


class BootingScreen(BaseScreen):
    """Booting screen - system starting up."""

    def build(self) -> tk.Frame:
        """Build booting screen."""
        frame = tk.Frame(self.parent, bg=UIConfig.WINDOW_BG)

        # Center content
        center = tk.Frame(frame, bg=UIConfig.WINDOW_BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            center,
            text="SafeHome Security System",
            font=("Arial", 28, "bold"),
            bg=UIConfig.WINDOW_BG,
        ).pack(pady=20)

        # Status
        tk.Label(
            center,
            text="⏳ STARTING SYSTEM...",
            font=("Arial", 20, "bold"),
            fg=UIConfig.COLOR_PRIMARY,
            bg=UIConfig.WINDOW_BG,
        ).pack(pady=30)

        # Progress message
        tk.Label(
            center, text="Please wait", font=UIConfig.FONT_LABEL, bg=UIConfig.WINDOW_BG
        ).pack(pady=10)

        return frame
