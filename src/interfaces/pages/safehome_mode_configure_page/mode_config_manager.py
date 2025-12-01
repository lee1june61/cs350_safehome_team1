"""Coordinates SafeHome mode configuration logic for the configure page."""

import tkinter as tk
from tkinter import ttk
from typing import Set, List, Dict, Any, Optional, TYPE_CHECKING

from .mode_ui_updater import ModeUIUpdater
from .sensor_selection_handler import SensorSelectionHandler
from .mode_configuration_handler import ModeConfigurationHandler
from .controllers import ModeEditSession, ModeSwitcher

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ModeConfigManager:
    MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST']

    def __init__(
        self,
        page: Any,
        floorplan: 'FloorPlan',
        sel_info_label: ttk.Label,
        mode_var: tk.StringVar,
        mode_desc_label: ttk.Label,
        sensor_listbox: Optional[tk.Listbox] = None,
    ):
        self.page = page
        self.floorplan = floorplan
        self.sel_info_label = sel_info_label
        self.mode_var = mode_var
        self.mode_desc_label = mode_desc_label
        self.sensor_listbox = sensor_listbox

        self._sensors: List[Dict] = []
        self._selected_sensors: Set[str] = set()
        self._original_configs: Dict[str, Set[str]] = {}
        self._mode_cache: Dict[str, Set[str]] = {}
        self._dirty = False
        self._current_mode = mode_var.get()
        self._ui_updater = ModeUIUpdater(
            self, floorplan, sel_info_label, mode_desc_label, sensor_listbox
        )
        self._sensor_handler = SensorSelectionHandler(self, self._ui_updater)
        self._config_handler = ModeConfigurationHandler(self, self._ui_updater)
        self._edit_session = ModeEditSession(self)
        self._mode_switcher = ModeSwitcher(self)

    # ------------------------------------------------------------------ #
    # Public API used by the page
    # ------------------------------------------------------------------ #
    def on_sensor_click(self, dev_id: str, dev_type: str, selected: bool = False):
        self._sensor_handler.on_sensor_click(dev_id, dev_type, selected)

    def save_mode(self) -> bool:
        success = self._config_handler.save_mode()
        if success:
            mode = self.mode_var.get()
            self._mode_cache[mode] = set(self._selected_sensors)
            self._dirty = False
        return success

    def on_show(self):
        self._mode_switcher.on_show()

    def handle_mode_change(self, new_mode: str):
        self._mode_switcher.change_mode(new_mode)

    # ------------------------------------------------------------------ #
    # Internal helpers used by handlers
    # ------------------------------------------------------------------ #
    def _mark_dirty(self):
        mode = self.mode_var.get()
        cached = self._mode_cache.get(mode, set())
        self._dirty = self._selected_sensors != cached

    def has_unsaved_changes(self) -> bool:
        return self._dirty

    def cache_mode_config(self, mode: str, sensors: Set[str]):
        self._mode_cache[mode] = set(sensors)
        self._dirty = False

    def store_original_config(self, mode: str, sensors: Set[str]):
        self._original_configs[mode] = set(sensors)
        if mode not in self._mode_cache:
            self._mode_cache[mode] = set(sensors)

    def get_original_config(self, mode: str) -> Set[str]:
        return self._original_configs.get(mode, set()).copy()

    def is_editing_active(self) -> bool:
        return self._edit_session.is_active

    # ------------------------------------------------------------------ #
    # Editing workflow helpers
    # ------------------------------------------------------------------ #
    def begin_edit_mode(self):
        self._edit_session.begin()

    def notify_selection_updated(self):
        self._edit_session.notify_selection_updated()
