"""Selection session management for safety zone creation/editing."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Dict

from .selection_dialog import SelectionDialogController

if TYPE_CHECKING:  # pragma: no cover
    from ...components.floor_plan import FloorPlan
    from .zone_ui_updater import ZoneUIUpdater
    from .zone_manager import ZoneManager


class ZoneSelectionSession:
    """Handles floorplan select-mode, dialogs, and session state."""
    def __init__(
        self,
        manager: "ZoneManager",
        floorplan: "FloorPlan",
        ui_updater: "ZoneUIUpdater",
    ):
        self._manager = manager
        self._floorplan = floorplan
        self._ui = ui_updater
        self._pending_name: Optional[str] = None
        self._editing_zone_id: Optional[int] = None
        self._dialog = SelectionDialogController(manager.page)

    @property
    def pending_name(self) -> Optional[str]:
        return self._pending_name

    @property
    def editing_zone_id(self) -> Optional[int]:
        return self._editing_zone_id

    def reset(self) -> None:
        self._pending_name = None
        self._editing_zone_id = None
        self._floorplan.set_select_mode(False)
        self._floorplan.clear_selection()
        self._ui.update_selection_info()
        self._ui.update_status_label("", is_error=False)
        self._dialog.close()

    def begin_creation(self, name: str) -> None:
        self._pending_name = name
        self._editing_zone_id = None
        self._floorplan.set_select_mode(True)
        self._floorplan.clear_selection()
        self._ui.update_selection_info()
        self._set_status(f"Creating '{name}'. Select sensors (click or drag).")
        self._dialog.open(
            title=f"Create Zone: {name}",
            description="Select sensors on the floor plan. They will appear below. Click Finish Selection when ready.",
            on_finish=self._manager.save_zone_sensors,
            on_cancel=lambda: self.cancel_creation(close_dialog=False),
            selected=self._floorplan.get_selected(),
        )

    def _set_status(self, message: str, *, is_error: bool = False):
        self._ui.update_status_label(message, is_error=is_error)

    def finalize_creation(self) -> None:
        self._pending_name = None
        self._floorplan.set_select_mode(False)
        self._floorplan.clear_selection()
        self._ui.update_selection_info()
        self._set_status("Safety zone saved.")
        self._dialog.close()

    def cancel_creation(self, close_dialog: bool = True) -> None:
        if not self._pending_name:
            return
        self._pending_name = None
        self._floorplan.set_select_mode(False)
        self._floorplan.clear_selection()
        self._ui.update_selection_info()
        self._set_status("")
        if close_dialog:
            self._dialog.close()

    def begin_edit(self, zone: Dict) -> None:
        self._pending_name = None
        self._editing_zone_id = zone.get("id")
        self._floorplan.set_select_mode(True)
        self._floorplan.set_selected(zone.get("sensors", []))
        self._ui.update_selection_info()
        self._set_status(f"Editing '{zone.get('name', 'Zone')}'. Adjust sensors as needed.")
        self._dialog.open(
            title=f"Edit Zone: {zone.get('name', 'Zone')}",
            description="Adjust the sensor selection. Click Finish Selection to save changes.",
            on_finish=self._manager.save_zone_sensors,
            on_cancel=lambda: self.finish_edit(close_dialog=False),
            selected=self._floorplan.get_selected(),
        )

    def finish_edit(self, close_dialog: bool = True) -> None:
        self._editing_zone_id = None
        self._floorplan.set_select_mode(False)
        self._floorplan.clear_selection()
        self._ui.update_selection_info()
        self._set_status("")
        if close_dialog:
            self._dialog.close()

    def update_dialog(self) -> None:
        self._dialog.update(self._floorplan.get_selected())

