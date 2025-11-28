import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional, List, Any

class ZoneDialogManager:
    """
    Manages the logic for creating and updating safety zones in the dialog.
    """
    def __init__(self, dialog_instance: Any, web_interface: Any, mode: str, 
                 zone_data: Optional[Dict], name_var: tk.StringVar, listbox: tk.Listbox):
        self._dialog = dialog_instance
        self._web_interface = web_interface
        self._mode = mode
        self._zone_data = zone_data
        self._name_var = name_var
        self._listbox = listbox
        self._sensors: List[Dict] = []

    def load_sensors(self) -> None:
        """Load available sensors from the system."""
        response = self._web_interface.send_message('get_sensors')
        if response.get('success'):
            self._sensors = response.get('data', [])
            for sensor in self._sensors:
                self._listbox.insert(tk.END, f"{sensor['name']} ({sensor['type']})")

    def load_zone_data(self) -> None:
        """Load existing zone data into the dialog fields."""
        if self._zone_data:
            self._name_var.set(self._zone_data.get('name', ''))
            zone_sensor_ids = self._zone_data.get('sensor_ids', [])
            for i, sensor in enumerate(self._sensors):
                if sensor['id'] in zone_sensor_ids:
                    self._listbox.selection_set(i)

    def handle_save(self) -> None:
        """Handles saving (creating or updating) the zone."""
        name = self._name_var.get().strip()
        if not name:
            self._dialog._show_error("Zone name required")
            return
        
        selected = self._listbox.curselection()
        if not selected:
            self._dialog._show_error("Select at least one sensor")
            return
        
        sensor_ids = [self._sensors[i]['id'] for i in selected]
        
        if self._mode == 'create':
            response = self._web_interface.send_message('create_safety_zone', 
                                                        zone_name=name, sensor_ids=sensor_ids)
        else:
            if not self._zone_data or 'id' not in self._zone_data:
                self._dialog._show_error("Zone ID missing for update.")
                return
            response = self._web_interface.send_message('update_safety_zone',
                                                        zone_id=self._zone_data['id'],
                                                        zone_name=name, sensor_ids=sensor_ids)
        
        if response.get('success'):
            self._dialog._show_info(response.get('message', 'Success'))
            self._dialog._on_ok()
        else:
            self._dialog._show_error(response.get('message', 'Failed'))
