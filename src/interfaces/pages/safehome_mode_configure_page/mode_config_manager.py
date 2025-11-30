"""
ModeConfigManager - A helper class to manage SafeHome mode configuration logic
for the SafeHomeModeConfigurePage.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Set, List, Dict, Any, Optional, TYPE_CHECKING

from .mode_ui_updater import ModeUIUpdater
from .sensor_selection_handler import SensorSelectionHandler
from .mode_configuration_handler import ModeConfigurationHandler
from ..safety_zone_page.sensor_selection_dialog import SensorSelectionDialog

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
        self._editing_active = False
        self._selection_dialog: Optional[SensorSelectionDialog] = None
        self._edit_snapshot: Set[str] = set()

        self._ui_updater = ModeUIUpdater(
            self, floorplan, sel_info_label, mode_desc_label, sensor_listbox
        )
        self._sensor_handler = SensorSelectionHandler(self, self._ui_updater)
        self._config_handler = ModeConfigurationHandler(self, self._ui_updater)

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
        self._config_handler.load_sensors_and_original_configs()
        self._current_mode = self.mode_var.get()
        self._config_handler.load_mode()

    def handle_mode_change(self, new_mode: str):
        current = self._current_mode or self.mode_var.get()
        if new_mode == current:
            return
        if self._editing_active:
            messagebox.showwarning(
                "Edit Mode",
                "Finish or cancel the current edit before switching modes."
            )
            self.mode_var.set(current)
            return

        if self.has_unsaved_changes():
            save = messagebox.askyesno(
                "Save Changes",
                f"Save changes to '{current}' before switching?",
            )
            if save:
                if not self.save_mode():
                    self.mode_var.set(current)
                    return
            else:
                self._selected_sensors = set(self._mode_cache.get(current, set()))
                self._ui_updater.update_display(self._sensors, self._selected_sensors)
                self._dirty = False

        self._current_mode = new_mode
        self.mode_var.set(new_mode)
        self._config_handler.load_mode()

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
        return self._editing_active

    # ------------------------------------------------------------------ #
    # Editing workflow helpers
    # ------------------------------------------------------------------ #
    def begin_edit_mode(self):
        mode = self.mode_var.get()
        if not mode:
            messagebox.showwarning("Edit Mode", "Select a mode first.")
            return
        if self._editing_active:
            if self._selection_dialog:
                self._selection_dialog.lift()
            return
        self._editing_active = True
        self._edit_snapshot = set(self._selected_sensors)
        self.floorplan.set_select_mode(True)
        self.floorplan.set_selected(list(self._selected_sensors))
        self._open_selection_dialog(mode)
        self._update_selection_dialog()

    def _finish_edit_save(self):
        if self.save_mode():
            self._edit_snapshot = set(self._selected_sensors)
            messagebox.showinfo("Saved", f"{self.mode_var.get()} configuration saved.")
            self._end_edit_session()

    def _handle_edit_cancel(self):
        self._selected_sensors = set(self._edit_snapshot)
        self._ui_updater.update_display(self._sensors, self._selected_sensors)
        self._dirty = False
        messagebox.showinfo("Reset", "Changes discarded.")
        self._end_edit_session()

    def _end_edit_session(self):
        self._editing_active = False
        self.floorplan.set_select_mode(False)
        self._close_selection_dialog()

    def notify_selection_updated(self):
        if not self._editing_active:
            return
        self._mark_dirty()
        self._update_selection_dialog()

    def _open_selection_dialog(self, mode: str):
        parent = self.page.get_frame().winfo_toplevel()
        self._close_selection_dialog()
        description = (
            f"Editing '{mode}'. Select sensors on the floor plan.\n"
            "Click Finish Selection to save your changes or Cancel to discard."
        )
        self._selection_dialog = SensorSelectionDialog(
            parent=parent,
            title=f"Edit Mode: {mode}",
            description=description,
            on_finish=self._finish_edit_save,
            on_cancel=self._handle_edit_cancel,
        )
        self._selection_dialog.update_selected(self.floorplan.get_selected())

    def _close_selection_dialog(self):
        if self._selection_dialog:
            self._selection_dialog.close()
            self._selection_dialog = None

    def _update_selection_dialog(self):
        if self._selection_dialog:
            self._selection_dialog.update_selected(self.floorplan.get_selected())
