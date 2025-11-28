"""
ModeConfigManager - A helper class to manage SafeHome mode configuration logic
for the SafeHomeModeConfigurePage.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Set, List, Dict, Any, TYPE_CHECKING

from .mode_ui_updater import ModeUIUpdater
from .sensor_selection_handler import SensorSelectionHandler
from .mode_configuration_handler import ModeConfigurationHandler

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ModeConfigManager:
    MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST'] # Keep for external reference if needed

    def __init__(self, page: Any, floorplan: 'FloorPlan', sel_info_label: ttk.Label, mode_var: tk.StringVar, mode_desc_label: ttk.Label, sensor_listbox: tk.Listbox):
        self.page = page
        self.floorplan = floorplan
        self.sel_info_label = sel_info_label
        self.mode_var = mode_var
        self.mode_desc_label = mode_desc_label
        self.sensor_listbox = sensor_listbox

        self._sensors: List[Dict] = []
        self._selected_sensors: Set[str] = set()
        self._original_configs: Dict[str, Set[str]] = {}

        self._ui_updater = ModeUIUpdater(self, floorplan, sel_info_label, mode_desc_label, sensor_listbox)
        self._sensor_handler = SensorSelectionHandler(self, self._ui_updater)
        self._config_handler = ModeConfigurationHandler(self, self._ui_updater)


    def on_sensor_click(self, dev_id: str, dev_type: str):
        self._sensor_handler.on_sensor_click(dev_id, dev_type)

    def load_sensors(self):
        self._config_handler.load_sensors_and_original_configs()

    def load_mode(self):
        self._config_handler.load_mode()

    def _update_display(self): # This is now handled by the UI Updater
        self._ui_updater.update_display(self._sensors, self._selected_sensors)

    def select_all(self):
        self._sensor_handler.select_all()

    def clear_all(self):
        self._sensor_handler.clear_all()

    def save_mode(self):
        self._config_handler.save_mode()

    def reset_mode(self):
        self._config_handler.reset_mode()

    def on_show(self):
        self._config_handler.load_sensors_and_original_configs()
        self._config_handler.load_mode()
