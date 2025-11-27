"""Safety zone management controller."""

import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Set
from ..services.zone_service import ZoneService
from ..services.device_service import DeviceService
from ..views.zone_creation_window import ZoneCreationWindow


class ZoneController:
    """Controller for safety zone operations.

    Handles zone creation, modification, and deletion.
    """

    def __init__(
        self,
        parent: tk.Widget,
        zone_service: ZoneService,
        device_service: DeviceService,
    ):
        """Initialize zone controller.

        Args:
            parent: Parent widget
            zone_service: Zone service
            device_service: Device service
        """
        self.parent = parent
        self.zone_service = zone_service
        self.device_service = device_service

        # State
        self._creation_window: ZoneCreationWindow = None
        self._selected_sensors: Set[int] = set()
        self._floor_plan_controller = None  # Will be set externally

    def set_floor_plan_controller(self, controller):
        """Set floor plan controller reference.

        Args:
            controller: FloorPlanController instance
        """
        self._floor_plan_controller = controller
        if controller:
            controller.on_sensor_selected = self._handle_sensor_selection

    def start_zone_creation(self):
        """Start safety zone creation process."""
        # Ask for zone name
        zone_name = simpledialog.askstring("New Safety Zone", "Enter zone name:")
        if not zone_name:
            return

        # Validate zone name
        from ..utils.validators import validate_zone_name

        is_valid, error = validate_zone_name(zone_name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error)
            return

        # Clear previous selections
        self._selected_sensors.clear()
        for device in self.device_service.get_all_devices():
            device.is_selected = False

        # Enable zone creation mode on floor plan
        if self._floor_plan_controller:
            self._floor_plan_controller.set_zone_creation_mode(True)

        # Show creation window
        self._creation_window = ZoneCreationWindow(
            self.parent,
            zone_name,
            self.device_service.get_all_devices(),
            on_finish=self._handle_zone_finish,
            on_cancel=self._handle_zone_cancel,
        )
        self._creation_window.show()

    def _handle_sensor_selection(self, device):
        """Handle sensor selection during zone creation.

        Args:
            device: Selected/deselected device
        """
        if device.is_selected:
            self._selected_sensors.add(device.device_id)
        else:
            self._selected_sensors.discard(device.device_id)

        # Update creation window
        if self._creation_window:
            self._creation_window.update_selection(self._selected_sensors)

    def _handle_zone_finish(self, zone_name: str, sensor_ids: list):
        """Handle zone creation finish.

        Args:
            zone_name: Zone name
            sensor_ids: List of sensor IDs
        """
        try:
            zone_id = self.zone_service.create_zone(zone_name, sensor_ids)

            messagebox.showinfo(
                "Success",
                f"Safety Zone '{zone_name}' created with {len(sensor_ids)} sensors.",
            )

            self._cleanup_zone_creation()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create zone: {e}")

    def _handle_zone_cancel(self):
        """Handle zone creation cancellation."""
        self._cleanup_zone_creation()

    def _cleanup_zone_creation(self):
        """Clean up zone creation state."""
        # Clear selections
        self._selected_sensors.clear()
        for device in self.device_service.get_all_devices():
            device.is_selected = False

        # Disable zone creation mode
        if self._floor_plan_controller:
            self._floor_plan_controller.set_zone_creation_mode(False)

        # Close window
        if self._creation_window:
            self._creation_window.close()
            self._creation_window = None
