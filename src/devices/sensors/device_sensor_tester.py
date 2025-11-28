"""
Wrappers around TA-provided virtual sensor tester.
"""

from src.virtual_devices.device_sensor_tester import (
    DeviceSensorTester as _VirtualDeviceSensorTester,
)


class DeviceSensorTester(_VirtualDeviceSensorTester):
    """Expose TA sensor tester through the devices namespace."""

    pass
