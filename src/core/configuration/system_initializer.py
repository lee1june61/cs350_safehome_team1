"""Bootstrap helper that wires together default SafeHome resources."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from ...configuration import AccessLevel, StorageManager
from ...configuration.password_utils import hash_password
from ...core.system_defaults import (
    CAMERAS,
    MODE_CONFIGS,
    SAFETY_ZONES,
    SENSORS,
    SENSOR_COORDS,
)


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
        self._storage = storage
        self._zone_service = zone_service
        self._mode_service = mode_service
        self._sensor_service = sensor_service
        self._camera_service = camera_service

    def bootstrap_all(self):
        """Ensure a working baseline configuration."""
        self._ensure_default_users()
        self._sensor_service.initialize_defaults(SENSORS, SENSOR_COORDS)
        self._camera_service.initialize_defaults(CAMERAS)
        self._zone_service.bootstrap_defaults(SAFETY_ZONES)
        self._mode_service.bootstrap_defaults(MODE_CONFIGS)

    # --------------------------------------------------------------------- #
    # Users
    # --------------------------------------------------------------------- #
    def _ensure_default_users(self):
        self._ensure_user(
            username="master",
            password="1234",
            interface="control_panel",
            access_level=int(AccessLevel.MASTER_ACCESS),
        )
        self._ensure_user(
            username="guest",
            password="5678",
            interface="control_panel",
            access_level=int(AccessLevel.GUEST_ACCESS),
        )
        self._ensure_user(
            username="admin",
            password="password",
            interface="web",
            access_level=int(AccessLevel.MASTER_ACCESS),
        )

    def _ensure_user(
        self,
        username: str,
        password: str,
        interface: str,
        access_level: int,
        extra: Dict | None = None,
    ):
        record = {
            "username": username,
            "password_hash": hash_password(password),
            "interface": interface,
            "access_level": access_level,
            "login_attempts": 0,
            "is_locked": False,
            "password_min_length": 4,
            "password_requires_digit": False,
            "password_requires_special": False,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None,
        }
        if extra:
            record.update(extra)
        existing = self._storage.get_login_interface(username, interface)
        if existing:
            needs_update = False
            updated = existing.copy()
            desired_hash = record["password_hash"]
            if updated.get("password_hash") != desired_hash:
                updated["password_hash"] = desired_hash
                needs_update = True
            for key in ("login_attempts", "is_locked", "password_min_length", "password_requires_digit", "password_requires_special"):
                target = record.get(key)
                if target is not None and updated.get(key) != target:
                    updated[key] = target
                    needs_update = True
            if needs_update:
                self._storage.save_login_interface(updated)
            return
        self._storage.save_login_interface(record)


