"""
Wrappers around TA-provided virtual sensor interfaces.
"""

from src.virtual_devices.interface_sensor import (
    InterfaceSensor as _VirtualInterfaceSensor,
)


class InterfaceSensor(_VirtualInterfaceSensor):
    """Keep TA interface under the devices namespace."""

    pass
