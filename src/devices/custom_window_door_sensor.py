"""Custom window/door sensor that extends the TA virtual device."""

from ..virtual_devices.device_windoor_sensor import DeviceWinDoorSensor as BaseWinDoorSensor
from .custom_window_door_sensor_features import WinDoorSensorStatusMixin


class CustomWinDoorSensor(WinDoorSensorStatusMixin, BaseWinDoorSensor):
    """Detailed virtual window/door contact sensor."""

    def __init__(self, location: str, sensor_id: int, sensor_subtype: str = "door"):
        super().__init__()
        self.sensor_id = sensor_id
        self._location = location
        self._subtype = sensor_subtype
        self._battery_level = 100.0

    def arm(self) -> bool:
        """Arm the sensor. Cannot arm if door/window is currently open."""
        if self.opened:
            return False
        super().arm()
        return True

    def disarm(self) -> bool:
        """Disarm the sensor."""
        super().disarm()
        return True

    def read(self) -> bool:
        """Returns True if door/window is open AND sensor is armed."""
        return self.armed and self.opened

    def set_open(self, is_open: bool):
        """Simulate opening/closing the sensor."""
        if is_open:
            self.intrude()
        else:
            self.release()

    def open(self):
        """Simulate opening."""
        self.set_open(True)

    def close(self):
        """Simulate closing."""
        self.set_open(False)
