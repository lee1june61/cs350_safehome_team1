import tkinter as tk
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_page import MainPage
    from ...components.floor_plan import FloorPlan


class MainPageUpdater:
    """
    Manages updating various UI elements on the MainPage.
    """
    def __init__(self, page_instance: 'MainPage', floor_plan: 'FloorPlan', status_label: tk.Label, system_mode_label: tk.Label):
        self._page = page_instance
        self.floor_plan = floor_plan
        self.status_label = status_label
        self.system_mode_label = system_mode_label

    def set_device_armed_status(self, device_id: str, armed: bool):
        """Set the armed status of a device on the floor plan."""
        if self.floor_plan:
            self.floor_plan.set_armed(device_id, armed)
            self.floor_plan.refresh()

    def update_status(self, message: str):
        """Update the status bar message."""
        if self.status_label:
            self.status_label.config(text=message)

    def update_system_mode(self, mode_text: str, color: str):
        """Update the system mode display."""
        if self.system_mode_label:
            self.system_mode_label.config(text=mode_text, fg=color)
            
    def refresh_floor_plan(self):
        """Refreshes the floor plan when the page is shown."""
        if self.floor_plan:
            self.floor_plan.refresh()
