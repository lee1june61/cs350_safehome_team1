"""
Custom Window/Door contact sensor implementation.
A detailed magnetic contact sensor simulation that extends the base virtual device.
"""
from ..virtual_devices.device_windoor_sensor import DeviceWinDoorSensor as BaseWinDoorSensor


class CustomWinDoorSensor(BaseWinDoorSensor):
    """
    A custom, more detailed virtual window/door contact sensor.
    It simulates battery drain and provides a richer interface, while extending
    the base DeviceWinDoorSensor.
    """
    
    def __init__(self, location: str, sensor_id: int, sensor_subtype: str = "door"):
        """
        Initialize the custom window/door sensor.
        
        Args:
            location: Physical location (e.g., "Front Door", "Kitchen Window")
            sensor_id: Unique sensor identifier
            sensor_subtype: Type of sensor ("door" or "window")
        """
        super().__init__()
        # Override the ID assigned by the base class
        self.sensor_id = sensor_id
        
        self._location = location
        self._subtype = sensor_subtype  # "door" or "window"
        self._battery_level = 100.0
        
        # The state 'self.opened' and 'self.armed' are inherited from BaseWinDoorSensor
        # and will be the single source of truth.

    # ============================================================
    # Override and extend base class methods
    # ============================================================
    
    def arm(self) -> bool:
        """
        Arm the sensor.
        Cannot arm if door/window is currently open (safety feature).
        """
        if self.opened:
            return False  # Cannot arm when open
        
        super().arm()
        return True
    
    def disarm(self) -> bool:
        """Disarm the sensor."""
        super().disarm()
        return True

    def read(self) -> bool:
        """
        Returns True if door/window is open AND sensor is armed.
        This is the triggered state.
        """
        # This now relies entirely on the state from the base class
        return self.armed and self.opened

    # ============================================================
    # Custom methods specific to this detailed simulation
    # ============================================================
    
    def get_location(self) -> str:
        return self._location

    def get_type(self) -> str:
        return f"{self._subtype}_sensor"

    def get_sensor_id(self) -> int:
        """Get sensor ID."""
        return self.sensor_id

    def get_subtype(self) -> str:
        """Get sensor subtype (door or window)."""
        return self._subtype

    def get_battery_level(self) -> int:
        """Get battery level."""
        if self.armed and self._battery_level > 0:
            self._battery_level -= 0.005
        
        return max(0, int(self._battery_level))

    def set_open(self, is_open: bool):
        """
        Simulate opening/closing the sensor.
        This updates the state in the base class.
        
        Args:
            is_open: True to simulate open, False for closed
        """
        if is_open:
            self.intrude()  # Sets self.opened = True in base class
        else:
            self.release()  # Sets self.opened = False in base class

    def is_open(self) -> bool:
        """Check if door/window is currently open."""
        return self.opened

    def is_closed(self) -> bool:
        """Check if door/window is currently closed."""
        return not self.opened
    
    def open(self):
        """Simulate opening (convenience method for testing)."""
        self.set_open(True)
    
    def close(self):
        """Simulate closing (convenience method for testing)."""
        self.set_open(False)

    def can_arm(self) -> bool:
        """Check if sensor can be armed (must be closed)."""
        return not self.opened

    def get_status(self) -> dict:
        """Get comprehensive sensor status."""
        return {
            'id': f"S{self.sensor_id}",
            'type': self.get_type(),
            'subtype': self._subtype,
            'location': self._location,
            'armed': self.armed,
            'is_open': self.opened,
            'triggered': self.read(),
            'battery': self.get_battery_level(),
            'can_arm': self.can_arm()
        }
    
    def __repr__(self):
        status = "ARMED" if self.armed else "DISARMED"
        state = "OPEN" if self.opened else "CLOSED"
        trigger = " [TRIGGERED]" if self.read() else ""
        return (
            f"CustomWinDoorSensor(id={self.sensor_id}, type={self._subtype}, "
            f"location='{self._location}', state={state}, status={status}{trigger})"
        )
