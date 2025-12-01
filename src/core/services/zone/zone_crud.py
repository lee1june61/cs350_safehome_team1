"""Zone CRUD helpers."""

from __future__ import annotations

from typing import Dict, List, Optional


class ZoneCrudService:
    """Handles zone create/update/delete operations."""

    def __init__(self, repo, logger, zone_list_fn, refresh_fn):
        self._repo = repo
        self._logger = logger
        self._zones = zone_list_fn
        self._refresh = refresh_fn

    def create(self, name: str, sensors: List[str], user: Optional[str]) -> Dict:
        normalized_name = (name or "").strip()
        sensor_ids = self._sanitize_sensors(sensors)
        if not normalized_name or not sensor_ids:
            return {"success": False, "message": self._missing_selection_message()}
        self._refresh()
        if self._zone_name_exists(normalized_name):
            return {"success": False, "message": "Same safety zone exists"}
        zone_id = self._repo.add_zone(normalized_name, sensor_ids)
        if zone_id is None:
            return {"success": False, "message": "Failed to create zone"}
        self._refresh()
        self._logger.add_event("CONFIGURATION", f"Safety zone created: {normalized_name}", user=user)
        return {"success": True, "zone_id": zone_id, "message": "Safety zone created"}

    def update(self, zone_id: int, name: Optional[str], sensors: Optional[List[str]], user: Optional[str]) -> Dict:
        updated_name = (name or "").strip() if name is not None else None
        sensor_ids = self._sanitize_sensors(sensors) if sensors is not None else None
        if updated_name is not None and not updated_name:
            return {"success": False, "message": self._missing_selection_message()}
        if sensor_ids is not None and not sensor_ids:
            return {"success": False, "message": "Select at least one sensor"}
        self._refresh()
        if updated_name and self._zone_name_exists(updated_name, exclude_id=zone_id):
            return {"success": False, "message": "Same safety zone exists"}
        if not self._repo.update_zone(zone_id, updated_name, sensor_ids):
            return {"success": False, "message": "Zone not found"}
        self._refresh()
        zone = next((z for z in self._zones() if z["id"] == zone_id), None)
        zone_name = zone["name"] if zone else str(zone_id)
        self._logger.add_event("CONFIGURATION", f"Safety zone updated: {zone_name}", user=user)
        return {"success": True, "message": "Safety zone updated"}

    def delete(self, zone_id: int, user: Optional[str]) -> Dict:
        zone_name = self._repo.delete_zone(zone_id)
        if not zone_name:
            return {"success": False, "message": "Zone not found"}
        self._refresh()
        self._logger.add_event("CONFIGURATION", f"Safety zone deleted: {zone_name}", user=user)
        return {"success": True, "message": "Safety zone deleted"}

    def _zone_name_exists(self, name: str, *, exclude_id: Optional[int] = None) -> bool:
        target = name.casefold()
        for zone in self._zones():
            if exclude_id is not None and zone["id"] == exclude_id:
                continue
            if zone["name"].casefold() == target:
                return True
        return False

    def _sanitize_sensors(self, sensors: Optional[List[str]]) -> List[str]:
        if not sensors:
            return []
        return sorted({str(sid).strip() for sid in sensors if str(sid).strip()})

    def _missing_selection_message(self) -> str:
        return "Select new safety zone and type safety zone name"

