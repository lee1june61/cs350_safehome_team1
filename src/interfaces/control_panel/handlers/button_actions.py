"""Button action handlers for control panel."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class ButtonActions:
    """Handles button press actions based on current state."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel

    def handle_digit(self, digit: str):
        """Handle digit button press."""
        state = self._panel._state
        if state == self._panel.STATE_IDLE:
            self._panel._password.add_digit(digit, self._try_login)
        elif state == self._panel.STATE_CHANGING_PW:
            self._panel._password.add_new_digit(digit, self._finish_pw_change)

    def handle_button1(self):
        """Handle button 1: Turn on or digit."""
        if self._panel._state == self._panel.STATE_OFF:
            self._turn_on()
        else:
            self.handle_digit("1")

    def handle_button3(self):
        """Handle button 3: Turn off or digit."""
        if self._panel._state == self._panel.STATE_LOGGED_IN:
            self._turn_off()
        else:
            self.handle_digit("3")

    def handle_button6(self):
        """Handle button 6: Reset or digit."""
        if self._panel._state == self._panel.STATE_LOGGED_IN:
            self._reset()
        else:
            self.handle_digit("6")

    def handle_button7(self):
        """Handle button 7: Arm AWAY or digit."""
        if self._panel._state == self._panel.STATE_LOGGED_IN:
            self._arm("AWAY")
        else:
            self.handle_digit("7")

    def handle_button8(self):
        """Handle button 8: Disarm (HOME) or digit."""
        if self._panel._state == self._panel.STATE_LOGGED_IN:
            self._disarm()
        else:
            self.handle_digit("8")

    def handle_button9(self):
        """Handle button 9: Change password or digit."""
        if self._panel._state == self._panel.STATE_LOGGED_IN:
            self._start_pw_change()
        else:
            self.handle_digit("9")

    def handle_panic(self):
        """Handle panic button (* or #)."""
        self._panel._system_ctrl.panic()
        self._panel.set_display_short_message1("PANIC!")
        self._panel.set_display_short_message2("Calling service...")







