"""State transition logic for control panel."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class StateTransitions:
    """Handles state transitions and related actions."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def turn_on(self):
        """Start boot sequence."""
        if self._panel._state != self._panel.STATE_OFF:
            return
        self._panel._state = self._panel.STATE_BOOTING
        self._panel._display.show_booting()
        self._panel.after(1000, self._boot_done)

    def _boot_done(self):
        """Complete boot sequence."""
        self._panel._system_ctrl.turn_on()
        self._panel._state = self._panel.STATE_IDLE
        self._panel._display.show_idle()
        self._panel._alarm.start_polling()

    def turn_off(self):
        """Start shutdown sequence."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        self._panel._display.show_stopping()
        self._panel.after(500, self._complete_off)

    def _complete_off(self):
        """Complete shutdown."""
        self._panel._system_ctrl.turn_off()
        self._panel._password.reset()
        self._panel._alarm.stop_polling()
        self._panel._state = self._panel.STATE_OFF
        self._panel._display.init_off_display()

    def reset(self):
        """Start reset sequence."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        self._panel._display.show_resetting()
        self._panel.after(500, self._complete_reset)

    def _complete_reset(self):
        """Complete reset."""
        self._panel._system_ctrl.reset()
        self._panel._state = self._panel.STATE_OFF
        self._panel._display.init_off_display()
        self._panel.after(300, self.turn_on)

    def try_login(self):
        """Attempt login with entered password."""
        if self._panel._password.try_login():
            self._panel._state = self._panel.STATE_LOGGED_IN
            self._panel._display.show_welcome(self._panel._password.access_level)
            self._panel._display.cancel_lock_countdown()
            self._panel._update_leds()
        elif self._panel._password.is_locked_out():
            self._panel._state = self._panel.STATE_LOCKED
            self._panel._display.show_locked()
            duration_ms = self._panel._password.lock_time_ms
            self._panel._display.start_lock_countdown(
                self._panel._password.lock_time_seconds
            )
            self._panel.after(duration_ms, self._unlock)
        else:
            attempts = self._panel._password.get_remaining_attempts()
            self._panel._display.show_wrong_password(attempts)

    def _unlock(self):
        """Unlock after timeout."""
        self._panel._password.unlock()
        self._panel._state = self._panel.STATE_IDLE
        self._panel._display.cancel_lock_countdown()
        self._panel._display.show_idle()

    def start_pw_change(self):
        """Start password change mode."""
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        if not self._panel._password.is_master():
            self._panel.set_display_short_message1("Master only")
            return
        self._panel._state = self._panel.STATE_CHANGING_PW
        self._panel._password.start_change()
        self._panel.set_display_short_message1("New password:")
        self._panel.set_display_short_message2("")

    def finish_pw_change(self):
        """Complete password change."""
        self._panel._password.finish_change()
        self._panel._state = self._panel.STATE_LOGGED_IN
        self._panel.set_display_short_message1("Password changed")
        self._panel.set_display_short_message2("")


