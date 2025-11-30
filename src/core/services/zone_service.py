"""Safety zone CRUD helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

from ...configuration import ConfigurationManager
from ..logging.system_logger import SystemLogger
from .zone.zone_repository import ZoneRepository


class ZoneService:
    def __init__(self, config_manager: ConfigurationManager, logger: SystemLogger):
        self._repo = ZoneRepository(config_manager)
        self._logger = logger
        self._zones: List[Dict] = []

    # ------------------------------------------------------------------ #
    def bootstrap_defaults(self, default_zones: List[Dict]):
        self._zones = self._repo.ensure_defaults(default_zones)

    def refresh(self):
        self._zones = self._repo.load_all()

    # ------------------------------------------------------------------ #
    def get_zones(self) -> List[Dict]:
        return self._zones

    def arm_zone(self, zone_id: int, sensor_service) -> Dict:
        zone = self._find_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        zone["armed"] = True
        for sid in zone["sensors"]:
            sensor_service.set_sensor_armed(sid, True)
        self._logger.add_event("ARM_ZONE", f"Zone '{zone['name']}' armed")
        return {"success": True}

    def disarm_zone(self, zone_id: int, sensor_service) -> Dict:
        zone = self._find_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        zone["armed"] = False
        for sid in zone["sensors"]:
            sensor_service.set_sensor_armed(sid, False)
        self._logger.add_event("DISARM_ZONE", f"Zone '{zone['name']}' disarmed")
        return {"success": True}

    def create_zone(self, name: str, sensors: List[str], user: Optional[str]) -> Dict:
        if not name:
            return {"success": False, "message": "Zone name required"}
        zone_id = self._repo.add_zone(name, sensors or [])
        if zone_id is None:
            return {"success": False, "message": "Failed to create zone"}
        self.refresh()
        self._logger.add_event(
            "CONFIGURATION",
            f"Safety zone created: {name}",
            user=user,
        )
        return {"success": True, "zone_id": zone_id}

    def update_zone(
        self,
        zone_id: int,
        name: Optional[str],
        sensors: Optional[List[str]],
        user: Optional[str],
    ) -> Dict:
        if not self._repo.update_zone(zone_id, name, sensors):
            return {"success": False, "message": "Zone not found"}
        self.refresh()
        zone = next((z for z in self._zones if z["id"] == zone_id), None)
        zone_name = zone["name"] if zone else str(zone_id)
        self._logger.add_event(
            "CONFIGURATION", f"Safety zone updated: {zone_name}", user=user
        )
        return {"success": True}

    def delete_zone(self, zone_id: int, user: Optional[str]) -> Dict:
        zone_name = self._repo.delete_zone(zone_id)
        if not zone_name:
            return {"success": False, "message": "Zone not found"}
        self.refresh()
        self._logger.add_event(
            "CONFIGURATION",
            f"Safety zone deleted: {zone_name}",
            user=user,
        )
        return {"success": True}

    def _find_zone(self, zone_id: int) -> Optional[Dict]:
        for zone in self._zones:
            if zone["id"] == zone_id:
                return zone
        return None


