"""Metadata mixin for window/door sensors."""

from __future__ import annotations

from typing import Any, Dict, Optional


class WindowDoorSensorMetadataMixin:
    """Provides metadata and status helpers for window/door sensors."""

    _friendly_id: str
    _location_label: str
    _category: str
    _extra: Dict[str, Any]

    def set_metadata(
        self,
        friendly_id: str,
        location_name: str,
        category: str = "sensor",
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Attach presentation metadata (id, friendly name, type)."""
        self._friendly_id = friendly_id or self._friendly_id
        self._location_label = location_name or self._location_label
        normalized = (category or "sensor").lower()
        if normalized == "door":
            self._category = "door_sensor"
        elif normalized == "window":
            self._category = "sensor"
        else:
            self._category = normalized
        self._extra = extra or {}

    def get_sensor_id(self) -> int:
        """Legacy helper used by System."""
        return self.getID()

    def get_location(self) -> str:
        """Return human readable location string."""
        return self._location_label

    def get_type(self) -> str:
        """Return presentation type string used by UI/floor plan."""
        return self._category

    def get_status(self) -> Dict[str, Any]:
        """Return structured status for UI/system queries."""
        is_open = self.isOpen()
        return {
            "id": self._friendly_id,
            "name": self._location_label,
            "type": self.get_type(),
            "location": self._location_label,
            "armed": self.isArmed(),
            "is_open": is_open,
            "status": "open" if is_open else "closed",
            "can_arm": self.can_arm(),
            "extra": self._extra.copy(),
        }

