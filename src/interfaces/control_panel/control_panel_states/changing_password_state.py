from .__init__ import ControlPanelState
from .logged_in_state import LoggedInState # Assuming LoggedInState will be in its own file

class ChangingPasswordState(ControlPanelState):
    def enter(self) -> None:
        self._panel._new_pw_buffer = ''
        self._panel.set_display_short_message1("New password:")
        self._panel.set_display_short_message2("")

    def exit(self) -> None:
        pass

    def handle_digit(self, digit: str) -> None:
        self._panel._new_pw_buffer += digit
        self._panel.set_display_short_message2('*' * len(self._panel._new_pw_buffer))
        if len(self._panel._new_pw_buffer) == 4:
            self._finish_pw_change()

    def _finish_pw_change(self) -> None:
        self._req('change_password', new_password=self._panel._new_pw_buffer)
        self._panel._new_pw_buffer = ''
        self._panel.set_display_short_message1("Password changed")
        self._panel.set_display_short_message2("")
        self._panel.transition_to(LoggedInState(self._panel))
