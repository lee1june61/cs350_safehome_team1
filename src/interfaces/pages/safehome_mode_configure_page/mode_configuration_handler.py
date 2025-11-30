import tkinter as tk
from tkinter import messagebox
from typing import Set, List, Dict, Any, TYPE_CHECKING

from ....core.system_defaults import MODE_CONFIGS

if TYPE_CHECKING:
    from .mode_config_manager import ModeConfigManager
    from .mode_ui_updater import ModeUIUpdater


class ModeConfigurationHandler:
    MODES = ['HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED', 'GUEST']
    MODE_DESCRIPTIONS = {
        'HOME': 'At home - perimeter sensors only',
        'AWAY': 'Away from home - all sensors active',
        'OVERNIGHT': 'Overnight travel - all except motion',
        'EXTENDED': 'Extended travel - all sensors active',
        'GUEST': 'Guest at home - same as HOME'
    }

    def __init__(self, manager_instance: Any, ui_updater: 'ModeUIUpdater'):
        self._manager = manager_instance
        self._ui_updater = ui_updater

    @property
    def page(self) -> Any:
        return self._manager.page

    @property
    def mode_var(self) -> tk.StringVar:
        return self._manager.mode_var

    @property
    def _sensors(self) -> List[Dict]:
        return self._manager._sensors

    @_sensors.setter
    def _sensors(self, value: List[Dict]):
        self._manager._sensors = value

    @property
    def _selected_sensors(self) -> Set[str]:
        return self._manager._selected_sensors

    @_selected_sensors.setter
    def _selected_sensors(self, value: Set[str]):
        self._manager._selected_sensors = value

    @property
    def _original_configs(self) -> Dict[str, Set[str]]:
        return self._manager._original_configs

    def load_sensors_and_original_configs(self):
        """Load all sensors from system and store original configurations for reset."""
        res = self.page.send_to_system('get_sensors')
        self._sensors = res.get('data', []) if res.get('success') else []
        
        for mode in self.MODES:
            res = self.page.send_to_system('get_mode_configuration', mode=mode)
            sensors = set(res.get('data', [])) if res.get('success') else set()
            if not sensors:
                default = MODE_CONFIGS.get(mode.upper(), [])
                if default:
                    sensors = set(default)
                    self.page.send_to_system(
                        'configure_safehome_mode',
                        mode=mode,
                        sensors=list(default),
                    )
            self._manager.store_original_config(mode, sensors)

    def load_mode(self):
        """Load sensor configuration for selected mode."""
        mode = self.mode_var.get()
        
        self._ui_updater.update_mode_description(self.MODE_DESCRIPTIONS.get(mode, ''))
        
        res = self.page.send_to_system('get_mode_configuration', mode=mode)
        self._selected_sensors = set(res.get('data', [])) if res.get('success') else set()
        self._ui_updater.update_display(self._sensors, self._selected_sensors)
        self._manager.cache_mode_config(mode, self._selected_sensors)

    def save_mode(self):
        """Save current mode configuration."""
        mode = self.mode_var.get()
        sensors = list(self._selected_sensors)
        
        res = self.page.send_to_system('configure_safehome_mode', mode=mode, sensors=sensors)
        if res.get('success'):
            messagebox.showinfo("Success", f"Mode '{mode}' configuration saved\nActive sensors: {len(sensors)}")
            return True
        messagebox.showerror("Error", res.get('message', 'Failed to save'))
        return False

    def reset_mode(self):
        """Reset to original configuration."""
        if messagebox.askyesno("Confirm", "Reset to original configuration?"):
            mode = self.mode_var.get()
            original = self._manager.get_original_config(mode)
            if original:
                self._selected_sensors = original
                self._ui_updater.update_display(self._sensors, self._selected_sensors)
            else:
                messagebox.showwarning("Warning", "Original configuration not found for this mode.")
