"""Panic verification handler for control panel."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .control_panel import SafeHomeControlPanel


class PanicVerificationMixin:
    """Handles panic mode verification and lockout."""

    _panic_prev_state: Optional[str]
    _panic_lock_id: Optional[str]
    _panic_lock_seconds: int
    _panic_lock_message: str
    _panic_locked: bool
    _state: str
    _password: object
    _display: object

    def enter_panic_verification(self):
        """Prompt user for master password to cancel panic."""
        if self._state != "panic_verify":
            self._panic_prev_state = self._state
        self._state = "panic_verify"
        self._panic_locked = False
        self._password.clear_buffer()
        if hasattr(self._password, "clear_master_buffer"):
            self._password.clear_master_buffer()
        self.set_display_short_message1("PANIC MODE")
        self.set_display_short_message2("Enter master password")

    def exit_panic_verification(self):
        """Return to previous state after panic process."""
        self._clear_panic_lock_timer()
        self._panic_locked = False
        self._state = self._panic_prev_state or "idle"
        self._panic_prev_state = None
        self._password.clear_buffer()
        if hasattr(self._password, "clear_master_buffer"):
            self._password.clear_master_buffer()
        if self._state == "idle":
            self._display.show_idle()
        elif self._state == "logged_in":
            self._display.show_welcome(self._password.access_level)

    def show_panic_lock(self, message: str, seconds: int):
        self._panic_locked = True
        self._panic_lock_message = message or "Locked"
        self._panic_lock_seconds = max(seconds, 0)
        self._update_panic_lock_display()
        self._schedule_panic_lock_tick()

    def _update_panic_lock_display(self):
        timer_text = f"{self._panic_lock_seconds}s remaining" if self._panic_lock_seconds > 0 else ""
        self.set_display_short_message1(self._panic_lock_message[:16])
        self.set_display_short_message2(timer_text[:16])

    def _schedule_panic_lock_tick(self):
        self._clear_panic_lock_timer()
        if self._panic_lock_seconds <= 0:
            self.exit_panic_verification()
            return
        self._panic_lock_id = self.after(1000, self._tick_panic_lock)

    def _tick_panic_lock(self):
        self._panic_lock_seconds -= 1
        self._update_panic_lock_display()
        if self._panic_lock_seconds <= 0:
            self.exit_panic_verification()
        else:
            self._panic_lock_id = self.after(1000, self._tick_panic_lock)

    def _clear_panic_lock_timer(self):
        if self._panic_lock_id:
            self.after_cancel(self._panic_lock_id)
            self._panic_lock_id = None

