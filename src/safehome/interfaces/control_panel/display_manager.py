"""Display Manager.

Manages control panel display hardware only.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from device.device_control_panel_abstract import (
        DeviceControlPanelAbstract
    )


class DisplayManager:
    """Manages control panel display hardware."""
    
    def __init__(self, panel: 'DeviceControlPanelAbstract') -> None:
        """Initialize display manager.
        
        Args:
            panel: Control panel hardware instance
        """
        self.panel = panel
    
    def initialize(self) -> None:
        """Initialize display to default state."""
        self.panel.set_powered_led(True)
        self.panel.set_armed_led(False)
        self.panel.set_display_away(False)
        self.panel.set_display_stay(False)
        self.panel.set_display_not_ready(False)
        self.panel.set_security_zone_number(0)
    
    def show_message(self, line1: str, line2: str = "") -> None:
        """Show message on display.
        
        Args:
            line1: First line message
            line2: Second line message (optional)
        """
        self.panel.set_display_short_message1(line1)
        if line2:
            self.panel.set_display_short_message2(line2)
    
    def show_masked_password(self, length: int, mask: str = "*") -> None:
        """Show masked password on display.
        
        Args:
            length: Length of password entered
            mask: Mask character
        """
        masked = mask * length
        self.panel.set_display_short_message2(f"Code: {masked}")
    
    def set_armed_led(self, armed: bool) -> None:
        """Set armed LED status.
        
        Args:
            armed: True if armed
        """
        self.panel.set_armed_led(armed)
    
    def set_away_mode(self, active: bool) -> None:
        """Set away mode display.
        
        Args:
            active: True if away mode active
        """
        self.panel.set_display_away(active)
    
    def set_stay_mode(self, active: bool) -> None:
        """Set stay mode display.
        
        Args:
            active: True if stay mode active
        """
        self.panel.set_display_stay(active)
    
    def clear_mode_indicators(self) -> None:
        """Clear all mode indicators."""
        self.panel.set_display_away(False)
        self.panel.set_display_stay(False)