"""Display and LED handler for control panel."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class DisplayHandler:
    """Handles display and LED updates."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def init_off_display(self):
        """Initialize display for OFF state."""
        self._panel.set_powered_led(False)
        self._panel.set_armed_led(False)
        self._panel.set_display_short_message1("System OFF")
        self._panel.set_display_short_message2("Press 1 to start")
        self._panel.set_display_away(False)
        self._panel.set_display_stay(False)

    def show_booting(self):
        """Show booting message."""
        self._panel.set_display_short_message1("Starting...")
        self._panel.set_display_short_message2("Please wait")
        self._panel.set_powered_led(True)

    def show_idle(self):
        """Show idle/login prompt."""
        self._panel.set_display_short_message1("Enter password")
        self._panel.set_display_short_message2("")

    def show_welcome(self, access_level: str):
        """Show welcome message after login."""
        self._panel.set_display_short_message1(f"Welcome ({access_level})")
        self._panel.set_display_short_message2("7=Away 8=Home")

    def show_locked(self):
        """Show locked message."""
        self._panel.set_display_short_message1("LOCKED")
        self._panel.set_display_short_message2("Wait 60 sec")

    def show_wrong_password(self, attempts: int):
        """Show wrong password message."""
        self._panel.set_display_short_message1("Wrong password")
        self._panel.set_display_short_message2(f"{attempts} tries left")

    def show_stopping(self):
        """Show stopping message."""
        self._panel.set_display_short_message1("Stopping...")
        self._panel.set_display_short_message2("Please wait")

    def show_resetting(self):
        """Show resetting message."""
        self._panel.set_display_short_message1("Resetting...")
        self._panel.set_display_short_message2("Please wait")

    def update_leds_from_status(self, data: dict):
        """Update LEDs based on system status."""
        armed = data.get("armed", False)
        mode = data.get("mode", "DISARMED")
        self._panel.set_armed_led(armed)
        self._panel.set_display_away(mode == "AWAY")
        self._panel.set_display_stay(mode == "HOME")

