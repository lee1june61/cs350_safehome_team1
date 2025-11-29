"""SafeHomeMode manages sensor configurations for different home modes."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from .exceptions import ValidationError


@dataclass
class SafeHomeMode:
    """Sensor configuration for a specific home mode."""

    mode_id: int
    mode_name: str
    sensor_ids: List[int] = None
    is_active: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        if self.sensor_ids is None:
            self.sensor_ids = []

    def add_sensor(self, sensor_id: int) -> bool:
        """Add sensor to this mode."""
        if sensor_id not in self.sensor_ids:
            self.sensor_ids.append(sensor_id)
            return True
        return False

    def remove_sensor(self, sensor_id: int) -> bool:
        """Remove sensor from this mode."""
        if sensor_id in self.sensor_ids:
            self.sensor_ids.remove(sensor_id)
            return True
        return False

    def clear_sensors(self) -> None:
        """Remove all sensors from this mode."""
        self.sensor_ids.clear()

    def has_sensor(self, sensor_id: int) -> bool:
        """Check if sensor is in this mode."""
        return sensor_id in self.sensor_ids

    def get_sensor_count(self) -> int:
        """Return number of sensors in this mode."""
        return len(self.sensor_ids)

    def validate(self) -> bool:
        """Validate mode configuration."""
        if not self.mode_name:
            raise ValidationError("Mode name must not be empty")
        if self.mode_id < 0:
            raise ValidationError("Mode ID must be non-negative")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SafeHomeMode":
        """Create SafeHomeMode from dictionary."""
        sensor_raw = data.get("sensor_ids", [])
        if isinstance(sensor_raw, str):
            sensor_ids = json.loads(sensor_raw) if sensor_raw else []
        else:
            sensor_ids = list(sensor_raw)

        return SafeHomeMode(
            mode_id=int(data["mode_id"]),
            mode_name=data["mode_name"],
            sensor_ids=sensor_ids,
            is_active=bool(data.get("is_active", True)),
            description=data.get("description", ""),
        )
