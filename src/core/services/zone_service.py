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
        self.refresh()
        zone = self._find_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        if not zone.get("sensors"):
            return {"success": False, "message": self._missing_selection_message()}

        blocked_sensor = self._find_open_entry_sensor(zone, sensor_service)
        if blocked_sensor:
            return {"success": False, "message": "Doors and windows not closed"}

        if not self._repo.set_zone_state(zone_id, True):
            return {"success": False, "message": "Zone not found"}

        zone["armed"] = True
        for sid in zone["sensors"]:
            sensor_service.set_sensor_armed(sid, True)
        self._logger.add_event("ARM_ZONE", f"Zone '{zone['name']}' armed")
        self.refresh()
        return {"success": True}

    def disarm_zone(self, zone_id: int, sensor_service) -> Dict:
        self.refresh()
        zone = self._find_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        if not self._repo.set_zone_state(zone_id, False):
            return {"success": False, "message": "Zone not found"}

        zone["armed"] = False
        for sid in zone["sensors"]:
            if not self._sensor_required_elsewhere(zone_id, sid):
                sensor_service.set_sensor_armed(sid, False)
        self._logger.add_event("DISARM_ZONE", f"Zone '{zone['name']}' disarmed")
        self.refresh()
        return {"success": True}

    def create_zone(self, name: str, sensors: List[str], user: Optional[str]) -> Dict:
        normalized_name = (name or "").strip()
        sensor_ids = self._sanitize_sensors(sensors)
        if not normalized_name or not sensor_ids:
            return {"success": False, "message": self._missing_selection_message()}

        self.refresh()
        if self._zone_name_exists(normalized_name):
            return {"success": False, "message": "Same safety zone exists"}

        zone_id = self._repo.add_zone(normalized_name, sensor_ids)
        if zone_id is None:
            return {"success": False, "message": "Failed to create zone"}
        self.refresh()
        self._logger.add_event(
            "CONFIGURATION",
            f"Safety zone created: {normalized_name}",
            user=user,
        )
        return {"success": True, "zone_id": zone_id, "message": "Safety zone created"}

    def update_zone(
        self,
        zone_id: int,
        name: Optional[str],
        sensors: Optional[List[str]],
        user: Optional[str],
    ) -> Dict:
        updated_name = (name or "").strip() if name is not None else None
        sensor_ids = self._sanitize_sensors(sensors) if sensors is not None else None

        if updated_name is not None and not updated_name:
            return {"success": False, "message": self._missing_selection_message()}
        if sensor_ids is not None and not sensor_ids:
            return {"success": False, "message": "Select at least one sensor"}

        self.refresh()
        if updated_name and self._zone_name_exists(updated_name, exclude_id=zone_id):
            return {"success": False, "message": "Same safety zone exists"}

        if not self._repo.update_zone(zone_id, updated_name, sensor_ids):
            return {"success": False, "message": "Zone not found"}

        self.refresh()
        zone = next((z for z in self._zones if z["id"] == zone_id), None)
        zone_name = zone["name"] if zone else str(zone_id)
        self._logger.add_event(
            "CONFIGURATION", f"Safety zone updated: {zone_name}", user=user
        )
        return {"success": True, "message": "Safety zone updated"}

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
        return {"success": True, "message": "Safety zone deleted"}

    def _find_zone(self, zone_id: int) -> Optional[Dict]:
        for zone in self._zones:
            if zone["id"] == zone_id:
                return zone
        return None

    def _zone_name_exists(self, name: str, *, exclude_id: Optional[int] = None) -> bool:
        target = name.casefold()
        for zone in self._zones:
            if exclude_id is not None and zone["id"] == exclude_id:
                continue
            if zone["name"].casefold() == target:
                return True
        return False

    def _sensor_required_elsewhere(self, current_zone_id: int, sensor_id: str) -> bool:
        for zone in self._zones:
            if zone["id"] == current_zone_id:
                continue
            if zone.get("armed") and sensor_id in zone.get("sensors", []):
                return True
        return False

    def _sanitize_sensors(self, sensors: Optional[List[str]]) -> List[str]:
        if not sensors:
            return []
        return sorted({str(sensor_id).strip() for sensor_id in sensors if str(sensor_id).strip()})

    def _missing_selection_message(self) -> str:
        return "Select new safety zone and type safety zone name"

    def _find_open_entry_sensor(self, zone: Dict, sensor_service) -> Optional[str]:
        metadata = getattr(sensor_service, "metadata", {}) or {}
        for sensor_id in zone.get("sensors", []):
            info = metadata.get(sensor_id, {})
            sensor_type = (info.get("type") or "").upper()
            sensor_obj = sensor_service.get_sensor(sensor_id)
            if not sensor_type and sensor_obj and hasattr(sensor_obj, "get_type"):
                sensor_type = sensor_obj.get_type().upper()
            if sensor_type not in {"DOOR", "WINDOW"}:
                continue
            if sensor_obj and hasattr(sensor_obj, "can_arm") and not sensor_obj.can_arm():
                return sensor_id
        return None


