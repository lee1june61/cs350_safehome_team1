from .__init__ import ControlPanelState
from .idle_state import IdleState # Assuming IdleState will be in its own file

class LockedState(ControlPanelState):
    def enter(self) -> None:
        self._panel.set_display_short_message1("LOCKED")
        self._panel.set_display_short_message2("Wait 60 sec")
        self._panel.after(60000, self._unlock)

    def exit(self) -> None:
        pass

    def _unlock(self) -> None:
        self._panel._attempts = 3
        self._panel.transition_to(IdleState(self._panel))
