"""Sensor arming/disarming utilities."""

from __future__ import annotations

from typing import Optional

from .sensor_registry import SensorRegistry


class SensorArmService:
    """Controls armed state and polling for sensors."""

    def __init__(self, registry: SensorRegistry):
        self._registry = registry

    def set_sensor_armed(self, sensor_id: str, armed: bool) -> bool:
        sensor = self._registry.get_sensor(sensor_id)
        if not sensor:
            return False
        if armed:
            sensor.arm()
        else:
            sensor.disarm()
        return True

    def disarm_all(self):
        for sensor in self._registry.instances:
            sensor.disarm()

    def door_or_window_open(self) -> Optional[str]:
        for sensor_id, metadata in self._registry.metadata.items():
            if metadata.get("type") not in {"WINDOW", "DOOR"}:
                continue
            sensor = self._registry.get_sensor(sensor_id)
            if sensor and hasattr(sensor, "can_arm") and not sensor.can_arm():
                return metadata.get("location") or sensor_id
        return None

    def poll_armed_sensors(self, armed_mode: bool):
        if not armed_mode:
            return {"success": True, "intrusion_detected": False}

        for sensor_id in self._registry.lookup.keys():
            sensor = self._registry.get_sensor(sensor_id)
            if not sensor:
                continue
            status = sensor.get_status()
            if not status.get("armed"):
                continue
            triggered = bool(status.get("is_open")) or bool(status.get("triggered"))
            if triggered:
                return {
                    "success": True,
                    "intrusion_detected": True,
                    "sensor_id": sensor_id,
                }
        return {"success": True, "intrusion_detected": False}


