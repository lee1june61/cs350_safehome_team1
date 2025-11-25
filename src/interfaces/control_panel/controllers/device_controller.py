"""Device control controller."""

import tkinter as tk
from tkinter import messagebox, simpledialog
from ..models.device_icon import DeviceIcon
from ..services.device_service import DeviceService
from ..views.device_windows import (
    SensorWindow,
    CameraWindow,
    CameraFeedWindow,
    CameraPTZWindow,
)


class DeviceController:
    """Controller for device operations.

    Handles device detail windows and operations.
    """

    def __init__(self, parent: tk.Widget, device_service: DeviceService, system):
        """Initialize device controller.

        Args:
            parent: Parent widget
            device_service: Device service
            system: SafeHome system instance
        """
        self.parent = parent
        self.device_service = device_service
        self.system = system

    def show_device_window(self, device: DeviceIcon):
        """Show appropriate window for device.

        Args:
            device: Device to show
        """
        if device.is_sensor:
            self._show_sensor_window(device)
        else:
            self._show_camera_window(device)

    def _show_sensor_window(self, device: DeviceIcon):
        """Show sensor control window.

        Args:
            device: Sensor device
        """
        window = SensorWindow(
            self.parent,
            device,
            on_arm=self._handle_arm_sensor,
            on_disarm=self._handle_disarm_sensor,
        )
        window.show()

    def _show_camera_window(self, device: DeviceIcon):
        """Show camera control window.

        Args:
            device: Camera device
        """
        window = CameraWindow(
            self.parent,
            device,
            on_enable=self._handle_enable_camera,
            on_disable=self._handle_disable_camera,
            on_view_feed=self._handle_view_feed,
            on_ptz=self._handle_ptz,
            on_set_password=self._handle_set_password,
        )
        window.show()

    def _handle_arm_sensor(self, sensor_id: int) -> bool:
        """Handle arm sensor request.

        Args:
            sensor_id: Sensor ID

        Returns:
            True if successful
        """
        try:
            return self.device_service.arm_sensor(sensor_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to arm sensor: {e}")
            return False

    def _handle_disarm_sensor(self, sensor_id: int) -> bool:
        """Handle disarm sensor request.

        Args:
            sensor_id: Sensor ID

        Returns:
            True if successful
        """
        try:
            return self.device_service.disarm_sensor(sensor_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disarm sensor: {e}")
            return False

    def _handle_enable_camera(self, camera_id: int) -> bool:
        """Handle enable camera request.

        Args:
            camera_id: Camera ID

        Returns:
            True if successful
        """
        return self.device_service.enable_camera(camera_id)

    def _handle_disable_camera(self, camera_id: int) -> bool:
        """Handle disable camera request.

        Args:
            camera_id: Camera ID

        Returns:
            True if successful
        """
        return self.device_service.disable_camera(camera_id)

    def _handle_view_feed(self, device: DeviceIcon):
        """Handle view camera feed request.

        Args:
            device: Camera device
        """
        window = CameraFeedWindow(self.parent, device, self.system)
        window.show()

    def _handle_ptz(self, device: DeviceIcon):
        """Handle PTZ control request.

        Args:
            device: Camera device
        """
        window = CameraPTZWindow(self.parent, device, self.system)
        window.show()

    def _handle_set_password(self, device: DeviceIcon):
        """Handle set camera password request.

        Args:
            device: Camera device
        """
        password = simpledialog.askstring(
            "Password", f"Set password for {device.name}:", show="*", parent=self.parent
        )

        if password:
            self.system.set_camera_password(device.device_id, password)
            messagebox.showinfo("Success", "Camera password set")
