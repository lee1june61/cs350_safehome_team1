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

    def arm_home(self):
        """Arm system in HOME (stay) mode."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        res = self._panel._system_ctrl.arm("HOME")
        if res.get("success"):
            self._panel.set_display_short_message1("HOME mode")
            self._panel.set_display_short_message2("Perimeter armed")
        else:
            self._panel.set_display_short_message1("Cannot arm HOME")
            self._panel.set_display_short_message2(res.get("message", "")[:20])
        self._panel._update_leds()

    def panic(self):
        """Trigger panic alarm and require master password to cancel."""
        self._panel._system_ctrl.panic()
        self._panel.enter_panic_verification()

    def handle_panic_code(self):
        """Process master password input during panic."""
        res = self._panel._password.verify_master_code()
        if res.get("success"):
            self._panel.set_display_short_message1("Panic cleared")
            self._panel.set_display_short_message2("")
            self._panel.send_request("clear_alarm")
            self._panel.exit_panic_verification()
            return

        if res.get("locked"):
            seconds = res.get("seconds_remaining") or res.get("lock_duration")
            msg = res.get("message", "Locked")
            self._panel.show_panic_lock(msg, int(seconds or 0))
        else:
            attempts = res.get("attempts_remaining")
            msg = res.get("message", "Incorrect")
            detail = f"{attempts} attempts left" if attempts is not None else ""
            self._panel.set_display_short_message1(msg[:16])
            self._panel.set_display_short_message2(detail[:16])

