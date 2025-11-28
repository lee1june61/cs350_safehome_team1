"""SafeHome Control Panel - Main entry point.

This is the refactored control panel following SOLID principles and
modern development practices:
- Single Responsibility: Each class has one clear purpose
- Separation of Concerns: Models, Views, Controllers, Services
- Dependency Injection: Controllers receive their dependencies
- MVP Pattern: Presenters (Controllers) mediate between Views and Services
"""

from typing import Optional
from ...devices import DeviceControlPanelAbstract
from .controllers.panel_controller import PanelController


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """Main control panel interface.

    This is a thin wrapper that delegates to the PanelController.
    Implements the DeviceControlPanelAbstract interface required by the system.

    Following the design from SDS document:
    - SafeHomeControlPanel class
    - State machine: SYSTEM_OFF -> BOOTING -> READY -> LOGGED_IN
    - Integration with System, LoginManager, ConfigurationManager
    """

    def __init__(self, system):
        """Initialize control panel.

        Args:
            system: SafeHome system instance
        """
        self.system = system
        self._controller: Optional[PanelController] = None

    def start(self):
        """Start the control panel GUI.

        This is the main entry point called by the system.
        """
        self._controller = PanelController(self.system)
        self._controller.start()

    def stop(self):
        """Stop the control panel."""
        if self._controller:
            self._controller.stop()

    # Abstract methods implementation (for compatibility)

    def display_message(self, message: str, message_type: str = "info"):
        """Display a message to the user.

        Args:
            message: Message to display
            message_type: Type of message (info, warning, error)
        """
        print(f"[{message_type.upper()}] {message}")

    def get_user_input(self, prompt: str, input_type: str = "text") -> Optional[str]:
        """Get input from user.

        Args:
            prompt: Prompt to display
            input_type: Type of input (text, password, etc.)

        Returns:
            User input or None if cancelled
        """
        from tkinter import simpledialog

        if input_type == "password":
            return simpledialog.askstring("Input", prompt, show="*")
        return simpledialog.askstring("Input", prompt)

    def show_system_status(self, status: dict):
        """Show system status.

        Args:
            status: Status dictionary
        """
        if self._controller and self._controller._current_screen:
            if hasattr(self._controller._current_screen, "update_status"):
                mode = status.get("mode", "Unknown")
                self._controller._current_screen.update_status(f"Mode: {mode}")

    def play_alarm_sound(self, duration: float = 5.0):
        """Play alarm sound.

        Args:
            duration: Duration in seconds
        """
        if self._controller and self._controller._window:
            self._controller._window.bell()

        from tkinter import messagebox

        messagebox.showwarning("ALARM", "🚨 ALARM TRIGGERED!")

    def update_zone_display(self, zone_id: int, zone_name: str, is_armed: bool):
        """Update safety zone display.

        Args:
            zone_id: Zone ID
            zone_name: Zone name
            is_armed: Whether zone is armed
        """
        # This would update the UI if we had a dedicated zone display
        pass
