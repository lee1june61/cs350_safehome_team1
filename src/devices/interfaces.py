"""
Device interfaces exposed through the SafeHome namespace.
"""

from ..virtual_devices.interface_camera import (
    InterfaceCamera as _VirtualInterfaceCamera,
)
from .sensors.interface_sensor import InterfaceSensor as _SensorInterface


class InterfaceCamera(_VirtualInterfaceCamera):
    """Thin wrapper over the TA camera interface."""

    pass


class InterfaceSensor(_SensorInterface):
    """Reuse the sensor interface wrapper from the sensors package."""

    pass
