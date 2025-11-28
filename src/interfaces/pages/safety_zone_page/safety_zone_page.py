"""SafetyZonePage - Safety zone management (SRS V.2.c-h)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page
from .left_panel import create_left_panel
from .right_panel import create_right_panel
from .zone_manager import ZoneManager


class SafetyZonePage(Page):
    """Safety Zone management with floorplan and sensor selection."""

    def _build_ui(self):
        self._create_header("Safety Zone Management", back_page='security')

        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=15, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        # Create left panel (floor plan)
        self._floorplan, self._sel_info = create_left_panel(
            content,
            on_sensor_selected=self._on_sensor_selected,
            on_device_click=self._on_device_click
        )

        # Create right panel (zone list and controls)
        callbacks = {
            'on_zone_select': self._on_zone_select,
            'arm_zone': self._arm_zone,
            'disarm_zone': self._disarm_zone,
            'create_zone': self._create_zone,
            'delete_zone': self._delete_zone,
            'edit_sensors': self._start_edit_sensors,
            'save_sensors': self._save_zone_sensors,
        }
        self._zone_list, self._status_label = create_right_panel(
            content, callbacks
        )

        # Initialize zone manager
        self._manager = ZoneManager(
            self, self._floorplan, self._zone_list,
            self._status_label, self._sel_info
        )

    def _on_zone_select(self, event):
        self._manager.on_zone_select(event)

    def _on_sensor_selected(self, sensor_id: str, dtype: str, selected: bool):
        self._manager.on_sensor_selected(sensor_id, dtype, selected)

    def _on_device_click(self, dev_id: str, dtype: str):
        self._manager.handle_device_click_info(dev_id, dtype)

    def _arm_zone(self):
        self._manager.arm_zone()

    def _disarm_zone(self):
        self._manager.disarm_zone()

    def _create_zone(self):
        self._manager.create_zone()

    def _start_edit_sensors(self):
        self._manager.start_edit_sensors()

    def _save_zone_sensors(self):
        self._manager.save_zone_sensors()

    def _delete_zone(self):
        self._manager.delete_zone()

    def on_show(self):
        self._manager.on_show()

