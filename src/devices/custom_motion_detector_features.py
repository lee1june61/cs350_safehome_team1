"""Feature mixins for custom motion detector."""

from __future__ import annotations


class MotionDetectorSettingsMixin:
    """Settings management for motion detector."""

    _sensitivity: float
    _detection_range: float

    def set_sensitivity(self, sensitivity: float):
        """Set detection sensitivity (0.0 to 1.0)."""
        self._sensitivity = max(0.0, min(1.0, sensitivity))

    def get_sensitivity(self) -> float:
        return self._sensitivity

    def set_detection_range(self, range_meters: float):
        """Set detection range in meters."""
        self._detection_range = max(1.0, range_meters)

    def get_detection_range(self) -> float:
        return self._detection_range


class MotionDetectorStatusMixin:
    """Status helpers for motion detector."""

    sensor_id: int
    _location: str
    _triggered: bool
    _battery_level: float
    _sensitivity: float
    _detection_range: float
    _last_trigger_time: float
    armed: bool
    detected: bool

    def get_location(self) -> str:
        return self._location

    def get_type(self) -> str:
        return "motion_custom"

    def get_battery_level(self) -> int:
        if self.armed and self._battery_level > 0:
            self._battery_level -= 0.01
        return max(0, int(self._battery_level))

    def get_sensor_id(self) -> int:
        return self.sensor_id

    def get_status(self) -> dict:
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

