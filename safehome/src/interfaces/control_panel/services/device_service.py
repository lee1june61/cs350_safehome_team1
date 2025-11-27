"""Device management service."""

from typing import List, Optional
from ..models.device_icon import DeviceIcon
from ..config.layout_config import DevicePositions


class DeviceService:
    """Service for managing devices and their states.

    Following the Device-related classes from SDS:
    - SensorController
    - CameraController
    - DeviceIcon management
    """

    def __init__(self, system):
        """Initialize device service.

        Args:
            system: SafeHome system instance
        """
        self.system = system
        self._devices: List[DeviceIcon] = []

    def initialize_devices(self) -> List[DeviceIcon]:
        """Initialize all devices with their positions.

        Returns:
            List of device icons
        """
        self._devices.clear()

        # Load window/door sensors
        for sid, name, x, y, armed in DevicePositions.WINDOW_DOOR_SENSORS:
            icon = DeviceIcon(sid, "window_door", x, y, name)
            icon.is_armed = armed
            self._devices.append(icon)

        # Load motion sensors
        for sid, name, x, y, armed in DevicePositions.MOTION_SENSORS:
            icon = DeviceIcon(sid, "motion", x, y, name)
            icon.is_armed = armed
            self._devices.append(icon)

        # Load cameras
        for cid, name, x, y, enabled in DevicePositions.CAMERAS:
            icon = DeviceIcon(cid, "camera", x, y, name)
            icon.is_enabled = enabled
            self._devices.append(icon)

        return self._devices

    def get_all_devices(self) -> List[DeviceIcon]:
        """Get all device icons."""
        return self._devices

    def get_device_by_id(self, device_id: int) -> Optional[DeviceIcon]:
        """Get device icon by ID."""
        for device in self._devices:
            if device.device_id == device_id:
                return device
        return None

    def get_sensors(self) -> List[DeviceIcon]:
        """Get all sensors (window_door and motion)."""
        return [d for d in self._devices if d.is_sensor]

    def get_cameras(self) -> List[DeviceIcon]:
        """Get all cameras."""
        return [d for d in self._devices if d.is_camera]

    def find_device_at_position(self, x: int, y: int) -> Optional[DeviceIcon]:
        """Find device at given position.

        Args:
            x, y: Coordinates to check

        Returns:
            DeviceIcon if found, None otherwise
        """
        for device in self._devices:
            if device.contains_point(x, y):
                return device
        return None

    def arm_sensor(self, device_id: int) -> bool:
        """Arm a sensor.

        Args:
            device_id: Sensor ID

        Returns:
            True if successful
        """
        try:
            if self.system.arm_safety_zone(device_id):
                device = self.get_device_by_id(device_id)
                if device:
                    device.is_armed = True
                return True
        except Exception as e:
            print(f"Error arming sensor {device_id}: {e}")
        return False

    def disarm_sensor(self, device_id: int) -> bool:
        """Disarm a sensor.

        Args:
            device_id: Sensor ID

        Returns:
            True if successful
        """
        try:
            if self.system.disarm_safety_zone(device_id):
                device = self.get_device_by_id(device_id)
                if device:
                    device.is_armed = False
                return True
        except Exception as e:
            print(f"Error disarming sensor {device_id}: {e}")
        return False

    def enable_camera(self, device_id: int) -> bool:
        """Enable a camera.

        Args:
            device_id: Camera ID

        Returns:
            True if successful
        """
        if self.system.enable_camera(device_id):
            device = self.get_device_by_id(device_id)
            if device:
                device.is_enabled = True
            return True
        return False

    def disable_camera(self, device_id: int) -> bool:
        """Disable a camera.

        Args:
            device_id: Camera ID

        Returns:
            True if successful
        """
        if self.system.disable_camera(device_id):
            device = self.get_device_by_id(device_id)
            if device:
                device.is_enabled = False
            return True
        return False
