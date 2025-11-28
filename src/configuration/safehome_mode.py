"""SafeHomeMode entity for SafeHome configuration.

Each :class:`SafeHomeMode` describes which sensors are active when the
system is in a particular mode (Home, Away, Overnight, Extended, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List

from .exceptions import ValidationError


ALLOWED_MODE_NAMES = {"Home", "Away", "Overnight", "Extended"}


@dataclass
class SafeHomeMode:
    """Represents sensor configuration for a specific SafeHome mode."""

    mode_id: int
    mode_name: str
    sensor_ids: List[int] = field(default_factory=list)
    is_active: bool = True
    description: str = ""

    # ------------------------------------------------------------------
    # Sensor list manipulation
    # ------------------------------------------------------------------
    def add_sensor(self, sensor_id: int) -> bool:
        """Add a sensor to the mode if not already present."""
        if sensor_id not in self.sensor_ids:
            self.sensor_ids.append(sensor_id)
            return True
        return False

    def remove_sensor(self, sensor_id: int) -> bool:
        """Remove a sensor from the mode."""
        if sensor_id in self.sensor_ids:
            self.sensor_ids.remove(sensor_id)
            return True
        return False

    def clear_sensors(self) -> None:
        """Remove all sensors from the mode."""
        self.sensor_ids.clear()

    def has_sensor(self, sensor_id: int) -> bool:
        """Return True if the given sensor is part of this mode."""
        return sensor_id in self.sensor_ids

    def get_sensor_count(self) -> int:
        """Return the number of sensors associated with this mode."""
        return len(self.sensor_ids)

    # ------------------------------------------------------------------
    # Validation and serialization
    # ------------------------------------------------------------------
    def validate(self) -> bool:
        """Validate mode configuration."""
        if self.mode_name not in ALLOWED_MODE_NAMES:
            raise ValidationError(f"Unsupported mode name: {self.mode_name}")
        if self.mode_id < 0:
            raise ValidationError("Mode ID must be non‑negative.")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation suitable for persistence."""
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SafeHomeMode":
        """Create :class:`SafeHomeMode` from dictionary (DB row)."""
        sensor_raw = data.get("sensor_ids", [])
        if isinstance(sensor_raw, str):
            # StorageManager stores JSON arrays as TEXT.
            import json  # local import to avoid global dependency

            try:
                sensor_ids = [int(x) for x in json.loads(sensor_raw)]
            except Exception:
                sensor_ids = []
        else:
            sensor_ids = [int(x) for x in sensor_raw]

        return SafeHomeMode(
            mode_id=int(data.get("mode_id", 0)),
            mode_name=str(data.get("mode_name", "")),
            sensor_ids=sensor_ids,
            is_active=bool(data.get("is_active", True)),
            description=str(data.get("description", "")),
        )



