"""Repository helpers for safety zones."""

from __future__ import annotations

from typing import Dict, List, Optional

from src.configuration import ConfigurationManager, SafetyZone


class ZoneRepository:
    """Encapsulates persistence logic for safety zones."""

    def __init__(self, config_manager: ConfigurationManager):
        self._config_manager = config_manager

    def load_all(self) -> List[Dict]:
        zones = self._config_manager.get_all_safety_zones()
        return self._serialize(zones)

    def ensure_defaults(self, defaults: List[Dict]) -> List[Dict]:
        zones = self._config_manager.get_all_safety_zones()
        if not zones:
            for entry in defaults:
                zone = SafetyZone(
                    zone_id=0,
                    zone_name=entry["name"],
                    sensor_ids=entry["sensors"],
                    is_armed=entry.get("armed", False),
                )
                self._config_manager.add_safety_zone(zone)
            zones = self._config_manager.get_all_safety_zones()
        return self._serialize(zones)

    def add_zone(self, name: str, sensors: List[str]) -> Optional[int]:
        zone = SafetyZone(
            zone_id=0,
            zone_name=name,
            sensor_ids=sensors or [],
            is_armed=False,
        )
        success = self._config_manager.add_safety_zone(zone)
        if not success:
            return None
        zones = self._config_manager.get_all_safety_zones()
        for z in zones:
            if z.zone_name == name:
                return z.zone_id
        return None

    def update_zone(
        self, zone_id: int, name: Optional[str], sensors: Optional[List[str]]
    ) -> bool:
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return False
        if name is not None:
            zone.zone_name = name
        if sensors is not None:
            zone.sensor_ids = sensors
        return self._config_manager.update_safety_zone(zone)

    def delete_zone(self, zone_id: int) -> Optional[str]:
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return None
        if self._config_manager.delete_safety_zone(zone_id):
            return zone.zone_name
        return None

    def set_zone_state(self, zone_id: int, armed: bool) -> bool:
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return False
        zone.is_armed = armed
        return self._config_manager.update_safety_zone(zone)

    def get_zone(self, zone_id: int) -> Optional[Dict]:
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return None
        return {
            "id": zone.zone_id,
            "name": zone.zone_name,
            "sensors": zone.sensor_ids[:],
            "armed": zone.is_armed,
        }

    def _serialize(self, zones) -> List[Dict]:
        return [
            {
                "id": zone.zone_id,
                "name": zone.zone_name,
                "sensors": zone.sensor_ids[:],
                "armed": zone.is_armed,
            }
            for zone in zones
        ]


