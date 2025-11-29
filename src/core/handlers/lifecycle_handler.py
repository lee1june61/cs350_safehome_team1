"""Lifecycle-related command implementations."""

from __future__ import annotations

from typing import Dict, Any


class LifecycleHandler:
    """Handles system lifecycle commands and status aggregation."""

    def __init__(
        self,
        system,
        alarm_service,
        sensor_service,
        camera_service,
        auth_service,
        mode_service,
    ):
        self._system = system
        self._alarm_service = alarm_service
        self._sensor_service = sensor_service
        self._camera_service = camera_service
        self._auth_service = auth_service
        self._mode_service = mode_service

    def turn_on(self, **_) -> Dict[str, Any]:
        success = bool(self._system.turn_on())
        return {"success": success, "state": self._alarm_service.state}

    def turn_off(self, **_) -> Dict[str, Any]:
        return {"success": bool(self._system.turn_off())}

    def reset(self, **_) -> Dict[str, Any]:
        self._mode_service.disarm_system(self._system.zone_service, log_event=False)
        return {"success": True}

    def get_status(self, **_) -> Dict[str, Any]:
        sensor_states = self._sensor_service.collect_statuses()
        active_sensors = sum(1 for s in sensor_states if s.get("armed"))
        camera_states = self._camera_service.camera_info()
        enabled_cameras = sum(1 for c in camera_states if c.get("enabled"))
        data = {
            "state": self._alarm_service.state,
            "mode": self._mode_service.current_mode,
            "armed": self._mode_service.current_mode
            != self._system.MODE_DISARMED,
            "user": self._auth_service.current_user,
            "verified": self._auth_service.is_verified,
            "alarm_active": self._alarm_service.state == "ALARM",
            "sensor_count": len(sensor_states),
            "active_sensors": active_sensors,
            "camera_count": len(camera_states),
            "enabled_cameras": enabled_cameras,
        }
        return {"success": True, "data": data}


