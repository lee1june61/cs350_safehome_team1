"""
SafeHome Devices Module.
Contains all device implementations and interfaces.
"""

# Import interfaces
from .interfaces import InterfaceCamera, InterfaceSensor

# Import device implementations
from .camera import DeviceCamera
from .motion_sensor import DeviceMotionDetector
from .window_door_sensor import DeviceWinDoorSensor
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
