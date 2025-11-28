import tkinter as tk
from tkinter import ttk
from typing import Set, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ZoneUIUpdater:
    def __init__(self, zone_manager_instance: Any, floorplan: 'FloorPlan', zone_list: tk.Listbox, status_label: ttk.Label, sel_info_label: ttk.Label):
        self._manager = zone_manager_instance
        self.floorplan = floorplan
        self.zone_list = zone_list
        self.status_label = status_label
        self.sel_info_label = sel_info_label

    def update_zone_list(self, zones: List[Dict]):
        self.zone_list.delete(0, tk.END)
        for z in zones:
            status = '🔴' if z.get('armed') else '⚪'
            self.zone_list.insert(tk.END, f"{status} {z['name']} ({len(z.get('sensors', []))} sensors)")
        self._update_floorplan_states(zones)

    def _update_floorplan_states(self, zones: List[Dict]):
        armed_sensors = {s for z in zones if z.get('armed') for s in z.get('sensors', [])}
        for sensor_id in self.floorplan.get_sensors():
            self.floorplan.set_armed(sensor_id, sensor_id in armed_sensors)
        self.floorplan.refresh()

    def update_selection_info(self):
        selected = self.floorplan.get_selected()
        text = f"Selected sensors: {', '.join(sorted(selected))}" if selected else "Selected sensors: None"
        self.sel_info_label.config(text=text)

    def update_status_label(self, message: str, is_error: bool = False):
        self.status_label.config(text=message, foreground='red' if is_error else 'black')

    def display_selected_zone_info(self, zone: Dict):
        armed_text = 'Armed' if zone.get('armed') else 'Disarmed'
        self.status_label.config(text=f"{zone['name']}: {armed_text}")
        self.floorplan.set_selected(zone.get('sensors', []))
        self.update_selection_info()

    def clear_all_display(self):
        self.floorplan.clear_selection()
        self.update_selection_info()
        self.status_label.config(text="")
