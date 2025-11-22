"""Device interfaces for SafeHome system.

This package contains abstract interfaces for all SafeHome devices.
"""

from .camera import InterfaceCamera
from .sensor import InterfaceSensor
from .control_panel import DeviceControlPanelAbstract

__all__ = [
    'InterfaceCamera',
    'InterfaceSensor',
    'DeviceControlPanelAbstract',
]
