"""
SafeHome Devices Module.
Contains all device implementations and interfaces.
"""

# Import interfaces
from .interfaces import InterfaceCamera, InterfaceSensor

# Import device implementations
from .cameras.device_camera import DeviceCamera
from .sensors.motion_sensor import DeviceMotionDetector
from .sensors.window_door_sensor import DeviceWinDoorSensor
from .control_panel_abstract import DeviceControlPanelAbstract


__all__ = [
    # Interfaces
    'InterfaceCamera',
    'InterfaceSensor',
    'DeviceControlPanelAbstract',
    
    # Implementations
    'DeviceCamera',
    'DeviceMotionDetector',
    'DeviceWinDoorSensor',
]

__version__ = '1.0.0'
