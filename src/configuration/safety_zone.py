"""SafetyZone groups sensors into logical zones."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from .exceptions import ValidationError


@dataclass
class SafetyZone:
    """Groups sensors into a logical zone (e.g., 'First Floor')."""

    zone_id: int
    zone_name: str
    sensor_ids: List[int] = None
    is_armed: bool = False
    description: str = ""

    def __post_init__(self) -> None:
        if self.sensor_ids is None:
            self.sensor_ids = []

    def add_sensor(self, sensor_id: int) -> bool:
        """Add sensor to this zone."""
        if sensor_id not in self.sensor_ids:
            self.sensor_ids.append(sensor_id)
            return True
        return False

    def remove_sensor(self, sensor_id: int) -> bool:
        """Remove sensor from this zone."""
        if sensor_id in self.sensor_ids:
            self.sensor_ids.remove(sensor_id)
            return True
        return False

    def clear_sensors(self) -> None:
        """Remove all sensors from this zone."""
        self.sensor_ids.clear()

    def has_sensor(self, sensor_id: int) -> bool:
        """Check if sensor is in this zone."""
        return sensor_id in self.sensor_ids

    def get_sensor_count(self) -> int:
        """Return number of sensors in this zone."""
        return len(self.sensor_ids)

    def arm(self) -> None:
        """Arm this zone."""
        self.is_armed = True

    def disarm(self) -> None:
        """Disarm this zone."""
        self.is_armed = False

    def validate(self) -> bool:
        """Validate zone configuration."""
        if not self.zone_name:
            raise ValidationError("Zone name must not be empty")
        if self.zone_id < 0:
            raise ValidationError("Zone ID must be non-negative")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        data = asdict(self)
        if data.get("zone_id") == 0:
            data["zone_id"] = None
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SafetyZone":
        """Create SafetyZone from dictionary."""
        sensor_raw = data.get("sensor_ids", [])
        if isinstance(sensor_raw, str):
            sensor_ids = json.loads(sensor_raw) if sensor_raw else []
        else:
            sensor_ids = list(sensor_raw)

        return SafetyZone(
            zone_id=int(data.get("zone_id", 0)),
            zone_name=data["zone_name"],
            sensor_ids=sensor_ids,
            is_armed=bool(data.get("is_armed", False)),
            description=data.get("description", ""),
        )
