"""Zone command helper."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ...services.zone_service import ZoneService
from ...services.sensor_service import SensorService
from ...services.auth_service import AuthService


class ZoneCommandHandler:
    """Handles CRUD and arm/disarm for zones."""

    def __init__(
        self,
        zone_service: ZoneService,
        sensor_service: SensorService,
        auth_service: AuthService,
    ):
        self._zones = zone_service
        self._sensors = sensor_service
        self._auth = auth_service

    def get_zones(self, **_) -> Dict[str, Any]:
        return {"success": True, "data": self._zones.get_zones()}

    def arm_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zones.arm_zone(zone_id, self._sensors)

    def disarm_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zones.disarm_zone(zone_id, self._sensors)

    def create_zone(self, name="", sensors=None, **_) -> Dict[str, Any]:
        return self._zones.create_zone(name, sensors or [], self._auth.current_user)

    def update_zone(self, zone_id=None, name=None, sensors=None, **_) -> Dict[str, Any]:
        return self._zones.update_zone(zone_id, name, sensors, self._auth.current_user)

    def delete_zone(self, zone_id=None, **_) -> Dict[str, Any]:
        return self._zones.delete_zone(zone_id, self._auth.current_user)


