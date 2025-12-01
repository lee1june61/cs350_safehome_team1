"""Text display helpers for the control panel."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..control_panel import SafeHomeControlPanel


class DisplayMessages:
    """Handles the two-line display text."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def init_off(self):
        self._panel.set_display_short_message1("System OFF")
        self._panel.set_display_short_message2("Press 1 to start")

    def show_booting(self):
        self._panel.set_display_short_message1("Starting...")
        self._panel.set_display_short_message2("Please wait")

    def show_idle(self):
        self._panel.set_display_short_message1("Enter password")
        self._panel.set_display_short_message2("")

    def show_welcome(self, access_level: str):
        self._panel.set_display_short_message1(f"Welcome ({access_level})")
        self._panel.set_display_short_message2("7=Away 8=Home")

    def show_locked(self, message: str = "Wait 60 sec"):
        self._panel.set_display_short_message1("LOCKED")
        self._panel.set_display_short_message2(message)

    def show_wrong_password(self, attempts: int):
        self._panel.set_display_short_message1("Wrong password")
        self._panel.set_display_short_message2(f"{attempts} tries left")

    def show_stopping(self):
        self._panel.set_display_short_message1("Stopping...")
        self._panel.set_display_short_message2("Please wait")

    def show_resetting(self):
        self._panel.set_display_short_message1("Resetting...")
        self._panel.set_display_short_message2("Please wait")

    def show_password_prompt(self, line1: str, line2: str = ""):
        self._panel.set_display_short_message1(line1)
        self._panel.set_display_short_message2(line2)

