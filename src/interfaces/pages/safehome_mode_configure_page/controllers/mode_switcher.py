"""Mode switching controller for SafeHome mode configuration."""

from __future__ import annotations

from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..safehome_mode_configure_page.mode_config_manager import ModeConfigManager


class ModeSwitcher:
    """Handle mode transitions with dirty-checks and persistence prompts."""

    def __init__(self, manager: "ModeConfigManager"):
        self._manager = manager

    def on_show(self) -> None:
        self._manager._config_handler.load_sensors_and_original_configs()
        self._manager._current_mode = self._manager.mode_var.get()
        self._manager._config_handler.load_mode()

    def change_mode(self, new_mode: str) -> None:
        current = self._manager._current_mode or self._manager.mode_var.get()
        if new_mode == current:
            return

        if self._manager.is_editing_active():
            messagebox.showwarning(
                "Edit Mode",
                "Finish or cancel the current edit before switching modes.",
            )
            self._manager.mode_var.set(current)
            return

        if self._manager.has_unsaved_changes():
            if not self._confirm_or_revert(current):
                return

        self._manager._current_mode = new_mode
        self._manager.mode_var.set(new_mode)
        self._manager._config_handler.load_mode()

    def _confirm_or_revert(self, current: str) -> bool:
        save = messagebox.askyesno(
            "Save Changes",
            f"Save changes to '{current}' before switching?",
        )
        if save:
            if not self._manager.save_mode():
                self._manager.mode_var.set(current)
                return False
        else:
            cached = self._manager._mode_cache.get(current, set())
            self._manager._selected_sensors = set(cached)
            self._manager._ui_updater.update_display(
                self._manager._sensors, self._manager._selected_sensors
            )
            self._manager._dirty = False
        return True




