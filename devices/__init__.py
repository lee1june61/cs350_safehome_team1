"""
SafeHome Devices Package
========================
This package contains device-related modules for the SafeHome security system.

Modules:
    cameras: Camera management and control
    sensors: Sensor management and monitoring (to be implemented by team)
    alarm: Alarm system (to be implemented by team)

Usage:
    from safehome.devices.cameras import CameraController
    
    controller = CameraController()
    cam_id = controller.add_camera(100, 200)
"""

# Camera module is implemented
from .cameras import (
    InterfaceCamera,
    DeviceCamera,
    SafeHomeCamera,
    CameraController
)

__all__ = [
    # Camera classes
    'InterfaceCamera',
    'DeviceCamera',
    'SafeHomeCamera',
    'CameraController',
]

__version__ = '1.0.0'
