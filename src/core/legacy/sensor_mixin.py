"""Legacy sensor-related methods for backward compatibility."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class LegacySensorMixin:
    """Provides legacy sensor APIs required by older unit tests."""

    @property
    def _sensors(self):
        return getattr(self.sensor_service, "_sensors", [])

    @_sensors.setter
    def _sensors(self, value):
        setattr(self.sensor_service, "_sensors", value)

    def arm_sensors(self, sensor_ids):
        if not sensor_ids:
            return False
        if hasattr(self.sensor_controller, "arm_sensors"):
            return bool(self.sensor_controller.arm_sensors(sensor_ids))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), True) for sid in sensor_ids
        )

    def disarm_sensors(self, sensor_ids):
        if not sensor_ids:
            return False
        if hasattr(self.sensor_controller, "disarm_sensors"):
            return bool(self.sensor_controller.disarm_sensors(sensor_ids))
        return all(
            self.sensor_service.set_sensor_armed(str(sid), False) for sid in sensor_ids
        )

    def read_sensor(self):
        if hasattr(self.sensor_controller, "read"):
            return self.sensor_controller.read()
        return self.sensor_service.collect_statuses()

    def get_alarm_info(self) -> Dict[str, any]:
        is_ringing = bool(getattr(self.alarm, "is_ringing", lambda: False)())
        alarm_id = self.alarm.get_id() if hasattr(self.alarm, "get_id") else None
        location = (
            self.alarm.get_location() if hasattr(self.alarm, "get_location") else None
        )
        timestamp = datetime.now().isoformat() if is_ringing else None
        return {
            "is_ringing": is_ringing,
            "alarm_id": alarm_id,
            "location": location,
            "timestamp": timestamp,
        }

