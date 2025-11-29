"""Alarm command helper."""

from __future__ import annotations

from typing import Any, Dict

from ...services.sensor_service import SensorService
from ...services.zone_service import ZoneService
from ...services.alarm_service import AlarmService
from ...services.auth_service import AuthService
from ...logging.system_logger import SystemLogger


class AlarmCommandHandler:
    """Handles alarm trigger/clear/status operations."""

    def __init__(
        self,
        sensor_service: SensorService,
        zone_service: ZoneService,
        alarm_service: AlarmService,
        auth_service: AuthService,
        logger: SystemLogger,
    ):
        self._sensors = sensor_service
        self._zones = zone_service
        self._alarm = alarm_service
        self._auth = auth_service
        self._logger = logger

    def trigger(self, sensor_id="") -> Dict[str, Any]:
        sensor_info = "Unknown"
        sensor = self._sensors.get_sensor(sensor_id)
        if sensor:
            status = sensor.get_status()
            sensor_info = (
                f"{status.get('id', sensor_id)} "
                f"({status.get('type', 'N/A')} @ {status.get('location', 'N/A')})"
            )

        zone_info = "Unknown"
        for zone in self._zones.get_zones():
            if sensor_id in zone.get("sensors", []):
                zone_info = zone["name"]
                break

        return self._alarm.trigger(sensor_info, zone_info, self._auth.current_user)

    def clear(self, **_) -> Dict[str, Any]:
        return self._alarm.clear()

    def status(self, **_) -> Dict[str, Any]:
        latest = self._logger.latest(limit=1)
        return self._alarm.get_alarm_status(latest)


