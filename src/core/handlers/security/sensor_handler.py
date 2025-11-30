"""Sensor command helper."""

from __future__ import annotations

from typing import Any, Dict

from ...services.sensor_service import SensorService
from ...services.mode_service import ModeService
from ...services.camera_service import CameraService


class SensorCommandHandler:
    """Handles sensor queries and arm/disarm logic."""

    def __init__(
        self,
        sensor_service: SensorService,
        mode_service: ModeService,
        camera_service: CameraService,
    ):
        self._sensors = sensor_service
        self._modes = mode_service
        self._cameras = camera_service

    def get_sensors(self, **_) -> Dict[str, Any]:
        return {"success": True, "data": self._sensors.collect_statuses()}

    def get_devices(self, **_) -> Dict[str, Any]:
        devices = self._sensors.get_devices_payload(
            self._cameras.camera_info(), self._cameras.labels
        )
        return {"success": True, "data": devices}

    def arm_sensor(self, sensor_id="", **_) -> Dict[str, Any]:
        if not self._sensors.set_sensor_armed(sensor_id, True):
            return {"success": False, "message": "Sensor not found"}
        return {"success": True}

    def disarm_sensor(self, sensor_id="", **_) -> Dict[str, Any]:
        if not self._sensors.set_sensor_armed(sensor_id, False):
            return {"success": False, "message": "Sensor not found"}
        return {"success": True}

    def poll_sensors(self):
        armed_mode = self._modes.current_mode != self._modes.MODE_DISARMED
        return self._sensors.poll_armed_sensors(armed_mode)


