"""
Custom motion detection sensor.
A detailed PIR (Passive Infrared) motion sensor simulation that extends the base
virtual device.
"""

import random
import time
from ..virtual_devices.device_motion_detector import (
    DeviceMotionDetector as BaseMotionDetector,
)


class CustomMotionDetector(BaseMotionDetector):
    """
    A custom, more detailed virtual motion detection sensor.
    It simulates PIR sensor behavior, including battery drain, sensitivity,
    and random triggering, while extending the base DeviceMotionDetector.
    """

    def __init__(self, location: str, sensor_id: int):
        """
        Initialize the custom motion sensor.

        Args:
            location: Physical location (e.g., "Hallway", "Living Room")
            sensor_id: Unique sensor identifier
        """
        super().__init__()
        # Override the ID assigned by the base class to use the specific one provided.
        self.sensor_id = sensor_id

        self._location = location
        self._triggered = False  # Custom trigger state
        self._battery_level = 100.0
        self._last_trigger_time = 0
        self._detection_range = 5.0  # meters
        self._sensitivity = 0.5  # 0.0 (low) to 1.0 (high)

    # ============================================================
    # Override and extend base class methods
    # ============================================================

    def read(self) -> bool:
        """
        Check if motion is detected.
        In simulation mode, randomly triggers to simulate real motion detection
        and updates the base class state.
        """
        if not self.armed:  # 'self.armed' is from the base class
            return False

        current_time = time.time()

        # Cooldown period (prevent rapid re-triggering)
        if current_time - self._last_trigger_time < 5:
            return self.detected  # 'self.detected' is from the base class

        # Simulate random motion detection
        if random.random() < (0.1 * self._sensitivity):
            self._triggered = True
            self._last_trigger_time = current_time
            self.intrude()  # Call base class method to set self.detected = True
        else:
            self._triggered = False
            self.release()  # Call base class method to set self.detected = False

        return self.detected

    def arm(self):
        """Arm the motion sensor for detection."""
        super().arm()  # Sets self.armed = True in the base class
        self._triggered = False

    def disarm(self):
        """Disarm the motion sensor."""
        super().disarm()  # Sets self.armed = False in the base class
        self._triggered = False

    # ============================================================
    # Custom methods specific to this detailed simulation
    # ============================================================

    def get_location(self) -> str:
        return self._location

    def get_type(self) -> str:
        return "motion_custom"

    def get_battery_level(self) -> int:
        """Get battery level (slowly drains when armed)."""
        if self.armed and self._battery_level > 0:
            self._battery_level -= 0.01

        return max(0, int(self._battery_level))

    def get_sensor_id(self) -> int:
        """Get sensor ID."""
        return self.sensor_id

    def reset_trigger(self):
        """Reset triggered state (for testing/simulation)."""
        self._triggered = False
        self.release()
        self._last_trigger_time = 0

    def force_trigger(self):
        """Force trigger for testing purposes."""
        if self.armed:
            self._triggered = True
            self._last_trigger_time = time.time()
            self.intrude()

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
            "id": f"M{self.sensor_id}",
            "type": self.get_type(),
            "location": self._location,
            "armed": self.armed,
            "triggered": self.detected,
            "battery": self.get_battery_level(),
            "sensitivity": self._sensitivity,
            "range": self._detection_range,
            "last_trigger": self._last_trigger_time,
        }

    def __repr__(self):
        status = "ARMED" if self.armed else "DISARMED"
        trigger = " [TRIGGERED]" if self.detected else ""
        return (
            f"CustomMotionDetector(id={self.sensor_id}, location='{self._location}', "
            f"status={status}{trigger}, battery={int(self._battery_level)}%)"
        )
