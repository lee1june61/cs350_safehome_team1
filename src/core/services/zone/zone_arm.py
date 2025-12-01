"""Zone arming/disarming helpers."""

from __future__ import annotations

from typing import Dict, Optional


class ZoneArmService:
    """Handles zone arm/disarm operations."""

    def __init__(self, repo, logger, zone_list_fn):
        self._repo = repo
        self._logger = logger
        self._zones = zone_list_fn

    def arm(self, zone_id: int, sensor_service) -> Dict:
        zone = self._find_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}
        if not zone.get("sensors"):
            return {"success": False, "message": self._missing_selection_message()}
        blocked = self._find_open_entry_sensor(zone, sensor_service)
        if blocked:
            return {"success": False, "message": "Doors and windows not closed"}
        if not self._repo.set_zone_state(zone_id, True):
            return {"success": False, "message": "Zone not found"}
        zone["armed"] = True
        for sid in zone["sensors"]:
            sensor_service.set_sensor_armed(sid, True)
        self._logger.add_event("ARM_ZONE", f"Zone '{zone['name']}' armed")
        return {"success": True}

    def disarm(self, zone_id: int, sensor_service) -> Dict:
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
        return {"success": True}

    def _find_zone(self, zone_id: int) -> Optional[Dict]:
        for zone in self._zones():
            if zone["id"] == zone_id:
                return zone
        return None

    def _sensor_required_elsewhere(self, current_zone_id: int, sensor_id: str) -> bool:
        for zone in self._zones():
            if zone["id"] == current_zone_id:
                continue
            if zone.get("armed") and sensor_id in zone.get("sensors", []):
                return True
        return False

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

    def _missing_selection_message(self) -> str:
        return "Select new safety zone and type safety zone name"

