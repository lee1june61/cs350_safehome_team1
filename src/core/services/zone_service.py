"""Safety zone CRUD helpers."""

from __future__ import annotations

from typing import Dict, List, Optional

from ...configuration import ConfigurationManager
from ..logging.system_logger import SystemLogger
from .zone import ZoneRepository, ZoneArmService, ZoneCrudService


class ZoneService:
    """Orchestrates zone operations."""

    def __init__(self, config_manager: ConfigurationManager, logger: SystemLogger):
        self._repo = ZoneRepository(config_manager)
        self._logger = logger
        self._zones: List[Dict] = []
        self._arm = ZoneArmService(self._repo, logger, self.get_zones)
        self._crud = ZoneCrudService(self._repo, logger, self.get_zones, self.refresh)

    def bootstrap_defaults(self, default_zones: List[Dict]):
        self._zones = self._repo.ensure_defaults(default_zones)

    def refresh(self):
        self._zones = self._repo.load_all()

    def get_zones(self) -> List[Dict]:
        return self._zones

    def arm_zone(self, zone_id: int, sensor_service) -> Dict:
        self.refresh()
        result = self._arm.arm(zone_id, sensor_service)
        self.refresh()
        return result

    def disarm_zone(self, zone_id: int, sensor_service) -> Dict:
        self.refresh()
        result = self._arm.disarm(zone_id, sensor_service)
        self.refresh()
        return result

    def create_zone(self, name: str, sensors: List[str], user: Optional[str]) -> Dict:
        return self._crud.create(name, sensors, user)

    def update_zone(
        self, zone_id: int, name: Optional[str], sensors: Optional[List[str]], user: Optional[str]
    ) -> Dict:
        return self._crud.update(zone_id, name, sensors, user)

    def delete_zone(self, zone_id: int, user: Optional[str]) -> Dict:
        return self._crud.delete(zone_id, user)
