import tkinter as tk
from tkinter import ttk
from typing import Optional

class MainScreenUpdater:
    """
    Manages updating various UI elements on the MainScreen.
    """
    def __init__(self, status_indicator: ttk.Label, system_status_label: ttk.Label, status_label: ttk.Label):
        self.status_indicator = status_indicator
        self.system_status_label = system_status_label
        self.status_label = status_label

    def update_system_status(self, armed: bool, mode: str) -> None:
        """Update system armed/disarmed status and mode."""
        if armed:
            self.status_indicator.config(text="🔴", fg="#e74c3c")
            self.system_status_label.config(
                text=f"ARMED ({mode})",
                fg="#e74c3c",
            )
        else:
            self.status_indicator.config(text="🟢", fg="#27ae60")
            self.system_status_label.config(
                text="DISARMED",
                fg="#27ae60",
            )

    def update_status(self, message: str) -> None:
        """Update status bar message."""
        if self.status_label:
            self.status_label.config(text=message)
