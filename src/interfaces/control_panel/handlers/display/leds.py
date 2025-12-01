"""LED and indicator helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..control_panel import SafeHomeControlPanel


class LedController:
    """Updates LEDs and mode indicators."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def init_off(self):
        self._panel.set_powered_led(False)
        self._panel.set_armed_led(False)
        self._panel.set_display_away(False)
        self._panel.set_display_stay(False)

    def show_booting(self):
        self._panel.set_powered_led(True)

    def update_from_status(self, data: dict):
        armed = data.get("armed", False)
        mode = data.get("mode", "DISARMED")
        self._panel.set_armed_led(armed)
        self._panel.set_display_away(mode == "AWAY")
        self._panel.set_display_stay(mode == "HOME")






