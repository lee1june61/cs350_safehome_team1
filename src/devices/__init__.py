"""
SafeHome Devices Package

This package contains custom device implementations that extend the base
virtual devices.
"""

# Import interfaces
from .interfaces import InterfaceCamera, InterfaceSensor

# Import device implementations
from .cameras.device_camera import DeviceCamera
from .sensors.motion_sensor import DeviceMotionDetector
from .sensors.window_door_sensor import DeviceWinDoorSensor
from .control_panel_abstract import DeviceControlPanelAbstract


__all__ = [
    "CustomDeviceCamera",
    "CustomMotionDetector",
    "CustomWinDoorSensor",
    "DeviceControlPanelAbstract",
]
