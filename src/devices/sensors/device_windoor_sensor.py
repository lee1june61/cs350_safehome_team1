"""
Wrappers around TA-provided virtual window/door sensor.
"""

from src.virtual_devices.device_windoor_sensor import (
    DeviceWinDoorSensor as _VirtualDeviceWinDoorSensor,
)


class DeviceWinDoorSensor(_VirtualDeviceWinDoorSensor):
    """Expose TA window/door sensor through the devices namespace."""

    pass
