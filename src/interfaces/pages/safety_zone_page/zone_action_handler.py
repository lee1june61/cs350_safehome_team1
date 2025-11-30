"""Zone action handler for SafetyZonePage."""
from tkinter import messagebox, simpledialog
from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .zone_manager import ZoneManager

CREATE_VALIDATION_MSG = "Select new safety zone and type safety zone name"
UPDATE_SELECTION_MSG = "Choose a safety zone for updating"
DELETE_SELECTION_MSG = "Choose a safety zone for deletion"

class ZoneActionHandler:
    def __init__(self, manager: "ZoneManager"):
        self._m = manager

    def _get_zone(self) -> Optional[Dict]:
        return self._m.get_selected_zone()

    def _require_zone(self, warning: str) -> Optional[Dict]:
        zone = self._get_zone()
        if not zone:
            messagebox.showwarning("Warning", warning)
        return zone

    def set_armed_state(self, armed: bool):
        zone = self._require_zone(UPDATE_SELECTION_MSG)
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
            messagebox.showwarning("Warning", CREATE_VALIDATION_MSG)
            return
        trimmed = name.strip()
        self._m.begin_new_zone(trimmed)

    def start_edit_sensors(self):
        zone = self._require_zone(UPDATE_SELECTION_MSG)
        if not zone:
            return
        self._m.cancel_pending_creation()
        self._m.floorplan.set_select_mode(True)
        self._m.floorplan.set_selected(zone.get("sensors", []))
        self._m._editing_zone_id = zone["id"]
        self._m._ui_updater.update_selection_info()
        self._m._ui_updater.update_status_label(
            f"Editing '{zone['name']}'. Adjust sensors as needed.",
            is_error=False,
        )
        self._m.update_selection_dialog()
        self._m.open_edit_selection_dialog(zone["name"])

    def save_zone_sensors(self):
        selected = self._m.floorplan.get_selected()
        if self._m._pending_zone_name:
            if not selected:
                messagebox.showwarning("Warning", CREATE_VALIDATION_MSG)
                return
            res = self._m.page.send_to_system(
                "create_safety_zone",
                name=self._m._pending_zone_name,
                sensors=list(selected),
            )
            if res.get("success"):
                messagebox.showinfo("Success", res.get("message", "Safety zone created"))
                new_id = res.get("zone_id")
                self._m.finalize_new_zone()
                self._m.load_zones()
                self._m.select_zone(new_id)
            else:
                messagebox.showerror("Error", res.get("message", "Failed"))
            return

        if not self._m._editing_zone_id:
            messagebox.showwarning("Warning", UPDATE_SELECTION_MSG)
            return
        if not selected:
            messagebox.showwarning("Warning", "Select at least one sensor")
            return

        res = self._m.page.send_to_system(
            "update_safety_zone",
            zone_id=self._m._editing_zone_id, sensors=list(selected))
        if res.get("success"):
            messagebox.showinfo("Success", res.get("message", "Sensors updated"))
            zone_id = self._m._editing_zone_id
            self._m.finish_edit_mode()
            self._m.load_zones()
            self._m.select_zone(zone_id)
        else:
            messagebox.showerror("Error", res.get("message", "Failed"))

    def delete_zone(self):
        zone = self._require_zone(DELETE_SELECTION_MSG)
        if not zone:
            return
        if not messagebox.askyesno("Confirm", f"Delete '{zone['name']}'?"):
            return
        res = self._m.page.send_to_system("delete_safety_zone", zone_id=zone["id"])
        if res.get("success"):
            messagebox.showinfo("Deleted", res.get("message", "Safety zone deleted"))
            self._m.finish_edit_mode()
            self._m.cancel_pending_creation()
            self._m.load_zones()
            self._m._ui_updater.clear_all_display()
        else:
            messagebox.showerror("Error", res.get("message", "Failed"))
