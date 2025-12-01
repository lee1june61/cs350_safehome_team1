"""System control handler for control panel."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class SystemHandler:
    """Handles system on/off/reset and arm/disarm."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def turn_on(self):
        """Send turn on command to system."""
        self._panel.send_request("turn_on")

    def turn_off(self):
        """Send turn off command to system."""
        self._panel.send_request("turn_off")

    def reset(self):
        """Send reset command to system."""
        self._panel.send_request("reset_system")

    def arm(self, mode: str) -> dict:
        """Arm system with specified mode."""
        return self._panel.send_request("arm_system", mode=mode)

    def disarm(self):
        """Disarm system."""
        self._panel.send_request("disarm_system")

    def panic(self):
        """Trigger panic alarm."""
        self._panel.send_request("panic")

    def get_status(self) -> dict:
        """Get current system status."""
        return self._panel.send_request("get_status")






