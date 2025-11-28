"""Security actions (arm/disarm) for control panel."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class SecurityActions:
    """Handles arm/disarm and panic operations."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def arm(self, mode: str):
        """Arm system with specified mode."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        res = self._panel._system_ctrl.arm(mode)
        if res.get("success"):
            self._panel.set_display_short_message1(f"Armed: {mode}")
            self._panel.set_display_short_message2("")
        else:
            self._panel.set_display_short_message1("Cannot arm")
            msg = res.get("message", "")[:20]
            self._panel.set_display_short_message2(msg)
        self._panel._update_leds()

    def disarm(self):
        """Disarm system to HOME mode."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        self._panel._system_ctrl.disarm()
        self._panel.set_display_short_message1("HOME mode")
        self._panel.set_display_short_message2("Disarmed")
        self._panel._update_leds()

    def panic(self):
        """Trigger panic alarm."""
        self._panel._system_ctrl.panic()
        self._panel.set_display_short_message1("PANIC!")
        self._panel.set_display_short_message2("Calling service...")

