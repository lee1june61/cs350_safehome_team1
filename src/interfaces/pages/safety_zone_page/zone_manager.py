from tkinter import messagebox, ttk
import tkinter as tk
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from .zone_ui_updater import ZoneUIUpdater
from .zone_action_handler import ZoneActionHandler # Added import

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ZoneManager:
    def __init__(self, page: Any, floorplan: 'FloorPlan', zone_list: tk.Listbox, status_label: ttk.Label, sel_info_label: ttk.Label):
        self.page = page
        self.floorplan = floorplan
        self.zones: List[Dict] = []
        self._editing_zone_id: Optional[str] = None # Added type hint
        self._ui_updater = ZoneUIUpdater(self, floorplan, zone_list, status_label, sel_info_label)
        self._action_handler = ZoneActionHandler(self) # Instantiated action handler

    def load_zones(self):
        res = self.page.send_to_system('get_safety_zones')
        self.zones = res.get('data', []) if res.get('success') else []
        self._ui_updater.update_zone_list(self.zones)

    def get_selected_zone(self) -> Optional[Dict]:
        sel = self._ui_updater.zone_list.curselection()
        if sel and sel[0] < len(self.zones):
            return self.zones[sel[0]]
        return None

    def on_zone_select(self, event: Any):
        zone = self.get_selected_zone()
        if zone:
            self._ui_updater.display_selected_zone_info(zone)
        else:
            self._ui_updater.clear_all_display()

    def _update_selection_info(self): # This is called by the UI Updater now
        self._ui_updater.update_selection_info()

    def arm_zone(self):
        self._action_handler._set_zone_armed_state(True) # Delegated to action handler

    def disarm_zone(self):
        self._action_handler._set_zone_armed_state(False) # Delegated to action handler

    def create_zone(self):
        self._action_handler.create_zone() # Delegated to action handler

    def start_edit_sensors(self):
        self._action_handler.start_edit_sensors() # Delegated to action handler

    def save_zone_sensors(self):
        self._action_handler.save_zone_sensors() # Delegated to action handler

    def delete_zone(self):
        self._action_handler.delete_zone() # Delegated to action handler

    def on_show(self):
        self._editing_zone_id = None
        self.floorplan.set_select_mode(False)
        self.load_zones()
        self._ui_updater.clear_all_display()

    def on_sensor_selected(self, sensor_id: str, dtype: str, is_selected: bool):
        self._ui_updater.update_selection_info()

    def handle_device_click_info(self, dev_id: str, dtype: str):
        """Handle device click (non-select mode) to display sensor info."""
        if dtype not in ('sensor', 'motion'):
            return
            
        res = self.page.send_to_system('get_sensors')
        if not res.get('success'):
            return
            
        for s in res.get('data', []):
            if s['id'] == dev_id:
                armed = 'Armed' if s.get('armed') else 'Disarmed'
                messagebox.showinfo("Sensor Info", 
                    f"ID: {dev_id}\nType: {s.get('type', 'Unknown')}\n"
                    f"Location: {s.get('location', 'Unknown')}\nStatus: {armed}")
                return
