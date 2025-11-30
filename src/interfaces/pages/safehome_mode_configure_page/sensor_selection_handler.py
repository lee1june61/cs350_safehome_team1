from typing import Set, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .mode_config_manager import ModeConfigManager
    from .mode_ui_updater import ModeUIUpdater

class SensorSelectionHandler:
    """
    Handles the logic for selecting and deselecting sensors for mode configuration.
    """
    def __init__(self, manager_instance: Any, ui_updater: 'ModeUIUpdater'):
        self._manager = manager_instance
        self._ui_updater = ui_updater

    @property
    def _sensors(self) -> List[Dict]:
        return self._manager._sensors

    @property
    def _selected_sensors(self) -> Set[str]:
        return self._manager._selected_sensors

    @_selected_sensors.setter
    def _selected_sensors(self, value: Set[str]):
        self._manager._selected_sensors = value

    def on_sensor_click(self, dev_id: str, dev_type: str, _selected: bool = False):
        """Handle sensor click to toggle selection."""
        if not self._manager.is_editing_active():
            from tkinter import messagebox
            messagebox.showinfo("Edit Mode", "Click 'Edit Mode' before modifying sensors.")
            return
        if dev_type not in ('sensor', 'motion', 'door_sensor'):
            return
        
        if dev_id in self._selected_sensors:
            self._selected_sensors.discard(dev_id)
        else:
            self._selected_sensors.add(dev_id)
        
        self._ui_updater.update_display(self._sensors, self._selected_sensors)
        self._manager.notify_selection_updated()

    def select_all(self):
        """Select all sensors."""
        self._selected_sensors = {s['id'] for s in self._sensors}
        self._ui_updater.update_display(self._sensors, self._selected_sensors)
        self._manager.notify_selection_updated()

    def clear_all(self):
        """Clear all selections."""
        self._selected_sensors = set()
        self._ui_updater.update_display(self._sensors, self._selected_sensors)
        self._manager.notify_selection_updated()