"""ConfigurationManager - Facade for all configuration operations."""

from __future__ import annotations
from typing import List, Optional
from .safehome_mode import SafeHomeMode
from .safety_zone import SafetyZone
from .storage_manager import StorageManager
from .system_settings import SystemSettings


class ConfigurationManager:
    """Central manager for all configuration access and updates."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager

    def initialize_configuration(self) -> bool:
        # Import here to avoid circular import
        try:
            from ..core.system_defaults import MODE_CONFIGS
        except ImportError:
            # If core module not available, use empty configs
            MODE_CONFIGS = {}

        default_definitions = [
            ("HOME", "Minimal sensors when home"),
            ("AWAY", "All sensors when away"),
            ("OVERNIGHT", "Night mode"),
            ("EXTENDED", "Long absence mode"),
            ("GUEST", "Guest mode"),
        ]
        for idx, (name, desc) in enumerate(default_definitions, start=1):
            sensors = MODE_CONFIGS.get(name.upper(), [])
            mode = SafeHomeMode(idx, name, list(sensors), True, desc)
            self._storage_manager.save_safehome_mode(mode.to_dict())
        settings = SystemSettings()
        settings.save_to_database(self._storage_manager)
        return True

    # Legacy aliases expected by older unit tests
    def initialize(self) -> bool:
        return self.initialize_configuration()

    def reset_to_default(self) -> bool:
        return self.initialize_configuration()

    def get_system_settings(self) -> SystemSettings:
        settings = SystemSettings()
        settings.load_from_database(self._storage_manager)
        return settings

    def update_system_settings(self, settings: SystemSettings) -> bool:
        return settings.save_to_database(self._storage_manager)

    def get_safehome_mode(self, mode_id: int) -> Optional[SafeHomeMode]:
        modes = self._storage_manager.get_safehome_modes()
        for mode_data in modes:
            if mode_data["mode_id"] == mode_id:
                return SafeHomeMode.from_dict(mode_data)
        return None

    def get_all_safehome_modes(self) -> List[SafeHomeMode]:
        modes = self._storage_manager.get_safehome_modes()
        return [SafeHomeMode.from_dict(m) for m in modes]

    def update_safehome_mode(self, mode: SafeHomeMode) -> bool:
        return self._storage_manager.save_safehome_mode(mode.to_dict())

    def get_safety_zone(self, zone_id: int) -> Optional[SafetyZone]:
        zones = self._storage_manager.get_safety_zones()
        for zone_data in zones:
            if zone_data["zone_id"] == zone_id:
                return SafetyZone.from_dict(zone_data)
        return None

    def get_all_safety_zones(self) -> List[SafetyZone]:
        zones = self._storage_manager.get_safety_zones()
        return [SafetyZone.from_dict(z) for z in zones]

    def add_safety_zone(self, zone: SafetyZone) -> bool:
        return self._storage_manager.save_safety_zone(zone.to_dict())

    def update_safety_zone(self, zone: SafetyZone) -> bool:
        return self._storage_manager.save_safety_zone(zone.to_dict())

    def delete_safety_zone(self, zone_id: int) -> bool:
        return self._storage_manager.delete_safety_zone(zone_id)
