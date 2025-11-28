from .__init__ import ControlPanelState
from .idle_state import IdleState # Assuming IdleState will be in its own file

class BootingState(ControlPanelState):
    def enter(self) -> None:
        self._panel.set_powered_led(True)
        self._panel.set_display_short_message1("Starting...")
        self._panel.set_display_short_message2("Please wait")
        self._panel.after(1000, self._boot_done)

    def exit(self) -> None:
        pass

    def _boot_done(self) -> None:
        self._req('turn_on')
        self._panel.transition_to(IdleState(self._panel))
