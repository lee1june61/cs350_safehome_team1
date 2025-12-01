"""
Abstract control panel device interface.
Defines the interface for physical control panels or mobile apps.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from .control_panel_optional import ControlPanelOptionalFeatures


class DeviceControlPanelAbstract(ControlPanelOptionalFeatures, ABC):
    """
    Abstract base class for control panel devices.
    Both physical control panels and mobile apps implement this interface.
    """
    
    @abstractmethod
    def display_message(self, message: str, message_type: str = "info"):
        """
        Display a message on the control panel.
        
        Args:
            message: Message text to display
            message_type: Type of message - one of:
                - "info": Informational message (blue/normal)
                - "warning": Warning message (yellow/orange)
                - "error": Error message (red)
                - "alarm": Alarm condition (red, bold, urgent)
        """
        pass
    
    @abstractmethod
    def get_user_input(self, prompt: str, input_type: str = "text") -> Optional[str]:
        """
        Get user input from control panel.
        
        Args:
            prompt: Prompt message to display to user
            input_type: Type of input expected:
                - "text": Free text input
                - "password": Password (masked input)
                - "numeric": Numeric input only
                - "yes_no": Yes/No confirmation
        
        Returns:
            User input as string, or None if cancelled/timeout
        """
        pass
    
    @abstractmethod
    def show_system_status(self, status: Dict[str, Any]):
        """
        Display current system status on control panel.
        
        Args:
            status: Dictionary containing system status information:
                {
                    'mode': str,              # Current security mode
                    'is_armed': bool,         # Armed status
                    'zones': dict,            # Safety zone statuses
                    'alarms': list,           # Active alarms
                    'camera_count': int,      # Number of cameras
                    'sensor_count': int,      # Number of sensors
                    'logged_in_user': str,    # Current user
                }
        """
        pass
    
    @abstractmethod
    def play_alarm_sound(self, duration: float = 5.0):
        """
        Play alarm sound through control panel speaker.
        
        Args:
            duration: Duration in seconds (default 5.0)
        """
        pass
    
    @abstractmethod
    def update_zone_display(self, zone_id: int, zone_name: str, is_armed: bool):
        """
        Update safety zone display on control panel.
        
        Args:
            zone_id: Unique zone identifier
            zone_name: Human-readable zone name
            is_armed: Whether the zone is currently armed
        """
        pass
    