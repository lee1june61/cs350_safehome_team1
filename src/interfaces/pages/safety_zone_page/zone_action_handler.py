"""Zone action handler for SafetyZonePage."""
from tkinter import messagebox, simpledialog
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .zone_manager import ZoneManager


class ZoneActionHandler:
    def __init__(self, manager: "ZoneManager"):
        self._m = manager

    def _get_zone(self) -> Optional[Dict]:
        return self._m.get_selected_zone()

    def _require_zone(self) -> Optional[Dict]:
        zone = self._get_zone()
        if not zone:
            messagebox.showwarning("Warning", "Select a zone first")
        return zone

    def set_armed_state(self, armed: bool):
        zone = self._require_zone()
        if not zone:
            return
        cmd = "arm_zone" if armed else "disarm_zone"
        res = self._m.page.send_to_system(cmd, zone_id=zone["id"])
        if res.get("success"):
            self._m.load_zones()
            state = "armed" if armed else "disarmed"
            messagebox.showinfo("Success", f"Zone '{zone['name']}' {state}")
        else:
            messagebox.showerror("Error", res.get("message", "Failed"))

    def create_zone(self):
        name = simpledialog.askstring("Create Zone", "Zone name:")
        if not name or not name.strip():
            return
        self._m.floorplan.set_select_mode(True)
        self._m.floorplan.clear_selection()
        res = self._m.page.send_to_system(
            "create_safety_zone", name=name.strip(), sensors=[])
        if res.get("success"):
            self._m._editing_zone_id = res.get("zone_id")
            self._m.load_zones()
            self._m._ui_updater.zone_list.selection_set(len(self._m.zones) - 1)
            self._m.on_zone_select(None)
            messagebox.showinfo("Created", "Click sensors and Save")

    def start_edit_sensors(self):
        zone = self._require_zone()
        if not zone:
            return
        self._m.floorplan.set_select_mode(True)
        self._m.floorplan.set_selected(zone.get("sensors", []))
        self._m._editing_zone_id = zone["id"]
        self._m._ui_updater.update_selection_info()
        messagebox.showinfo("Edit", f"Editing '{zone['name']}'")

    def save_zone_sensors(self):
        if not self._m._editing_zone_id:
            messagebox.showwarning("Warning", "No zone being edited")
            return
        selected = self._m.floorplan.get_selected()
        res = self._m.page.send_to_system(
            "update_safety_zone",
            zone_id=self._m._editing_zone_id, sensors=list(selected))
        if res.get("success"):
            messagebox.showinfo("Success", "Sensors updated")
            self._m._editing_zone_id = None
            self._m.floorplan.set_select_mode(False)
            self._m.load_zones()
        else:
            messagebox.showerror("Error", res.get("message", "Failed"))

    def delete_zone(self):
        zone = self._require_zone()
        if not zone:
            return
        if not messagebox.askyesno("Confirm", f"Delete '{zone['name']}'?"):
            return
        res = self._m.page.send_to_system("delete_safety_zone", zone_id=zone["id"])
        if res.get("success"):
            self._m._editing_zone_id = None
            self._m.floorplan.clear_selection()
            self._m._ui_updater.update_selection_info()
            self._m.load_zones()
