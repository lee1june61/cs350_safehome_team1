"""Control panel state/mode transitions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..control_panel import SafeHomeControlPanel


class ControlPanelModeManager:
    """Encapsulates state transitions and lock countdowns."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def turn_on(self):
        if self._panel._state != self._panel.STATE_OFF:
            return
        self._panel._state = self._panel.STATE_BOOTING
        self._panel._display.show_booting()
        self._panel.after(1000, self._boot_done)

    def _boot_done(self):
        self._panel._system_ctrl.turn_on()
        self._panel._state = self._panel.STATE_IDLE
        self._panel._display.show_idle()
        self._panel._alarm.start_polling()

    def turn_off(self):
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        self._panel._display.show_stopping()
        self._panel.after(500, self._complete_off)

    def _complete_off(self):
        self._panel._system_ctrl.turn_off()
        self._panel._password.reset()
        self._panel._alarm.stop_polling()
        self._panel._state = self._panel.STATE_OFF
        self._panel._display.init_off_display()

    def reset(self):
        if self._panel._state != self._panel.STATE_LOGGED_IN:
            return
        self._panel._display.show_resetting()
        self._panel.after(500, self._complete_reset)

    def _complete_reset(self):
        self._panel._system_ctrl.reset()
        self._panel._state = self._panel.STATE_OFF
        self._panel._display.init_off_display()
        self._panel.after(300, self.turn_on)

    def try_login(self):
        if self._panel._password.try_login():
            self._panel._state = self._panel.STATE_LOGGED_IN
            self._panel._display.show_welcome(self._panel._password.access_level)
            self._panel._display.cancel_lock_countdown()
            self._panel._update_leds()
        elif self._panel._password.is_locked_out():
            self._panel._state = self._panel.STATE_LOCKED
            self._panel._display.show_locked()
            duration_ms = self._panel._password.lock_time_ms
            self._panel._display.start_lock_countdown(self._panel._password.lock_time_seconds)
            self._panel.after(duration_ms, self._unlock)
        else:
            attempts = self._panel._password.get_remaining_attempts()
            self._panel._display.show_wrong_password(attempts)

    def _unlock(self):
        self._panel._password.unlock()
        self._panel._state = self._panel.STATE_IDLE
        self._panel._display.cancel_lock_countdown()
        self._panel._display.show_idle()

    def start_pw_change(self):
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
        self._panel._password.finish_change()
        self._panel._state = self._panel.STATE_LOGGED_IN
        self._panel.set_display_short_message1("Password changed")
        self._panel.set_display_short_message2("")

