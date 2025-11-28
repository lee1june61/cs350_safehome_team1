"""
ControlPanelState - State machine for the SafeHome Control Panel.

This module defines the abstract base class for control panel states and concrete
implementations for each state, handling input and state transitions.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel # Circular import, handled by TYPE_CHECKING


class ControlPanelState(ABC):
    """Abstract base class for all control panel states."""

    def __init__(self, panel: 'SafeHomeControlPanel'):
        self._panel = panel

    @abstractmethod
    def enter(self) -> None:
        """Actions to perform when entering this state."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Actions to perform when exiting this state."""
        pass

    def handle_digit(self, digit: str) -> None:
        """Handle digit input (0-9)."""
        pass

    def handle_button1(self) -> None:
        """Handle button 1 press."""
        pass

    def handle_button3(self) -> None:
        """Handle button 3 press."""
        pass

    def handle_button6(self) -> None:
        """Handle button 6 press."""
        pass

    def handle_button7(self) -> None:
        """Handle button 7 press."""
        pass

    def handle_button8(self) -> None:
        """Handle button 8 press."""
        pass

    def handle_button9(self) -> None:
        """Handle button 9 press."""
        pass

    def handle_button_star(self) -> None:
        """Handle '*' button press."""
        pass

    def handle_button_sharp(self) -> None:
        """Handle '#' button press."""
        pass

    def _req(self, cmd: str, **kw) -> Dict[str, Any]:
        """Helper to send request to system."""
        return self._panel.req(cmd, **kw)


from .off_state import OffState
from .booting_state import BootingState
from .idle_state import IdleState
from .logged_in_state import LoggedInState
from .changing_password_state import ChangingPasswordState
from .locked_state import LockedState
