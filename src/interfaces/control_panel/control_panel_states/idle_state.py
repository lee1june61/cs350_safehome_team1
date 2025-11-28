from .__init__ import ControlPanelState
from .logged_in_state import LoggedInState # Assuming LoggedInState will be in its own file
from .locked_state import LockedState # Assuming LockedState will be in its own file

class IdleState(ControlPanelState):
    def enter(self) -> None:
        self._panel.set_display_short_message1("Enter password")
        self._panel.set_display_short_message2("")
        self._panel._pw_buffer = ''
        self._panel._attempts = 3 # Reset attempts

    def exit(self) -> None:
        pass

    def handle_digit(self, digit: str) -> None:
        self._panel._pw_buffer += digit
        self._panel.set_display_short_message2('*' * len(self._panel._pw_buffer))
        if len(self._panel._pw_buffer) == 4:
            self._try_login()

    def _try_login(self) -> None:
        res = self._req('login_control_panel', password=self._panel._pw_buffer)
        self._panel._pw_buffer = ''
        if res.get('success'):
            self._panel._access_level = res.get('access_level', 'GUEST')
            self._panel._attempts = 3
            self._panel.transition_to(LoggedInState(self._panel))
        else:
            self._panel._attempts -= 1
            if self._panel._attempts <= 0:
                self._panel.transition_to(LockedState(self._panel))
            else:
                self._panel.set_display_short_message1("Wrong password")
                self._panel.set_display_short_message2(f"{self._panel._attempts} tries left")
