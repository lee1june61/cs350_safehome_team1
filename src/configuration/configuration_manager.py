"""ConfigurationManager facade for SafeHome.

Provides a high‑level, cohesive interface for accessing and mutating
system settings, SafeHome modes, and safety zones.
"""

from __future__ import annotations

import threading
from typing import List, Optional

from .exceptions import ConfigurationError
from .safehome_mode import SafeHomeMode
from .safety_zone import SafetyZone
from .storage_manager import StorageManager
from .system_settings import SystemSettings


class ConfigurationManager:
    """Central manager for configuration‑related information."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    def initialize_configuration(self) -> bool:
        """Initialize configuration information.

        Ensures the database schema is available and that core structures
        such as system settings and default modes exist.
        """
        with self._lock:
            self._storage_manager.connect()
            # Ensure settings exist; if not, store defaults.
            settings = SystemSettings()
            if not settings.load_from_database(self._storage_manager):
                settings.save_to_database(self._storage_manager)

            # Ensure at least stub modes exist.
            existing_modes = self.get_all_safehome_modes()
            if not existing_modes:
                self._create_default_modes()
            return True

    def _create_default_modes(self) -> None:
        """Create minimal default modes."""
        default_names = ["Home", "Away", "Overnight", "Extended"]
        for idx, name in enumerate(default_names, start=1):
            mode = SafeHomeMode(mode_id=idx, mode_name=name)
            mode.validate()
            self.update_safehome_mode(mode)

    # ------------------------------------------------------------------
    # System settings
    # ------------------------------------------------------------------
    def get_system_settings(self) -> SystemSettings:
        """Return current system settings."""
        with self._lock:
            settings = SystemSettings()
            settings.load_from_database(self._storage_manager)
            return settings

    def update_system_settings(self, settings: SystemSettings) -> bool:
        """Persist new system settings."""
        with self._lock:
            if not settings.validate_settings():
                raise ConfigurationError("Invalid system settings.")
            return settings.save_to_database(self._storage_manager)

    # ------------------------------------------------------------------
    # SafeHome modes
    # ------------------------------------------------------------------
    def get_safehome_mode(self, mode_id: int) -> SafeHomeMode:
        """Return a specific SafeHome mode by identifier."""
        with self._lock:
            rows = self._storage_manager.get_safehome_modes()
            for row in rows:
                if int(row.get("mode_id", -1)) == mode_id:
                    return SafeHomeMode.from_dict(row)
            raise ConfigurationError(f"SafeHome mode with id {mode_id} not found.")

    def get_all_safehome_modes(self) -> List[SafeHomeMode]:
        """Return all SafeHome modes."""
        with self._lock:
            rows = self._storage_manager.get_safehome_modes()
            return [SafeHomeMode.from_dict(row) for row in rows]

    def update_safehome_mode(self, mode: SafeHomeMode) -> bool:
        """Insert or update a SafeHome mode."""
        with self._lock:
            mode.validate()
            self._storage_manager.save_safehome_mode(mode.to_dict())
            return True

    # ------------------------------------------------------------------
    # Safety zones
    # ------------------------------------------------------------------
    def get_safety_zone(self, zone_id: int) -> SafetyZone:
        """Return a specific safety zone."""
        with self._lock:
            rows = self._storage_manager.get_safety_zones()
            for row in rows:
                if int(row.get("zone_id", -1)) == zone_id:
                    return SafetyZone.from_dict(row)
            raise ConfigurationError(f"Safety zone with id {zone_id} not found.")

    def get_all_safety_zones(self) -> List[SafetyZone]:
        """Return all safety zones."""
        with self._lock:
            rows = self._storage_manager.get_safety_zones()
            return [SafetyZone.from_dict(row) for row in rows]

    def add_safety_zone(self, zone: SafetyZone) -> bool:
        """Add a new safety zone."""
        with self._lock:
            zone.validate()
            # New zone; ensure id is not negative. DB will assign if needed.
            if zone.zone_id < 0:
                zone.zone_id = 0
            self._storage_manager.save_safety_zone(zone.to_dict())
            return True

    def update_safety_zone(self, zone: SafetyZone) -> bool:
        """Update an existing safety zone."""
        with self._lock:
            zone.validate()
            if zone.zone_id <= 0:
                raise ConfigurationError("Zone ID must be positive for update.")
            self._storage_manager.save_safety_zone(zone.to_dict())
            return True

    def delete_safety_zone(self, zone_id: int) -> bool:
        """Delete a safety zone."""
        with self._lock:
            return self._storage_manager.delete_safety_zone(zone_id)



