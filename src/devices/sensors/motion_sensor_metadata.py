"""Metadata mixin for motion sensors."""

from __future__ import annotations

from typing import Any, Dict, Optional


class MotionSensorMetadataMixin:
    """Provides metadata and status helpers for motion sensors."""

    _friendly_id: str
    _location_label: str
    _category: str
    _extra: Dict[str, Any]
    _armed: bool
    _detected: bool

    def set_metadata(
        self,
        friendly_id: str,
        location_name: str,
        category: str = "motion",
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Attach friendly metadata for UI display."""
        self._friendly_id = friendly_id or self._friendly_id
        self._location_label = location_name or self._location_label
        self._category = (category or "motion").lower()
        self._extra = extra or {}

    def get_sensor_id(self) -> int:
        """Return numeric ID (legacy helper)."""
        return self.getID()

    def get_location(self) -> str:
        """Return human readable location."""
        return self._location_label

    def get_type(self) -> str:
        """Return presentation type string."""
        return "motion"

    def can_arm(self) -> bool:
        """Motion sensors can always be armed."""
        return True

    def reset_trigger(self):
        """Clear detection state."""
        self._detected = False
        self._detectedSignal = 0

    def force_trigger(self):
        """Force a detection event (testing helper)."""
        if self._armed:
            self._detected = True
            self._detectedSignal = 1

    def get_status(self) -> Dict[str, Any]:
        """Return structured status information."""
        triggered = bool(self.isDetected())
        return {
            "id": self._friendly_id,
            "name": self._location_label,
            "type": self.get_type(),
            "location": self._location_label,
            "armed": self.isArmed(),
            "triggered": triggered,
            "status": "motion" if triggered else "idle",
            "extra": self._extra.copy(),
        }

