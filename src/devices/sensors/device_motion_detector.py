"""
Wrappers around TA-provided virtual motion detector.
"""

from src.virtual_devices.device_motion_detector import (
    DeviceMotionDetector as _VirtualDeviceMotionDetector,
)


class DeviceMotionDetector(_VirtualDeviceMotionDetector):
    """Expose TA motion detector through the devices namespace."""

    pass
