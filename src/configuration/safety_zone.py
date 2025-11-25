"""SafetyZone entity for grouping sensors logically.

Zones allow users to arm/disarm logical groups of sensors such as
"First Floor" or "Bedrooms".
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .exceptions import ValidationError


@dataclass
class SafetyZone:
    """Represents a safety zone for a group of sensors."""

    zone_id: int
    zone_name: str
    sensor_ids: List[int] = field(default_factory=list)
    is_armed: bool = False
    description: str = ""

    # ------------------------------------------------------------------
    # Sensor list manipulation
    # ------------------------------------------------------------------
    def add_sensor(self, sensor_id: int) -> bool:
        """Add a sensor to the zone if not already present."""
        if sensor_id not in self.sensor_ids:
            self.sensor_ids.append(sensor_id)
            return True
        return False

    def remove_sensor(self, sensor_id: int) -> bool:
        """Remove a sensor from the zone."""
        if sensor_id in self.sensor_ids:
            self.sensor_ids.remove(sensor_id)
            return True
        return False

    def clear_sensors(self) -> None:
        """Remove all sensors from the zone."""
        self.sensor_ids.clear()

    def has_sensor(self, sensor_id: int) -> bool:
        """Return True if the given sensor belongs to this zone."""
        return sensor_id in self.sensor_ids

    def get_sensor_count(self) -> int:
        """Return the number of sensors in this zone."""
        return len(self.sensor_ids)

    # ------------------------------------------------------------------
    # Arming / disarming
    # ------------------------------------------------------------------
    def arm(self) -> None:
        """Arm this zone."""
        self.is_armed = True

    def disarm(self) -> None:
        """Disarm this zone."""
        self.is_armed = False

    # ------------------------------------------------------------------
    # Validation and serialization
    # ------------------------------------------------------------------
    def validate(self) -> bool:
        """Validate zone configuration."""
        if not self.zone_name:
            raise ValidationError("Zone name must not be empty.")
        if self.zone_id < 0:
            raise ValidationError("Zone ID must be non‑negative.")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation suitable for persistence."""
        data = asdict(self)
        # Treat zone_id=0 as None for DB insertion
        if data.get("zone_id") == 0:
            data["zone_id"] = None
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SafetyZone":
        """Create :class:`SafetyZone` from dictionary (DB row)."""
        sensor_raw = data.get("sensor_ids", [])
        if isinstance(sensor_raw, str):
            import json

            try:
                sensor_ids = [int(x) for x in json.loads(sensor_raw)]
            except Exception:
                sensor_ids = []
        else:
            sensor_ids = [int(x) for x in sensor_raw]

        return SafetyZone(
            zone_id=int(data.get("zone_id", 0)),
            zone_name=str(data.get("zone_name", "")),
            sensor_ids=sensor_ids,
            is_armed=bool(data.get("is_armed", False)),
            description=str(data.get("description", "")),
        )



