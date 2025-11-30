from tkinter import messagebox, ttk
import tkinter as tk
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from .zone_ui_updater import ZoneUIUpdater
from .zone_action_handler import ZoneActionHandler
from .sensor_selection_dialog import SensorSelectionDialog

if TYPE_CHECKING:
    from ...components.floor_plan import FloorPlan


class ZoneManager:
    def __init__(self, page: Any, floorplan: 'FloorPlan', zone_list: tk.Listbox, status_label: ttk.Label, sel_info_label: ttk.Label):
        self.page = page
        self.floorplan = floorplan
        self.zones: List[Dict] = []
        self._editing_zone_id: Optional[int] = None
        self._pending_zone_name: Optional[str] = None
        self._sensor_cache: List[Dict] = []
        self._selection_dialog: Optional[SensorSelectionDialog] = None
        self._ui_updater = ZoneUIUpdater(self, floorplan, zone_list, status_label, sel_info_label)
        self._action_handler = ZoneActionHandler(self)

    def load_zones(self):
        self._refresh_sensor_cache()
        res = self.page.send_to_system('get_safety_zones')
        self.zones = res.get('data', []) if res.get('success') else []
        self._ui_updater.update_zone_list(self.zones)

    def _refresh_sensor_cache(self):
        """Fetch latest sensor info from the system."""
        res = self.page.send_to_system('get_sensors')
        if res.get('success'):
            self._sensor_cache = res.get('data', [])
        else:
            self._sensor_cache = []

    def get_selected_zone(self) -> Optional[Dict]:
        sel = self._ui_updater.zone_list.curselection()
        if sel and sel[0] < len(self.zones):
            return self.zones[sel[0]]
        return None

    def on_zone_select(self, event: Any):
        self.cancel_pending_creation()
        zone = self.get_selected_zone()
        if zone:
            self._ui_updater.display_selected_zone_info(zone)
        else:
            self._ui_updater.clear_all_display()

    def _update_selection_info(self): # This is called by the UI Updater now
        self._ui_updater.update_selection_info()

    def arm_zone(self):
        self._action_handler.set_armed_state(True)

    def disarm_zone(self):
        self._action_handler.set_armed_state(False)

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
        self._pending_zone_name = None
        self.floorplan.set_select_mode(False)
        self.load_zones()
        self._ui_updater.clear_all_display()

    def on_sensor_selected(self, sensor_id: str, dtype: str, is_selected: bool):
        self._ui_updater.update_selection_info()
        self.update_selection_dialog()

    def handle_device_click_info(self, dev_id: str, dtype: str):
        """Handle device click (non-select mode) to display sensor info."""
        if dtype not in ('sensor', 'motion', 'door_sensor'):
            return
        if not self._sensor_cache:
            self._refresh_sensor_cache()

        for sensor in self._sensor_cache:
            if sensor.get('id') == dev_id:
                armed = 'Armed' if sensor.get('armed') else 'Disarmed'
                messagebox.showinfo(
                    "Sensor Info",
                    f"ID: {dev_id}\nType: {sensor.get('type', 'Unknown')}\n"
                    f"Location: {sensor.get('location', 'Unknown')}\nStatus: {armed}",
                )
                return

    def begin_new_zone(self, name: str):
        self._pending_zone_name = name
        self._editing_zone_id = None
        self.floorplan.set_select_mode(True)
        self.floorplan.clear_selection()
        self._ui_updater.update_selection_info()
        self._ui_updater.update_status_label(
            f"Creating '{name}'. Select sensors (click or drag).",
            is_error=False,
        )
        self._open_selection_dialog(
            title=f"Create Zone: {name}",
            description="Select sensors on the floor plan. They will appear below. Click Finish Selection when ready.",
            cancel_callback=lambda: self.cancel_pending_creation(close_dialog=False),
        )
        self.update_selection_dialog()

    def finalize_new_zone(self):
        self._pending_zone_name = None
        self._editing_zone_id = None
        self.floorplan.set_select_mode(False)
        self.floorplan.clear_selection()
        self._ui_updater.update_selection_info()
        self._ui_updater.update_status_label("Safety zone saved.", is_error=False)
        self._close_selection_dialog()

    def cancel_pending_creation(self, close_dialog: bool = True):
        if self._pending_zone_name:
            self._pending_zone_name = None
            self.floorplan.set_select_mode(False)
            self.floorplan.clear_selection()
            self._ui_updater.update_selection_info()
            self._ui_updater.update_status_label("", is_error=False)
            if close_dialog:
                self._close_selection_dialog()
            else:
                self._selection_dialog = None

    def finish_edit_mode(self, close_dialog: bool = True):
        self._editing_zone_id = None
        self.floorplan.set_select_mode(False)
        self.floorplan.clear_selection()
        self._ui_updater.update_selection_info()
        self._ui_updater.update_status_label("", is_error=False)
        if close_dialog:
            self._close_selection_dialog()
        else:
            self._selection_dialog = None

    def select_zone(self, zone_id: Optional[int]):
        if zone_id is None:
            return
        for idx, zone in enumerate(self.zones):
            if zone.get('id') == zone_id:
                self._ui_updater.zone_list.selection_clear(0, tk.END)
                self._ui_updater.zone_list.selection_set(idx)
                self.on_zone_select(None)
                break

    def open_edit_selection_dialog(self, zone_name: str):
        self._open_selection_dialog(
            title=f"Edit Zone: {zone_name}",
            description="Adjust the sensor selection. Click Finish Selection to save changes.",
            cancel_callback=lambda: self.finish_edit_mode(close_dialog=False),
        )
        self.update_selection_dialog()

    def _open_selection_dialog(self, title: str, description: str, cancel_callback):
        parent = self.page.get_frame().winfo_toplevel()
        self._close_selection_dialog()
        self._selection_dialog = SensorSelectionDialog(
            parent=parent,
            title=title,
            description=description,
            on_finish=self.save_zone_sensors,
            on_cancel=cancel_callback,
        )
        self._selection_dialog.update_selected(self.floorplan.get_selected())

    def update_selection_dialog(self):
        if self._selection_dialog:
            self._selection_dialog.update_selected(self.floorplan.get_selected())

    def _close_selection_dialog(self):
        if self._selection_dialog:
            self._selection_dialog.close()
            self._selection_dialog = None
