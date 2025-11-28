"""System OFF screen view."""

import tkinter as tk
from .base_screen import BaseScreen
from ..config.ui_config import UIConfig


class SystemOffScreen(BaseScreen):
    """System OFF screen - initial state."""

    def __init__(self, parent: tk.Widget, on_power_on):
        """Initialize system OFF screen.

        Args:
            parent: Parent widget
            on_power_on: Callback for power on button
        """
        super().__init__(parent)
        self.on_power_on = on_power_on

    def build(self) -> tk.Frame:
        """Build system OFF screen."""
        frame = tk.Frame(self.parent, bg=UIConfig.WINDOW_BG)

        # Center content
        center = tk.Frame(frame, bg=UIConfig.WINDOW_BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            center,
            text="SafeHome Security System",
            font=UIConfig.FONT_TITLE,
            bg=UIConfig.WINDOW_BG,
        ).pack(pady=20)

        # Status
        tk.Label(
            center,
            text="SYSTEM OFF",
            font=UIConfig.FONT_SUBTITLE,
            fg=UIConfig.COLOR_DANGER,
            bg=UIConfig.WINDOW_BG,
        ).pack(pady=20)

        # Power button
        tk.Button(
            center,
            text="⚡ POWER ON",
            font=("Arial", 20, "bold"),
            bg=UIConfig.COLOR_SUCCESS,
            fg=UIConfig.COLOR_WHITE,
            width=15,
            height=2,
            command=self.on_power_on,
        ).pack(pady=30)

        return frame
