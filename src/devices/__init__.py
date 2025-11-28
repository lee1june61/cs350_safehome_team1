"""
SafeHome Devices Package

Only the camera-related APIs are imported eagerly here to avoid pulling in
sensor modules (which may not be needed for every test suite).
"""

from .interfaces import InterfaceCamera, InterfaceSensor
from .cameras.device_camera import DeviceCamera
from .cameras.safehome_camera import SafeHomeCamera
from .custom_device_camera import CustomDeviceCamera
from .custom_motion_detector import CustomMotionDetector
from .custom_window_door_sensor import CustomWinDoorSensor
from .control_panel_abstract import DeviceControlPanelAbstract

# Import sensor-related classes from the sensors subpackage
from .sensors import (
    Sensor,
    WindowDoorSensor,
    MotionSensor,
    SensorController,
    DeviceSensorTester,
    DeviceWinDoorSensor,
    DeviceMotionDetector,
)

# Import alarm
from .alarm import Alarm

__all__ = [
    "InterfaceCamera",
    "InterfaceSensor",
    "DeviceCamera",
    "SafeHomeCamera",
    "CustomDeviceCamera",
    "CustomMotionDetector",
    "CustomWinDoorSensor",
    "DeviceSensorTester",
    "DeviceWinDoorSensor",
    "DeviceMotionDetector",
    "DeviceControlPanelAbstract",
    "Sensor",
    "WindowDoorSensor",
    "MotionSensor",
    "SensorController",
    "Alarm",
]
