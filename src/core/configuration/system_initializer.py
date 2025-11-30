"""Bootstrap helper that wires together default SafeHome resources."""

from __future__ import annotations

from ...configuration import StorageManager
from ...core.system_defaults import (
    CAMERAS,
    MODE_CONFIGS,
    SAFETY_ZONES,
    SENSORS,
    SENSOR_COORDS,
)
from .user_bootstrap import UserBootstrap


class SystemInitializer:
    """Provision default users/devices/modes/zones for a fresh install."""

    def __init__(
        self,
        storage: StorageManager,
        zone_service,
        mode_service,
        sensor_service,
        camera_service,
    ):
        self._user_bootstrap = UserBootstrap(storage)
        self._zone_service = zone_service
        self._mode_service = mode_service
        self._sensor_service = sensor_service
        self._camera_service = camera_service

    def bootstrap_all(self):
        """Ensure a working baseline configuration."""
        self._user_bootstrap.ensure_defaults()
        self._sensor_service.initialize_defaults(SENSORS, SENSOR_COORDS)
        self._camera_service.initialize_defaults(CAMERAS)
        self._zone_service.bootstrap_defaults(SAFETY_ZONES)
        self._mode_service.bootstrap_defaults(MODE_CONFIGS)
