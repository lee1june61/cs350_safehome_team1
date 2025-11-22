"""
Motion detection sensor implementation.
PIR (Passive Infrared) motion sensor simulation.
"""
import random
import time
from .interfaces import InterfaceSensor


class DeviceMotionDetector(InterfaceSensor):
    """
    Virtual motion detection sensor.
    Simulates PIR sensor behavior for detecting movement.
    """
    
    def __init__(self, location: str, sensor_id: int):
        """
        Initialize motion sensor.
        
        Args:
            location: Physical location (e.g., "Hallway", "Living Room")
            sensor_id: Unique sensor identifier
        """
        self._location = location
        self._sensor_id = sensor_id
        self._armed = False
        self._triggered = False
        self._battery_level = 100.0
        self._last_trigger_time = 0
        self._detection_range = 5.0  # meters
        self._sensitivity = 0.5  # 0.0 (low) to 1.0 (high)
    
    # ============================================================
    # InterfaceSensor Implementation
    # ============================================================
    
    def get_location(self) -> str:
        return self._location
    
    def get_type(self) -> str:
        return "motion"
    
    def is_triggered(self) -> bool:
        """
        Check if motion is detected.
        In simulation mode, randomly triggers to simulate real motion detection.
        """
        if not self._armed:
            return False
        
        current_time = time.time()
        
        # Cooldown period (prevent rapid re-triggering)
        if current_time - self._last_trigger_time < 5:
            return self._triggered
        
        # Simulate random motion detection (10% chance per check when armed)
        # In real implementation, this would read from actual PIR sensor
        if random.random() < (0.1 * self._sensitivity):
            self._triggered = True
            self._last_trigger_time = current_time
            return True
        
        self._triggered = False
        return False
    
    def arm(self) -> bool:
        """Arm the motion sensor for detection."""
        self._armed = True
        self._triggered = False
        return True
    
    def disarm(self) -> bool:
        """Disarm the motion sensor."""
        self._armed = False
        self._triggered = False
        return True
    
    def is_armed(self) -> bool:
        return self._armed
    
    def get_battery_level(self) -> int:
        """Get battery level (slowly drains when armed)."""
        # Simulate slow battery drain
        if self._armed and self._battery_level > 0:
            self._battery_level -= 0.01
        
        return max(0, int(self._battery_level))
    
    # ============================================================
    # Additional Motion Sensor Methods
    # ============================================================
    
    def get_sensor_id(self) -> int:
        """Get sensor ID."""
        return self._sensor_id
    
    def reset_trigger(self):
        """Reset triggered state (for testing/simulation)."""
        self._triggered = False
        self._last_trigger_time = 0
    
    def force_trigger(self):
        """Force trigger for testing purposes."""
        if self._armed:
            self._triggered = True
            self._last_trigger_time = time.time()
    
    def set_sensitivity(self, sensitivity: float):
        """
        Set detection sensitivity.
        
        Args:
            sensitivity: Value between 0.0 (low) and 1.0 (high)
        """
        self._sensitivity = max(0.0, min(1.0, sensitivity))
    
    def get_sensitivity(self) -> float:
        """Get current sensitivity setting."""
        return self._sensitivity
    
    def set_detection_range(self, range_meters: float):
        """Set detection range in meters."""
        self._detection_range = max(1.0, range_meters)
    
    def get_detection_range(self) -> float:
        """Get detection range in meters."""
        return self._detection_range
    
    def get_status(self) -> dict:
        """Get comprehensive sensor status."""
        return {
            'sensor_id': self._sensor_id,
            'type': 'motion',
            'location': self._location,
            'armed': self._armed,
            'triggered': self._triggered,
            'battery': self.get_battery_level(),
            'sensitivity': self._sensitivity,
            'range': self._detection_range,
            'last_trigger': self._last_trigger_time
        }
    
    def __repr__(self):
        status = "ARMED" if self._armed else "DISARMED"
        trigger = " [TRIGGERED]" if self._triggered else ""
        return (
            f"DeviceMotionDetector(id={self._sensor_id}, location='{self._location}', "
            f"status={status}{trigger}, battery={self.get_battery_level()}%)"
        )