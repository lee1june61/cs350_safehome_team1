from .__init__ import ControlPanelState
from .booting_state import BootingState # Assuming BootingState will be in its own file

class OffState(ControlPanelState):
    def enter(self) -> None:
        self._panel.set_powered_led(False)
        self._panel.set_armed_led(False)
        self._panel.set_display_short_message1("System OFF")
        self._panel.set_display_short_message2("Press 1 to start")
        self._panel.set_display_away(False)
        self._panel.set_display_stay(False)
        self._panel._pw_buffer = '' # Reset buffer on entering OFF

    def exit(self) -> None:
        pass

    def handle_button1(self) -> None:
        self._panel.transition_to(BootingState(self._panel))
