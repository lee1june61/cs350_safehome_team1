"""Display and LED handler for control panel."""
from typing import TYPE_CHECKING

from .display.messages import DisplayMessages
from .display.leds import LedController
from .display.lock_countdown import LockCountdown

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class DisplayHandler:
    """Coordinates text display, LEDs, and lock countdown."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._messages = DisplayMessages(panel)
        self._leds = LedController(panel)
        self._lock = LockCountdown(panel, self._messages)

    def init_off_display(self):
        self._lock.cancel()
        self._leds.init_off()
        self._messages.init_off()

    def show_booting(self):
        self._lock.cancel()
        self._leds.show_booting()
        self._messages.show_booting()

    def show_idle(self):
        self._lock.cancel()
        self._messages.show_idle()

    def show_welcome(self, access_level: str):
        self._lock.cancel()
        self._messages.show_welcome(access_level)

    def show_locked(self):
        self._messages.show_locked()

    def show_wrong_password(self, attempts: int):
        self._messages.show_wrong_password(attempts)

    def show_stopping(self):
        self._lock.cancel()
        self._messages.show_stopping()

    def show_resetting(self):
        self._lock.cancel()
        self._messages.show_resetting()

    def update_leds_from_status(self, data: dict):
        self._leds.update_from_status(data)

    def start_lock_countdown(self, total_seconds: int):
        self._lock.start(total_seconds)

    def cancel_lock_countdown(self):
        self._lock.cancel()


