"""SafeHome mode orchestration."""

from __future__ import annotations

from typing import Dict, List, Optional

from ...configuration import ConfigurationManager
from ..logging.system_logger import SystemLogger
from .sensor_service import SensorService
from .zone_service import ZoneService


class ModeService:
    MODE_DISARMED = "DISARMED"

    def __init__(
        self,
        config_manager: ConfigurationManager,
        sensor_service: SensorService,
        logger: SystemLogger,
    ):
        self._config_manager = config_manager
        self._sensor_service = sensor_service
        self._logger = logger
        self._mode_configs: Dict[str, List[str]] = {}
        self._current_mode = self.MODE_DISARMED

    # ------------------------------------------------------------------ #
    def bootstrap_defaults(self, defaults: Dict[str, List[str]]):
        self._sync_modes()
        if not self._mode_configs:
            self._mode_configs = {k: v[:] for k, v in defaults.items()}

    def _sync_modes(self):
        self._mode_configs = {}
        config_modes = self._config_manager.get_all_safehome_modes()
        for mode in config_modes:
            mode_name = mode.mode_name.upper()
            self._mode_configs[mode_name] = mode.sensor_ids[:]

    # ------------------------------------------------------------------ #
    def arm_system(self, mode="AWAY", user=None) -> Dict:
        door_open = self._sensor_service.door_or_window_open()
        if door_open:
            return {"success": False, "message": f"Cannot arm. {door_open} is open."}

        active_sensors = set(self._mode_configs.get(mode, []))
        for sensor_id in self._sensor_service.sensor_ids:
            self._sensor_service.set_sensor_armed(sensor_id, sensor_id in active_sensors)

        self._current_mode = mode
        self._logger.add_event("ARM", f"System armed: {mode}", user=user)
        return {"success": True, "mode": mode}

    def disarm_system(self, zone_service: ZoneService, *, log_event: bool = True) -> Dict:
        self._current_mode = self.MODE_DISARMED
        self._sensor_service.disarm_all()
        for zone in zone_service.get_zones():
            zone["armed"] = False
        if log_event:
            self._logger.add_event("DISARM", "System disarmed")
        return {"success": True}

    def get_mode_configuration(self, mode: str) -> Dict:
        if mode in self._mode_configs:
            return {"success": True, "data": self._mode_configs[mode]}
        return {"success": False, "message": "Unknown mode"}

    def configure_mode(
        self, mode: str, sensors: List[str], user: Optional[str]
    ) -> Dict:
        if not mode or sensors is None:
            return {"success": False, "message": "Mode and sensors required"}
        invalid = [sid for sid in sensors if sid not in self._sensor_service.sensor_ids]
        if invalid:
            return {
                "success": False,
                "message": f"Unknown sensors: {', '.join(sorted(invalid))}",
            }

        mode_name = mode.upper()
        modes = self._config_manager.get_all_safehome_modes()
        for entry in modes:
            if entry.mode_name.upper() == mode_name:
                entry.sensor_ids = sensors
                if self._config_manager.update_safehome_mode(entry):
                    self._sync_modes()
                    self._logger.add_event(
                        "CONFIGURATION",
                        f"Mode configured: {mode_name}",
                        user=user,
                    )
                    return {"success": True}
                return {"success": False, "message": "Failed to update mode"}
        return {"success": False, "message": "Mode not found"}

    def get_all_modes(self) -> Dict:
        return {"success": True, "data": self._mode_configs}

    @property
    def current_mode(self) -> str:
        return self._current_mode


