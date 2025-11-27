"""Safety zone creation window."""

import tkinter as tk
from tkinter import messagebox
from typing import Set, List, Callable
from ..models.device_icon import DeviceIcon


class ZoneCreationWindow:
    """Window for creating new safety zones.

    Following the SafetyZone configuration from SDS document.
    """

    def __init__(
        self,
        parent: tk.Widget,
        zone_name: str,
        devices: List[DeviceIcon],
        on_finish: Callable[[str, List[int]], None],
        on_cancel: Callable,
    ):
        """Initialize zone creation window.

        Args:
            parent: Parent widget
            zone_name: Name for the new zone
            devices: List of all devices
            on_finish: Callback when zone creation is finished
            on_cancel: Callback when cancelled
        """
        self.parent = parent
        self.zone_name = zone_name
        self.devices = devices
        self.on_finish = on_finish
        self.on_cancel = on_cancel

        self.window: tk.Toplevel = None
        self.selected_sensors: Set[int] = set()
        self.count_label: tk.Label = None
        self.listbox: tk.Listbox = None

    def show(self):
        """Show zone creation window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Create Safety Zone")
        self.window.geometry("400x250")
        self.window.protocol("WM_DELETE_WINDOW", self._handle_cancel)

        # Title
        tk.Label(
            self.window,
            text=f"Creating Zone: {self.zone_name}",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        # Instructions
        tk.Label(
            self.window,
            text="Click sensors on the floor plan to add them to this zone.\nSelected sensors will be highlighted in yellow.",
            font=("Arial", 10),
        ).pack(pady=10)

        # Selected count
        self.count_label = tk.Label(
            self.window, text="Selected sensors: 0", font=("Arial", 11, "bold")
        )
        self.count_label.pack(pady=10)

        # Sensor list
        list_frame = tk.LabelFrame(self.window, text="Selected Sensors")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, height=4)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="✓ Finish",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self._handle_finish,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="✗ Cancel",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=12,
            command=self._handle_cancel,
        ).pack(side=tk.LEFT, padx=5)

    def update_selection(self, selected_sensor_ids: Set[int]):
        """Update the display with current selection.

        Args:
            selected_sensor_ids: Set of selected sensor IDs
        """
        self.selected_sensors = selected_sensor_ids

        # Update count
        self.count_label.config(text=f"Selected sensors: {len(self.selected_sensors)}")

        # Update listbox
        self.listbox.delete(0, tk.END)
        for device in self.devices:
            if device.device_id in self.selected_sensors and device.is_sensor:
                self.listbox.insert(
                    tk.END, f"  • {device.name} (ID: {device.device_id})"
                )

    def _handle_finish(self):
        """Handle finish button."""
        if len(self.selected_sensors) == 0:
            messagebox.showwarning(
                "No Sensors",
                "Please select at least one sensor for the zone.",
                parent=self.window,
            )
            return

        self.on_finish(self.zone_name, list(self.selected_sensors))

    def _handle_cancel(self):
        """Handle cancel button."""
        self.on_cancel()

    def close(self):
        """Close the window."""
        if self.window:
            self.window.destroy()
            self.window = None
