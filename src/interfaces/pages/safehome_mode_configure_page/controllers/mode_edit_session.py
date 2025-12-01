"""Edit-session controller for SafeHome mode configuration."""

from __future__ import annotations

from tkinter import messagebox
from typing import Optional, TYPE_CHECKING, Set

from ...safety_zone_page.sensor_selection_dialog import SensorSelectionDialog

if TYPE_CHECKING:  # pragma: no cover
    from ..safehome_mode_configure_page.mode_config_manager import ModeConfigManager


class ModeEditSession:
    """Encapsulates edit-mode lifecycle (start, finish, cancel, dialog sync)."""

    def __init__(self, manager: "ModeConfigManager"):
        self._manager = manager
        self._active = False
        self._snapshot: Set[str] = set()
        self._dialog: Optional[SensorSelectionDialog] = None

    @property
    def is_active(self) -> bool:
        return self._active

    def begin(self) -> None:
        mode = self._manager.mode_var.get()
        if not mode:
            messagebox.showwarning("Edit Mode", "Select a mode first.")
            return
        if self._active:
            if self._dialog:
                self._dialog.lift()
            return

        self._active = True
        self._snapshot = set(self._manager._selected_sensors)
        self._manager.floorplan.set_select_mode(True)
        self._manager.floorplan.set_selected(list(self._manager._selected_sensors))
        self._open_dialog(mode)
        self._sync_dialog()

    def notify_selection_updated(self) -> None:
        if not self._active:
            return
        self._manager._mark_dirty()
        self._sync_dialog()

    def finish_and_save(self) -> None:
        if self._manager.save_mode():
            self._snapshot = set(self._manager._selected_sensors)
            messagebox.showinfo("Saved", f"{self._manager.mode_var.get()} configuration saved.")
            self._end_session()

    def cancel(self) -> None:
        self._manager._selected_sensors = set(self._snapshot)
        self._manager._ui_updater.update_display(
            self._manager._sensors, self._manager._selected_sensors
        )
        self._manager._dirty = False
        messagebox.showinfo("Reset", "Changes discarded.")
        self._end_session()

    def _open_dialog(self, mode: str) -> None:
        parent = self._manager.page.get_frame().winfo_toplevel()
        self._close_dialog()
        description = (
            f"Editing '{mode}'. Select sensors on the floor plan.\n"
            "Click Finish Selection to save your changes or Cancel to discard."
        )
        self._dialog = SensorSelectionDialog(
            parent=parent,
            title=f"Edit Mode: {mode}",
            description=description,
            on_finish=self.finish_and_save,
            on_cancel=self.cancel,
        )
        self._dialog.update_selected(self._manager.floorplan.get_selected())

    def _sync_dialog(self) -> None:
        if self._dialog:
            self._dialog.update_selected(self._manager.floorplan.get_selected())

    def _end_session(self) -> None:
        self._active = False
        self._manager.floorplan.set_select_mode(False)
        self._close_dialog()

    def _close_dialog(self) -> None:
        if self._dialog:
            self._dialog.close()
            self._dialog = None

