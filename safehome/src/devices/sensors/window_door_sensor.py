"""
Window/Door contact sensor implementation.
Magnetic contact sensor for detecting open/closed state.
"""
from ..interfaces import InterfaceSensor


class DeviceWinDoorSensor(InterfaceSensor):
    """
    Virtual window/door contact sensor.
    Detects when doors or windows are opened using magnetic contact.
    """
    
    def __init__(self, location: str, sensor_id: int, sensor_subtype: str = "door"):
        """
        Initialize window/door sensor.
        
        Args:
            location: Physical location (e.g., "Front Door", "Kitchen Window")
            sensor_id: Unique sensor identifier
            sensor_subtype: Type of sensor ("door" or "window")
        """
        self._location = location
        self._sensor_id = sensor_id
        self._subtype = sensor_subtype  # "door" or "window"
        self._armed = False
        self._is_open = False  # True = open (contact broken), False = closed
        self._battery_level = 100.0
    
    # ============================================================
    # InterfaceSensor Implementation
    # ============================================================
    
    def get_location(self) -> str:
        return self._location
    
    def get_type(self) -> str:
        return f"{self._subtype}_sensor"
    
    def is_triggered(self) -> bool:
        """
        Returns True if door/window is open AND sensor is armed.
        Triggered state = armed + open.
        """
        return self._armed and self._is_open
    
    def arm(self) -> bool:
        """
        Arm the sensor.
        Cannot arm if door/window is currently open (safety feature).
        """
        if self._is_open:
            return False  # Cannot arm when open
        
        self._armed = True
        return True
    
    def disarm(self) -> bool:
        """Disarm the sensor."""
        self._armed = False
        return True
    
    def is_armed(self) -> bool:
        return self._armed
    
    def get_battery_level(self) -> int:
        """Get battery level."""
        # Simulate very slow battery drain
        if self._armed and self._battery_level > 0:
            self._battery_level -= 0.005
        
        return max(0, int(self._battery_level))
    
    # ============================================================
    # Additional Window/Door Sensor Methods
    # ============================================================
    
    def get_sensor_id(self) -> int:
        """Get sensor ID."""
        return self._sensor_id
    
    def get_subtype(self) -> str:
        """Get sensor subtype (door or window)."""
        return self._subtype
    
    def set_open(self, is_open: bool):
        """
        Simulate opening/closing (for testing).
        In real implementation, this would be read from magnetic contact.
        
        Args:
            is_open: True to simulate open, False for closed
        """
        self._is_open = is_open
    
    def is_open(self) -> bool:
        """Check if door/window is currently open."""
        return self._is_open
    
    def is_closed(self) -> bool:
        """Check if door/window is currently closed."""
        return not self._is_open
    
    def open(self):
        """Simulate opening (convenience method for testing)."""
        self.set_open(True)
    
    def close(self):
        """Simulate closing (convenience method for testing)."""
        self.set_open(False)
    
    def can_arm(self) -> bool:
        """Check if sensor can be armed (must be closed)."""
        return not self._is_open
    
    def get_status(self) -> dict:
        """Get comprehensive sensor status."""
        return {
            'sensor_id': self._sensor_id,
            'type': self.get_type(),
            'subtype': self._subtype,
            'location': self._location,
            'armed': self._armed,
            'is_open': self._is_open,
            'triggered': self.is_triggered(),
            'battery': self.get_battery_level(),
            'can_arm': self.can_arm()
        }
    
    def __repr__(self):
        status = "ARMED" if self._armed else "DISARMED"
        state = "OPEN" if self._is_open else "CLOSED"
        trigger = " [TRIGGERED]" if self.is_triggered() else ""
        return (
            f"DeviceWinDoorSensor(id={self._sensor_id}, type={self._subtype}, "
            f"location='{self._location}', state={state}, status={status}{trigger})"
        )
