import tkinter as tk
from tkinter import ttk
from typing import Set, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ModeUIUpdater:
    def __init__(self, manager_instance: Any, floorplan: 'FloorPlan', sel_info_label: ttk.Label, mode_desc_label: ttk.Label, sensor_listbox: tk.Listbox):
        self._manager = manager_instance
        self.floorplan = floorplan
        self.sel_info_label = sel_info_label
        self.mode_desc_label = mode_desc_label
        self.sensor_listbox = sensor_listbox

    def update_display(self, sensors: List[Dict], selected_sensors: Set[str]):
        """Update floor plan and sensor list display."""
        for s in sensors:
            self.floorplan.set_armed(s['id'], s['id'] in selected_sensors)
        self.floorplan.refresh()
        
        self.sensor_listbox.delete(0, tk.END)
        for s in sensors:
            status = "✓" if s['id'] in selected_sensors else "○"
            self.sensor_listbox.insert(tk.END, f"{status} {s['id']}: {s['type']} @ {s['location']}")
        
        if selected_sensors:
            self.sel_info_label.config(text=f"Active sensors: {', '.join(sorted(selected_sensors))}")
        else:
            self.sel_info_label.config(text="Active sensors: None")

    def update_mode_description(self, description: str):
        self.mode_desc_label.config(text=description)
