"""
Alarm system component.
Manages alarm states and audible alerts.
"""
from typing import Optional


class Alarm:
    """
    Alarm controller for SafeHome system.
    Manages alarm triggering, sounding, and acknowledgment.
    """
    
    def __init__(self):
        """Initialize alarm system."""
        self._state = "INACTIVE"  # INACTIVE, TRIGGERED, SOUNDING, ACKNOWLEDGED
        self._trigger_reason = None
        self._trigger_time = None
    
    def trigger(self, reason: str):
        """Trigger the alarm."""
        print(f"Alarm: trigger(reason={reason}) called")
        self._state = "TRIGGERED"
        self._trigger_reason = reason
    
    def sound(self):
        """Start sounding the alarm."""
        print("Alarm: sound() called")
        self._state = "SOUNDING"
    
    def acknowledge(self):
        """Acknowledge alarm (silence it)."""
        print("Alarm: acknowledge() called")
        self._state = "ACKNOWLEDGED"
    
    def reset(self):
        """Reset alarm to inactive state."""
        print("Alarm: reset() called")
        self._state = "INACTIVE"
        self._trigger_reason = None
    
    def get_state(self) -> str:
        """Get current alarm state."""
        return self._state
    
    def is_active(self) -> bool:
        """Check if alarm is currently active (triggered or sounding)."""
        return self._state in ["TRIGGERED", "SOUNDING"]
    
    def get_trigger_reason(self) -> Optional[str]:
        """Get reason for alarm trigger."""
        return self._trigger_reason