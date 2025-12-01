"""State transition logic for control panel."""
from typing import TYPE_CHECKING

from .controllers.mode_manager import ControlPanelModeManager

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class StateTransitions:
    """Delegates transitions to ControlPanelModeManager."""

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._manager = ControlPanelModeManager(panel)

    def turn_on(self):
        self._manager.turn_on()

    def turn_off(self):
        self._manager.turn_off()

    def reset(self):
        self._manager.reset()

    def try_login(self):
        self._manager.try_login()

    def start_pw_change(self):
        self._manager.start_pw_change()

    def finish_pw_change(self):
        self._manager.finish_pw_change()


